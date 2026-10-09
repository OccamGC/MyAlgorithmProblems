"""Independent small-instance checks for batch R11. Compile references first."""
import itertools
import json
import os
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(2026092911)
PROBLEMS = (('trees', 'festival-plan'), ('trees', 'grinder'),
            ('optimization', 'metro-delivery'), ('graphs', 'tour-planning'),
            ('strings', 'magic-bread'), ('graphs', 'auto-wiring'))


def run(slug, data):
    program = ROOT/'build/bin'/(slug + ('.exe' if os.name == 'nt' else ''))
    return subprocess.run([str(program)], input=data.encode('ascii'),
                          capture_output=True, check=True, timeout=20).stdout.decode('ascii').split()


def tree_answer(values, edges, low, high, downward):
    n = len(values)
    graph = [[] for _ in values]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    root_parent = [-1]*n
    order = [0]
    for u in order:
        for v in graph[u]:
            if v != root_parent[u]:
                root_parent[v] = u
                order.append(v)
    answer = [-1061109568]*n
    for start in range(n):
        stack = [(start, -1, [start])]
        while stack:
            u, parent, path = stack.pop()
            length = len(path) if downward else len(path)-1
            if low <= length <= high:
                total = sum(values[v] for v in path)
                for v in path:
                    answer[v] = max(answer[v], total)
            for v in graph[u]:
                if v != parent and (not downward or root_parent[v] == u):
                    stack.append((v, u, path+[v]))
    return answer


def tree_data(values, edges, low, high):
    return f'{len(values)} {low} {high}\n'+' '.join(map(str, values))+'\n'+''.join(f'{u+1} {v+1}\n' for u, v in edges)


def check_tree(downward):
    slug = 'festival-plan' if downward else 'grinder'
    count = 0
    for trial in range(420):
        n = RNG.randint(1, 15)
        values = [RNG.randint(-10, 10) for _ in range(n)]
        edges = [(v, RNG.randrange(v)) for v in range(1, n)]
        if trial % 5 == 0:
            edges = [(v, v-1) for v in range(1, n)]
        if trial % 5 == 1:
            edges = [(v, 0) for v in range(1, n)]
        lower = 1 if downward else 0
        upper = n if downward else n-1
        low, high = sorted((RNG.randint(lower, upper), RNG.randint(lower, upper)))
        expected = tree_answer(values, edges, low, high, downward)
        data = tree_data(values, edges, low, high)
        assert list(map(int, run(slug, data))) == expected, (slug, data, expected)
        count += 1
    return count


def metro_answer(rows, budget):
    n = len(rows)+1
    best = None
    for reductions in itertools.product(*(range(d+1) for _, _, d in rows)):
        if sum(reductions) > budget:
            continue
        arrival = 0
        total = 0
        produced = []
        for i, ((num, ready, travel), cut) in enumerate(zip(rows, reductions)):
            produced.append((num, ready))
            if num > 0:
                arrival = max(arrival, ready)
            arrival += travel-cut
            total += sum(quantity*(arrival-time) for quantity, time in produced)
        best = total if best is None else min(best, total)
    return best % 1000000009


def check_metro():
    rng = random.Random(2026092912)
    cases = [([], 0), ([], 500000000), ([(1, 0, 1), (0, 100, 1)], 0),
             ([(1, 0, 1), (1, 100, 1)], 0), ([(0, 1000000000, 0)]*6, 7),
             ([(100000, 1000000000, 3)]*6, 0), ([(1, 0, 3), (0, 1000000000, 3)], 6),
             ([(1, 0, 0), (0, 1000000000, 0), (1, 2, 0)], 500000000)]
    for trial in range(700):
        n = rng.randint(1, 7)
        rows = [(rng.choice((0, 0, 1, 2, 5)), rng.randint(0, 12), rng.randint(0, 3)) for _ in range(n-1)]
        budget = rng.randint(0, 18)
        cases.append((rows, budget))
    for rows, budget in cases:
        n = len(rows)+1
        data = f'{n} {budget}\n'+''.join(f'{a} {t} {d}\n' for a, t, d in rows)
        expected = metro_answer(rows, budget)
        assert run('metro-delivery', data) == [str(expected)], (data, expected)
    return len(cases)


def bread_answer(s, K):
    n = len(s)
    answer = []
    for i in range(n):
        result = 0
        for j in range(1, K+1):
            best = 0
            for direction in (-1, 1):
                sequence = ''.join(s[(i+direction*t)%n] for t in range(n))
                block = sequence[:j]
                if len(block) != j or block != block[::-1]:
                    continue
                length = 0
                while length+j <= n and sequence[length:length+j] == block:
                    length += j
                best = max(best, length)
            result ^= best*j
        answer.append(result)
    return answer


def check_bread():
    count = 0
    for n in range(1, 9):
        for bits in itertools.product('01', repeat=n):
            s = ''.join(bits)
            K = max(9, n)
            data = f'{n} {K}\n{s}\n'
            assert list(map(int, run('magic-bread', data))) == bread_answer(s, K), data
            count += 1
    for _ in range(150):
        n = RNG.randint(1, 40)
        K = RNG.randint(1, 20)
        s = ''.join(RNG.choices('01', k=n))
        data = f'{n} {K}\n{s}\n'
        assert list(map(int, run('magic-bread', data))) == bread_answer(s, K), data
        count += 1
    return count


