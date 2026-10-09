"""Independent small-instance oracles for the six R6 programs."""
from collections import Counter
from functools import lru_cache
import itertools
import json
import math
import os
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / 'build/bin'
MODULUS = 100000007


def execute(slug, text):
    path = BIN / (slug + ('.exe' if os.name == 'nt' else ''))
    result = subprocess.run([str(path)], input=text.encode('utf-8'), capture_output=True,
                            check=True, timeout=20)
    return result.stdout.decode('utf-8').split()


def graph_input(n, edges):
    return f'{n} {len(edges)}\n' + ''.join(f'Unit{u} Unit{v}\n' for u, v in edges)


def cover_oracle(n, edges):
    actions = [1 << i for i in range(n)] + [(1 << u) | (1 << v) for u, v in edges]

    @lru_cache(None)
    def solve(mask):
        if mask == (1 << n) - 1:
            return 0
        first = next(i for i in range(n) if not mask >> i & 1)
        return 1 + min(solve(mask | action) for action in actions if action >> first & 1)

    return solve(0)


def check_chaos():
    rng = random.Random(2026092808)
    cases = []
    for n in range(1, 6):
        possible = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            cases.append((n, [edge for i, edge in enumerate(possible) if mask >> i & 1]))
    for _ in range(200):
        n = rng.randint(6, 12)
        cases.append((n, [edge for edge in itertools.combinations(range(n), 2) if rng.randrange(3) == 0]))
    for n, edges in cases:
        data = graph_input(n, edges)
        assert execute('chaos-drone', data) == [str(cover_oracle(n, edges))], data
    data = '5 2\n甲 A\na -700\n'
    assert execute('chaos-drone', data) == ['3']
    return len(cases) + 1


def shield_input(buildings, events, m, r, s):
    attacks = [event for event in events if event[-1] >= 0]
    repairs = [event for event in events if event[-1] < 0]
    rows = [f'{len(buildings)} {m} {r} {s} {len(attacks)} {len(repairs)}']
    rows += [f'{x} {t}' for x, t in buildings]
    rows += [f'{l} {h} {t} {k} {abs(d)}' for l, h, t, k, d in attacks + repairs]
    return '\n'.join(rows) + '\n'


def shield_oracle(buildings, events, m, r, s):
    horizon = max((t+k-1 for _, _, t, k, _ in events), default=0)
    damage = [[0] * (horizon+1) for _ in buildings]
    for i, (x, born) in enumerate(buildings):
        for l, h, t, k, amount in events:
            if l <= x <= h:
                for moment in range(max(t, born), t+k):
                    damage[i][moment] += amount
    baseline = sum(map(sum, damage))
    positions = sorted({x for x, _ in buildings})

    @lru_cache(None)
    def search(t):
        if t > horizon:
            return 0
        best = search(t+1)
        for l in positions:
            for h in positions:
                if not l <= h <= l+m:
                    continue
                saved = sum(sum(damage[i][t:min(horizon+1, t+r)])
                            for i, (x, born) in enumerate(buildings)
                            if l <= x <= h and born <= t)
                best = max(best, saved + search(t+r+s))
        return best

    return baseline - search(1)


def check_shield():
    rng = random.Random(2026092809)
    cases = [([(0, 1)], [], 0, 1, 0),
             ([(0, 1)], [(0, 0, 1, 1, 5)], 0, 1, 0),
             ([(0, 1), (1, 1)], [(0, 1, 1, 1, 5)], 1, 1, 0),
             ([(0, 1)], [(0, 0, 1, 3, -4)], 0, 2, 1),
             ([(0, 1), (0, 2)], [(0, 0, 1, 3, 5)], 0, 3, 1),
             ([(0, 3)], [(0, 0, 1, 5, 10)], 0, 1, 0)]
    for _ in range(240):
        buildings = [(rng.randint(-2, 2), rng.randint(1, 8)) for _ in range(rng.randint(1, 7))]
        events = []
        for _ in range(rng.randint(0, 7)):
            l, h = sorted([rng.randint(-3, 3), rng.randint(-3, 3)])
            t = rng.randint(1, 7)
            events.append((l, h, t, rng.randint(1, 8-t), rng.randint(-7, 7)))
        cases.append((buildings, events, rng.randint(0, 5), rng.randint(1, 5), rng.randint(0, 4)))
    for case in cases:
        data = shield_input(*case)
        assert execute('force-shield', data) == [str(shield_oracle(*case))], data
    return len(cases)


def imploder_oracle(points, operations):
    points = [list(point) for point in points]
    answers = []
    for operation in operations:
        code, *args = operation
        if code == 7:
            answers.extend(points[args[0]-1])
            continue
        l, r, *extra = args
        for i in range(l-1, r):
            x, y = points[i]
            if code == 0:
                x += extra[0]
            elif code == 1:
                y += extra[0]
            elif code == 2:
                y = -y
            elif code == 3:
                x = -x
            elif code == 4:
                x, y = y, x
            elif code == 5:
                x, y = -y, -x
            else:
                angle = math.radians(extra[0])
                x, y = x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)
            points[i] = [x, y]
    answers.extend(itertools.chain.from_iterable(points))
    return answers


