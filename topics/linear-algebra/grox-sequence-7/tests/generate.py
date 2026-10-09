"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    k,mode=spec['k'],spec['mode'];n=1<<k
    rows=[]
    duplicate=[rng.randrange(1000) for _ in range(n)]
    for i in range(n):
        if mode=='zero':a=[0]*n
        elif mode=='equal':a=duplicate
        elif mode=='constant':a=[i%1000]+[0]*(n-1)
        elif mode=='monomial':a=[i+1 if j==i else 0 for j in range(n)]
        elif mode=='maximum':a=[999 if (i+j)%3 else 998 for j in range(n)]
        else:a=[rng.randrange(1000) for _ in range(n)]
        rows.append(' '.join(map(str,a)))
    return str(k)+'\n'+'\n'.join(rows)+'\n'


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
