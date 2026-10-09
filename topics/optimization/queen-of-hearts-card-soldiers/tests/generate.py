"""Reproduce formal input recipes with the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    n=case['n'];mode=case['mode'];points=[]
    for i in range(n):
        if mode=='increasing':point=(i,i)
        elif mode=='decreasing':point=(i,-i)
        elif mode=='equal':point=(1000000000,-1000000000)
        elif mode=='ties':point=(rng.randrange(10),rng.randrange(10))
        elif mode=='same-attack':point=(0,rng.randrange(-1000000000,1000000001))
        else:point=(rng.randrange(-1000000000,1000000001),rng.randrange(-1000000000,1000000001))
        points.append(point)
    rng.shuffle(points)
    return str(n)+'\n'+''.join(f'{a} {b}\n' for a,b in points)

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