def tour_answer(n, edges, people):
    infinity = 10**30
    distance = [[infinity]*n for _ in range(n)]
    for i in range(n):
        distance[i][i] = 0
    for u, v, w in edges:
        distance[u][v] = min(distance[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distance[i][k] != infinity and distance[k][j] != infinity:
                    distance[i][j] = min(distance[i][j], distance[i][k]+distance[k][j])
    if any(distance[i][i] < 0 for i in range(n)):
        return 'Negative loop found.'
    travelers = []
    for i, (k, quantity, visits, _, _) in enumerate(people):
        choices = sorted((distance[i][j], abs(i-j), j) for j in range(n) if j != i and distance[i][j] != infinity)
        eligible = []
        if k and choices:
            cutoff = choices[min(k, len(choices))-1][:2]
            eligible = [j for dist, delta, j in choices if (dist, delta) <= cutoff]
        travelers += [(i, visits, eligible)]*quantity
    # Enumerate assignments of individually labelled travelers; capacity is a state.
    dp = {(0,)*n: 0}
    for _, visits, eligible in travelers:
        next_dp = dict(dp)
        for used, cost in dp.items():
            for j in eligible:
                if used[j] < people[j][3]:
                    state = list(used)
                    state[j] += 1
                    state = tuple(state)
                    value = cost + visits*people[j][4]
                    next_dp[state] = min(next_dp.get(state, infinity), value)
        dp = next_dp
    maximum = max(map(sum, dp))
    return str(min(cost for used, cost in dp.items() if sum(used) == maximum))


def check_tour():
    for trial in range(320):
        n = RNG.randint(2, 6)
        potential = [RNG.randint(-5, 5) for _ in range(n)]
        edges = []
        for _ in range(RNG.randint(1, n*n)):
            u, v = RNG.sample(range(n), 2)
            w = RNG.randint(0, 6)+potential[v]-potential[u]
            if trial % 7 == 0:
                w = RNG.randint(-5, 5)
            edges.append((u, v, w))
        people = [(RNG.randint(0, 10), RNG.randint(0, 2), RNG.randint(0, 5), RNG.randint(0, 2), RNG.randint(0, 5)) for _ in range(n)]
        data = f'{n} {len(edges)}\n'+''.join(f'{u+1} {v+1} {w}\n' for u, v, w in edges)+''.join(' '.join(map(str, row))+'\n' for row in people)
        expected = tour_answer(n, edges, people)
        assert ' '.join(run('tour-planning', data)) == expected, (data, expected)
    return 320


def cover_answer(n, edges):
    return min(mask.bit_count() for mask in range(1 << n) if all((mask >> u & 1) or (mask >> v & 1) for u, v in edges))


def check_wiring():
    count = 0
    cases = []
    for mask in range(1, 1 << 9):
        cases.append((6, [0]*3+[1]*3, [(i//3, i%3+3) for i in range(9) if mask >> i & 1]))
    for _ in range(250):
        n = RNG.randint(2, 12)
        split = RNG.randint(1, n-1)
        sides = [0]*split+[1]*(n-split)
        edges = [(RNG.randrange(split), RNG.randrange(split, n)) for _ in range(RNG.randint(1, 25))]
        cases.append((n, sides, edges))
    for n, sides, edges in cases:
        data = f'{n} {len(edges)}\n'+' '.join(map(str, sides))+'\n'+''.join(f'{u+1} {v+1}\n' for u, v in edges)
        out = list(map(int, run('auto-wiring', data)))
        chosen = {v-1 for v in out[1:]}
        assert out[0] == len(out)-1 == len(chosen) == cover_answer(n, edges), (data, out)
        assert all(0 <= v < n for v in chosen) and all(u in chosen or v in chosen for u, v in edges)
        count += 1
    return count


def check_checker():
    import tempfile
    from validate_r11 import CHECKER
    sample = ROOT/'topics/graphs/auto-wiring/tests/samples'
    cases = [
        ('3\n1 3 6\n', True), ('3\n2 4 5\n', True), ('3 6 3 1', True),
        ('3\n1 1 6\n', False), ('3\n0 3 6\n', False), ('3\n1 3 7\n', False),
        ('2\n1 3\n', False), ('4\n1 2 3 6\n', False), ('3\n1 2 3\n', False),
        ('3\n1 3\n', False), ('3\n1 3 6 2\n', False), ('', False),
        ('3\n1 3 -6\n', False), ('3\n1 3 6.0\n', False), ('nan', False),
    ]
    with tempfile.TemporaryDirectory(prefix='r11-checker-') as directory:
        output = Path(directory)/'candidate.out'
        for content, expected in cases:
            output.write_text(content, encoding='ascii')
            accepted, _ = CHECKER.check(sample/'01.in', sample/'01.out', output)
            assert accepted == expected, (content, expected, accepted)
    return len(cases)


def check_tour_boundaries():
    large = '2 2\n1 2 0\n2 1 0\n1 1000000000 30 1000000000 30\n1 1000000000 30 1000000000 30\n'
    assert run('tour-planning', large) == ['1800000000000']
    disconnected = '4 3\n1 2 1\n3 4 -2\n4 3 1\n' + '0 0 0 0 0\n'*4
    assert run('tour-planning', disconnected) == ['Negative', 'loop', 'found.']
    return 2


def main():
    results = {}
    checks = [('festival-plan', lambda: check_tree(True)), ('grinder', lambda: check_tree(False)),
              ('tour-planning', check_tour),
              ('magic-bread', check_bread), ('auto-wiring', check_wiring),
              ('metro-delivery', check_metro)]
    for slug, check in checks:
        results[slug] = check()
        print(f'{slug}: {results[slug]} independent comparisons passed', flush=True)
    checker_tests = check_checker()
    targeted_tour_tests = check_tour_boundaries()
    print(f'Checker: {checker_tests}; targeted tour checks: {targeted_tour_tests}', flush=True)
    (ROOT/'build/R11-checks.json').write_text(json.dumps(dict(seed=2026092911, metro_seed=2026092912, comparisons=results,
        checker_tests=checker_tests, targeted_tour_tests=targeted_tour_tests), indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
