"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    n, q, mode = spec['n'], spec['q'], spec['mode']
    rows = []
    for i in range(q):
        if mode == 'empty':
            a, b = rng.randint(n+1,5000), rng.randint(n+1,5000)
        elif mode == 'zero':
            a,b = 0,i%(n+1)
        elif mode == 'long':
            a,b = 1,1
        elif mode == 'boundary':
            a,b = rng.choice([0,1,n,n+1,5000]),rng.choice([0,1,n,n+1,5000])
            a,b = min(a,5000),min(b,5000)
        else:
            a,b = rng.randrange(5001),rng.randrange(5001)
        rows.append(f'{a} {b}')
    return f'{n} {q}\n'+'\n'.join(rows)+'\n'


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
