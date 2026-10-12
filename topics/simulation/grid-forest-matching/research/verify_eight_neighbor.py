"""Eight-neighbor research audit; finite evidence, not the general proof.

Reuses the published complete-charge certificate core in an isolated module,
replacing every geometry/answer dependency with the eight-neighbor model.
Induced-forest checks use all eight edges. The independent answer oracle moves
absolute surviving positions at EVERY step, with no first-visit cache.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
RESEARCH = Path(__file__).resolve().parent
REPO = RESEARCH.parents[3]
sys.path.insert(0, str(RESEARCH))
import verify_cubic_bound as original

DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, 1), (-1, 1), (1, -1))
LETTERS = dict(zip(DIRS, (-1, 1, -2, 2, -3, 3, -4, 4)))


class King:
    DIRECTIONS = DIRS
    LETTERS = LETTERS
    add = staticmethod(original.base.add)
    sub = staticmethod(original.base.sub)
    reduce_word = staticmethod(original.base.reduce_word)

    @staticmethod
    def neighbors(x):
        return [(x[0] + dr, x[1] + dc) for dr, dc in DIRS]

    @staticmethod
    def components(points):
        comp = {}
        for root in sorted(points):
            if root in comp:
                continue
            comp[root] = root
            queue = [root]
            for x in queue:
                for y in King.neighbors(x):
                    if y in points and y not in comp:
                        comp[y] = root
                        queue.append(y)
        return comp

    @staticmethod
    def query_data(order):
        parent, words = {order[0]: None}, {order[0]: ()}
        for x in order[1:]:
            earlier = [y for y in King.neighbors(x) if y in parent]
            assert len(earlier) == 1, 'Successful prefix is not an induced king tree'
            parent[x] = p = earlier[0]
            words[x] = words[p] + (LETTERS[King.sub(x, p)],)
        return parent, words


def check_forest(points):
    """Union-find enumerating every unordered induced eight-neighbor edge."""
    parents = {x: x for x in points}
    def root(x):
        while x != parents[x]:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x
    for x in points:
        for y in King.neighbors(x):
            if y in points and x < y:
                a, b = root(x), root(y)
                assert a != b, 'Induced eight-neighbor cycle'
                parents[a] = b


def direct_answers(points, moves):
    positions = set(points)
    answers = [len(positions)]
    for d in moves:
        dr, dc = DIRS[d]
        positions = {(r + dr, c + dc) for r, c in positions
                     if (r + dr, c + dc) in points}
        answers.append(len(positions))
    return answers


def bit_answers(n, points, moves):
    mask = sum(1 << (r * n + c) for r, c in points)
    candidates = mask
    row_repeat = ((1 << (n * n)) - 1) // ((1 << n) - 1)
    r = c = scans = 0
    seen = {(0, 0)}
    answers = [len(points)]
    for d in moves:
        dr, dc = DIRS[d]
        r, c = r + dr, c + dc
        if candidates and (r, c) not in seen:
            seen.add((r, c))
            if abs(r) >= n or abs(c) >= n:
                candidates = 0
            else:
                scans += candidates.bit_count()
                offset = r * n + c
                shifted = mask >> offset if offset >= 0 else mask << -offset
                lo, hi = max(0, -c), min(n, n - c)
                columns = (((1 << (hi - lo)) - 1) << lo) * row_repeat
                candidates &= shifted & columns
        answers.append(candidates.bit_count())
    return answers, scans


spec = importlib.util.spec_from_file_location('eight_neighbor_certificate_core',
                                             RESEARCH / 'verify_cubic_bound.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
audit.base = King
audit.DELTAS = {v: k for k, v in LETTERS.items()}
audit.check_forest = check_forest
audit.count_with_bitsets = bit_answers
audit.small_oracle = direct_answers


def walk_component(points, root, seed):
    rng = random.Random(seed)
    moves, visited = [], {root}
    def visit(x):
        neighbors = King.neighbors(x)
        rng.shuffle(neighbors)
        for y in neighbors:
            if y in points and y not in visited:
                visited.add(y)
                moves.append(DIRS.index(King.sub(y, x)))
                visit(y)
                moves.append(DIRS.index(King.sub(x, y)))
    visit(root)
    return moves


def lift_orthogonal(points, moves):
    """Scale six; route each original edge as an induced bent king path.

    E becomes NE,E,SE,SE,E,NE; S is its clockwise rotation. Every incident
    branch leaves its coarse vertex diagonally, preventing corner triangles.
    This is only a fixture generator; all resulting induced edges are checked.
    """
    east = [(-1, 1), (0, 1), (1, 1), (1, 1), (0, 1), (-1, 1)]
    south = [(dc, -dr) for dr, dc in east]
    def edge(a, b):
        reverse = a > b
        if reverse:
            a, b = b, a
        path = [(6 * a[0], 6 * a[1])]
        for d in (east if a[0] == b[0] else south):
            path.append(King.add(path[-1], d))
        assert path[-1] == (6 * b[0], 6 * b[1])
        return path[::-1] if reverse else path
    result = {(6 * r, 6 * c) for r, c in points}
    for a in points:
        for d in ((1, 0), (0, 1)):
            b = King.add(a, d)
            if b in points:
                result.update(edge(a, b))
    walk, x = [(0, 0)], (0, 0)
    for d in moves:
        y = King.add(x, original.base.DIRECTIONS[d])
        walk.extend(edge(x, y)[1:])
        x = y
    new_moves = [DIRS.index(King.sub(b, a)) for a, b in zip(walk, walk[1:])]
    check_forest(result)
    return result, new_moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check-published', action='store_true',
                        help='Require the regenerated report to equal the published JSON')
    args = parser.parse_args()
    report = {'model': 'all eight induced neighbors; unrestricted diagonal moves',
              'certificate_core': (RESEARCH / 'verify_cubic_bound.py').relative_to(REPO).as_posix(),
              'status': 'running', 'cases': []}
    output = args.output
    report['source_hash_format'] = 'SHA-256 of UTF-8 source normalized to LF'
    report['verification_sources_sha256'] = {
        name: hashlib.sha256((RESEARCH / name).read_text(encoding='utf8').encode('utf8')).hexdigest()
        for name in ['verify_eight_neighbor.py', 'verify_cubic_bound.py',
                     'verify_reference_components.py', 'verify_reference_capacity.py',
                     'verify_examples.py']
    }
    totals = Counter()
    def record(name, points, moves, n=None):
        row = audit.certify(points, moves, n)
        row['name'] = name
        report['cases'].append(row)
        for k in ['scans', 'successful_checks', 'failed_checks', 'labels', 'stars',
                  'cut_marks', 'reference_marks', 'nonreference_marks', 'same_early_pairs',
                  'power_one_same_early_pairs', 'power_one_curved', 'nonempty_curved']:
            totals[k] += row.get(k, 0)
        for k in ['max_label_capacity', 'max_nonreference_capacity']:
            totals[k] = max(totals[k], row.get(k, 0))
        return row

    # Negative control: a valid four-neighbor path becomes an eight-neighbor triangle.
    triangle = {(0, 0), (0, 1), (1, 1)}
    original.check_forest(triangle)
    try:
        check_forest(triangle)
    except AssertionError:
        report['triangle_negative_control'] = 'rejected'
    else:
        raise AssertionError('Missed diagonal edge of a triangle')

    for n in range(1, 4):
        cells = list(product(range(n), repeat=2))
        valid = 0
        for mask in range(1 << len(cells)):
            totals['checked_road_subsets'] += 1
            points = {x for k, x in enumerate(cells) if mask >> k & 1}
            try:
                check_forest(points)
            except AssertionError:
                continue
            valid += 1
            totals['valid_induced_forests'] += 1
            for word in product(range(8), repeat=4):
                answers, work = bit_answers(n, points, word)
                assert answers == direct_answers(points, word)
                assert work <= (5 * n - 3) * len(points)
                totals['exhaustive_walk_cases'] += 1
            if not points:
                record(f'{n}-empty', points, list(range(8)), n)
            for root in sorted(points):
                record(f'{n}-mask{mask}-root{root}', points,
                       walk_component(points, root, mask), n)
        report[f'forests_{n}x{n}'] = valid
        print(f'Passed all {n}x{n} forests: {valid}', flush=True)

    rng = random.Random(2026101208)
    for trial in range(180):
        n = rng.randrange(5, 13)
        cells = list(product(range(n), repeat=2))
        rng.shuffle(cells)
        points = set()
        for x in cells:
            if rng.random() < 0.2:
                continue
            try:
                check_forest(points | {x})
            except AssertionError:
                continue
            points.add(x)
        root = rng.choice(sorted(points))
        record(f'random-forest-{trial}', points, walk_component(points, root, trial), n)
        if trial < 40:
            record(f'random-walk-{trial}', points, [rng.randrange(8) for _ in range(60)], n)
    print('Passed random mixed-direction forests and walks', flush=True)

    for n in (4, 8, 16, 32, 64):
        points = {(r, c) for r in range(0, n, 2) for c in range(n)}
        moves = [DIRS.index((0, 1))] * (n - 1)
        row = record(f'lower-bound-stripes-{n}', points, moves, n)
        assert row['scans'] == ((n + 1) // 2) * (n - 1) * (n + 2) // 2

    fixtures = []
    for distance, arms in ((2, (0, 0, 0)), (3, (1, -1, 1)), (6, (4, -4, 2))):
        points, order, _ = original.opposite_arms((10, 23, 40), arms, distance)
        fixtures.append((f'opposite-arms-{distance}', points, original.base.realize(order)))
    points, moves = original.power_one_forest(rows=(3, 7, 13))
    fixtures.append(('curved-power-one', points, moves))
    for k, t, w in ((2, 1, 1), (3, 2, 1)):
        points, order, _ = original.base.nested_combs(k, t, w)
        fixtures.append((f'nested-combs-{k}-{t}-{w}', points, original.base.realize(order)))
    for name, points, moves in fixtures:
        points, moves = lift_orthogonal(points, moves)
        row = record('eight-neighbor-' + name, points, moves)
        assert set(moves) == set(range(8)), 'Fixture must use all eight directions'
        print(f'Passed {name}: N={len(points)}, moves={len(moves)}, '
              f'nonreference={row["nonreference_marks"]}', flush=True)

    assert totals['nonreference_marks'] > 0
    assert totals['same_early_pairs'] > 0
    assert totals['power_one_same_early_pairs'] > 0
    assert 1 <= totals['max_nonreference_capacity'] <= 2
    totals['certificate_cases'] = len(report['cases'])
    report['totals'] = dict(totals)
    report['status'] = 'passed'
    if args.check_published:
        published = json.loads((RESEARCH / 'eight-neighbor-results.json').read_text(encoding='utf8'))
        assert report == published, 'Regenerated evidence differs from the published report'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(json.dumps(report['totals'], indent=2))


if __name__ == '__main__':
    main()
