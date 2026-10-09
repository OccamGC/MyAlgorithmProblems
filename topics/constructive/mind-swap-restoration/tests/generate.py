"""Deterministic test recipes; Python standard library only."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];mode=case['mode']
    if mode=='chain':pairs=[(i,i+1) for i in range(1,m+1)]
    elif mode=='star':pairs=[(1,i+2) for i in range(m)]
    elif mode=='pairs':pairs=[(2*i+1,2*i+2) for i in range(m)]
    else:
        pairs=[];used=set()
        while len(pairs)<m:
            u=rng.randint(1,n);v=rng.randint(1,n)
            if u==v:continue
            pair=tuple(sorted((u,v)))
            if pair not in used:used.add(pair);pairs.append((u,v))
    return f'{n} {m}\n'+''.join(f'{u} {v}\n' for u,v in pairs)


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
