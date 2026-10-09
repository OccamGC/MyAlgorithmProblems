"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    n,mode=spec['n'],spec['mode']
    if mode=='same-first':a=[(1000000000,i-n//2) for i in range(n)]
    elif mode=='same-second':a=[(i-n//2,-1000000000) for i in range(n)]
    elif mode=='sum-ties':a=[(i-n//2,n//2-i) for i in range(n)]
    else:a=[(i-n//2,(-1 if i%2 else 1)*1000000000) for i in range(n)]
    if mode=='descending':a.reverse()
    elif mode=='zigzag':a=a[::2]+a[1::2][::-1]
    elif mode not in ('ascending','same-first','same-second','sum-ties'):rng.shuffle(a)
    return str(n)+'\n'+'\n'.join(f'{x} {y}' for x,y in a)+'\n'


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
