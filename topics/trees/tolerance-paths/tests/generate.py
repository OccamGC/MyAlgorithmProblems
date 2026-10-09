"""Deterministic test recipes; Python standard library only."""
import argparse,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];mode=case['mode']
    edges=[(0 if mode=='star' else v-1 if mode in ['chain','holes'] else rng.randrange(v),v) for v in range(1,n)]
    bounds=[(-10**9,10**9) if mode=='broad' else (1,1) if mode=='star' else (0,0) if mode in ['chain','holes','zero'] else tuple(sorted([rng.randrange(-10,11),rng.randrange(-10,11)])) for _ in range(n)]
    special=[]
    for i in range(m):
        e=i%(n-1)
        if mode=='holes':w=2*(i//(n-1)%2)+(e%2)
        elif mode=='broad':w=rng.randrange(-100000000,100000001)
        elif mode=='star':w=(e%100)+(i//(n-1))%3
        else:w=rng.randrange(-5,6)
        if mode=='zero' and e%11==0:e=(e+1)%(n-1)
        special.append((e+1,w))
    return f'{n} {m}\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges)+''.join(f'{l} {r}\n' for l,r in bounds)+''.join(f'{e} {w}\n' for e,w in special)


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
