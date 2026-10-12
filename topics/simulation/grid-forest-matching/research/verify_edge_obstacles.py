"""Finite audit for undirected edge-blocked four/eight-neighbor forests.

Reuses the published charging core, explicitly replacing induced connectivity
by common OPEN edges. The independent oracle moves positions at every step.
This research script and its finite results do not replace the written proof.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import inspect
from itertools import product
import json
from pathlib import Path
import random
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
RESEARCH = Path(__file__).resolve().parent
ROOT = RESEARCH.parents[3]
sys.path.insert(0, str(RESEARCH))
import verify_cubic_bound as old
import verify_eight_neighbor as eight

add, sub = old.base.add, old.base.sub
DIRS = eight.DIRS
LETTERS = eight.LETTERS


def edge(a, b):
    return tuple(sorted((a, b)))


def shifted(e, h):
    return edge(add(e[0], h), add(e[1], h))


def adjacency(points, edges):
    adj = {x: [] for x in points}
    for a, b in sorted(edges):
        if a in points and b in points:
            adj[a].append(b)
            adj[b].append(a)
    return adj


def forest(points, edges, directions):
    parent = {x: x for x in points}
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        assert a in points and b in points and sub(b, a) in directions
        ra, rb = root(a), root(b)
        assert ra != rb, 'Open-edge graph has a cycle'
        parent[ra] = rb


def words_on_forest(points, edges):
    adj = adjacency(points, edges)
    comp, words, groups = {}, {}, {}
    for root in sorted(points):
        if root in words:
            continue
        comp[root], words[root] = root, ()
        queue = [root]
        for a in queue:
            for b in adj[a]:
                if b not in words:
                    comp[b], words[b] = root, words[a] + (LETTERS[sub(b, a)],)
                    queue.append(b)
        groups[root] = queue
    return comp, words, groups


def components(points, edges):
    return words_on_forest(points, edges)[0]


def query_data(order, edges):
    adj = adjacency(set(order), edges)
    parent, words = {order[0]: None}, {order[0]: ()}
    for x in order[1:]:
        before = [a for a in adj[x] if a in parent]
        assert len(before) == 1
        p = before[0]
        parent[x], words[x] = p, words[p] + (LETTERS[sub(x, p)],)
    return parent, words


def direct(points, edges, moves, directions):
    positions, answers = set(points), [len(points)]
    for d in moves:
        delta = directions[d]
        positions = {add(x, delta) for x in positions if edge(x, add(x, delta)) in edges}
        answers.append(len(positions))
    return answers


def history(points, edges, moves, n, directions):
    alive, seen, point = set(points), {(0, 0)}, (0, 0)
    order, query_edges, events = [(0, 0)], set(), defaultdict(list)
    answers = [len(alive)]
    scans = successes = failures = last = cycle_clears = 0
    for d in moves:
        previous, point = point, add(point, directions[d])
        step = edge(previous, point)
        if alive:
            if max(map(abs, point)) >= n:
                alive.clear()
            elif point not in seen:
                seen.add(point)
                order.append(point)
                query_edges.add(step)
                j = len(order) - 1
                scans += len(alive)
                survivors = {a for a in alive if shifted(step, a) in edges}
                failures += len(alive) - len(survivors)
                alive = survivors
                successes += len(alive)
                if alive:
                    last = j
                for a in alive:
                    events[(add(a, point), point[0])].append((j, a))
            elif step not in query_edges:
                # A new edge between two old vertices closes a query cycle.
                alive.clear()
                cycle_clears += 1
        answers.append(len(alive))
    marks = defaultdict(list)
    for group in events.values():
        i, _ = group[0]
        for j, a in group[1:]:
            h = sub(order[j], order[i])
            assert h[0] == 0 and h[1] != 0
            marks[h].append((a, i, j))
    order = order[:last + 1]
    retained = set(order)
    query_edges = {e for e in query_edges if set(e) <= retained}
    assert scans == successes + failures and failures <= len(points)
    assert successes == len(events) + sum(map(len, marks.values()))
    assert len(events) <= n * len(points)
    return order, marks, answers, scans, successes, failures, len(events), query_edges, cycle_clears


def make_audit(directions):
    """Adapt only the documented geometry boundaries of the existing core."""
    source = inspect.getsource(old.certify)
    changes = [
        ('def certify(roads, moves,', 'def certify(roads, edges, moves,'),
        ('    check_forest(roads)', '    assert program is None\n    forest(roads, edges, directions)'),
        ('order, marks, answers, scans, successes, failures, stars = full_history(roads, moves, n)',
         'order, marks, answers, scans, successes, failures, stars, query_edges, cycle_clears = history(roads, edges, moves, n, directions)'),
        ('    bit_answers, bit_scans = count_with_bitsets(n, normalized, moves)\n'
         '    assert answers == bit_answers and scans == bit_scans\n'
         '    literal = len(roads) <= 200 and len(moves) <= 300\n'
         '    if literal:\n        assert answers == small_oracle(roads, moves)',
         '    literal = True\n    assert answers == direct(roads, edges, moves, directions)'),
        ('base.query_data(order)', 'query_data(order, query_edges)'),
        ('words_on_forest(roads)', 'words_on_forest(roads, edges)'),
        ('failed_checks=failures, scans=scans)', 'failed_checks=failures, scans=scans, cycle_clears=cycle_clears)'),
        ('        component = base.components(intersection)',
         '        common_edges = {e for e in edges if shifted(e, h) in edges}\n'
         '        component = components(intersection, common_edges)'),
        ('base.components(old_pairs)',
         'components(old_pairs, {e for e in query_edges if shifted(e, h) in query_edges})'),
        ('            assert resource <= intersection and len({component[x] for x in resource}) == 1',
         '            assert resource <= intersection and len({component[x] for x in resource}) == 1\n'
         '            assert all(shifted(e, a) in common_edges for e in query_edges if set(e) <= prefixes[i])'),
        ('json.dumps([sorted(roads), moves])', 'json.dumps([sorted(roads), sorted(edges), moves])'),
    ]
    for before, after in changes:
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    namespace = dict(vars(old))
    namespace.update(globals())
    namespace['directions'] = directions
    namespace['base'] = SimpleNamespace(add=add, sub=sub, reduce_word=old.base.reduce_word)
    exec(compile(source, 'edge_obstacle_certificate_core', 'exec'), namespace)
    return namespace['certify']


def induced_edges(points, directions):
    return {edge(a, add(a, d)) for a in points for d in directions if add(a, d) in points}


def dfs_moves(points, edges, root, directions):
    adj = adjacency(points, edges)
    moves = []
    def visit(a, parent):
        for b in adj[a]:
            if b != parent:
                moves.append(directions.index(sub(b, a)))
                visit(b, a)
                moves.append(directions.index(sub(a, b)))
    visit(root, None)
    return moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check-published', action='store_true',
                        help='Require the regenerated report to equal the published JSON')
    args = parser.parse_args()
    report = {'status': 'running', 'model': 'static undirected edge obstacles; open-edge forest',
              'core': 'adapted verify_cubic_bound.certify; common OPEN-edge intersections', 'models': {}}
    report['source_hash_format'] = 'SHA-256 of UTF-8 source normalized to LF'
    report['verification_sources_sha256'] = {
        name: hashlib.sha256((RESEARCH / name).read_text(encoding='utf8').encode('utf8')).hexdigest()
        for name in ['verify_edge_obstacles.py', 'verify_eight_neighbor.py',
                     'verify_cubic_bound.py', 'verify_reference_components.py',
                     'verify_reference_capacity.py', 'verify_examples.py']
    }
    for degree in (4, 8):
        directions = DIRS[:degree]
        certify = make_audit(directions)
        rows, totals = [], Counter()
        def record(name, points, edges, moves, n=None):
            row = certify(points, edges, moves, n)
            row.update(name=name, open_edges=len(edges))
            rows.append(row)
            for key in ['scans', 'nonreference_marks', 'same_early_pairs', 'power_one_same_early_pairs', 'cycle_clears']:
                totals[key] += row.get(key, 0)
            for key in ['max_label_capacity', 'max_nonreference_capacity']:
                totals[key] = max(totals[key], row.get(key, 0))
            return row

        cells = list(product(range(2), repeat=2))
        for mask in range(16):
            points = {x for i, x in enumerate(cells) if mask >> i & 1}
            possible = sorted(induced_edges(points, directions))
            for edge_mask in range(1 << len(possible)):
                edges = {e for i, e in enumerate(possible) if edge_mask >> i & 1}
                try:
                    forest(points, edges, directions)
                except AssertionError:
                    continue
                totals['valid_2x2_forests'] += 1
                for word in product(range(degree), repeat=4):
                    h = history(points, edges, word, 2, directions)
                    assert h[2] == direct(points, edges, word, directions)
                    assert h[3] <= 7 * len(points)
                    totals['exhaustive_walk_cases'] += 1
                for root in sorted(points) or [None]:
                    moves = dfs_moves(points, edges, root, directions) if root is not None else []
                    record(f'2x2-{mask}-{edge_mask}-{root}', points, edges, moves, 2)
        print(f'{degree}-neighbor: exhaustive small forests passed', flush=True)

        # Revisiting the origin on an untraversed edge must clear all candidates.
        path = [(0, 0), (0, 1), (1, 1)] if degree == 8 else [(0, 0), (0, 1), (1, 1), (1, 0)]
        edges = {edge(a, b) for a, b in zip(path, path[1:])}
        moves = [directions.index(sub(b, a)) for a, b in zip(path, path[1:] + path[:1])]
        assert direct(set(path), edges, moves, directions)[-2:] == [1, 0]
        row = record('new-edge-to-old-vertex-cycle', set(path), edges, moves, 2)
        assert row['cycle_clears'] == 1

        rng = random.Random(2026101300 + degree)
        for trial in range(100):
            n = rng.randrange(3, 10)
            points = {x for x in product(range(n), repeat=2) if rng.random() < .9}
            possible = sorted(induced_edges(points, directions))
            rng.shuffle(possible)
            edges = set()
            for e in possible:
                if rng.random() < .12:
                    continue
                try:
                    forest(points, edges | {e}, directions)
                except AssertionError:
                    continue
                edges.add(e)
            root = rng.choice(sorted(points))
            record(f'random-{trial}', points, edges, dfs_moves(points, edges, root, directions), n)
            if trial < 30:
                record(f'random-walk-{trial}', points, edges, [rng.randrange(degree) for _ in range(45)], n)

        for n in (4, 8, 16, 32):
            points = set(product(range(n), repeat=2))
            edges = {edge((r, c), (r, c+1)) for r in range(n) for c in range(n-1)}
            row = record(f'full-road-horizontal-forest-{n}', points, edges, [3]*(n-1), n)
            assert row['scans'] == n*(n-1)*(n+2)//2

        fixtures = []
        points, order, _ = old.opposite_arms()
        fixtures.append(('opposite-arms', points, old.base.realize(order)))
        points, moves = old.power_one_forest()
        fixtures.append(('curved-power-one', points, moves))
        points, order, _ = old.base.nested_combs(3, 2, 1)
        fixtures.append(('nested-combs', points, old.base.realize(order)))
        for name, points, moves in fixtures:
            edges = induced_edges(points, DIRS[:4])
            record(name, points, edges, moves)
            if degree == 8:
                points, moves = eight.lift_orthogonal(points, moves)
                record('mixed-eight-' + name, points, induced_edges(points, directions), moves)

        assert totals['nonreference_marks'] > 0 and totals['same_early_pairs'] > 0
        assert totals['power_one_same_early_pairs'] > 0
        totals['certificate_cases'] = len(rows)
        report['models'][str(degree)] = {'totals': dict(totals), 'cases': rows}
        print(degree, json.dumps(dict(totals)), flush=True)
    # Vertex intersection alone incorrectly joins these two overlap vertices.
    points = {(0,0), (0,1), (0,2)}
    edges = {edge((0,0), (0,1))}
    h = (0,1)
    overlap = {x for x in points if add(x,h) in points}
    common = {e for e in edges if shifted(e,h) in edges}
    assert len(set(components(overlap, edges).values())) == 1
    assert len(set(components(overlap, common).values())) == 2
    report['common_edge_negative_control'] = 'passed'
    report['status'] = 'passed'
    if args.check_published:
        published = json.loads((RESEARCH / 'edge-obstacles-results.json').read_text(encoding='utf8'))
        assert report == published, 'Regenerated evidence differs from the published report'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf8', newline='\n')


if __name__ == '__main__':
    main()
