"""Bounded follow-up experiments, October 2026; see the bilingual round log.

All tests rebuild genuine earliest stars. Relaxations are explicitly named.
The script never treats a finite pass as a proof of direction A.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
import verify_reference_components as base
from verify_examples import check_forest, read_case

HERE = Path(__file__).resolve().parent


def history(roads, order, labels=None):
    alive, stars, marks, death, work = set(roads), {}, defaultdict(list), {}, 0
    last = 0
    for j, f in enumerate(order[1:], 1):
        if not alive:
            break
        work += len(alive)
        now = {a for a in alive if base.add(a, f) in roads}
        for a in alive - now:
            death[a] = j
        alive = now
        if alive:
            last = j
        for a in sorted(alive):
            key = (base.add(a, f), f[0])
            if key not in stars:
                stars[key] = j
            else:
                i = stars[key]
                h = base.sub(f, order[i])
                if labels is None or h in labels:
                    marks[h].append((a, i, j))
    parent, words = base.query_data(order[:last + 1])
    return marks, death, parent, words, work, last


def scenarios(roads, order, labels=None, all_cuts=False, min_power=4, keep_reference=False):
    marks, death, parent, words, work, last = history(roads, order, labels)
    for h, raw in sorted(marks.items()):
        cuts = sorted({i for _, i, _ in raw}) if all_cuts else [max(i for _, i, _ in raw)]
        cache = {}
        for cut in cuts:
            prefix = set(order[:cut + 1])
            tau = min((i for i, p in enumerate(order[:cut + 1]) if base.add(p, h) in prefix), default=cut + 1)
            groups = defaultdict(list)
            for a, i, j in raw:
                if i >= tau or j <= cut:
                    continue
                if (i, j) not in cache:
                    ge = base.reduce_word(words[order[j]] + tuple(-x for x in reversed(words[order[i]])))
                    cache[i, j] = ge, base.word_type(ge)
                ge, kind = cache[i, j]
                if kind[1] >= min_power:
                    groups[kind].append((a, i, j, ge))
            for kind, family in groups.items():
                axes = defaultdict(list)
                for marker in family:
                    axes[marker[3]].append(marker)
                for axis, items in axes.items():
                    ref = max(items, key=lambda m: m[1])
                    selected = [m for m in family if m[1] <= ref[1] and (keep_reference or m[3] != axis)]
                    if not selected:
                        continue
                    by_source = defaultdict(list)
                    for m in selected:
                        by_source[m[0]].append(m)
                    resources, exits = {}, {}
                    for a, items in by_source.items():
                        imax = max(m[1] for m in items)
                        resources[a] = {base.add(a, p) for p in order[:imax + 1]}
                        assert all(base.add(x, h) in roads for x in resources[a])
                        assert not any(base.add(x, h) in resources[a] for x in resources[a])
                        if items[0][3] != axis:
                            j = death.get(base.add(a, h), len(order))
                            assert imax < j <= ref[1]
                            assert death.get(a, len(order)) > ref[2]
                            x, y = base.add(a, parent[order[j]]), base.add(a, order[j])
                            assert base.add(x, h) in roads and base.add(y, h) not in roads and y in roads
                            exits[a] = (x, y)
                    union = set().union(*resources.values())
                    comp = base.components(union)
                    points, part_marks = defaultdict(set), defaultdict(list)
                    for point, root in comp.items():
                        points[root].add(point)
                    for m in selected:
                        part_marks[comp[m[0]]].append(m)
                    parts = []
                    for root, items in part_marks.items():
                        cells = points[root]
                        repeat = max(Counter(m[1] for m in items).values())
                        overlap = sorted(p for p in cells if base.add(p, h) in cells)
                        parts.append({'points': cells, 'markers': items, 'overlap': overlap,
                                      'early_multiplicity': repeat, 'axes': len({m[3] for m in items}),
                                      'width': max(p[1] for p in cells) - min(p[1] for p in cells) + 1})
                    yield {'h': h, 'cut': cut, 'tau': tau, 'kind': kind, 'reference': ref,
                           'markers': selected, 'resources': resources, 'exits': exits,
                           'parts': parts, 'raw_work': work, 'last_success': last}


def audit(roads, order, labels=None, **options):
    check_forest(roads)
    stats, witness = Counter(cases=1), None
    for scenario in scenarios(roads, order, labels, **options):
        stats['scenarios'] += 1
        stats['markers_with_scenario_multiplicity'] += len(scenario['markers'])
        stats['max_exit_multiplicity'] = max(stats['max_exit_multiplicity'],
            max(Counter(scenario['exits'].values()).values(), default=0))
        for part in scenario['parts']:
            stats['components'] += 1
            stats['mixed_components'] += part['axes'] > 1
            stats['wide_components'] += part['width'] > abs(scenario['h'][1])
            stats['overlap_components'] += bool(part['overlap'])
            stats['repeated_early_components'] += part['early_multiplicity'] > 1
            stats['max_axes'] = max(stats['max_axes'], part['axes'])
            if witness is None and (part['overlap'] or part['early_multiplicity'] > 1):
                witness = {'h': scenario['h'], 'cut': scenario['cut'], 'tau': scenario['tau'],
                           'kind': scenario['kind'], 'reference': scenario['reference'],
                           'markers': part['markers'], 'overlap': part['overlap'],
                           'early_multiplicity': part['early_multiplicity']}
    return dict(stats), witness


def straight_axis_span(scenario, part):
    assert len(scenario['kind'][0]) == 1
    a, _, _, word = part['markers'][0]
    left, right = 0, len(word)
    while left < right and word[left] == -word[right - 1]:
        left += 1
        right -= 1
    row = a[0] + sum(1 if letter == 1 else -1 if letter == -1 else 0 for letter in word[:left])
    columns = [p[1] for p in part['points'] if p[0] == row]
    return max(columns) - min(columns) if columns else 0


def merge(total, stats):
    for key, value in stats.items():
        if key.startswith('max_'):
            total[key] = max(total[key], value)
        else:
            total[key] += value


def prefix_host(order, sources, endpoints, h):
    index = {p: i for i, p in enumerate(order)}
    roads = set()
    for a, e in zip(sources, endpoints):
        for source, last in [(a, base.add(e, h)), (base.add(a, h), e)]:
            roads.update(base.add(source, p) for p in order[:index[last] + 1])
    return roads


def comb_geometry(k=6, w=1, columns=None, heights=None, arms=None, label=None):
    """Variable source phases, row gaps, and early arm lengths.

    Road legality and actual stars are checked after taking the full-prefix
    union; prescribed pairs alone never count as genuine markers.
    """
    depth, phase = 6 * w, 2 * w + 5
    h = (0, 3 * phase if label is None else label)
    heights = heights or [(i + 1) * (depth + 3) for i in range(k)]
    arms = arms or [2] * k
    columns = columns or [0] * k
    walk = [(0, 0)]

    def go(delta, count):
        for _ in range(count):
            walk.append(base.add(walk[-1], delta))

    def comb(sign):
        for r in range(1, depth + 1):
            go((1, 0), 1)
            if r % 3 == 0:
                go((0, sign), w)
                go((0, -sign), w)
        go((-1, 0), depth)

    previous = 0
    for row, arm in zip(heights, arms):
        go((1, 0), row - previous)
        go((0, 1), arm)
        comb(1)
        go((0, -1), arm)
        previous = row
    go((0, 1), phase)
    comb(-1)
    go((0, 1), h[1])
    comb(-1)
    go((0, -1), h[1] + phase)
    for i in reversed(range(k - 1)):
        go((-1, 0), heights[i + 1] - heights[i])
        go((0, 1), h[1] + arms[i])
        comb(1)
        go((0, -1), h[1] + arms[i])
    order = list(dict.fromkeys(walk))
    base.query_data(order)
    sources = [(-row, column) for row, column in zip(heights, columns)]
    ends = [(row + depth, arm + w) for row, arm in zip(heights[:-1], arms[:-1])]
    ends.append((heights[-1] + depth, phase - w))
    return prefix_host(order, sources, ends, h), order, h


def reroot_order(query, root, seed, mode):
    rng = random.Random(seed)
    order, seen, frontier = [root], {root}, []
    for point in sorted(base.neighbors(root)):
        if point in query:
            frontier.append(point)
            seen.add(point)
    while frontier:
        index = 0 if mode == 'breadth' else -1 if mode == 'depth' else rng.randrange(len(frontier))
        point = frontier.pop(index)
        order.append(point)
        children = [p for p in sorted(base.neighbors(point)) if p in query and p not in seen]
        rng.shuffle(children)
        seen.update(children)
        frontier.extend(children)
    assert seen == query
    return [base.sub(point, root) for point in order]


def mutate_forest(roads, protected, seed, operations):
    rng, roads = random.Random(seed), set(roads)
    assert protected <= roads
    for turn in range(operations):
        if turn % 2 == 0:
            choices = [p for p in sorted(roads - protected) if sum(q in roads for q in base.neighbors(p)) == 1]
            if choices:
                roads.remove(rng.choice(choices))
        else:
            for _ in range(30):
                p = rng.choice(sorted(roads))
                q = rng.choice(base.neighbors(p))
                if q not in roads and sum(v in roads for v in base.neighbors(q)) == 1:
                    roads.add(q)
                    break
    return roads


def run_round(number):
    result = {'round': number, 'stats': {}, 'cases': [], 'counterexamples': []}
    total = Counter()

    def record(name, roads, order, labels=None, **options):
        try:
            check_forest(roads)
        except AssertionError:
            total['rejected_nonforests'] += 1
            return
        stats, witness = audit(roads, order, labels, **options)
        merge(total, stats)
        result['cases'].append({'name': name, 'N': len(roads), 'query_size': len(order), **stats,
                               'sha256': hashlib.sha256(json.dumps([sorted(roads), order]).encode()).hexdigest()})
        if witness:
            result['counterexamples'].append({'name': name, 'roads': sorted(roads),
                                              'order': order, 'witness': witness})

    if number == 1:
        result['purpose'] = 'Positive control: retain reference markers, then remove them correctly.'
        for filename in ['connected-resources.in', 'repeated-axis-classes.in']:
            _, roads, moves = read_case(HERE / 'examples/inputs' / filename)
            order = base.discovery(moves)
            record(filename + '/keep-reference', roads, order, keep_reference=True)
            record(filename + '/remove-reference', roads, order)
    elif number == 2:
        result['purpose'] = 'Verify unbounded reuse of one shifted-source failure edge.'
        for k in [6, 7, 9, 12, 18, 30]:
            roads, order, h = base.nested_combs(k, 1, 3)
            chosen = max(scenarios(roads, order, {h}), key=lambda s: s['reference'][1])
            multiplicity = Counter(chosen['exits'].values())
            expected_edge = ((0, 0), (1, 0))
            assert len(chosen['exits']) == k - 1
            assert set(chosen['exits'].values()) == {expected_edge}
            # The Section 29 four-class payment plus a new reference removes
            # four upper classes in addition to the bottom class.
            remaining = {a: edge for a, edge in chosen['exits'].items() if -a[0] <= (k - 5) * 21}
            assert len(remaining) == k - 5
            result['cases'].append({'k': k, 'N': len(roads), 'nonreference_sources': k - 1,
                                    'shared_exit_edge': expected_edge,
                                    'sources_after_four_classes_and_reference': len(remaining),
                                    'excess_per_source': 3, 'total_remaining_excess': 3 * (k - 5)})
        total['cases'] = len(result['cases'])
    elif number == 3:
        result['purpose'] = 'Check the column-band explanation for the original nested-comb family.'
        for k, t, w in itertools.product([6, 9, 12], [1, 2, 3], [3, 5]):
            roads, order, h = base.nested_combs(k, t, w)
            for scenario in scenarios(roads, order, {h}):
                union = set().union(*scenario['resources'].values())
                phase = 2 * w + 5
                assert all(0 <= p[1] % (5 * phase) <= w + 2 for p in union)
                assert not any(base.add(p, h) in union for p in union)
            record(f'k{k}-t{t}-w{w}', roads, order, {h})
    elif number == 4:
        result['purpose'] = 'Change source phases in full-prefix constructions, rejecting every induced cycle.'
        for k in [4, 6, 8]:
            for step in range(-8, 37):
                for reverse in [False, True]:
                    cols = [i * step for i in range(k)]
                    if reverse:
                        cols.reverse()
                    roads, order, h = comb_geometry(k=k, columns=cols)
                    record(f'k{k}-step{step}-reverse{reverse}', roads, order, {h})
    elif number == 5:
        result['purpose'] = 'Vary row gaps and early arm lengths together with nonaligned source phases.'
        rng = random.Random(2026101205)
        for trial in range(600):
            k, w = rng.choice([4, 6, 8]), rng.choice([1, 2])
            heights, row = [], 0
            for _ in range(k):
                row += 6 * w + rng.choice([3, 4, 6, 9])
                heights.append(row)
            arms = [rng.choice([2, 3, 4, 5]) for _ in range(k)]
            cols = [rng.randrange(-12, 13) for _ in range(k)]
            try:
                roads, order, h = comb_geometry(k, w, cols, heights, arms)
            except AssertionError:
                total['rejected_query_nonforests'] += 1
                continue
            record(f'trial{trial}', roads, order, {h})
    elif number == 6:
        result['purpose'] = 'Change query roots and use depth-first, breadth-first, and random connected orders.'
        for k, t in itertools.product([3, 4, 6, 8], [1, 2]):
            roads, original, h = base.nested_combs(k, t, 1)
            query = set(original)
            indices = sorted({0, len(original) // 5, len(original) // 3, len(original) // 2,
                              2 * len(original) // 3, len(original) - 1})
            for index in indices:
                for mode in ['depth', 'breadth', 'random']:
                    seed = 2026101206 + 1000 * k + 100 * t + index
                    order = reroot_order(query, original[index], seed, mode)
                    record(f'k{k}-t{t}-root{index}-{mode}', roads, order, {h})
    elif number == 7:
        result['purpose'] = 'Leaf removals and additions preserve the induced tree and one complete query copy.'
        for trial in range(160):
            k, t, w = [4, 6][trial % 2], [1, 2][(trial // 2) % 2], [1, 2][(trial // 4) % 2]
            roads, original, h = base.nested_combs(k, t, w)
            survivor = (-(6 * w + 3), 0)
            protected = {base.add(survivor, p) for p in original}
            roads = mutate_forest(roads, protected, 2026101207 + trial, 10 + 2 * (trial % 25))
            if trial % 3:
                order = base.perturb_order(original, 2026101307 + trial, 64)
            else:
                root = original[(trial * 37) % len(original)]
                order = reroot_order(set(original), root, 2026101307 + trial, 'random')
            record(f'mutation{trial}', roads, order, {h})
    elif number == 8:
        result['purpose'] = 'All early-time cuts and all horizontal labels on small fixtures and rerooted queries.'
        for filename in ['unchanged-bounding-box.in', 'unchanged-union.in',
                         'local-path-capacity-k2.in', 'connected-resources.in']:
            _, roads, moves = read_case(HERE / 'examples/inputs' / filename)
            record(filename, roads, base.discovery(moves), all_cuts=True)
        for k in [3, 4, 5]:
            roads, original, h = base.nested_combs(k, 1, 1)
            for root_index in [0, len(original) // 3, len(original) - 1]:
                for mode in ['depth', 'breadth', 'random']:
                    order = reroot_order(set(original), original[root_index], 2026101208 + root_index, mode)
                    record(f'k{k}-root{root_index}-{mode}', roads, order, all_cuts=True)
    elif number == 9:
        result['purpose'] = 'Audit the proved axis-span equivalence on both ordinary and positive-control unions.'
        for k, t, w in [(4, 2, 1), (6, 1, 3), (7, 3, 4), (9, 2, 3)]:
            roads, order, h = base.nested_combs(k, t, w)
            for keep in [False, True]:
                stats = Counter()
                for scenario in scenarios(roads, order, {h}, keep_reference=keep):
                    for part in scenario['parts']:
                        span = straight_axis_span(scenario, part)
                        assert bool(part['overlap']) == (span >= abs(h[1]))
                        stats['components'] += 1
                        stats['overlap_components'] += bool(part['overlap'])
                        stats['max_axis_span'] = max(stats['max_axis_span'], span)
                        stats['max_label_length'] = max(stats['max_label_length'], abs(h[1]))
                result['cases'].append({'k': k, 't': t, 'w': w, 'keep_reference': keep, **stats})
                merge(total, stats)
        total['cases'] = len(result['cases'])
    elif number == 10:
        result['purpose'] = 'Independently check full-prefix stars and the actual Section 29/38 remainder.'
        for filename in ['local-path-capacity-k2.in', 'connected-resources.in']:
            _, roads, moves = read_case(HERE / 'examples/inputs' / filename)
            order = base.discovery(moves)
            rebuilt, _, _, _, _, _ = history(roads, order)
            literal = defaultdict(list)
            for j, f in enumerate(order[1:], 1):
                for a in sorted(roads):
                    if not all(base.add(a, p) in roads for p in order[:j + 1]):
                        continue
                    target = base.add(a, f)
                    for i in range(1, j):
                        e = order[i]
                        if e[0] != f[0]:
                            continue
                        source = base.sub(target, e)
                        if all(base.add(source, p) in roads for p in order[:i + 1]):
                            literal[base.sub(f, e)].append((a, i, j))
                            break
            assert {h: set(items) for h, items in literal.items()} == {h: set(items) for h, items in rebuilt.items()}
            result['cases'].append({'file': filename, 'literal_markers': sum(map(len, literal.values()))})
        for k, w in [(6, 3), (9, 3), (18, 3), (30, 3), (8, 5)]:
            roads, order, h = base.nested_combs(k, 1, w)
            phase, row_step = 2 * w + 5, 6 * w + 3
            comb_size = 2 * w * w + 6 * w
            assert {c for r, c in roads if r == 1} == {0, 2, phase, h[1] + 2, h[1] + phase}
            _, deaths, _, _, _, _ = history(roads, order, {h})
            index = {p: j for j, p in enumerate(order)}
            assert all(deaths[(-i * row_step, h[1])] == index[(i * row_step + 1, 0)] for i in range(1, k))
            scenario = max(scenarios(roads, order, {h}, keep_reference=True), key=lambda s: s['reference'][1])
            long_marks = []
            for marker in scenario['markers']:
                a, early, _, _ = marker
                columns = [a[1] + p[1] for p in order[:early + 1] if a[0] + p[0] == 0]
                if columns and max(columns) - min(columns) >= 2:
                    long_marks.append(marker)
            by_axis = defaultdict(list)
            for marker in long_marks:
                by_axis[marker[3]].append(marker)
            paid = set(sorted(by_axis, key=lambda g: (len(by_axis[g]), max(m[1] for m in by_axis[g])), reverse=True)[:4])
            remainder = [m for m in long_marks if m[3] not in paid]
            reference = max(remainder, key=lambda m: m[1])
            counts = Counter(m[0] for m in remainder if m[3] != reference[3])
            assert set(counts.values()) == {comb_size + 1}
            assert len(counts) == k - 5
            excess = sum(max(0, count - (h[1] + 1)) for count in counts.values())
            assert excess == (2 * w * w - 15) * (k - 5)
            assert {scenario['exits'][a] for a in counts} == {((0, 0), (1, 0))}
            n = max(max(p[d] for p in roads) - min(p[d] for p in roads) + 1 for d in [0, 1])
            result['cases'].append({'k': k, 'w': w, 'n': n, 'within_official_side_limit': n <= 1000,
                                    'actual_long_axis_classes': len(by_axis), 'actual_remaining_sources': len(counts),
                                    'actual_remaining_excess': excess, 'distinct_failure_edges': 1})
        total['cases'] = len(result['cases'])
    if number == 1:
        controls = []
        for item in result['counterexamples']:
            witness = item['witness']
            controls.append({'name': item['name'], 'h': witness['h'], 'cut': witness['cut'],
                             'early_multiplicity': witness['early_multiplicity'],
                             'first_overlap_point': witness['overlap'][:1],
                             'note': 'Reference class deliberately retained; not a counterexample to direction A.'})
        result['positive_controls'] = controls
        result['counterexamples'] = []
    result['stats'] = dict(total)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--round', type=int, choices=range(1, 11), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run_round(args.round)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'round': args.round, 'stats': result['stats'],
                      'saved_counterexamples': len(result['counterexamples'])}, indent=2))


if __name__ == '__main__':
    main()
