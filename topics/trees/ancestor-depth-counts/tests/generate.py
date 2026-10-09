"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);mode=recipe['mode']
    if mode=='literal':return recipe['input']
    n=recipe['n'];shape=recipe['shape']
    if mode=='postal':
        m=recipe['m']
        if shape=='equal':x=[100000000]*n
        elif shape=='extremes':x=[0 if i%2 else 100000000 for i in range(n)]
        elif shape=='linear':x=[i*50000 for i in range(n)]
        elif shape=='clusters':x=[rng.randrange(5)*20000000+rng.randrange(11) for i in range(n)]
        else:x=[rng.randrange(100000001) for _ in range(n)]
        rng.shuffle(x);return f'{n} {m}\n'+' '.join(map(str,x))+'\n'
    if mode=='graph':
        m=recipe['m'];energy=recipe.get('energy');h=[rng.randrange(-100000,100001) for _ in range(n)]
        if shape in ['chain','layered']:h=[i-50000 for i in range(n)]
        elif shape in ['equal','loops']:h=[-100000]*n
        elif shape=='extremes':h=[100000 if i%2 else -100000 for i in range(n)]
        edges=[]
        for i in range(m):
            if shape=='chain':u=i%(n-1)+1;v=u+1
            elif shape=='star':u=1;v=i%(n-1)+2
            elif shape=='loops':u=i%n+1;v=u
            elif shape=='layered':u=i//2+1;v=u+1
            else:u=rng.randrange(1,n+1);v=rng.randrange(1,n+1)
            edges.append(f'{u} {v}\n')
        return f'{n} {m}'+(f' {energy}' if energy is not None else '')+'\n'+' '.join(map(str,h))+'\n'+''.join(edges)
    if mode=='stack':
        m=recipe['m']
        if shape=='increasing':x=list(range(n))
        elif shape=='decreasing':x=list(range(n,0,-1))
        elif shape=='equal':x=[1000000000]*n
        elif shape=='saw':x=[i%997 for i in range(n)]
        else:x=[rng.randrange(1000000001) for _ in range(n)]
        lines=[f'{n} {m}\n',' '.join(map(str,x))+'\n']
        for i in range(m):
            l=rng.randrange(1,n+1);r=rng.randrange(l,n+1)
            if shape=='same_right':r=n
            elif shape=='same_left':l=1
            if i==0:l=1;r=n
            lines.append(f'{l} {r}\n')
        return ''.join(lines)
    if mode=='tree':
        p=[0,0]
        for u in range(2,n+1):
            if shape=='chain':v=u-1
            elif shape=='star':v=1
            elif shape=='binary':v=u//2
            elif shape=='ternary':v=(u+1)//3
            elif shape=='broom':v=u-1 if u<=n//2 else n//2
            elif shape=='comb':v=u-1 if u<=n//2 else u-n//2
            else:v=rng.randrange(1,u)
            p.append(v)
        if recipe.get('relabel'):
            labels=list(range(n+1));tail=labels[2:];rng.shuffle(tail);labels[2:]=tail;q=[0]*(n+1)
            for u in range(2,n+1):q[labels[u]]=labels[p[u]]
            p=q
        return str(n)+'\n'+' '.join(map(str,p[2:]))+'\n'
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
