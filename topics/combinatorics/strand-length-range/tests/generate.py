"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(case):
    if 'queries' in case:queries=case['queries']
    else:
        rng=random.Random(case['seed']);queries=[]
        for i in range(case['M']):
            top=case['R'];L=rng.randint(1,top);R=rng.randint(L,top);K=rng.randint(1,case['K'])
            if case['mode']=='singular':K=500000004
            if case['mode']=='single':L=R
            if case['mode']=='edges':L=1 if i%2 else top;R=top;K=[1,500000004,1000000000][i%3]
            queries.append((L,R,K))
    return str(len(queries))+'\n'+''.join(' '.join(map(str,q))+'\n' for q in queries)

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
