"""Independent dense-graph MST and tour/checker tests for the two nomadism tasks."""

import itertools
import json
import math
import os
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ('nomadism-day', 'nomadism-night')


def executable(slug, suffix=''):
    return ROOT / 'build/bin' / (slug + suffix + ('.exe' if os.name == 'nt' else ''))


def encode(points):
    return (str(len(points)) + '\n' + ''.join(f'{x} {y}\n' for x, y in points)).encode('ascii')


def distance(a, b, metric):
    dx, dy = a[0] - b[0], a[1] - b[1]
    if metric == 'nomadism-night':
        return abs(dx) + abs(dy)
    square = dx * dx + dy * dy
    if metric == 'squared':
        return square
    root = math.isqrt(square)
    return root + (root * root != square)


def dense_mst(points, metric):
    """O(n^2) Prim on the complete graph, independent of sparse candidates."""
    n = len(points)
    best = [10**30] * n
    seen = [False] * n
    best[0] = 0
    total = 0
    for _ in points:
        u = min((i for i in range(n) if not seen[i]), key=best.__getitem__)
        total += best[u]
        seen[u] = True
        for v in range(n):
            if not seen[v]:
                best[v] = min(best[v], distance(points[u], points[v], metric))
    return total


def tour_cost(points, tokens, metric):
    route = list(map(int, tokens))
    assert len(route) == len(points) + 1 and route[0] == route[-1] == 1
    assert sorted(route[:-1]) == list(range(1, len(points) + 1))
    return sum(distance(points[a-1], points[b-1], metric) for a, b in zip(route, route[1:]))


def make_cases():
    rng = random.Random(2026092808)
    cases = []
    grid = list(itertools.product(range(-1, 2), repeat=2))
    for mask in range(1, 1 << len(grid)):
        points = [p for i, p in enumerate(grid) if (mask >> i) & 1]
        rng.shuffle(points)
        cases.append(points)
    circle = [(x, y) for x in range(-65, 66) for y in range(-65, 66) if x*x+y*y == 65*65]
    for iteration in range(1800):
        n = rng.randint(1, 70)
        kind = iteration % 9
        if kind == 0:
            points = [(rng.randint(-10000, 10000), rng.randint(-10000, 10000)) for _ in range(n)]
        elif kind == 1:
            points = [(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(n)]
        elif kind == 2:
            points = [(0, rng.randint(-10000, 10000)) for _ in range(n)]
        elif kind == 3:
            points = [(x, x) for x in (rng.randint(-10000, 10000) for _ in range(n))]
        elif kind == 4:
            points = [rng.choice(circle) for _ in range(n)]
        elif kind == 5:
            points = [(rng.choice((-10000, 10000)), rng.randint(-10000, 10000)) for _ in range(n)]
        elif kind == 6:
            points = [(rng.randint(9900, 10000), rng.randint(-10000, -9900)) for _ in range(n)]
        elif kind == 7:
            points = [(rng.randint(-10000, 10000), 0) for _ in range(n)]
        else:
            points = [(rng.randint(-10000, 10000), rng.randint(-1, 1)) for _ in range(n)]
        rng.shuffle(points)
        cases.append(points)
    # Near-degenerate full-range predicates, repeated corners and rounded ties.
    cases += [[(-10000,-10000),(10000,-10000),(10000,10000),(-10000,10000),(9999,9998)],
              [(0,0),(2,2),(4,4)], [(0,0)]*100,
              list(itertools.product(range(-8,9), repeat=2)), circle,
              [(x, y) for x in (-10000, 0, 10000) for y in range(-100, 101)]]
    return cases


def check_checker(slug):
    cases = []
    square = [(0,0),(1,0),(1,1),(0,1)]
    for text, code in [('1 2 3 4 1\n',0), ('1 4 3 2 1\n',0),
                       ('1 2 1 3 4\n',1), ('2 1 3 4 2\n',1),
                       ('1 2 2 4 1\n',1), ('1 2 3 1\n',1),
                       ('1 2 3 5 1\n',1), ('1 2 3 0 1\n',1),
                       ('1 2 3 -1 1\n',1), ('1 2 3 4 1 7\n',1),
                       ('1 2 3 4 1 x\n',1), ('1 2 3 4 1.0\n',1),
                       ('1 2 3 4 99999999999999999999999999\n',1), ('',1)]:
        cases.append((square,text,code))
    for text, code in [('1 1\n',0),('1\n',1),('1 1 1\n',1),('1 2\n',1)]:
        cases.append(([(10000,-10000)],text,code))
    cases.append(([(0,0)]*4,'1 3 2 4 1\n',0))
    # M=2000: threshold=4002.001. A length-4002 tour passes; 4004 fails.
    points = [(0,0),(1,0),(2,0),(3,0),(2000,0)]
    cases.extend([(points,'1 3 2 4 5 1\n',0), (points,'1 4 2 3 5 1\n',1)])
    # The additive 0.001 matters: M=1999 permits C=4000 exactly.
    cases.append(([(0,0),(1,0),(2,0),(3,0),(1999,0)],'1 3 2 4 5 1\n',0))
    cases.append(([(0,0),(1,0),(2,0),(3,0),(1998,0)],'1 3 2 4 5 1\n',1))
    # This route satisfies 2 OPT but exceeds the new bound.
    cases.append(([(x,0) for x in range(5)],'1 3 5 2 4 1\n',1))
    count = 0
    with tempfile.TemporaryDirectory(dir=ROOT/'build') as folder:
        folder = Path(folder)
        paths = [folder/name for name in ('input','reference','contestant')]
        for points, text, code in cases:
            paths[0].write_bytes(encode(points))
            paths[2].write_text(text,encoding='ascii')
            # Neither a malformed nor a very long reference tour can relax M.
            for reference in ('', '999999999999999999999999\n', text):
                paths[1].write_text(reference,encoding='ascii')
                result = subprocess.run([str(executable(slug,'-checker')),*map(str,paths)],
                                        capture_output=True,timeout=10)
                assert result.returncode == code,(slug,points,text,code,result.stderr)
                count += 1
    return count


def main():
    cases = make_cases()
    data = b''.join(map(encode,cases))
    counts = {}
    for slug in SLUGS:
        result = subprocess.run([str(executable(slug,'-mst'))],input=data,capture_output=True,
                                check=True,timeout=60)
        weights = [list(map(int,line.split())) for line in result.stdout.splitlines()]
        assert len(weights) == len(cases)
        for index,(points,(weight,squares)) in enumerate(zip(cases,weights)):
            assert weight == dense_mst(points,slug),(slug,index,points,weight)
            if slug == 'nomadism-day':
                assert squares == dense_mst(points,'squared'),(slug,index,'squared MST')
        print(f'{slug}: {len(cases)} dense-graph comparisons passed',flush=True)
        tour_count = 0
        for index in [*range(0,len(cases),13),*range(len(cases)-6,len(cases))]:
            points = cases[index]
            result = subprocess.run([str(executable(slug))],input=encode(points),
                                    capture_output=True,check=True,timeout=10)
            cost = tour_cost(points,result.stdout.split(),slug)
            assert cost <= 2*weights[index][0],(slug,index,cost,weights[index][0])
            tour_count += 1
        checker_count = check_checker(slug)
        counts[slug] = {'mst_cases':len(cases),'tour_cases':tour_count,'checker_cases':checker_count}
        print(f'{slug}: {tour_count} tours and {checker_count} checker decisions passed',flush=True)
    (ROOT/'build/R8-checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
