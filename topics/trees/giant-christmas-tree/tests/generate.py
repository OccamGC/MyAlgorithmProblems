"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];shape=case['shape'];state=case['state'];lines=[f'{n} {m}']
    for v in range(2,n+1):
        u=v-1 if shape=='chain' else 1 if shape=='star' else v//2 if shape=='balanced' else rng.randrange(1,v)
        s=rng.randrange(2) if state=='random' else int(state=='on');lines.append(f'{u} {v} {s}')
    for i in range(m):
        if case['mode']=='late-cut':u=v=rng.randint(1,n);v=n if i==m-1 else v;u=1 if i==m-1 else u
        elif case['mode']=='points':u=v=rng.randint(1,n)
        elif case['mode']=='leaves':u=rng.randint(max(1,n//2),n);v=rng.randint(max(1,n//2),n)
        else:u=rng.randint(1,n);v=rng.randint(1,n)
        lines.append(f'{u} {v}')
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
