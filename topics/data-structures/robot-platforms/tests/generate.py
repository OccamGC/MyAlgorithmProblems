"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess


def generate(case):
    rng = random.Random(case['seed'])
    n, m, mode = case['n'], case['m'], case['mode']
    size = n
    lines = [f'{n} {m}']
    for i in range(m):
        if mode == 'empty-cycle':
            op = [0, 4, 0, 2, 3, 1, 4, 1, 2, 4, 0, 4][i % 12]
        elif mode == 'insert':
            op = 4 if i % 17 == 16 else 1
        elif mode == 'delete':
            op = 4 if i % 7 == 6 else 0
        elif mode == 'moves':
            op = 4 if i % 11 == 10 else 2 + i % 2
        elif mode == 'query':
            op = 4
        else:
            op = rng.randrange(5)
        if op in (2, 3):
            if size == 0:
                x = rng.choice([-10**9, 0, 10**9])
            else:
                step = 500 if mode == 'moves' else rng.randint(-500, 500)
                laps = rng.randint(-5000, 5000)
                x = laps * size + step
                if abs(x) > 10**9:
                    x = step
            lines.append(f'{op} {x}')
        else:
            lines.append(str(op))
        if op == 0:
            size = max(0, size - 1)
        elif op == 1:
            size += 1
    return '\n'.join(lines) + '\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    selected = set(args.case or [case['id'] for case in plan['cases']])
    unknown = selected - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if case['id'] not in selected:
            continue
        path = args.out_dir / (case['id'] + '.in')
        path.write_text(generate(case), encoding='ascii', newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())], stdin=source,
                                        stdout=subprocess.PIPE, check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n', b'\n'))

if __name__ == '__main__':
    main()
