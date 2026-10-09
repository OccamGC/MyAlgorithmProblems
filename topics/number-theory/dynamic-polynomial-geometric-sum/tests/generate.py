"""Deterministic test recipes; Python standard library only."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];k=case['k'];a=case['a'];mode=case['mode'];bound=20 if case['group']==1 else 1000 if case['group']==2 else 10**9
    b=[rng.randrange(1000000007) for _ in range(k+1)]
    lines=[f'{n} {m} {k} {a}',' '.join(map(str,b))]
    for i in range(m):
        if mode=='n' or mode=='mixed' and i%2==0:lines.append(f'1 {rng.randint(1,bound)}')
        else:lines.append(f'2 {rng.randint(0,k)} {rng.randrange(1000000007)}')
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
