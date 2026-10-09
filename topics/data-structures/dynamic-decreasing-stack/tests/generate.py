"""Deterministic test recipes; Python standard library only."""
import argparse,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];shape=case['shape']
    if shape=='decreasing':a=list(range(n,0,-1))
    elif shape=='increasing':a=list(range(n))
    elif shape=='equal':a=[1000000000]*n
    else:a=[rng.randrange(case.get('alphabet',1000000001)) for _ in range(n)]
    lines=[f'{n} {m}',' '.join(map(str,a))]
    for i in range(m):
        if case.get('mode')=='updates' or i%3==0:
            x=rng.randint(1,n);v=rng.randrange(1000000001)
            if shape=='equal':v=1000000000
            if shape=='decreasing':v=n-x+1
            lines.append(f'1 {x} {v}')
        else:
            l,r=sorted([rng.randint(1,n),rng.randint(1,n)])
            if i%7==0:l=1;r=n
            lines.append(f'2 {l} {r}')
    return '\n'.join(lines)+'\n'


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
