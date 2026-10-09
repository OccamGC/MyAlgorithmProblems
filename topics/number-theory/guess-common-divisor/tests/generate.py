"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess


def generate(case):
    rng = random.Random(case['seed'])
    n, m, k, mode = (case[key] for key in ('n', 'm', 'k', 'mode'))
    if mode == 'rich':
        values = [case.get('value', 892371480)] * n
    elif mode == 'prime':
        values = [999999937] * n
    elif mode == 'hidden':
        values = [1] * (n - m) + [999999937] * m
    elif mode == 'squares':
        values = [rng.randrange(1, 31623)**2 for _ in range(n)]
    elif mode == 'common':
        values = [31019 * (30520 + i) for i in range(n)]
    else:
        values = [rng.randrange(1, 10**9 + 1) for _ in range(n)]
    return f'{n} {m} {k}\n' + ' '.join(map(str, values)) + '\n'

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
