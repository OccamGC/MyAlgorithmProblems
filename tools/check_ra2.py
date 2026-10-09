"""Independent small-case oracles for the fifth refresh batch."""

import collections
import itertools
import math
import random

from check_reference import run

P = 1000000009


def drone_oracle(rows):
    n, m = len(rows), len(rows[0])
    cells = list(itertools.product(range(n), range(m)))
    obstacles = {p for p in cells if rows[p[0]][p[1]] == 'B'}
    components = []
    remaining = set(obstacles)
    while remaining:
        component = {remaining.pop()}
        queue = collections.deque(component)
        while queue:
            x, y = queue.popleft()
            for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if p in remaining:
                    remaining.remove(p)
                    component.add(p)
                    queue.append(p)
        components.append(component)
    answers = []
    for start in cells:
        if rows[start[0]][start[1]] != 'S':
            continue
        best = None
        reachable = False
        for removed in [set(), *components]:
            opened = set(cells) - (obstacles - removed)
            adjacent = {u: [v for v in opened if u != v and
                           max(abs(u[0]-v[0]), abs(u[1]-v[1])) == 1]
                        for u in opened}
            seen_cells = {start}
            queue = collections.deque([start])
            while queue:
                u = queue.popleft()
                if rows[u[0]][u[1]] == 'T':
                    reachable = True
                for v in adjacent[u]:
                    if v not in seen_cells:
                        seen_cells.add(v)
                        queue.append(v)
            # Full ordered (fortress, drone) states; simulate the chase forward.
            queue = collections.deque((start, v, 0) for v in adjacent[start])
            seen = {(start, v) for v in adjacent[start]}
            while queue:
                u, v, distance = queue.popleft()
                if rows[v[0]][v[1]] == 'T':
                    best = min(best if best is not None else distance+1, distance+1)
                    break
                for w in adjacent[v]:
                    cross = (v[0]-u[0])*(w[1]-v[1]) - (v[1]-u[1])*(w[0]-v[0])
                    if cross != 0 and (v, w) not in seen:
                        seen.add((v, w))
                        queue.append((v, w, distance+1))
        answers.append(best if best is not None else (-2 if reachable else -1))
    return answers


def check_drone():
    rng = random.Random(2026092805)
    cases = []
    # Exhaust every 2x3 map with a fixed start and all other cell choices.
    for rest in itertools.product('BTE', repeat=5):
        text = 'S' + ''.join(rest)
        cases.append([text[:3], text[3:]])
    cases += [['S'], ['T'], ['STES'], ['SBBBT'], ['SBEBT'], ['SB', 'BT']]
    for _ in range(250):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        cases.append([''.join(rng.choices('BSTE', weights=[4, 2, 1, 3], k=m)) for _ in range(n)])
    for rows in cases:
        data = f'{len(rows)} {len(rows[0])}\n' + '\n'.join(rows) + '\n'
        expected = drone_oracle(rows)
        actual = run('terror-drone', data)
        assert actual == expected, (data, expected, actual)
    return len(cases)


def virus_input(A, B, N, M, updates, rates, times):
    lines = [f'{A} {B} {N} {M} {len(updates)} {len(times)}']
    lines += [' '.join(map(str, row)) for row in updates]
    lines += [' '.join(str(value) for pair in row for value in pair) for row in rates]
    lines += list(map(str, times))
    return '\n'.join(lines) + '\n'


