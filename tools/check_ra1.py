"""Independent exhaustive checks for the Red Alert batch (R4)."""
import random
import subprocess
import os
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(20260928)


def run(slug, data):
    binary = ROOT / 'build' / 'bin' / (slug + ('.exe' if os.name == 'nt' else ''))
    return subprocess.run([str(binary)], input=data.encode('utf-8'), capture_output=True,
                          check=True).stdout.decode().split()


def prism_exact(n, edges, damage, probabilities, allow_cuts):
    best = Fraction(0)
    for mask in range(1 << len(edges)) if allow_cuts else [0]:
        graph = [[] for _ in range(n)]
        for i, (u, v) in enumerate(edges):
            if not mask & (1 << i):
                graph[u].append(v)
                graph[v].append(u)

        def visit(u, parent):
            children = [v for v in graph[u] if v != parent]
            value = damage[u]
            if children:
                value += sum(visit(v, u) for v in children) * (
                    probabilities[u] + (1 - probabilities[u]) / len(children))
            return value

        best = max(best, *(visit(root, -1) for root in range(n)))
    return best


def check_prism():
    for _ in range(250):
        n = RNG.randint(1, 7)
        edges = [(RNG.randrange(v), v) for v in range(1, n) if RNG.randrange(4)]
        block_limit = RNG.randint(0, len(edges))
        damage = [Fraction(RNG.randrange(1001), 100) for _ in range(n)]
        probabilities = [Fraction(RNG.randrange(1001), 1000) for _ in range(n)]
        answer = prism_exact(n, edges, damage, probabilities, block_limit > 0)
        for cents in range(101):
            shifted = answer + Fraction(cents, 100)
            rounded = (shifted + Fraction(1, 2)).numerator // (shifted + Fraction(1, 2)).denominator
            if abs(shifted - rounded) <= Fraction(3, 10):
                break
        data = f'{n} {block_limit} {len(edges)} {cents / 100:.2f}\n'
        data += ''.join(f'{u+1} {v+1}\n' for u, v in edges)
        data += ' '.join(f'{float(x):.2f}' for x in damage) + '\n'
        data += ' '.join(f'{float(x):.3f}' for x in probabilities) + '\n'
        assert run('prism-tank', data) == [str(rounded)], data
    return 250


def commando_brute(bounds, operations):
    xmin, ymin, xmax, ymax = bounds
    grid = {(x, y): 0 for x in range(xmin, xmax + 1) for y in range(ymin, ymax + 1)}
    result = []
    for operation in operations:
        op, x1, y1, a, b, *rest = operation
        if op == 0:
            result.append(sum(value for (x, y), value in grid.items()
                              if x1 <= x <= a and y1 <= y <= b))
        elif op == 2:
            for x, y in grid:
                if x1 <= x <= a and y1 <= y <= b:
                    grid[x, y] -= rest[0]
        else:
            radius, power = a, b
            for x, y in grid:
                dx, dy = abs(x - x1), abs(y - y1)
                if radius == 1:
                    if dx == dy == 0:
                        grid[x, y] += power
                elif dx < radius and dy < radius:
                    grid[x, y] += power
                elif (dx == radius and dy < radius - 1) or (dy == radius and dx < radius - 1):
                    grid[x, y] += (power + 3) // 4
    return list(map(str, result))


