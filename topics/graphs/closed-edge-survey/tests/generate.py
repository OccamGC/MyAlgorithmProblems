"""Deterministic test recipes; Python standard library only."""
import argparse,bisect,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];mode=case['mode'];edges=[]
    if mode in ['tree','star']:
        for v in range(1,n):edges.append((0 if mode=='star' else rng.randrange(v),v,rng.randrange(1001)))
    else:
        leaves=case.get('leaves',0);core=n-leaves
        edges=[(i,(i+1)%core,rng.randrange(1001)) for i in range(core)]
        if mode=='chords':
            endpoints=rng.sample(range(core),20)
            edges += [(endpoints[i],endpoints[i+1],rng.randrange(1001)) for i in range(0,20,2)]
        else:
            for v in range(core,n):edges.append((0,v,rng.randrange(1001)))
            for _ in range(case.get('extra_pairs',0)):
                u,v=rng.sample(range(core),2);edges.extend([(u,v,rng.randrange(1001)),(u,v,rng.randrange(1001))])
        if mode=='zero':edges=[(u,v,0) for u,v,w in edges]
    rng.shuffle(edges)
    return f'{n} {len(edges)}\n'+''.join(f'{u+1} {v+1} {w}\n' for u,v,w in edges)


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
