"""Deterministic test recipes; Python standard library only."""
import argparse,bisect,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];q=case['q'];mode=case['mode'];P=1000000007
    if mode=='same':s='a'*n
    elif mode=='alternating':s=('ab'*n)[:n]
    elif mode=='singular':s='a'*11879+'b'*2+'c'*84166
    elif mode=='binary':s=''.join(rng.choice('ab') for _ in range(n))
    else:s=''.join(chr(rng.randint(33,126)) for _ in range(n))
    targets=([0,1,4,2**31,P,2*P,P*(P-15),10**18]+[rng.randrange(10**18+1) for _ in range(q)])[:q]
    return f'{len(s)} {q}\n{s}\n'+'\n'.join(map(str,targets))+'\n'


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
