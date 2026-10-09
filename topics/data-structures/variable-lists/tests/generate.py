"""Reproduce the accompanying input recipes using Python's standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];c=case['c'];mode=case['mode'];last=n*c;ops=[]
    for i in range(m):
        if mode=='invalid':op=rng.choice([1,2,5]);identifier=rng.choice([-10**9,-1,0,10**9]);extra=[rng.randint(-10**9,10**9)] if op==5 else []
        elif mode=='append':
            op=1 if i%100000==99999 else 4
            identifier=last if op==1 else (i%n+1);extra=[]
        elif mode=='front':op=3;identifier=i%n+1;extra=[]
        elif mode=='empty':
            phase=i%6
            if phase==0:op=2;identifier=last
            elif phase==1:op=1;identifier=last
            elif phase==2:op=3;identifier=1
            elif phase==3:op=5;identifier=last
            elif phase==4:op=1;identifier=last
            else:op=2;identifier=last
            extra=[-10**9] if op==5 else []
        elif mode=='query':op=1;identifier=rng.randint(1,last);extra=[]
        else:
            op=rng.randint(1,5)
            identifier=rng.randint(1,n) if op in (3,4) else rng.choice([rng.randint(1,last),last+1,-1,0,10**9])
            extra=[rng.randint(-10**9,10**9)] if op==5 else []
        if op in (3,4):last+=1
        ops.append(' '.join(map(str,[op,identifier]+extra)))
    return f'{n}\n'+' '.join([str(c)]*n)+f'\n{m}\n'+'\n'.join(ops)+'\n'

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
