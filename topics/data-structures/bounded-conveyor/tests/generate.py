"""Deterministic test recipes; Python 3 standard library only."""
from pathlib import Path
import argparse,json,random,subprocess

def generate(c):
    n=c['n'];m=c['m'];mode=c['mode'];rng=random.Random(c['seed']);out=[f'{n} {m}']
    for i in range(m):
        push=mode=='push' or mode=='cycle' and i%(n+5)<n+2 or mode=='mixed' and rng.randrange(5)<3
        if mode=='alternate':push=i%2==0
        if push:
            x=[0,-2147483648,2147483647,-1,1][i%5] if mode!='mixed' else rng.randint(-2147483648,2147483647)
            out.append(f'1 {x}')
        else:out.append('2')
    return '\n'.join(out)+'\n'

def validate(text):
    lines=text.splitlines();n,m=map(int,lines[0].split());assert 0<=n<=500000 and 0<=m<=3000000 and len(lines)==m+1
    for line in lines[1:]:
        z=list(map(int,line.split()));assert z and z[0] in [1,2]
        if z[0]==1:assert len(z)==2 and -2147483648<=z[1]<=2147483647
        else:assert len(z)==1

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case',action='append')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args();plan=json.loads(args.plan.read_text('utf-8'))
    ids={c['id'] for c in plan['cases']}
    if args.case and not set(args.case)<=ids:parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:continue
        text=generate(c);validate(text)
        p=args.out_dir/(c['id']+'.in');p.write_text(text,'utf-8',newline='\n')
        if args.std:
            answer=subprocess.run([str(args.std.resolve())],input=text.encode(),capture_output=True,check=True).stdout
            p.with_suffix('.out').write_bytes(answer.replace(b'\r\n',b'\n'))
if __name__=='__main__':main()
