"""Certificates for the opposite-arm obstruction and reference capacity draft.

All marks are rebuilt from actual candidate histories. Axis coordinates use
the host tree, including curved axes; coordinate widths are not substituted.
Finite checks support, but do not replace, the proof in reference-capacity.
"""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import explore_reference_rounds as old
from verify_examples import count_with_bitsets, small_oracle

base = old.base
HERE = Path(__file__).resolve().parent


def opposite_arms(rows=(10, 23, 40), arms=(4, -4, 2), distance=6,
                  complete_negative=False):
    """Build only required full prefixes, never arbitrary prescribed marks."""
    walk = [(0, 0)]

    def go(dr, dc, count):
        for _ in range(count):
            walk.append(base.add(walk[-1], (dr, dc)))

    previous, early = 0, []
    for row, arm in zip(rows, arms):
        go(1, 0, row - previous)
        sign = 1 if arm > 0 else -1
        go(0, sign, abs(arm))
        early.append(walk[-1])
        go(0, -sign, abs(arm))
        previous = row
    late = {}
    for row, arm in reversed(list(zip(rows, arms))):
        go(-1, 0, previous - row)
        end = distance if complete_negative and arm < 0 else distance + arm
        go(0, 1, end)
        late[row] = walk[-1]
        go(0, -1, end)
        previous = row
    order = list(dict.fromkeys(walk))
    base.query_data(order)
    index = {p: i for i, p in enumerate(order)}
    roads = set()
    for row, e in zip(rows, early):
        for source, end in [((-row, 0), late[row]), ((-row, distance), e)]:
            roads.update(base.add(source, p) for p in order[:index[end] + 1])
    old.check_forest(roads)
    return roads, order, (0, distance)


def inverse(word):
    return tuple(-x for x in reversed(word))


def host_words(roads):
    comp = base.components(roads)
    words = {}
    for p in sorted(roads):
        if comp[p] != p:
            continue
        words[p] = ()
        queue = [p]
        for x in queue:
            for y in base.neighbors(x):
                if y in roads and y not in words:
                    words[y] = words[x] + (base.LETTERS[base.sub(y, x)],)
                    queue.append(y)
    return comp, words


def projection(roads, comp, words, source, query_g):
    """Return the exact integer projection coordinate for every host vertex."""
    g = base.reduce_word(words[source] + query_g + inverse(words[source]))
    left, right = 0, len(g)
    while left < right and g[left] == -g[right - 1]:
        left, right = left + 1, right - 1
    conjugator, cyclic = g[:left], g[left:right]
    assert cyclic
    delta = {v: k for k, v in base.LETTERS.items()}
    root = comp[source]
    origin = root
    for letter in conjugator:
        origin = base.add(origin, delta[letter])
    assert origin in roads and comp[origin] == root
    axis = {origin: 0}
    for sign, period in [(1, cyclic), (-1, inverse(cyclic))]:
        point, step = origin, 0
        while True:
            next_point = base.add(point, delta[period[step % len(period)]])
            if next_point not in roads:
                break
            assert comp[next_point] == root and next_point not in axis
            step += 1
            axis[next_point] = sign * step
            point = next_point
    out = dict(axis)
    queue = deque(axis)
    while queue:
        x = queue.popleft()
        for y in base.neighbors(x):
            if y in roads and y not in out:
                out[y] = out[x]
                queue.append(y)
    assert len(out) == sum(c == root for c in comp.values())
    return g, len(cyclic), out


