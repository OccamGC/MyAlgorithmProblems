"""Generate deterministic inputs and optional LF-normalized reference outputs."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec):
    rng=random.Random(spec['seed'])
    mode,total=spec['mode'],spec['total']
    if mode=='empty':
        return '0\n'
    if mode=='single-zero': strings=['0']
    elif mode=='zero': strings=['0'*total]
    elif mode=='ones': strings=['1'*total]
    elif mode=='power': strings=['1'+'0'*(total-1)]
    elif mode=='leading-zero': strings=['0'*(total-1)+'1']
    elif mode=='alternating': strings=[('10'*((total+1)//2))[:total]]
    elif mode=='many': strings=[str(i%2) for i in range(total)]
    else:
        strings=[]
        remaining=total
        while remaining:
            size=min(remaining,rng.randrange(1,4001))
            strings.append(''.join(rng.choice('01') for _ in range(size)))
            remaining-=size
    return str(len(strings))+'\n'+'\n'.join(strings)+'\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case',action='append',dest='cases')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text(encoding='utf-8'))
    unknown=set(args.cases or [])-{c['id'] for c in plan['cases']}
    if unknown:
        parser.error('unknown case: '+', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for spec in plan['cases']:
        if args.cases and spec['id'] not in args.cases:
            continue
        path=args.out_dir/(spec['id']+'.in')
        path.write_text(generate(spec),encoding='ascii',newline='\n')
        if args.std:
            with path.open('rb') as source:
                result=subprocess.run([str(args.std.resolve())],stdin=source,capture_output=True,check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n',b'\n'))

if __name__=='__main__':
    main()
