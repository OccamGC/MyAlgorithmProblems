"""Generate deterministic inputs and optional LF-normalized reference outputs."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec):
    rng=random.Random(spec['seed'])
    n=spec['n']; mode=spec['mode']
    yield str(n)+'\n'
    for i in range(n+3):
        if mode=='spaces': name=' '+str(i).rjust(17,'_')+'  '
        elif mode=='same': name=' Same name '
        elif mode=='blank': name=' '*20
        elif mode=='random': name=''.join(rng.choice('aAzZ09_ ') for _ in range(20))
        else: name='P'+str(i) if i<3 else 'Block'+str(i-3)
        yield name+'\n'

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
