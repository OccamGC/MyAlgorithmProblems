"""Rebuild complete per-label charging certificates for cubic-bound.

Does not use history(), scenarios(), verify_bins(), or the earlier axis
projection implementation. Stars are obtained by grouping all successful
events after candidate processing. Axis coordinates come from distances to
two abstract axis anchors, never from horizontal bounding boxes.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys

sys.dont_write_bytecode = True
import verify_reference_components as base
from verify_examples import check_forest, count_with_bitsets, read_case, small_oracle
from verify_reference_capacity import opposite_arms, serialize_case

HERE = Path(__file__).resolve().parent
DELTAS = {v: k for k, v in base.LETTERS.items()}


def inv(word):
    return tuple(-x for x in reversed(word))


def cyclic_data(g):
    left, right = 0, len(g)
    while left < right and g[left] == -g[right - 1]:
        left, right = left + 1, right - 1
    cycle = g[left:right]
    assert cycle
    period = next(p for p in range(1, len(cycle) + 1)
                  if len(cycle) % p == 0 and cycle == cycle[:p] * (len(cycle) // p))
    return g[:left], cycle[:period], len(cycle) // period


def words_on_forest(roads):
    component, words, groups = {}, {}, {}
    for root in sorted(roads):
        if root in words:
            continue
        words[root], component[root] = (), root
        queue = [root]
        for x in queue:
            for y in base.neighbors(x):
                if y in roads and y not in words:
                    component[y] = root
                    words[y] = words[x] + (base.LETTERS[base.sub(y, x)],)
                    queue.append(y)
        groups[root] = queue
    return component, words, groups


def word_distance(a, b):
    same = 0
    for x, y in zip(a, b):
        if x != y:
            break
        same += 1
    return len(a) + len(b) - 2 * same


def abstract_projection(g, vertices, words):
    stem, primitive, power = cyclic_data(g)
    radius = max(map(lambda x: len(words[x]), vertices)) + 1
    plus = base.reduce_word(stem + (primitive * (radius // len(primitive) + 1))[:radius])
    backward = inv(primitive)
    minus = base.reduce_word(stem + (backward * (radius // len(backward) + 1))[:radius])
    assert word_distance(plus, minus) == 2 * radius
    projected = {}
    for x in vertices:
        difference = word_distance(words[x], minus) - word_distance(words[x], plus)
        assert difference % 2 == 0
        projected[x] = difference // 2
        assert abs(projected[x]) < radius
    return projected, len(primitive), power


def full_history(roads, moves, n):
    """Intersection constraints first; stars and marks are rebuilt afterwards."""
    alive, seen, point, order = set(roads), {(0, 0)}, (0, 0), [(0, 0)]
    events = defaultdict(list)
    answers, scans, successes, failure_checks, last = [len(roads)], 0, 0, 0, 0
    for direction in moves:
        point = base.add(point, base.DIRECTIONS[direction])
        if point not in seen:
            seen.add(point)
            order.append(point)
            j = len(order) - 1
            if alive:
                if max(map(abs, point)) >= n:
                    alive = set()
                else:
                    scans += len(alive)
                    constraint = {base.sub(v, point) for v in roads}
                    next_alive = alive & constraint
                    failure_checks += len(alive - next_alive)
                    alive = next_alive
                    successes += len(alive)
                    if alive:
                        last = j
                    for a in alive:
                        events[(base.add(a, point), point[0])].append((j, a))
        answers.append(len(alive))
    marks = defaultdict(list)
    for (target, row), group in events.items():
        i, _ = group[0]
        for j, a in group[1:]:
            h = base.sub(order[j], order[i])
            assert h[0] == 0 and h[1] != 0
            marks[h].append((a, i, j))
    assert scans == successes + failure_checks and failure_checks <= len(roads)
    assert successes == len(events) + sum(map(len, marks.values()))
    assert len(events) <= n * len(roads)
    return order[:last + 1], marks, answers, scans, successes, failure_checks, len(events)


def certify(roads, moves, board_side=None, program=None, retain=False):
    check_forest(roads)
    if roads:
        r0, c0 = min(r for r, c in roads), min(c for r, c in roads)
        n = max(max(r for r, c in roads) - r0 + 1, max(c for r, c in roads) - c0 + 1)
        normalized = {(r - r0, c - c0) for r, c in roads}
    else:
        n, normalized = 1, set()
    n = max(n, board_side or 1)
    order, marks, answers, scans, successes, failures, stars = full_history(roads, moves, n)
    bit_answers, bit_scans = count_with_bitsets(n, normalized, moves)
    assert answers == bit_answers and scans == bit_scans
    literal = len(roads) <= 200 and len(moves) <= 300
    if literal:
        assert answers == small_oracle(roads, moves)
    if program:
        data = f'{n} {len(moves)}\n' + '\n'.join(
            ''.join('1' if (r, c) in normalized else '0' for c in range(n))
            for r in range(n)) + '\n' + ' '.join(map(str, moves)) + '\n'
        output = subprocess.run([str(program.resolve())], input=data.encode(), capture_output=True,
                                check=True, timeout=30)
        assert list(map(int, output.stdout.split())) == answers
    _, query_words = base.query_data(order)
    host_comp, host_words, host_groups = words_on_forest(roads)
    prefixes = [set(order[:i + 1]) for i in range(len(order))]
    stats = Counter(labels=len(marks), stars=stars, successful_checks=successes,
                    failed_checks=failures, scans=scans)
    certificates = []
    for h, raw in sorted(marks.items()):
        intersection = {x for x in roads if base.add(x, h) in roads}
        component = base.components(intersection)
        size = Counter(component.values())
        cut = max(i for _, i, _ in raw)
        old_pairs = {x for x in prefixes[cut] if base.add(x, h) in prefixes[cut]}
        assert len(set(base.components(old_pairs).values())) <= 1
        tau = min((i for i, x in enumerate(order) if x in old_pairs), default=cut + 1)
        paid, strict, query_g = [], defaultdict(list), {}
        for m in raw:
            a, i, j = m
            k = base.reduce_word(query_words[order[j]] + inv(query_words[order[i]]))
            query_g[m] = k
            resource = {base.add(a, x) for x in prefixes[i]}
            assert resource <= intersection and len({component[x] for x in resource}) == 1
            is_paid = j <= cut or bool(prefixes[i] & old_pairs)
            assert is_paid == (j <= cut or i >= tau)
            if is_paid:
                paid.append(m)
            else:
                assert not any(base.add(x, h) in resource for x in resource)
                strict[component[a]].append(m)
        assert len({query_g[m] for m in paid}) <= 1
        assignments, uses = [], Counter()
        targets = [base.add(a, order[i]) for a, i, _ in paid]
        assert len(set(targets)) == len(targets)
        for m, target in zip(paid, targets):
            assignments.append((m, 'cut', target))
            uses[target] += 1
        stats['cut_marks'] += len(paid)
        for root, family in sorted(strict.items()):
            ref = max(family, key=lambda m: (m[1], m[2], m[0]))
            a0 = ref[0]
            g = base.reduce_word(host_words[base.add(a0, h)] + inv(host_words[a0]))
            for m in family:
                a, i, j = m
                assert base.reduce_word(host_words[a] + query_g[m] + inv(host_words[a])) == g
            projection, period, power = abstract_projection(g, host_groups[host_comp[a0]], host_words)
            length = period * power
            reference = [m for m in family if query_g[m] == query_g[ref]]
            other = [m for m in family if query_g[m] != query_g[ref]]
            ref_targets = [base.add(a, order[i]) for a, i, _ in reference]
            assert len(set(ref_targets)) == len(ref_targets)
            strict_use = Counter(ref_targets)
            for m, target in zip(reference, ref_targets):
                assignments.append((m, 'reference', target))
            bins, resources, equal_early = defaultdict(list), {}, defaultdict(list)
            for m in other:
                a, i, j = m
                assert i < ref[1] < ref[2] < j
                assert all(base.add(a, x) in roads for x in prefixes[ref[2]])
                cells = {base.add(a, x) for x in prefixes[i]}
                low, high = min(projection[x] for x in cells), max(projection[x] for x in cells)
                assert high - low < length
                resources[m] = cells
                bins[low // length].append(m)
                equal_early[i].append(low)
            pair_count = 0
            for locations in equal_early.values():
                locations.sort()
                for x, y in zip(locations, locations[1:]):
                    assert y - x > length
                    pair_count += 1
            nonref_use, point_bins = Counter(), defaultdict(set)
            for b, group in sorted(bins.items()):
                assert len(group) == len({m[1] for m in group})
                used = set()
                for m in sorted(group, key=lambda m: m[1]):
                    free = resources[m] - used
                    assert free
                    target = min(free)
                    used.add(target)
                    nonref_use[target] += 1
                    assignments.append((m, f'bin:{b}', target))
                    for x in resources[m]:
                        point_bins[x].add(b)
            assert max(nonref_use.values(), default=0) <= 2
            assert max(map(len, point_bins.values()), default=0) <= 2
            strict_use.update(nonref_use)
            assert max(strict_use.values(), default=0) <= 3
            assert len(family) <= 3 * size[root]
            uses.update(strict_use)
            stats['strict_components'] += 1
            stats['reference_marks'] += len(reference)
            stats['nonreference_marks'] += len(other)
            if other:
                stats[f'nonempty_power_{min(power, 4)}' + ('_or_more' if power >= 4 else '')] += 1
                stats['nonempty_curved'] += period > 1
                stats['same_early_pairs'] += pair_count
                if power == 1:
                    stats['power_one_same_early_pairs'] += pair_count
                    stats['power_one_curved'] += period > 1
            stats['max_nonreference_capacity'] = max(stats['max_nonreference_capacity'], max(nonref_use.values(), default=0))
        assert len(assignments) == len(raw)
        assert len({a[0] for a in assignments}) == len(raw)
        assert set(uses) <= intersection and max(uses.values(), default=0) <= 4
        assert len(raw) <= 4 * len(intersection)
        stats['max_label_capacity'] = max(stats['max_label_capacity'], max(uses.values(), default=0))
        certificates.append({'h': h, 'cut': cut, 'tau': tau, 'intersection_size': len(intersection),
                             'marks': len(raw), 'max_capacity': max(uses.values(), default=0),
                             'assignments': sorted(assignments)})
    assert stats['cut_marks'] + stats['reference_marks'] + stats['nonreference_marks'] == sum(map(len, marks.values()))
    assert scans <= (5 * n - 3) * len(roads)
    answer_digest = hashlib.sha256(json.dumps(answers).encode()).hexdigest()
    row = {'n': n, 'roads': len(roads), 'moves': len(moves), 'successful_query_size': len(order),
           'geometry_sha256': hashlib.sha256(json.dumps([sorted(roads), moves]).encode()).hexdigest(),
           'answer_sha256': answer_digest,
           'assignment_sha256': hashlib.sha256(json.dumps(certificates, sort_keys=True).encode()).hexdigest(),
           'literal_answers_verified': literal, 'program_compared': bool(program), **stats}
    if retain:
        row['certificates'] = certificates
    return row


def power_one_forest(rows=(3, 9, 21), phases=(0, 2)):
    """Lift a sparse edge tree into an induced grid tree with primitive period 10.

    The coarse vertices alone are NOT an induced forest. Only the required
    prefix edges are subdivided; every induced edge of the final grid is then
    checked. No nonforest coarse board is passed to the algorithm or audit.
    """
    walk = [(0, 0)]

    def step(dr, dc, count):
        for _ in range(count):
            walk.append(base.add(walk[-1], (dr, dc)))

    step(1, 0, rows[-1])
    current = rows[-1]
    for row in reversed(rows):
        step(-1, 0, current - row)
        step(0, 1, 1)
        step(0, -1, 1)
        current = row
    order = list(dict.fromkeys(walk))
    parent, _ = base.query_data(order)
    index = {x: i for i, x in enumerate(order)}
    vertices, edges = set(), set()
    for row in rows:
        for phase in phases:
            for source, end in [((-row, phase), (row, 1)), ((-row, phase + 1), (row, 0))]:
                for x in order[:index[end] + 1]:
                    y = base.add(source, x)
                    vertices.add(y)
                    if parent[x] is not None:
                        edges.add(tuple(sorted((y, base.add(source, parent[x])))))
    for column in range(min(phases), max(phases) + 1):
        edges.add(((0, column), (0, column + 1)))

    def edge_path(a, b):
        reverse = a > b
        if reverse:
            a, b = b, a
        path = [(6 * a[0], 6 * a[1])]
        steps = ([(1, 0)] * 6 if a[0] != b[0] else
                 [(0, 1)] * 2 + [(1, 0)] * 2 + [(0, 1)] * 2 +
                 [(-1, 0)] * 2 + [(0, 1)] * 2)
        for d in steps:
            path.append(base.add(path[-1], d))
        assert path[-1] == (6 * b[0], 6 * b[1])
        return list(reversed(path)) if reverse else path

    roads = {(6 * r, 6 * c) for r, c in vertices}
    for a, b in edges:
        roads.update(edge_path(a, b))
    fine_walk = [(0, 0)]
    for a, b in zip(walk, walk[1:]):
        fine_walk.extend(edge_path(a, b)[1:])
    moves = [base.DIRECTIONS.index(base.sub(b, a)) for a, b in zip(fine_walk, fine_walk[1:])]
    check_forest(roads)
    return roads, moves


def connected_order(roads, root, mode, seed):
    rng = random.Random(seed)
    visited, queue, order = {root}, [root], []
    while queue:
        k = 0 if mode == 'breadth' else -1 if mode == 'depth' else rng.randrange(len(queue))
        point = queue.pop(k)
        order.append(base.sub(point, root))
        children = [x for x in base.neighbors(point) if x in roads and x not in visited]
        rng.shuffle(children)
        visited.update(children)
        queue.extend(children)
    base.query_data(order)
    return order


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--program', type=Path)
    args = parser.parse_args()
    report = {'scope': 'complete-history, all-label, component-local charging certificates',
              'status': 'running', 'cases': []}

    def save():
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                               encoding='utf8', newline='\n')

    def record(name, roads, moves, n=None, retain=False, compare=False):
        if len(report['cases']) < 25 or len(report['cases']) % 250 == 0:
            print(f'Checking {name}: N={len(roads)}, moves={len(moves)}', flush=True)
        row = certify(roads, moves, n, args.program if compare else None, retain)
        row['name'] = name
        report['cases'].append(row)
        if len(report['cases']) <= 25 or len(report['cases']) % 250 == 0:
            save()
            print(f'Passed {name}: scans={row["scans"]}, labels={row["labels"]}', flush=True)
        return row

    for item in json.loads((HERE / 'examples/inputs/manifest.json').read_text(encoding='utf8')):
        n, roads, moves = read_case(HERE / 'examples/inputs' / item['file'])
        record(item['file'], roads, moves, n, compare=True)
    n, roads, moves = read_case(HERE / 'examples/inputs/opposite-arms.in')
    record('opposite-arms.in', roads, moves, n, retain=True, compare=True)
    for d, arms in [(3, (1, -1, 1)), (2, (0, 0, 0))]:
        roads, order, h = opposite_arms((10, 23, 40), arms, d)
        record(f'low-power-{d}', roads, base.realize(order), compare=True)
    roads, moves = power_one_forest()
    row = record('curved-power-one-two-phases', roads, moves, retain=True, compare=True)
    assert row['power_one_curved'] > 0 and row['power_one_same_early_pairs'] > 0

    for k, t, w in [(4, 2, 1), (6, 3, 2)]:
        roads, order, h = base.nested_combs(k, t, w)
        record(f'nested-{k}-{t}-{w}', roads, base.realize(order), compare=True)
    roads, original, h = base.nested_combs(3, 2, 1)
    roads, original = base.bend_grid(roads, original)
    record('bent-nested-3-2-1', roads, base.realize(original), compare=True)
    # Reordering a long tree creates very long real walks and expensive full
    # certificates. Keep the large original fixture, vary a smaller same-family
    # bent tree at three roots and with three different discovery orders.
    roads, original, h = base.nested_combs(2, 1, 1)
    roads, original = base.bend_grid(roads, original)
    for index in [0, len(original) // 3, len(original) - 1]:
        for mode in ['breadth', 'depth', 'random']:
            order = connected_order(set(original), original[index], mode, 7300 + index)
            record(f'bent-small-reroot-{index}-{mode}', roads, base.realize(order))

    valid_masks = 0
    for mask in range(512):
        roads = {(r, c) for r in range(3) for c in range(3) if mask & (1 << (3 * r + c))}
        try:
            check_forest(roads)
        except AssertionError:
            continue
        valid_masks += 1
        roots = sorted(roads)
        if not roots:
            record('3x3-empty', roads, [0, 1, 2, 3], 3)
        for root in roots:
            order = connected_order(roads, root, 'depth', mask)
            record(f'3x3-mask{mask}-root{root}', roads, base.realize(order), 3)
    rng = random.Random(2026101203)
    for trial in range(120):
        n = rng.randrange(4, 9)
        cells = [(r, c) for r in range(n) for c in range(n)]
        rng.shuffle(cells)
        roads = set()
        for cell in cells:
            if rng.random() < 0.25:
                continue
            candidate = roads | {cell}
            try:
                check_forest(candidate)
            except AssertionError:
                continue
            roads = candidate
        root = rng.choice(sorted(roads))
        order = connected_order(roads, root, ['breadth', 'depth', 'random'][trial % 3], trial)
        moves = base.realize(order)
        record(f'random-connected-{trial}', roads, moves, n)
        if trial < 30:
            record(f'random-walk-{trial}', roads, [rng.randrange(4) for _ in range(40)], n)
    record('single-cell-empty-walk', {(0, 0)}, [], 1, compare=True)
    record('single-cell-failure', {(0, 0)}, [0, 1, 2, 3], 1, compare=True)
    total = Counter(cases=len(report['cases']), valid_3x3_forests=valid_masks)
    for row in report['cases']:
        for key in ['labels', 'stars', 'successful_checks', 'failed_checks', 'scans', 'cut_marks',
                    'reference_marks', 'nonreference_marks', 'strict_components', 'same_early_pairs',
                    'power_one_same_early_pairs', 'power_one_curved', 'nonempty_curved',
                    'nonempty_power_1', 'nonempty_power_2', 'nonempty_power_3', 'nonempty_power_4_or_more',
                    'literal_answers_verified', 'program_compared']:
            total[key] += row.get(key, 0)
        for key in ['max_label_capacity', 'max_nonreference_capacity']:
            total[key] = max(total[key], row.get(key, 0))
    report['totals'] = dict(total)
    report['status'] = 'passed'
    save()
    print(json.dumps({'output': str(args.output), **total}, indent=2))


if __name__ == '__main__':
    main()
