"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    digits, k, p, mode = spec['digits'], spec['k'], spec['p'], spec['mode']
    if mode == 'max-n': n='1'+'0'*1000
    elif mode == 'zero': n='0'
    elif mode == 'small': n=str(rng.randrange(101))
    elif mode == 'ones': n='9'*digits
    else: n=str(rng.randrange(1,10))+''.join(str(rng.randrange(10)) for _ in range(digits-1))
    return f'{n} {k} {p}\n'


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
        if args.cases and spec['id'] not in args.cases:continue
        text = generate(spec)
        path = args.out_dir / (spec['id']+'.in')
        path.write_text(text,encoding='ascii',newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())],stdin=source,capture_output=True,check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n',b'\n'))


if __name__=='__main__':main()
