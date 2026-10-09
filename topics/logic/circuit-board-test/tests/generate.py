"""Generate deterministic inputs and optional LF-normalized reference outputs."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec):
    rng=random.Random(spec['seed'])
    mode=spec['mode']; size=spec['T']
    yield str(size)+'\n'
    for i in range(size):
        if mode=='boundary': x=[-1,0,1,3,4,14,15,26,27,44,45,-1000000000000000000,1000000000000000000][i%13]
        elif mode=='true': x=rng.randrange(4,15)
        elif mode=='small': x=i-500
        elif mode=='negative': x=-rng.randrange(1,1000000000000000001)
        elif mode=='huge': x=rng.choice([-1,1])*rng.randrange(10**17,10**18+1)
        else: x=rng.randrange(-10**18,10**18+1)
        yield str(x)+'\n'

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
