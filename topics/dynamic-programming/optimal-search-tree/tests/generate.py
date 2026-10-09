"""Deterministic test recipes; Python 3 standard library only."""
import argparse, json, random, subprocess
from pathlib import Path

def generate(case):
    rng = random.Random(case['seed'])
    n = case['n']
    mode = case['mode']
    if mode == 'zero':
        values = [0] * n
    elif mode == 'equal':
        values = [10**9] * n
    elif mode == 'spike':
        values = [0] * n
        values[n // 2] = 10**9
    elif mode == 'ramp':
        values = list(range(n))
    else:
        values = [rng.randrange(10**9 + 1) for _ in range(n)]
    return str(n) + '\n' + ' '.join(map(str, values)) + '\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    requested = set(args.case)
    unknown = requested - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if requested and case['id'] not in requested:
            continue
        target = args.out_dir / (case['id'] + '.in')
        target.write_text(generate(case), encoding='utf-8', newline='\n')
        if args.std:
            with target.open('rb') as source, target.with_suffix('.out').open('wb') as output:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=output, check=True)
if __name__ == '__main__':
    main()
