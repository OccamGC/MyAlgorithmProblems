"""Reproduce formal input recipes with the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    arrays=[];mode=case['mode']
    for index,n in enumerate(case['sizes']):
        if mode=='identity':a=list(range(n))
        elif mode=='pairs':a=[i^1 if (i^1)<n else i for i in range(n)]
        elif mode=='cycle':a=[(i+1)%n for i in range(n)]
        elif mode=='chain':a=[min(i+1,n-1) for i in range(n)]
        elif mode=='tail-three':a=[min(i+1,n-1) for i in range(n)];a[-1]=max(n-3,0)
        elif mode=='small':a=[rng.randrange(n) for _ in range(n)]
        else:
            a=[rng.randrange(i,n) for i in range(n)]
            if index%2 and n>=3:a[-3:]=[n-2,n-1,n-3]
        names=list(range(n));rng.shuffle(names);renamed=[0]*n
        for i,v in enumerate(a):renamed[names[i]]=names[v]+1
        arrays.append(str(n)+'\n'+'\n'.join(map(str,renamed))+'\n')
    return str(len(arrays))+'\n'+''.join(arrays)

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
