"""Reproduce the accompanying input recipes using Python's standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);n=case['n'];mode=case['mode']
    if mode=='self':target=list(range(n))
    elif mode=='cycle':target=[(i+1)%n for i in range(n)]
    elif mode=='chain':target=[min(i+1,n-1) for i in range(n)]
    elif mode=='tail-cycle':target=[i+1 for i in range(n)];target[-1]=n//2
    elif mode=='star':target=[0]*n
    elif mode=='pairs':target=[i^1 if (i^1)<n else i for i in range(n)]
    else:target=[rng.randrange(n) for _ in range(n)]
    if case.get('relabel'):
        labels=list(range(n));rng.shuffle(labels);new=[0]*n
        for i,v in enumerate(target):new[labels[i]]=labels[v]
        target=new
    return str(n)+'\n'+''.join(str(v+1)+'\n' for v in target)

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
