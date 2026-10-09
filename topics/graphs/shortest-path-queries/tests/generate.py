"""Generate reproducible formal inputs using the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    n=case['n'];m=case['m'];q=case['q'];mode=case['mode'];rows=[f'{n} {m} {q}']
    for i in range(m):
        if mode=='chain' and i<n-1:u=i+1;v=i+2;c=1000000000
        elif mode=='chain':u=1;v=1;c=0
        elif mode=='parallel':u=1;v=n;c=(1000000000-i)%1000000001
        elif mode=='disconnected':
            half=max(1,n//2);offset=0 if i%2 else half;count=half if offset==0 else n-half
            if count==0:offset=0;count=n
            u=offset+rng.randrange(count)+1;v=offset+rng.randrange(count)+1;c=rng.randrange(1000000001)
        else:u=rng.randrange(n)+1;v=rng.randrange(n)+1;c=0 if mode=='zero' else rng.randrange(1000000001)
        rows.append(f'{u} {v} {c}')
    for i in range(q):
        if q==1:u=1;v=n
        else:u=1 if case.get('one_source') else i%n+1;v=rng.randrange(n)+1
        rows.append(f'{u} {v}')
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
