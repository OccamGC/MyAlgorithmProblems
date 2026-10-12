"""Finite search for direction A; no claim of a general proof.

Rebuild genuine row-only earliest stars from complete candidate histories.
For each tested horizontal label, use its actual common cut, group strict
markers by primitive cyclic word and exponent >= 4, and test every possible
reference axis via its maximal eligible family. Connectivity includes ALL
induced grid edges, including edges between different resources.

Only the standard library and the public fixture verifier are required.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import heapq
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
from verify_examples import DIRECTIONS, check_forest, count_with_bitsets, read_case

HERE = Path(__file__).resolve().parent
LETTERS = {(-1, 0): -1, (1, 0): 1, (0, -1): -2, (0, 1): 2}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def neighbors(a):
    return [add(a, d) for d in DIRECTIONS]


def components(points):
    comp = {}
    for root in sorted(points):
        if root in comp:
            continue
        comp[root] = root
        queue = [root]
        for p in queue:
            for v in neighbors(p):
                if v in points and v not in comp:
                    comp[v] = root
                    queue.append(v)
    return comp


def reduce_word(word):
    out = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def word_type(g):
    left, right = 0, len(g)
    while left < right and g[left] == -g[right - 1]:
        left += 1
        right -= 1
    z = g[left:right]
    assert z
    p = next(p for p in range(1, len(z) + 1)
             if len(z) % p == 0 and z == z[:p] * (len(z) // p))
    u = z[:p]
    return min(u[i:] + u[:i] for i in range(p)), len(z) // p


def query_data(order):
    parent, words = {order[0]: None}, {order[0]: ()}
    for point in order[1:]:
        earlier = [p for p in neighbors(point) if p in parent]
        assert len(earlier) == 1, "Discovery prefixes must be induced trees"
        p = earlier[0]
        parent[point] = p
        words[point] = words[p] + (LETTERS[sub(point, p)],)
    return parent, words


def discovery(moves):
    walk = [(0, 0)]
    for d in moves:
        walk.append(add(walk[-1], DIRECTIONS[d]))
    return list(dict.fromkeys(walk))


def realize(order):
    """A legal tree walk realizing exactly this connected discovery order."""
    parent, words = query_data(order)
    walk = [order[0]]
    for target in order[1:]:
        a, b, tail = walk[-1], target, []
        while len(words[a]) > len(words[b]):
            a = parent[a]
            walk.append(a)
        while len(words[b]) > len(words[a]):
            tail.append(b)
            b = parent[b]
        while a != b:
            tail.append(b)
            a, b = parent[a], parent[b]
            walk.append(a)
        walk.extend(reversed(tail))
    moves = [DIRECTIONS.index(sub(b, a)) for a, b in zip(walk, walk[1:])]
    assert discovery(moves) == order
    return moves


def perturb_order(order, seed, window):
    """Randomize a parent-before-child order near its original ranking."""
    parent, _ = query_data(order)
    children = defaultdict(list)
    index = {p: i for i, p in enumerate(order)}
    for p in order[1:]:
        children[parent[p]].append(p)
    rng, queue = random.Random(seed), []
    result = [order[0]]
    for p in children[order[0]]:
        heapq.heappush(queue, (index[p] + rng.randrange(window), p))
    while queue:
        _, p = heapq.heappop(queue)
        result.append(p)
        for v in children[p]:
            heapq.heappush(queue, (index[v] + rng.randrange(window), v))
    assert len(result) == len(order)
    return result


def nested_combs(k, t, w):
    """Public nested-comb family, rebuilt directly from its defining prefixes."""
    depth, step, phase = 6 * w, 6 * w + 3, 2 * w + 5
    d = 3 * phase
    walk = [(0, 0)]

    def go(dr, dc, count):
        for _ in range(count):
            walk.append(add(walk[-1], (dr, dc)))

    def comb(sign):
        for r in range(1, depth + 1):
            go(1, 0, 1)
            if r % 3 == 0:
                go(0, sign, w)
                go(0, -sign, w)
        go(-1, 0, depth)

    for _ in range(k):
        go(1, 0, step)
        go(0, 1, 2)
        comb(1)
        go(0, -1, 2)
    go(0, 1, phase)
    comb(-1)
    go(0, 1, d)
    comb(-1)
    go(0, -1, d + phase)
    go(-1, 0, step)
    for _ in range(k - 1):
        go(0, 1, d + 2)
        comb(1)
        go(0, -1, d + 2)
        go(-1, 0, step)
    order = list(dict.fromkeys(walk))
    index = {p: i for i, p in enumerate(order)}
    upper = [(-i * step, 5 * phase * j) for i in range(1, k) for j in range(t)]
    bottom = [(-k * step, c) for c in range(0, 5 * phase * (t - 1) + 1, phase)]
    roads = set()
    for a in upper + bottom:
        e = (k * step + depth, phase - w) if a in bottom else (-a[0] + depth, 2 + w)
        for source, last in [(a, add(e, (0, d))), (add(a, (0, d)), e)]:
            roads.update(add(source, p) for p in order[:index[last] + 1])
    return roads, order, (0, d)


def bend_grid(roads, order):
    """Replace each horizontal unit edge by E2 S2 E2 N2 E2, scale six.

    Vertical edges become six-step segments. The corridors have at least
    one unused row/column between nonincident edges; check_forest below
    still verifies every induced edge explicitly.
    """
    def edge_path(a, b):
        reverse = a > b
        if reverse:
            a, b = b, a
        path = [(6 * a[0], 6 * a[1])]
        steps = ([(1, 0)] * 6 if a[0] != b[0] else
                 [(0, 1)] * 2 + [(1, 0)] * 2 + [(0, 1)] * 2 +
                 [(-1, 0)] * 2 + [(0, 1)] * 2)
        for delta in steps:
            path.append(add(path[-1], delta))
        assert path[-1] == (6 * b[0], 6 * b[1])
        return list(reversed(path)) if reverse else path

    bent = {(6 * r, 6 * c) for r, c in roads}
    for a in roads:
        for delta in ((1, 0), (0, 1)):
            b = add(a, delta)
            if b in roads:
                bent.update(edge_path(a, b))
    base_walk = [(0, 0)]
    for d in realize(order):
        base_walk.append(add(base_walk[-1], DIRECTIONS[d]))
    walk = [(0, 0)]
    for a, b in zip(base_walk, base_walk[1:]):
        walk.extend(edge_path(a, b)[1:])
    return bent, list(dict.fromkeys(walk))


def inspect(roads, order, labels=None, moves=None, board_side=None):
    check_forest(roads)
    alive, stars, marks, death = set(roads), {}, defaultdict(list), {}
    dyadic_scans = Counter()
    scans, last_success = 0, 0
    r0, c0 = min(r for r, c in roads), min(c for r, c in roads)
    n = max(max(r for r, c in roads) - r0 + 1, max(c for r, c in roads) - c0 + 1)
    if board_side is not None:
        assert board_side >= n
        n = board_side
    for j, f in enumerate(order[1:], 1):
        if not alive:
            break
        if max(abs(f[0]), abs(f[1])) < n:
            scans += len(alive)
            dyadic_scans[j.bit_length() - 1] += len(alive)
        survivors = {a for a in alive if add(a, f) in roads}
        for a in alive - survivors:
            death[a] = j
        alive = survivors
        if alive:
            last_success = j
        for a in sorted(alive):
            v = add(a, f)
            key = (v, f[0])
            if key not in stars:
                stars[key] = j
            else:
                i = stars[key]
                h = sub(f, order[i])
                if labels is None or h in labels:
                    marks[h].append((a, i, j))
    effective = order[:last_success + 1]
    parent, words = query_data(effective)
    if moves is None:
        moves = realize(order)
    normalized = {(r - r0, c - c0) for r, c in roads}
    answers, bit_scans = count_with_bitsets(n, normalized, moves)
    assert bit_scans == scans and answers[-1] == len(alive)
    stats = Counter(cases=1, labels=len(marks), marks=sum(map(len, marks.values())))
    witnesses = []
    for h, raw in sorted(marks.items()):
        tstar = max(i for _, i, _ in raw)
        prefix = set(order[:tstar + 1])
        tau = min((i for i, p in enumerate(order[:tstar + 1]) if add(p, h) in prefix), default=tstar + 1)
        groups = defaultdict(list)
        cache = {}
        for a, i, j in raw:
            if i >= tau or j <= tstar:
                continue
            if (i, j) not in cache:
                g = reduce_word(words[order[j]] + tuple(-x for x in reversed(words[order[i]])))
                cache[i, j] = g, word_type(g)
            g, kind = cache[i, j]
            if kind[1] >= 4:
                groups[kind].append((a, i, j, g))
        for kind, family in groups.items():
            stats['high_power_families'] += 1
            stats['strict_high_power_marks'] += len(family)
            stats['curved_families'] += len(kind[0]) > 1
            stats['max_primitive_period'] = max(stats['max_primitive_period'], len(kind[0]))
            stats['max_power'] = max(stats['max_power'], kind[1])
            axes = defaultdict(list)
            for m in family:
                axes[m[3]].append(m)
            for axis, same_axis in axes.items():
                reference = max(same_axis, key=lambda m: m[1])
                selected = [m for m in family if m[1] <= reference[1] and m[3] != axis]
                if not selected:
                    continue
                stats['nonempty_reference_scenarios'] += 1
                by_source = defaultdict(list)
                for m in selected:
                    by_source[m[0]].append(m)
                union = set()
                for a, items in by_source.items():
                    imax = max(m[1] for m in items)
                    resource = {add(a, p) for p in order[:imax + 1]}
                    assert all(add(x, h) in roads for x in resource)
                    assert not any(add(x, h) in resource for x in resource)
                    assert death.get(a, len(order)) > reference[2]
                    shifted_death = death.get(add(a, h), len(order))
                    assert imax < shifted_death <= reference[1]
                    fail_point = order[shifted_death]
                    x, y = add(a, parent[fail_point]), add(a, fail_point)
                    assert x in roads and add(x, h) in roads
                    assert y in roads and add(y, h) not in roads
                    stats['source_failure_checks'] += 1
                    union.update(resource)
                comp = components(union)
                parts, points = defaultdict(list), defaultdict(set)
                for m in selected:
                    parts[comp[m[0]]].append(m)
                for p, root in comp.items():
                    points[root].add(p)
                for root, items in parts.items():
                    stats['components'] += 1
                    axis_count = len({m[3] for m in items})
                    stats['mixed_axis_components'] += axis_count > 1
                    stats['at_least_three_axis_components'] += axis_count >= 3
                    stats['max_axes_in_component'] = max(stats['max_axes_in_component'], axis_count)
                    early = Counter(m[1] for m in items)
                    repeats = max(early.values()) > 1
                    overlap = sorted(p for p in points[root] if add(p, h) in points[root])
                    stats['repeated_early_components'] += repeats
                    stats['self_overlap_components'] += bool(overlap)
                    if repeats or overlap:
                        witnesses.append({'h': h, 'primitive': kind[0], 'power': kind[1],
                                          'reference': reference, 'markers': items, 'overlap': overlap})
    fingerprint = hashlib.sha256(json.dumps([sorted(roads), order], separators=(',', ':')).encode()).hexdigest()
    return dict(stats), {'n': n, 'N': len(roads), 'query_size': len(effective), 'walk_moves': len(moves),
                         'W': scans, 'W_over_n_cubed': scans / n ** 3,
                         'dyadic_scans': [dyadic_scans[i] for i in range(max(dyadic_scans, default=-1) + 1)],
                         'sha256': fingerprint}, witnesses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--quick', action='store_true', help='One generated parameter member, for development')
    args = parser.parse_args()
    records, total, violations = [], Counter(), []

    def run(name, roads, order, labels=None, moves=None, board_side=None):
        stats, size, bad = inspect(roads, order, labels, moves, board_side)
        records.append({'name': name, **size, 'tested_labels': sorted(labels) if labels else 'all', **stats})
        for key, value in stats.items():
            if key.startswith('max_'):
                total[key] = max(total[key], value)
            else:
                total[key] += value
        if bad:
            violations.append({'name': name, 'roads': sorted(roads), 'order': order, 'witnesses': bad})
        print(name, stats.get('components', 0), stats.get('mixed_axis_components', 0), file=sys.stderr, flush=True)

    if not args.quick:
        for item in json.loads((HERE / 'examples/inputs/manifest.json').read_text(encoding='utf8')):
            path = HERE / 'examples/inputs' / item['file']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
            n, roads, moves = read_case(path)
            run('public/' + item['file'], roads, discovery(moves), moves=moves, board_side=n)
    parameters = [(7, 2, 3)] if args.quick else [(k, t, w) for k in (6, 7, 9) for t in (1, 2, 3) for w in (3, 4)]
    for k, t, w in parameters:
        roads, original, h = nested_combs(k, t, w)
        for variant, window in enumerate((1, 8, 64, len(original))):
            seed = 20261012 + 10000 * k + 100 * t + 10 * w + variant
            order = original if variant == 0 else perturb_order(original, seed, window)
            run(f'nested/k{k}-t{t}-w{w}/window{window}', roads, order, {h})
    if not args.quick:
        for k, t, w in [(4, 2, 1), (5, 2, 1), (5, 2, 2), (7, 2, 1), (9, 2, 1)]:
            roads, original, h = nested_combs(k, t, w)
            for variant, window in enumerate((1, 8, 64, len(original))):
                seed = 20261012 + 10000 * k + 100 * t + 10 * w + variant
                order = original if variant == 0 else perturb_order(original, seed, window)
                bent, discovery_order = bend_grid(roads, order)
                run(f'curved/k{k}-t{t}-w{w}/window{window}', bent, discovery_order,
                    {(6 * h[0], 6 * h[1])})
    total['distinct_road_order_pairs'] = len({case['sha256'] for case in records})
    report = {'scope': __doc__, 'seed_base': 20261012, 'summary': dict(total),
              'cases': records, 'counterexamples': violations,
              'conclusion': 'counterexample found' if violations else 'no counterexample in these finite cases; not a proof'}
    data = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(data, encoding='utf8', newline='\n')
    print(json.dumps(report['summary'], indent=2))
    assert not violations, 'See saved counterexample certificates'


if __name__ == '__main__':
    main()
