"""Finite checks of the diagonal-to-orthogonal reduction; not a general proof."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path

DIAG = ((1, 1), (1, -1), (-1, 1), (-1, -1))
ORTH = ((1, 0), (0, 1), (0, -1), (-1, 0))


def transform(point, parity):
    x, y = point
    assert (x + y) % 2 == parity
    return ((x + y - parity) // 2, (x - y - parity) // 2)


def forest(points, directions):
    parent = {a: a for a in points}
    def root(a):
        while parent[a] != a:
            a = parent[a]
        return a
    for a in points:
        for dx, dy in directions:
            b = (a[0] + dx, a[1] + dy)
            if b in points and a < b:
                ra, rb = root(a), root(b)
                if ra == rb:
                    return False
                parent[ra] = rb
    return True


def run(points, moves):
    candidates = set(points)
    x = y = work = 0
    seen = {(0, 0)}
    answers = [len(candidates)]
    for dx, dy in moves:
        x, y = x + dx, y + dy
        if (x, y) not in seen:
            work += len(candidates)
            candidates = {a for a in candidates if (a[0] + x, a[1] + y) in points}
            seen.add((x, y))
        answers.append(len(candidates))
    return answers, work


def direct_answers(points, moves):
    """Move surviving absolute positions at every step, without a visited cache."""
    positions = set(points)
    answers = [len(positions)]
    for dx, dy in moves:
        positions = {(x + dx, y + dy) for x, y in positions
                     if (x + dx, y + dy) in points}
        answers.append(len(positions))
    return answers


board_checks = 0
for n in range(1, 13):
    for p in (0, 1):
        points = [(x, y) for x in range(n) for y in range(n) if (x + y) % 2 == p]
        images = [transform(a, p) for a in points]
        assert len(set(images)) == len(points)
        assert all((u + v + p, u - v) == a for a, (u, v) in zip(points, images))
        for axis in (0, 1):
            if images:
                assert max(a[axis] for a in images) - min(a[axis] for a in images) + 1 <= n
        for a, b in combinations(points, 2):
            ta, tb = transform(a, p), transform(b, p)
            diagonal = abs(a[0] - b[0]) == abs(a[1] - b[1]) == 1
            orthogonal = abs(ta[0] - tb[0]) + abs(ta[1] - tb[1]) == 1
            assert diagonal == orthogonal
        board_checks += 1

instances = forest_count = road_subsets = 0
for n in range(1, 4):
    cells = list(product(range(n), repeat=2))
    for mask in range(1 << len(cells)):
        road_subsets += 1
        points = {a for i, a in enumerate(cells) if mask >> i & 1}
        parts = [{transform(a, p) for a in points if sum(a) % 2 == p} for p in (0, 1)]
        is_forest = forest(points, DIAG)
        assert is_forest == all(forest(part, ORTH) for part in parts)
        if not is_forest:
            continue
        forest_count += 1
        for word in product(range(4), repeat=4):
            moves = [DIAG[d] for d in word]
            answers, work = run(points, moves)
            assert answers == direct_answers(points, moves)
            split = [run(part, [ORTH[d] for d in word]) for part in parts]
            assert answers == [a + b for a, b in zip(split[0][0], split[1][0])]
            assert work == split[0][1] + split[1][1]
            assert work <= (5 * n - 3) * len(points)
            instances += 1

lower = []
for k in (4, 8, 16, 32):
    original = {(u, v) for u in range(0, k, 2) for v in range(k)}
    diagonal = {(u + v, u - v + k - 1) for u, v in original}
    assert all(0 <= x < 2 * k - 1 and 0 <= y < 2 * k - 1 for x, y in diagonal)
    assert len(diagonal) == len(original)
    assert forest(diagonal, DIAG)
    old = run(original, [(0, 1)] * (k - 1))
    new = run(diagonal, [(1, -1)] * (k - 1))
    assert old == new
    expected = ((k + 1) // 2) * (k * (k + 1) // 2 - 1)
    assert new[1] == expected
    lower.append({'board_side': 2 * k - 1, 'roads': len(diagonal), 'moves': k - 1, 'checks': expected})

report = {'status': 'passed',
          'scope': 'Finite evidence for the written lattice-isomorphism proof; not a proof by enumeration.',
          'parity_board_side_range': [1, 12], 'parity_board_checks': board_checks,
          'road_subsets_n_1_to_3': road_subsets, 'forests_n_1_to_3': forest_count,
          'move_sequence_length': 4, 'forest_and_length_4_walk_cases': instances,
          'direct_simulation_answer_checks': instances, 'embedded_lower_bounds': lower}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='Optional reproducible JSON report')
args = parser.parse_args()
serialized = json.dumps(report, indent=2) + '\n'
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized, encoding='utf8', newline='\n')
print(serialized, end='')
