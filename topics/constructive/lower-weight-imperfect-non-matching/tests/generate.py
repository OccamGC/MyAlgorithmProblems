"""Deterministic test recipes; Python standard library only."""
import argparse,bisect,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];mode=case['mode'];edges=[]
    for v in range(2,n+1):
        u=1 if mode=='star' else v-1 if mode=='chain' else rng.randrange(1,v)
        edges.append((u,v,0 if mode=='zero' else 10000 if mode=='max' else rng.randrange(10001)))
    while len(edges)<m:
        u=rng.randrange(1,n+1);v=rng.randrange(1,n+1);w=0 if mode=='zero' else rng.randrange(10001)
        edges.append((u,v,w))
    rng.shuffle(edges)
    return f'{n} {m}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)


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
