"""Independent checks for P1's restored references.

Compile each std.cpp to build/bin/<slug>.exe before running this script.
The oracles are shared with the existing batch checkers, not the references.
"""
import importlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    counts = {}
    r1 = importlib.import_module('check_reference')
    counts['forest-ranger'] = r1.check_trail()
    r11 = importlib.import_module('check_r11')
    counts['festival-plan'] = r11.check_tree(True)
    counts['grinder'] = r11.check_tree(False)
    r6 = importlib.import_module('check_r6')
    counts['vacuum-imploder'] = r6.check_imploder()
    r7 = importlib.import_module('check_r7')
    rng = random.Random(2026093007)
    for _ in range(400):
        n = rng.randint(1, 70)
        values = [rng.randint(1, 5000) for _ in range(n)]
        control = list(range(n))
        rng.shuffle(control)
        edges = [(rng.randrange(v), v) for v in range(1, n)]
        rng.shuffle(edges)
        data = f'{n}\n' + ''.join(f'{a} {b+1}\n' for a,b in zip(values,control)) + ''.join(f'{a+1} {b+1}\n' for a,b in edges)
        assert list(map(int, r7.run('psychic-control-tree', data))) == r7.tree_oracle(values, control, edges), data
    counts['psychic-control-tree'] = 400
    r9 = importlib.import_module('check_r9')
    counts['spice-routes'] = r9.check_spice()
    counts['colony-trade'] = r9.check_trade()
    r12 = importlib.import_module('check_r12')
    for slug in ['gran-forest', 'crystal-list']:
        for index in range(520):
            r12.compare(slug, r12.random_case(slug, rng, index))
        counts[slug] = 520
    rng = random.Random(2026093012)
    for _ in range(16):
        n = 2021
        initial = [rng.randint(-10000, 10000) for _ in range(n)]
        ops = ['1 1 2021 10000', '2 1 2021 -10', '1 1 2021 7', '3 1 2021 -3',
               '4 1 2021 -3', '2 43 90 8', '1 44 88 -20', '4 1 2021 -100000000', '3 1 2021 8']
        for _ in range(60):
            l,r = sorted([rng.randint(1,n), rng.randint(1,n)])
            ops.append(f'{rng.randint(1,4)} {l} {r} {rng.randint(-10000,10000)}')
        data = f'{n} {n-1} {len(ops)}\n' + ' '.join(map(str,initial)) + '\n'
        data += ''.join(f'{i} {i+1}\n' for i in range(1,n)) + '\n'.join(ops) + '\n'
        r12.compare('gran-forest', data)
    n = 500000
    r12.compare('crystal-list', f'{n} 2 3\n' + ' '.join(['1'] * n) + f'\n1 50000\n0 1 {n} 2\n1 2 1\n0 1 {n} 1\n')
    report = {'differential': counts, 'targeted': {'gran-forest': 16, 'crystal-list': 1}}
    output = ROOT / 'build/original-priority'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'reproduced-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
