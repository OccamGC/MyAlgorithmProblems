"""Input, score-group and output checks for the fifth refresh batch."""

import collections
import math
import re


GROUP_SHARES = {
    'terror-drone': (30, 10, 20, 40),
    'virus-sniper': (30, 10, 20, 30, 10),
    'chrono-legion': (30, 30, 10, 10, 20),
}


def validate_drone(path):
    with path.open(encoding='ascii') as stream:
        n, m = map(int, stream.readline().split())
        assert 1 <= n <= 40 and 1 <= m <= 40
        rows = [stream.readline().rstrip('\n') for _ in range(n)]
        assert all(len(row) == m and set(row) <= set('BSTE') for row in rows)
        assert not stream.read()
    counts = collections.Counter(''.join(rows))
    return dict(n=n, m=m, starts=counts['S'], traps=counts['T'], obstacles=counts['B'])


def validate_virus(path):
    with path.open(encoding='ascii') as stream:
        A, B, N, M, Q, K = map(int, stream.readline().split())
        assert 1 <= N <= A <= 1000 and 1 <= M <= B <= 1000
        assert 1 <= N*M <= 50 and 1 <= Q <= 1000000 and 1 <= K <= 5
        for _ in range(Q):
            x1, y1, x2, y2, C = map(int, stream.readline().split())
            assert 1 <= x1 <= x2 <= A and 1 <= y1 <= y2 <= B
            assert 0 <= C <= 10**9
        for _ in range(N*M):
            row = list(map(int, stream.readline().split()))
            assert len(row) == 10
            for a, b in zip(row[::2], row[1::2]):
                assert 0 <= a <= b <= 10**9 and b >= 1
        times = [stream.readline().strip() for _ in range(K)]
        assert all(re.fullmatch(r'0|[1-9][0-9]*', value) for value in times)
        assert all(int(value) <= 10**1000 for value in times)
        assert not stream.read()
    return dict(A=A, B=B, N=N, M=M, Q=Q, K=K, max_time=str(max(map(int, times))),
                max_decimal_digits=max(map(len, times)))


def validate_chrono(path):
    with path.open(encoding='ascii') as stream:
        N, M, K, modulus = map(int, stream.readline().split())
        assert N >= 1 and M >= 1 and N*M <= 10**6 and 1 <= K <= 200
        assert 2 <= modulus <= 1000000500
        buildings = []
        for _ in range(K):
            x, y, time, count, *thresholds = map(int, stream.readline().split())
            assert 1 <= x <= N and 1 <= y <= M and 0 <= time <= 10**18
            assert 1 <= count <= K and len(thresholds) == count
            assert all(1 <= value <= K for value in thresholds)
            buildings.append((x,y,time,thresholds))
        assert len({b[2] for b in buildings}) == K and not stream.read()
    edges = set()
    for i, (x,y,_,thresholds) in enumerate(buildings):
        distances = [max(abs(x-u),abs(y-v)) for u,v,_,_ in buildings]
        ordered = sorted(distances)
        for D in thresholds:
            radius = ordered[D-1]
            j = max((j for j in range(K) if distances[j] <= radius), key=lambda j: buildings[j][2])
            if i != j:
                edges.add(tuple(sorted((i,j))))
    graph = [[] for _ in range(K)]
    for u,v in edges:
        graph[u].append(v)
        graph[v].append(u)
    reached = {0}
    queue = [0]
    for u in queue:
        for v in graph[u]:
            if v not in reached:
                reached.add(v)
                queue.append(v)
    assert len(reached) == K
    prime = all(modulus % divisor for divisor in range(2, math.isqrt(modulus)+1))
    return dict(N=N,M=M,K=K,mod=modulus,is_prime=prime,edge_count=len(edges),
                max_time=max(b[2] for b in buildings),max_threshold_count=max(len(b[3]) for b in buildings))


VALIDATORS = {'terror-drone': validate_drone, 'virus-sniper': validate_virus,
              'chrono-legion': validate_chrono}


def validate_group(slug, spec, dimensions):
    g, d = spec['group'], dimensions
    if slug == 'terror-drone':
        if g == 1:
            assert d['n'] <= 5 and d['m'] <= 5
        if g == 2:
            assert d['starts'] == d['traps'] == 1
        if g == 3:
            assert d['traps'] == 1
    elif slug == 'virus-sniper':
        time = int(d['max_time'])
        if g <= 3:
            assert d['A'] == d['N'] and d['B'] == d['M']
        if g == 1:
            assert time <= 1000 and d['Q'] <= 1000
        if g == 2:
            assert time == 0
        if g <= 4:
            assert time <= 10**18
    else:
        if g <= 4:
            assert d['is_prime']
        if g == 1:
            assert d['N'] <= 100 and d['M'] <= 100 and d['K'] <= 8 and d['max_time'] <= 200
        if g == 2:
            assert d['N'] <= 1000 and d['M'] <= 1000
        if g == 3:
            assert min(d['N'],d['M']) == 1


def check_output(slug, path, dimensions):
    lines = path.read_text(encoding='ascii').splitlines()
    if slug == 'terror-drone':
        assert len(lines) == dimensions['starts']
        for line in lines:
            assert re.fullmatch(r'-?[0-9]+', line)
            value = int(line)
            assert value in (-1, -2) or 1 <= value <= 4*dimensions['n']*dimensions['m']
        if dimensions['traps'] == 0:
            assert all(line == '-1' for line in lines)
        known = {'sample-bomb': ['5'], 'straight-corridor': ['1', '-2'],
                 'two-barriers': ['-1'], 'long-corridor': ['-2']}
    elif slug == 'virus-sniper':
        assert len(lines) == dimensions['K']
        for line in lines:
            values = line.split()
            assert len(values) == dimensions['N'] * dimensions['M']
            assert all(value.isdigit() and 0 <= int(value) < 1000000009 for value in values)
        known = {'sample-growth': ['5 2', '7 7', '14 14'],
                 'exponent-regression': ['1 1000000008'],
                 'online-sum': ['1000000000 1000000000', '11 11']}
        if path.stem == 'zero-transition':
            assert all(int(line) == 0 for line in lines[1:])
        if path.stem == 'time-zero':
            assert all(int(value) == 10**15 % 1000000009 for line in lines for value in line.split())
    else:
        assert len(lines) == 1 and lines[0].isdigit()
        value = int(lines[0])
        n, modulus, edges = dimensions['K'], dimensions['mod'], dimensions['edge_count']
        assert 0 <= value < modulus
        if edges == n-1:
            assert value == 1
        if edges == n*(n-1)//2 and n >= 2:
            assert value == pow(n,n-2,modulus)*math.factorial(edges-n+1) % modulus
        known = {'radius-zero': ['3'], 'composite-triangle': ['3']}
    if path.stem in known:
        assert lines == known[path.stem], (path, lines)
