"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess



def generate(case):
    rng=random.Random(case['seed'])
    N,M,mode=case['N'],case['M'],case['mode']
    if mode in ('overlap','near-miss'):s='a'*N
    elif mode=='periodic':s=('abac'*((N+3)//4))[:N]
    else:s=''.join(rng.choice('abcdefghijklmnopqrstuvwxyz' if mode=='alphabet' else 'abc') for _ in range(N))
    rows=[s,str(M)]
    for i in range(M):
        l,r=(1,N) if i%2==0 else (rng.randint(1,N),N)
        length=rng.randint(1,40)
        if mode=='overlap':t='a'*length
        elif mode=='near-miss':t='a'*39+'b'
        elif mode=='periodic':t=('abac'*10)[:length]
        elif i%3==0:t=s[l-1:min(N,l-1+length)]
        else:t=''.join(rng.choice('abc') for _ in range(length))
        rows.append(f'{l} {r} {t}')
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
