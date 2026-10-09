"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess



def generate(case):
    rng=random.Random(case['seed'])
    n,m,K=case['n'],case['m'],case['K'];mode=case['mode']
    rows=[f'{n} {m} {K}']
    for i in range(n):
        rows.append(' '.join(str((i*m+j) if mode=='rotation' else rng.randint(0,10**9)) for j in range(m)))
    for i in range(K):
        op=3 if mode=='rotation' else rng.randrange(1,4)
        if op==3:
            rows.append('3');n,m=m,n
        else:
            bound=n if op==1 else m
            if mode=='invalid':a,b=rng.choice([-30,0,30]),rng.choice([-30,0,30])
            elif mode=='mixed' and i%4==0:a,b=rng.randint(-30,30),rng.randint(-30,30)
            else:a,b=rng.randint(1,bound),rng.randint(1,bound)
            rows.append(f'{op} {a} {b}')
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
