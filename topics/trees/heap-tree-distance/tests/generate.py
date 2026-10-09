"""Reproduce the accompanying input recipes using Python's standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);pairs=[];mode=case['mode']
    extremes=[(1,1),(1,10**18),(10**18,10**18),(2**59,2**59-1),(10**18,10**18-1),(2,3),(2**59,3*2**58)]
    for i in range(case['m']):
        if mode=='boundary':a,b=extremes[i%len(extremes)]
        elif mode=='equal':a=b=rng.randint(1,10**18)
        elif mode=='ancestor':b=rng.randint(1,10**18);a=max(1,b>>rng.randrange(60))
        elif mode=='siblings':a=2*rng.randint(1,5*10**17-1);b=a+1
        elif mode=='opposite':a=rng.randint(2**59,3*2**58-1);b=rng.randint(3*2**58,10**18)
        else:a=rng.randint(1,10**18);b=rng.randint(1,10**18)
        pairs.append(f'{a} {b}')
    return str(len(pairs))+'\n'+'\n'.join(pairs)+'\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    selected = set(args.case or [case['id'] for case in plan['cases']])
    unknown = selected - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if case['id'] not in selected:
            continue
        path = args.out_dir / (case['id'] + '.in')
        path.write_text(generate(case), encoding='ascii', newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())], stdin=source,
                                        stdout=subprocess.PIPE, check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n', b'\n'))

if __name__ == '__main__':
    main()