def check_commando():
    # Exact coordinate extremes, fringe rounding, negative values and clipping.
    edge = 10**8
    bounds = (edge, edge, edge, edge)
    operations = [(1, edge - 2, edge, 2, 1), (0, edge, edge, edge, edge),
                  (2, edge - 1, edge - 1, edge, edge, 5),
                  (1, edge - 2, edge - 2, 2, 10000),
                  (0, edge, edge, edge, edge), (1, edge, edge, 1, 0)]
    data = f'{len(operations)} ' + ' '.join(map(str, bounds)) + '\n'
    data += ''.join(' '.join(map(str, op)) + '\n' for op in operations)
    assert run('psychic-commando', data) == commando_brute(bounds, operations), data

    # Maximum dimensions and update count; known sums exceed 32-bit range.
    header = '30000 99999000 -100000000 100000000 -99999000\n'
    query = '0 99999000 -100000000 100000000 -99999000\n'
    count = 29999
    magnitude = count * 10000 * 1001 * 1001
    for update, expected in [
        ('1 100000000 -100000000 100000000 10000\n', magnitude),
        ('2 99999000 -100000000 100000000 -99999000 10000\n', -magnitude),
    ]:
        assert run('psychic-commando', header + update * count + query) == [str(expected)]

    assert run('psychic-commando', '2 0 0 0 0\n1 0 0 1 1\n2 0 0 0 0 2\n') == []

    for _ in range(250):
        xmin = RNG.randint(-5, 0)
        ymin = RNG.randint(-5, 0)
        bounds = (xmin, ymin, xmin + RNG.randrange(7), ymin + RNG.randrange(7))
        operations = []
        for turn in range(RNG.randint(1, 30)):
            op = 0 if turn == 0 else RNG.randrange(3)
            if op == 1:
                operations.append((1, RNG.randint(-9, 9), RNG.randint(-9, 9),
                                   RNG.choice([1, 2, 3, 10**8]), RNG.randint(0, 10)))
            else:
                x1, x2 = sorted(RNG.choices(range(-9, 10), k=2))
                y1, y2 = sorted(RNG.choices(range(-9, 10), k=2))
                operations.append((op, x1, y1, x2, y2) + ((RNG.randint(0, 10),) if op == 2 else ()))
        data = f'{len(operations)} ' + ' '.join(map(str, bounds)) + '\n'
        data += ''.join(' '.join(map(str, op)) + '\n' for op in operations)
        assert run('psychic-commando', data) == commando_brute(bounds, operations), data
    return 254


def elite_brute(types, units, hp, attack, addition):
    initial = tuple((types[t][0] + attack - 1) // attack for t in units)
    states = {(initial, -1): hp + addition}
    for removed in range(len(types)):
        remaining = tuple(0 if t == removed else shots for t, shots in zip(units, initial))
        states[remaining, -1] = max(states.get((remaining, -1), 0), hp)
    best = 0
    for total in range(sum(initial), -1, -1):
        layer = [(state, health) for state, health in states.items() if sum(state[0]) == total]
        for (remaining, lock), health in layer:
            if total == 0:
                best = max(best, health)
            for i, shots in enumerate(remaining):
                if shots == 0 or (lock != -1 and units[i] != lock):
                    continue
                following = list(remaining)
                following[i] -= 1
                new_health = health - sum(types[t][1] for t, s in zip(units, following) if s)
                if new_health <= 0:
                    continue
                next_lock = units[i] if types[units[i]][1] > 0 else -1
                if next_lock != -1 and not any(t == next_lock and s for t, s in zip(units, following)):
                    next_lock = -1
                key = (tuple(following), next_lock)
                states[key] = max(states.get(key, 0), new_health)
    return str(best) if best else 'leave!'


def check_elite():
    boundary = '2 2 1 1 0\nEnemyA 2 1\nEnemyB 2 1\nEnemyA\nEnemyB\n'
    assert run('elite-combatant', boundary) == ['leave!'], boundary
    for _ in range(250):
        kinds = RNG.randint(1, 4)
        types = [(RNG.randint(1, 5), RNG.randint(-5, 7)) for _ in range(kinds)]
        units = [RNG.randrange(kinds) for _ in range(RNG.randint(1, 5))]
        hp = RNG.randint(1, 25)
        attack = RNG.randint(1, 5)
        addition = RNG.randint(0, 25)
        data = f'{kinds} {len(units)} {hp} {attack} {addition}\n'
        data += ''.join(f'Unit{i} {h} {a}\n' for i, (h, a) in enumerate(types))
        data += ''.join(f'Unit{i}\n' for i in units)
        expected = elite_brute(types, units, hp, attack, addition)
        assert run('elite-combatant', data) == [expected], (data, expected)
    return 251


if __name__ == '__main__':
    for label, check in [('prism', check_prism), ('commando', check_commando), ('elite', check_elite)]:
        print(f'{label}: {check()} comparisons passed', flush=True)
