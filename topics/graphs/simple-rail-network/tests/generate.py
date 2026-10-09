"""Generate deterministic inputs and optional LF-normalized reference outputs."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec):
    rng=random.Random(spec['seed'])
    n,m,mode=spec['n'],spec['m'],spec['mode']
    yield f'{n} {m}\n'
    for i in range(m):
        if mode=='negative-loops':
            a=b=1; w=-1000000000
        elif mode=='disconnected':
            a=rng.randrange(1,n); b=rng.randrange(1,n); w=rng.randrange(-1000000000,1000000001)
        elif mode=='parallel':
            a=1; b=2; w=rng.randrange(1,1000000001)
        elif mode=='boruvka':
            if i<n-1:
                a=i+1; b=i+2
                # Weight by the trailing-zero count of the boundary index.
                boundary=i+1
                level=0
                while boundary%2==0: level+=1; boundary//=2
                w=level+1
            else:
                a=rng.randrange(1,n+1); b=rng.randrange(1,n+1); w=1000000000
        elif mode=='all-negative':
            a=i+1 if i<n-1 else rng.randrange(1,n+1)
            b=i+2 if i<n-1 else rng.randrange(1,n+1)
            w=-rng.randrange(1,1000000001)
        else:
            a=i+1 if i<n-1 else rng.randrange(1,n+1)
            b=i+2 if i<n-1 else rng.randrange(1,n+1)
            w=rng.randrange(1,1000000001)
            if mode=='mixed' and i%3==0: w=-w
            if mode=='zero': w=0
        yield f'{a} {b} {w}\n'

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
        if args.cases and spec['id'] not in args.cases: continue
        path=args.out_dir/(spec['id']+'.in')
        with path.open('w',encoding='ascii',newline='\n') as stream:
            for line in generate(spec): stream.write(line)
        if args.std:
            with path.open('rb') as source:
                result=subprocess.run([str(args.std.resolve())],stdin=source,capture_output=True,check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n',b'\n'))

if __name__=='__main__':
    main()
