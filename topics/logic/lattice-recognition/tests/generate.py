"""Reproduce formal input recipes with the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    matrices=[];n=case['n'];mode=case['mode']
    for iteration in range(case['T']):
        if mode=='all-one':a=[[1]*n for _ in range(n)]
        elif mode=='chain':a=[[int(i<=j) for j in range(n)] for i in range(n)]
        elif mode=='aliases':
            labels=[rng.randrange(max(1,n//3)) for _ in range(n)]
            a=[[int(labels[i]<=labels[j]) for j in range(n)] for i in range(n)]
        elif mode=='diamond':a=[[int(i==j or i==0 or j==n-1) for j in range(n)] for i in range(n)]
        elif mode=='no-join':a=[[int(i==j or i==0 or j==n-1 or (i in [1,2] and j in [3,4])) for j in range(n)] for i in range(n)]
        elif mode=='no-bottom':a=[[int(i==j or j==n-1) for j in range(n)] for i in range(n)]
        elif mode=='almost-chain':
            a=[[int(i<=j) for j in range(n)] for i in range(n)]
            if iteration%2:a[0][n-1]=0
            else:a[n//2][n//2]=0
        else:a=[[rng.randrange(2) for _ in range(n)] for _ in range(n)]
        names=list(range(n));rng.shuffle(names);a=[[a[i][j] for j in names] for i in names]
        matrices.append(str(n)+'\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n')
    return str(len(matrices))+'\n'+''.join(matrices)

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
