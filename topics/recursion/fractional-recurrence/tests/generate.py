"""Reproduce formal input recipes with the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    n=case['N'];mode=case['mode']
    if mode=='zero':values=[0]*n
    elif mode=='maximum':values=[1000000000]*n
    elif mode=='small':values=[i%10001 for i in range(n)]
    elif mode=='powers':
        choices=sorted({x**5+d for x in range(1,64) for d in [-1,0,1] if 0<=x**5+d<=1000000000})
        values=[choices[i%len(choices)] for i in range(n)]
    elif mode=='cutoff':values=[max(0,min(1000000000,10000000+(i%201)-100)) for i in range(n)]
    elif mode=='descending':values=[1000000000-i for i in range(n)]
    elif mode=='cluster':values=[rng.randrange(999000000,1000000001) for _ in range(n)]
    else:values=[rng.randrange(1000000001) for _ in range(n)]
    return str(n)+'\n'+' '.join(map(str,values))+'\n'

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
