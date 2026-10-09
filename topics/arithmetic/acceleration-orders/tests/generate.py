"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess



def generate(case):
    rng=random.Random(case['seed'])
    T=case['T'];mode=case['mode'];rows=[]
    boundary=[-10000,-9999,-1,0,1,9999,10000]
    for i in range(T):
        if mode=='boundary':
            a=boundary[i%len(boundary)];t=boundary[i//len(boundary)%len(boundary)]
        elif mode=='zero':
            a,t=(0,rng.randint(-10000,10000)) if i%2 else (rng.randint(-10000,10000),0)
        elif mode=='odd':
            a=2*rng.randrange(-5000,5000)+1;t=2*rng.randrange(-5000,5000)+1
        else:
            a=rng.randint(-10000,10000);t=rng.randint(-10000,10000)
        rows.append(f'{a} {t}')
    return str(T)+'\n'+''.join(row+'\n' for row in rows)

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