def virus_oracle(A, B, N, M, updates, rates, times, direct=False):
    initial = [[0] * B for _ in range(A)]
    for x1, y1, x2, y2, value in updates:
        for x in range(x1-1, x2):
            for y in range(y1-1, y2):
                initial[x][y] += value
    d = N*M
    offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    # Column-vector matrix, independently oriented from the reference program.
    matrix = [[int(i == j) for j in range(d)] for i in range(d)]
    for source in range(d):
        for (dx, dy), (a, b) in zip(offsets, rates[source]):
            x, y = source//M+dx, source%M+dy
            if 0 <= x < N and 0 <= y < M:
                matrix[x*M+y][source] = (matrix[x*M+y][source] + a*pow(b, P-2, P)) % P

    def apply(mat, vec):
        return [sum(a*b for a, b in zip(row, vec)) % P for row in mat]

    def square(mat):
        columns = list(zip(*mat))
        return [[sum(a*b for a, b in zip(row, col)) % P for col in columns] for row in mat]

    answers = []
    origin_x = origin_y = 0
    for time in times:
        values = [initial[origin_x+i//M][origin_y+i%M] % P for i in range(d)]
        time = int(time)
        if direct:
            for _ in range(time):
                values = apply(matrix, values)
        else:
            power = matrix
            while time:
                if time & 1:
                    values = apply(power, values)
                power = square(power)
                time >>= 1
        answers.extend(values)
        total = sum(values)
        origin_x = total % (A-N+1)
        origin_y = 7*total % (B-M+1)
    return answers


def check_virus():
    rng = random.Random(2026092806)
    count = 0
    for index in range(260):
        N, M = rng.randint(1, 3), rng.randint(1, 3)
        A, B = N+rng.randint(0, 2), M+rng.randint(0, 2)
        updates = []
        for _ in range(rng.randint(1, 8)):
            x1, x2 = sorted([rng.randint(1, A), rng.randint(1, A)])
            y1, y2 = sorted([rng.randint(1, B), rng.randint(1, B)])
            updates.append((x1, y1, x2, y2, rng.randint(0, 10**9)))
        rates = []
        for _ in range(N*M):
            row = []
            for _ in range(5):
                b = rng.randint(1, 9)
                row.append((rng.randint(0, b), b))
            rates.append(row)
        times = [rng.randint(0, 15) for _ in range(5)] if index < 200 else [0, P-1, P, 10**18, 10**1000]
        data = virus_input(A, B, N, M, updates, rates, times)
        expected = virus_oracle(A, B, N, M, updates, rates, times, direct=index < 200)
        assert run('virus-sniper', data) == expected, (data, expected)
        count += 1
    # Non-diagonalizable, singular, scalar-zero, and identity transitions.
    zero = [(0, 1)] * 5
    special = [
        [[(0,1),(0,1),(0,1),(0,1),(1,1)], zero],
        [[(0,1),(0,1),(0,1),(0,1),(1,1)], [(0,1),(0,1),(0,1),(1,1),(0,1)]],
        [zero],
        [zero],
    ]
    # 9/(P-9) represents -1 modulo P, and is a legal probability.
    special[2] = [[(9, P-9), (1,1), (1,1), (1,1), (1,1)]]
    for rates in special:
        d = len(rates)
        updates = [(1, 1, 1, 1, 1)]
        times = [0, P-1, P, 10**1000-1, 10**1000]
        data = virus_input(1, d, 1, d, updates, rates, times)
        expected = virus_oracle(1, d, 1, d, updates, rates, times)
        assert run('virus-sniper', data) == expected, (data, expected)
        count += 1
    return count


def chrono_edges(buildings):
    edges = set()
    for i, (x, y, age, thresholds) in enumerate(buildings):
        distances = [max(abs(x-u), abs(y-v)) for u, v, _, _ in buildings]
        # Scan candidate radii and count all buildings instead of using rank groups.
        for count in thresholds:
            radius = next(r for r in sorted(set(distances)) if sum(d <= r for d in distances) >= count)
            newest = max((j for j, d in enumerate(distances) if d <= radius), key=lambda j: buildings[j][2])
            if newest != i:
                edges.add(tuple(sorted((i, newest))))
    return sorted(edges)


def count_trees(n, edges):
    count = 0
    for chosen in itertools.combinations(edges, n-1):
        parent = list(range(n))

        def find(u):
            while parent[u] != u:
                u = parent[u]
            return u

        for u, v in chosen:
            u, v = find(u), find(v)
            if u == v:
                break
            parent[u] = v
        else:
            count += 1
    return count


def exact_tree_count(n, edges):
    # Bareiss elimination over unbounded integers, no modular arithmetic.
    a = [[0]*(n-1) for _ in range(n-1)]
    for u, v in edges:
        if u < n-1:
            a[u][u] += 1
        if v < n-1:
            a[v][v] += 1
        if u < n-1 and v < n-1:
            a[u][v] -= 1
            a[v][u] -= 1
    if not a:
        return 1
    previous = 1
    for i in range(n-2):
        pivot = a[i][i]
        # Connected-graph Laplacian cofactors are positive definite.
        assert pivot != 0
        for j in range(i+1, n-1):
            for k in range(i+1, n-1):
                value = a[j][k]*pivot-a[j][i]*a[i][k]
                assert value % previous == 0
                a[j][k] = value//previous
        for j in range(i+1, n-1):
            a[j][i] = 0
        previous = pivot
    return a[-1][-1]


def chrono_input(N, M, modulus, buildings):
    return f'{N} {M} {len(buildings)} {modulus}\n' + ''.join(
        f'{x} {y} {age} {len(thresholds)} ' + ' '.join(map(str, thresholds)) + '\n'
        for x, y, age, thresholds in buildings)


def check_chrono():
    rng = random.Random(2026092807)
    count = 0
    for index in range(300):
        n = rng.randint(1, 6) if index < 250 else rng.randint(8, 30)
        N, M = rng.randint(1, 20), rng.randint(1, 20)
        ages = rng.sample(range(10**18-1000, 10**18+1), n)
        buildings = [(rng.randint(1, N), rng.randint(1, M), ages[i],
                      [rng.randint(1,n) for _ in range(rng.randint(0,n-1))] + [n]) for i in range(n)]
        modulus = rng.choice([2, 3, 4, 6, 8, 9, 10, 12, 97, 1000000000, 1000000007, 1000000500])
        edges = chrono_edges(buildings)
        trees = count_trees(n, edges) if index < 250 else exact_tree_count(n, edges)
        answer = trees * math.factorial(len(edges)-n+1) % modulus
        data = chrono_input(N, M, modulus, buildings)
        actual = run('chrono-legion', data)
        assert actual == [answer], (data, edges, answer, actual)
        count += 1
    # Equal-distance boundary, zero-radius overlaps, and noninvertible pivots.
    for modulus in (2, 4, 6, 8, 12, 1000000000, 1000000007):
        for buildings in (
            [(1,1,1,[1,3]), (1,1,2,[3]), (1,2,3,[3])],
            [(2,2,1,[2,4]), (1,1,2,[4]), (3,3,4,[4]), (1,3,3,[4])],
            [(1,2**i,i,list(range(1,9))) for i in range(8)],
        ):
            edges = chrono_edges(buildings)
            n = len(buildings)
            expected = exact_tree_count(n, edges)*math.factorial(len(edges)-n+1) % modulus
            assert run('chrono-legion', chrono_input(3,128,modulus,buildings)) == [expected]
            count += 1
    return count


if __name__ == '__main__':
    print('drone:', check_drone(), flush=True)
    print('virus:', check_virus(), flush=True)
    print('chrono:', check_chrono(), flush=True)
