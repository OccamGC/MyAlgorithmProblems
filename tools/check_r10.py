"""Independent matching enumeration and geometric checks for melon sequels."""
import itertools
import json
import os
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(2026092910)
COUNTS = {'graph_brute': 0, 'grid_brute': 0, 'cross_algorithm': 0, 'grid_symmetry': 0,
          'grid_components': 0}


def run(slug, data):
    executable = ROOT / 'build/bin' / (slug + ('.exe' if os.name == 'nt' else ''))
    output = subprocess.check_output([str(executable)], input=data.encode('ascii'), timeout=30)
    values = output.split()
    assert len(values) == 1 and values[0].isdigit(), (slug, output)
    return int(values[0])


def graph_input(adj, q):
    return f'{len(adj)} {max(q, 1)}\n' + ''.join(
        str(len(row)) + ''.join(f' {v + 1}' for v in row) + '\n' for row in adj)


def grid_input(grid):
    return f'{len(grid)} {len(grid[0])}\n' + '\n'.join(grid) + '\n'


def grid_graph(grid):
    n, m = len(grid), len(grid[0])
    plots = {(x, y): i for i, (x, y) in enumerate(
        (x, y) for x in range(n) for y in range(m) if grid[x][y] == 'o')}
    adj = [[plots[a, b] for a, b in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if (a,b) in plots]
           for x in range(n) for y in range(m) if grid[x][y] == 'l']
    return adj, len(plots)


def brute(adj):
    best = len(adj)

    def visit(u, occupied, idle):
        nonlocal best
        if u == len(adj):
            if all(all(v in occupied for v in adj[x]) for x in idle):
                best = min(best, len(occupied))
            return
        visit(u + 1, occupied, idle + [u])
        for v in adj[u]:
            if v not in occupied:
                visit(u + 1, occupied | {v}, idle)

    visit(0, set(), [])
    return best


def check_graph():
    for mask in range(1 << 9):
        adj = [[v for v in range(3) if mask >> (3*u+v) & 1] for u in range(3)]
        assert run('melon-planting-2', graph_input(adj, 3)) == brute(adj), adj
        COUNTS['graph_brute'] += 1
    for _ in range(200):
        p, q = RNG.randrange(9), RNG.randrange(1, 11)
        adj = [RNG.sample(range(q), RNG.randrange(min(4,q)+1)) for _ in range(p)]
        assert run('melon-planting-2', graph_input(adj, q)) == brute(adj), adj
        COUNTS['graph_brute'] += 1
    print('Graph brute comparisons:', COUNTS['graph_brute'], flush=True)


def check_grid():
    for cells in itertools.product('lox', repeat=6):
        grid = [''.join(cells[:3]), ''.join(cells[3:])]
        adj, q = grid_graph(grid)
        answer = brute(adj)
        assert run('melon-planting-3', grid_input(grid)) == answer, grid
        COUNTS['grid_brute'] += 1
    for _ in range(200):
        while True:
            grid = [''.join(RNG.choice('lloox') for _ in range(4)) for _ in range(3)]
            if sum(row.count('l') for row in grid) <= 9:
                break
        adj, q = grid_graph(grid)
        answer = brute(adj)
        assert run('melon-planting-3', grid_input(grid)) == answer, grid
        assert run('melon-planting-2', graph_input(adj, q)) == answer, grid
        COUNTS['grid_brute'] += 1
        COUNTS['graph_brute'] += 1
    print('Grid brute comparisons:', COUNTS['grid_brute'], flush=True)
    for _ in range(30):
        grid = [''.join(RNG.choice('lloox') for _ in range(5)) for _ in range(5)]
        adj, q = grid_graph(grid)
        if len(adj) > 18:
            continue
        answer = run('melon-planting-3', grid_input(grid))
        assert run('melon-planting-2', graph_input(adj,q)) == answer, grid
        old_input = f'5 5 1\n' + '\n'.join(grid) + '\n'
        assert run('melon-planting', old_input) == answer, grid
        COUNTS['cross_algorithm'] += 1
    for _ in range(30):
        grid = [''.join(RNG.choice('lloox') for _ in range(8)) for _ in range(24)]
        answer = run('melon-planting-3', grid_input(grid))
        transposed = [''.join(row) for row in zip(*grid)]
        reflected = [row[::-1] for row in grid]
        swapped = [row.translate(str.maketrans('lo','ol')) for row in grid]
        for variant in (transposed, reflected, swapped):
            assert run('melon-planting-3', grid_input(variant)) == answer, grid
            COUNTS['grid_symmetry'] += 1
        doubled = grid + ['x'*8] + grid
        assert run('melon-planting-3', grid_input(doubled)) == 2*answer
        COUNTS['grid_components'] += 1
    print('Cross-algorithm and geometric checks passed', flush=True)


def main():
    check_graph()
    check_grid()
    report = dict(COUNTS, total=sum(COUNTS.values()), seed=2026092910)
    (ROOT/'build/R10-checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