def verify_bins(roads, order, labels=None, all_cuts=False, min_power=4):
    old.check_forest(roads)
    comp, words = host_words(roads)
    stats = Counter()
    for s in old.scenarios(roads, order, labels, all_cuts=all_cuts, min_power=min_power):
        stats['scenarios'] += 1
        stats['curved_scenarios'] += len(s['kind'][0]) > 1
        stats['low_power_scenarios'] += s['kind'][1] < 4
        stats['power_one_scenarios'] += s['kind'][1] == 1
        h = s['h']
        intersection = {x for x in roads if base.add(x, h) in roads}
        labels_comp = base.components(intersection)
        families = defaultdict(list)
        for marker in s['markers']:
            families[labels_comp[marker[0]]].append(marker)
        for items in families.values():
            first = items[0]
            g, length, project = projection(roads, comp, words, first[0], first[3])
            assert length == len(s['kind'][0]) * s['kind'][1]
            intervals, resources, bins = {}, {}, defaultdict(list)
            by_early = defaultdict(list)
            for marker in items:
                a, i, j, query_g = marker
                assert base.reduce_word(words[a] + query_g + inverse(words[a])) == g
                assert all(base.add(a, p) in roads for p in order[:s['reference'][2] + 1])
                cells = {base.add(a, p) for p in order[:i + 1]}
                assert cells <= intersection
                low, high = min(project[x] for x in cells), max(project[x] for x in cells)
                assert high - low < length
                intervals[marker] = (low, high)
                resources[marker] = cells
                bins[low // length].append(marker)
                by_early[i].append(low)
            for same in by_early.values():
                same.sort()
                for x, y in zip(same, same[1:]):
                    stats['same_early_consecutive_pairs'] += 1
                    assert y - x > length, (h, s['reference'], x, y, length)
            uses, memberships = Counter(), defaultdict(set)
            for bin_id, group in bins.items():
                assert len({m[1] for m in group}) == len(group)
                used = set()
                for m in sorted(group, key=lambda m: m[1]):
                    free = resources[m] - used
                    assert free
                    cell = min(free)
                    used.add(cell)
                    uses[cell] += 1
                    for x in resources[m]:
                        memberships[x].add(bin_id)
            assert max(uses.values(), default=0) <= 2
            assert max(map(len, memberships.values()), default=0) <= 2
            stats['host_label_components'] += 1
            stats['assigned_marks'] += len(items)
            stats['max_capacity_used'] = max(stats['max_capacity_used'], max(uses.values(), default=0))
            stats['max_bins_at_a_resource_point'] = max(stats['max_bins_at_a_resource_point'],
                                                        max(map(len, memberships.values()), default=0))
    return dict(stats)


def literal_marks(roads, order):
    """Independent prefix-membership definition, without maintained stars."""
    result = defaultdict(list)
    for j, f in enumerate(order[1:], 1):
        for a in sorted(roads):
            if not all(base.add(a, p) in roads for p in order[:j + 1]):
                continue
            target = base.add(a, f)
            for i, e in enumerate(order[1:j], 1):
                if e[0] == f[0]:
                    source = base.sub(target, e)
                    if all(base.add(source, p) in roads for p in order[:i + 1]):
                        result[base.sub(f, e)].append((a, i, j))
                        break
    return {h: set(items) for h, items in result.items()}


def serialize_case(roads, order):
    r0, c0 = min(r for r, c in roads), min(c for r, c in roads)
    cells = {(r - r0, c - c0) for r, c in roads}
    n = max(max(r for r, c in cells), max(c for r, c in cells)) + 1
    moves = base.realize(order)
    rows = [''.join('1' if (r, c) in cells else '0' for c in range(n)) for r in range(n)]
    data = f'{n} {len(moves)}\n' + '\n'.join(rows) + '\n' + ' '.join(map(str, moves)) + '\n'
    return n, cells, moves, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--program', type=Path)
    parser.add_argument('--write-fixture', action='store_true')
    parser.add_argument('--min-power', type=int, default=4)
    args = parser.parse_args()
    assert args.min_power >= 1
    results = {'status': 'finite checks of an obstruction and reference capacity',
               'min_power': args.min_power, 'cases': []}

    def record(name, roads, order, labels=None, **options):
        row = {'name': name, 'roads': len(roads), 'query_size': len(order),
               'sha256': hashlib.sha256(json.dumps([sorted(roads), order]).encode()).hexdigest(),
               **verify_bins(roads, order, labels, min_power=args.min_power, **options)}
        results['cases'].append(row)
        return row

    roads, order, h = opposite_arms()
    rebuilt = old.history(roads, order)[0]
    assert {h: set(ms) for h, ms in rebuilt.items()} == literal_marks(roads, order)
    row = record('opposite-arms-small', roads, order, {h}, all_cuts=True)
    s = max(old.scenarios(roads, order, {h}), key=lambda s: s['reference'][1])
    assert len(s['parts']) == 1 and s['parts'][0]['overlap'] == [(0, -4), (0, -3), (0, -2)]
    row['obstruction'] = {'h': h, 'reference': s['reference'][:3],
                          'markers': [m[:3] for m in s['markers']],
                          'cut': s['cut'], 'tau': s['tau'],
                          'axis_span': old.straight_axis_span(s, s['parts'][0]),
                          'overlap': s['parts'][0]['overlap'],
                          'early_multiplicity': s['parts'][0]['early_multiplicity'],
                          'failure_edges': sorted(set(s['exits'].values()))}
    n, normalized, moves, data = serialize_case(roads, order)
    answers, scans = count_with_bitsets(n, normalized, moves)
    assert answers == small_oracle(normalized, moves)
    if args.program:
        output = subprocess.run([str(args.program.resolve())], input=data.encode(),
                                capture_output=True, check=True, timeout=30)
        assert list(map(int, output.stdout.split())) == answers
    row.update(n=n, moves=len(moves), scans=scans, literal_stars_verified=True,
               literal_answers_verified=True, program_compared=bool(args.program),
               input_sha256=hashlib.sha256(data.encode()).hexdigest())
    if args.write_fixture:
        (HERE / 'examples/inputs/opposite-arms.in').write_text(data, encoding='utf8', newline='\n')

    rows = tuple(3 * 2 ** i for i in range(7))
    arms = (6, -6, 6, -6, 6, -6, 6)
    roads, order, h = opposite_arms(rows, arms, 8, complete_negative=True)
    row = record('opposite-arms-seven-classes', roads, order, {h})
    s = max(old.scenarios(roads, order, {h}, keep_reference=True), key=lambda s: s['reference'][1])
    by_class = defaultdict(list)
    for m in s['markers']:
        a, i, _, _ = m
        columns = [a[1] + p[1] for p in order[:i + 1] if a[0] + p[0] == 0]
        if columns and max(columns) - min(columns) >= 2:
            by_class[m[3]].append(m)
    assert len(by_class) == 7
    paid = set(sorted(by_class, key=lambda g: (len(by_class[g]), max(m[1] for m in by_class[g])), reverse=True)[:4])
    remaining = [m for g, items in by_class.items() if g not in paid for m in items]
    ref = max(remaining, key=lambda m: m[1])
    remaining = [m for m in remaining if m[3] != ref[3]]
    union = set().union(*({base.add(m[0], p) for p in order[:m[1] + 1]} for m in remaining))
    overlap = sorted(p for p in union if base.add(p, h) in union)
    assert len(base.components(union).values()) and len(set(base.components(union).values())) == 1
    assert overlap and len({m[3] for m in remaining}) == 2
    row['after_four_classes_and_reference'] = {'long_class_counts': sorted(map(len, by_class.values())),
                                              'remaining_sources': sorted({m[0] for m in remaining}),
                                              'remaining_marks': len(remaining), 'overlap': overlap,
                                              'unpaid_after_source_blocks': sum(max(0, c - 9) for c in Counter(m[0] for m in remaining).values())}

    if args.min_power < 4:
        for distance, arms in [(3, (1, -1, 1)), (2, (0, 0, 0))]:
            roads, order, h = opposite_arms((10, 23, 40), arms, distance)
            rebuilt = old.history(roads, order)[0]
            assert {h: set(ms) for h, ms in rebuilt.items()} == literal_marks(roads, order)
            row = record(f'opposite-arms-power-{distance}', roads, order, {h})
            row['literal_stars_verified'] = True

    for item in json.loads((HERE / 'examples/inputs/manifest.json').read_text(encoding='utf8')):
        _, roads, moves = old.read_case(HERE / 'examples/inputs' / item['file'])
        record(item['file'], roads, base.discovery(moves))
    for k, t, w in [(4, 2, 1), (6, 3, 2), (9, 2, 3)]:
        roads, order, h = base.nested_combs(k, t, w)
        record(f'nested-k{k}-t{t}-w{w}', roads, order, {h})
    for k, t in [(3, 2), (4, 2), (6, 1)]:
        roads, order, h = base.nested_combs(k, t, 1)
        roads, order = base.bend_grid(roads, order)
        record(f'bent-k{k}-t{t}', roads, order, {(0, h[1] * 6)})
    total = Counter()
    for row in results['cases']:
        for key in ['scenarios', 'curved_scenarios', 'host_label_components', 'assigned_marks',
                    'same_early_consecutive_pairs', 'low_power_scenarios', 'power_one_scenarios']:
            total[key] += row.get(key, 0)
        for key in ['max_capacity_used', 'max_bins_at_a_resource_point']:
            total[key] = max(total[key], row.get(key, 0))
    results['totals'] = dict(total)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'output': str(args.output), 'cases': len(results['cases']), **total}, indent=2))


if __name__ == '__main__':
    main()
