"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess


def generate(case):
    rng = random.Random(case['seed'])
    mode = case['mode']
    length = case['length']
    if mode == 'empty':
        return '\n'
    if mode == 'zeros':
        return '0' * length + '\n'
    if mode == 'upper':
        return ''.join(rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length)) + '\n'
    if mode == 'lower':
        return ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)) + '\n'
    parts = []
    used = 0
    while used < length:
        if mode == 'cents':
            token = '.01a'
        elif mode == 'large':
            token = '999999.99Z'
        elif mode == 'integers':
            token = '999999z'
        else:
            kind = rng.randrange(5)
            value = rng.randrange(1000000)
            token = [str(value), f'{value}.{rng.randrange(100):02d}',
                     f'.{rng.randrange(10)}', f'{value}.', '000.00'][kind]
            token += rng.choice('aAzZ')
        if used + len(token) > length:
            parts.append('Q' * (length - used))
            break
        parts.append(token)
        used += len(token)
    return ''.join(parts) + '\n'

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
