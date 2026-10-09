"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    n,mode = spec['n'],spec['mode']
    rows = [str(n)]
    for v in range(2,n+1):
        if mode == 'chain': parent = v-1
        elif mode == 'star': parent = 1
        elif mode == 'balanced': parent = v//2
        elif mode == 'broom': parent = v-1 if v <= n//2 else n//2
        else: parent = rng.randrange(1,v)
        w = 0 if mode == 'zero' else 10000 if mode == 'chain' else rng.randrange(10001)
        rows.append(f'{parent} {v} {w}')
    return '\n'.join(rows)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', dest='cases')
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    known = {case['id'] for case in plan['cases']}
    if args.cases and set(args.cases)-known:
        parser.error('unknown case: '+', '.join(sorted(set(args.cases)-known)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in plan['cases']:
        if args.cases and spec['id'] not in args.cases:
            continue
        text = generate(spec)
        file = args.out_dir/(spec['id']+'.in')
        file.write_text(text, encoding='ascii', newline='\n')
        if args.std:
            output = subprocess.check_output([str(args.std.resolve())],input=text.encode('ascii'))
            file.with_suffix('.out').write_bytes(output.replace(b'\r\n',b'\n'))


if __name__ == '__main__':
    main()
