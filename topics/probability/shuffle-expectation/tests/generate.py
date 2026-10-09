"""Generate deterministic inputs and optional LF-normalized reference outputs."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec):
    rng=random.Random(spec['seed'])
    n,mode=spec['n'],spec['mode']
    if mode=='ascending': a=list(range(1,n+1))
    elif mode=='descending': a=list(range(n,0,-1))
    elif mode=='equal': a=[n]*n
    elif mode=='duplicate': a=[1]*(n//2)+[n]*(n-n//2)
    elif mode=='three-values': a=[rng.choice([1,(n+1)//2,n]) for _ in range(n)]
    else: a=[rng.randrange(1,n+1) for _ in range(n)]
    return str(n)+'\n'+' '.join(map(str,a))+'\n'

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
