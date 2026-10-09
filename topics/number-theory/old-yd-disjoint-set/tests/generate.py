"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path

import itertools

def generate(recipe):
    rng=random.Random(recipe['seed']);mode=recipe['mode']
    if mode=='literal':return recipe['input']
    n=recipe['n'];shape=recipe['shape']
    if mode=='tiles_a':
        m=recipe['m'];k=recipe['k'];lines=[f'{n} {m} {k}\n']
        for i in range(k):
            if shape=='same':a=1000000000;b=m;c=n
            elif shape=='runs':a=1;b=1;c=i+1
            elif shape=='triples':a=3;b=rng.randrange(1,m+1);c=rng.randrange(1,n+1)
            elif shape=='isolated':a=1;b=(i*1000003)%m+1;c=rng.randrange(1,n+1)
            elif shape=='large':a=1000000000;b=1;c=i+1
            elif shape=='boundary':a=1;b=i//2+1;c=i%2+1
            else:a=rng.randrange(1,11);b=rng.randrange(1,m+1);c=rng.randrange(1,n+1)
            lines.append(f'{a} {b} {c}\n')
        return ''.join(lines)
    if mode=='tiles_b':
        if shape=='random':a=[rng.randrange(1,1000000001) for _ in range(n)]
        elif shape=='small':a=[rng.randrange(1,8) for _ in range(n)]
        elif shape=='cycle':a=[1,2,3,4,5,6,7,8,9,10,1000000000]*(n//11)+[1,2,3,4,5,6,7,8,9,10,1000000000][:n%11]
        else:a=[int(shape)]*n
        return str(n)+'\n'+' '.join(map(str,a))+'\n'
    if mode=='recurrence':
        A,B,C,D=recipe['parameters'];q=recipe['queries']
        return f'{A} {B} {C} {D}\n{len(q)}\n'+'\n'.join(map(str,q))+'\n'
    if mode=='minimum':
        if shape=='increasing':a=range(-n//2,n-n//2)
        elif shape=='decreasing':a=range(n//2,n//2-n,-1)
        elif shape=='alternating':a=(1000000000 if i%2 else -1000000000 for i in range(n))
        elif shape=='random':a=(rng.randrange(-1000000000,1000000001) for _ in range(n))
        elif shape=='saw':a=((i%997)-498 for i in range(n))
        else:a=itertools.repeat(int(shape),n)
        return str(n)+'\n'+' '.join(map(str,a))+'\n'
    if mode=='zero':
        m=recipe['m']
        if shape=='zero':a=[0]*n
        elif shape=='positive':a=[1000000000]*n
        elif shape=='alternating':a=[1000000000 if i%2 else -1000000000 for i in range(n)]
        elif shape=='cycle':a=[1 if i%317!=316 else -316 for i in range(n)]
        elif shape=='smallwalk':a=[rng.randrange(-1,2) for _ in range(n)]
        elif shape=='wide':a=[rng.randrange(-1000000000,1000000001) for _ in range(n)]
        else:a=[rng.randrange(-3,4) for _ in range(n)]
        lines=[f'{n} {m}\n',' '.join(map(str,a))+'\n','0 '+str(n-1)+'\n']
        for _ in range(m-1):lines.append(f'{rng.randrange(1000000001)} {rng.randrange(1000000001)}\n')
        return ''.join(lines)
    raise ValueError(mode)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text(encoding='utf-8'))
    recipes=[item for item in plan['cases'] if args.case is None or item['id']==args.case]
    if not recipes:parser.error('unknown case: '+str(args.case))
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for recipe in recipes:
        path=args.out_dir/(recipe['id']+'.in')
        path.write_text(generate(recipe),encoding='ascii',newline='\n')
        if args.std:
            with path.open('rb') as inp,path.with_suffix('.out').open('wb') as out:
                subprocess.run([str(args.std.resolve())],stdin=inp,stdout=out,check=True)
    print('Generated',len(recipes),'input(s)')

if __name__=='__main__':main()