def imploder_input(points, operations):
    return '\n'.join([f'{len(points)} {len(operations)}',
                      *(' '.join(map(str, p)) for p in points),
                      *(' '.join(map(str, op)) for op in operations)]) + '\n'


def check_imploder():
    rng = random.Random(2026092810)
    for _ in range(220):
        n = rng.randint(1, 10)
        points = [(rng.randint(-100, 100), rng.randint(-100, 100)) for _ in range(n)]
        operations = []
        for _ in range(rng.randint(1, 60)):
            code = rng.randrange(8)
            l, r = sorted([rng.randint(1, n), rng.randint(1, n)])
            op = [code, l] if code == 7 else [code, l, r]
            if code <= 1:
                op.append(rng.randint(-100, 100))
            if code == 6:
                op.append(rng.randint(0, 360))
            operations.append(op)
        data = imploder_input(points, operations)
        actual = list(map(float, execute('vacuum-imploder', data)))
        expected = imploder_oracle(points, operations)
        assert len(actual) == len(expected)
        assert all(abs(a-b) < 1e-6 for a, b in zip(actual, expected)), data
    return 220


def check_toolkit():
    rng = random.Random(2026092811)
    cases = [[], [(10, 2), (1, 10), (1, 10)], [(0, 1000)] * 10, [(1000, 0)] * 10]
    for _ in range(220):
        cases.append([(rng.randint(0, 6), rng.randint(0, 12)) for _ in range(rng.randint(0, 7))])
    for boxes in cases:
        limits = [min(k, v//i) for i, (k, v) in enumerate(boxes, 1)]
        totals = Counter(map(sum, itertools.product(*(range(c+1) for c in limits))))
        expected = [str(totals[i] % MODULUS) for i in range(sum(limits)+1)]
        data = str(len(boxes))+'\n'+''.join(f'{k} {v}\n' for k,v in boxes)
        assert execute('upgrade-toolkit', data) == expected, data
    return len(cases)


def xor_sum(values):
    answer = 0
    for i in range(len(values)):
        value = 0
        for j in range(i, len(values)):
            value ^= values[j]
            answer += value
    return answer


def check_nano():
    rng = random.Random(2026092812)
    for _ in range(240):
        n = rng.randint(1, 14)
        values = [rng.choice([0, 1, 65535, 65536, rng.randint(0, 65536)]) for _ in range(n)]
        rows = [f'{n} 50', ' '.join(map(str, values))]
        expected = []
        for _ in range(50):
            if rng.randrange(3):
                l, r = sorted([rng.randint(1,n), rng.randint(1,n)])
                rows.append(f'1 {l} {r}')
                expected.append(str(xor_sum(values[l-1:r])))
            else:
                p, value = rng.randint(1,n), rng.randint(0,65536)
                rows.append(f'2 {p} {value}')
                values[p-1] = value
        data = '\n'.join(rows)+'\n'
        assert execute('nano-computer', data) == expected, data
    return 240


def check_clone():
    rng = random.Random(2026092813)
    sources = []
    for n in (1, 3, 5):
        sources.extend(''.join(chars) for chars in itertools.product('0123', repeat=n))
    sources += [''.join(rng.choices('0123', k=7)) for _ in range(150)]
    queries = []
    expected = []
    for source in sources:
        n = len(source)
        best = {}
        for chars in itertools.product('0123', repeat=n//2+1):
            left = ''.join(chars[:-1])
            target = left+chars[-1]+left
            distance = sum(a != b for a,b in zip(source, target))
            best.setdefault(distance, target)
        for m in range(n+1):
            queries.append(f'{n} {m} {source}')
            expected.append(best.get(m, 'failed'))
    data = str(len(queries))+'\n'+'\n'.join(queries)+'\n'
    assert execute('cloning-vat', data) == expected
    return len(queries)


def check_checker():
    checker = BIN / ('vacuum-checker.exe' if os.name == 'nt' else 'vacuum-checker')
    with tempfile.TemporaryDirectory(dir=ROOT / 'build') as folder:
        directory = Path(folder)
        source = directory/'test.in'
        answer = directory/'test.out'
        candidate = directory/'user.out'
        source.write_text('2 1\n0 0\n1 2\n7 1\n')
        answer.write_text('0 0\n0 0\n1 2\n')
        cases = [('0 0\n0 0\n1 2\n', 0), ('0.049 0\n0 0\n1 2\n', 0),
                 ('0.051 0\n0 0\n1 2\n', 1), ('0 0 0 0 1', 1),
                 ('0 0 0 0 1 2 9', 1), ('nan 0 0 0 1 2', 1),
                 ('inf 0 0 0 1 2', 1), ('0 0 0 0 1 3', 1)]
        for text, code in cases:
            candidate.write_text(text)
            actual = subprocess.run([str(checker), str(source), str(answer), str(candidate)], check=False)
            assert actual.returncode == code, (text, actual.returncode)
    return len(cases)


CHECKS = {'chaos-drone': check_chaos, 'force-shield': check_shield,
          'vacuum-imploder': check_imploder, 'upgrade-toolkit': check_toolkit,
          'nano-computer': check_nano, 'cloning-vat': check_clone, 'checker': check_checker}


def main():
    results = {}
    for name, check in CHECKS.items():
        results[name] = check()
        print(f'{name}: {results[name]} independent cases passed', flush=True)
    (ROOT/'build/R6-checks.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
