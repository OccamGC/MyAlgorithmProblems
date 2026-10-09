"""Reproduce input recipes using Python standard-library tools."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])
    n=case['n'];m=case['m'];mode=case['mode']
    directions=[rng.randrange(2) for _ in range(n)]
    labels=[chr(65+rng.randrange(26)) for _ in range(n)]
    if mode=='same-label':labels=['A']*n
    rows=[f'{n} {m}']+[f'{d} {c}' for d,c in zip(directions,labels)]
    pos=0
    for i in range(m):
        d=rng.randrange(2)
        right=d!=directions[pos]
        if case['group']==1:
            upper=min(100,n-1-pos if right else pos)
            p=rng.randint(0,upper)
        elif case['group']==2:p=rng.randint(0,100)
        elif mode=='multiples':p=(10**9//n)*n
        elif mode=='extreme':p=10**9 if i%2 else 0
        else:p=rng.randint(0,10**9)
        rows.append(f'{d} {p}')
        pos=(pos+(p if right else -p))%n
    return '\n'.join(rows)+'\n'

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
