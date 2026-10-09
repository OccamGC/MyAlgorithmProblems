"""Reproduce formal input recipes with the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path
SAMPLE='8\n1 1 3 7 3 6 7 6 \n2 2 3 4 5 6 7 8 \n1 2 3 6 3 6 6 6 \n2 2 2 4 8 6 7 8 \n2 2 5 2 5 6 6 8 \n1 2 3 4 5 6 6 6 \n1 2 1 4 2 7 7 6 \n2 2 5 4 5 8 4 8\n'

def generate(case):
    rng=random.Random(case["seed"])

    n=case['n'];mode=case['mode']
    if mode=='sample':return SAMPLE
    relation=[[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if mode=='chain':relation[i][j]=i<=j
            elif mode=='diamond':relation[i][j]=i==j or i==0 or j==n-1
            elif mode=='pentagon':relation[i][j]=i==j or i==0 or j==4 or (i==1 and j==2)
            elif mode=='product':
                width=case.get('width',3);relation[i][j]=(i//width<=j//width and i%width<=j%width)
    names=list(range(n));rng.shuffle(names);inverse={v:i for i,v in enumerate(names)};a=[]
    for x,i in enumerate(names):
        row=[]
        for y,j in enumerate(names):
            if x<=y:
                bounds=[k for k in range(n) if relation[i][k] and relation[j][k]]
                result=next(k for k in bounds if all(relation[k][v] for v in bounds))
            else:
                bounds=[k for k in range(n) if relation[k][i] and relation[k][j]]
                result=next(k for k in bounds if all(relation[v][k] for v in bounds))
            row.append(inverse[result]+1)
        a.append(row)
    return str(n)+'\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n'

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
