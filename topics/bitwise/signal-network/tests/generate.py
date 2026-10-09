"""Reproduce the accompanying input recipes using Python's standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);mode=case['mode'];ops=[]
    boundary=['2','3 0 127','2','1 0','1 128','1 -128','2','3 63 64','1 64','2','1 1','2','1 -1','2','3 0 0','3 127 127','1 127','2','1 -1000000000','1 1000000000','2']
    for i in range(case['N']):
        if mode=='boundary':line=boundary[i%len(boundary)]
        elif mode=='query':line='3 0 127' if i==0 else '2'
        elif mode=='flip':line='2' if i%10000==9999 else f'3 {i%64} {127-i%64}'
        elif mode=='rotate':line='3 0 15' if i==0 else ('2' if i%16==15 else f'1 {rng.choice([0,1,-1,64,127,128,-128,10**9,-10**9])}')
        elif mode=='alternating':
            if i%3==0:line=f'3 {i%128} {min(127,i%128+15)}'
            elif i%3==1:line=f'1 {i%255-127}'
            else:line='2'
        else:
            op=rng.randint(1,3)
            if op==1:line=f'1 {rng.randint(-10**9,10**9)}'
            elif op==2:line='2'
            else:l=rng.randrange(128);r=rng.randrange(l,128);line=f'3 {l} {r}'
        ops.append(line)
    return str(len(ops))+'\n'+''.join(line+'\n' for line in ops)

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
