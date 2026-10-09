"""Deterministic test recipes; Python standard library only."""
import argparse,collections,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);n=case['n'];p=list(range(1,n+1));mode=case['mode']
    if mode=='reverse':p.reverse()
    elif mode=='random':rng.shuffle(p)
    elif mode=='middle':p=p[1:n//2+1]+[1]+p[n//2+1:]
    elif mode=='zigzag':p=p[::2]+p[1::2][::-1]
    return str(n)+'\n'+' '.join(map(str,p))+'\n'


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
            import importlib.util
            spec=importlib.util.spec_from_file_location('local_judge',Path(__file__).parents[1]/'judge.py')
            judge=importlib.util.module_from_spec(spec);spec.loader.exec_module(judge)
            hidden=judge.read_hidden(target.read_text('utf-8'))
            judge.run(args.std,hidden)
            target.with_suffix('.out').write_text(' '.join(map(str,hidden))+'\n','utf-8',newline='\n')
if __name__ == '__main__':
    main()
