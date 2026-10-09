"""Deterministic test recipes; Python standard library only."""
import argparse,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];bmax=case['bmax'];mode=case['mode']
    b=[rng.randint(1,bmax) for _ in range(n)];a=[10**16]*n
    if mode=='staggered':b=[bmax]*n;a=[i*bmax for i in range(n)]
    elif mode=='zero':b=[0]*n;a=[rng.choice([0,10**16]) for _ in range(n)]
    elif mode=='covered':a=[m*v for v in b]
    elif mode=='impossible':a[0]=a[1]=0
    elif mode=='overflow':b=[bmax]*n;a=[0]*n
    elif mode=='single':b=[0]*(n-1)+[bmax];a[-1]=0
    elif mode=='random':
        order=list(range(n));rng.shuffle(order)
        for t,i in enumerate(order[:min(n,m)]):a[i]=b[i]*rng.randrange(t,m)+rng.randrange(b[i])
    elif mode=='late-conflict':
        for i in range(min(n,m)):a[i]=b[i]*(m-2)
    return f'{n} {m}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    requested = set(args.case)
    unknown = requested - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if requested and case['id'] not in requested:
            continue
        target = args.out_dir / (case['id'] + '.in')
        target.write_text(generate(case), encoding='utf-8', newline='\n')
        if args.std:
            with target.open('rb') as source, target.with_suffix('.out').open('wb') as output:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=output, check=True)
if __name__ == '__main__':
    main()
