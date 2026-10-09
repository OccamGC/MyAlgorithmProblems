"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);mode=recipe['mode']
    if mode=='literal':return recipe['input']
    n=recipe['n'];shape=recipe['shape']
    if mode=='demolition':
        labels=[1]+list(range(2,n+1))
        if shape=='relabelled':rng.shuffle(labels[1:])
        if shape=='negative':p=[-rng.randrange(1000001) for _ in range(n)]
        elif shape=='equal':p=[0]*n
        elif shape=='near_density':p=[999999+(i%2) for i in range(n)]
        elif shape=='chain':p=[min(1000000,i+1) for i in range(n-1)]+[1]
        else:p=[rng.randrange(-1000000,1000001) for _ in range(n)]
        edges=[]
        if shape=='relabelled':
            rest=labels[1:];rng.shuffle(rest);labels=[1]+rest
        for i in range(1,n):
            j=i-1 if shape in ['chain','relabelled','near_density'] else 0 if shape=='star' else (i-1)//2 if shape in ['balanced','equal'] else i-1 if shape=='broom' and i<n//2 else n//2-1 if shape=='broom' else rng.randrange(i)
            edges.append(f'{labels[j]} {labels[i]}\n')
        return str(n)+'\n'+' '.join(map(str,p))+'\n'+''.join(edges)
    if mode=='transport':
        m=recipe['m']
        if shape=='warehouse':cap=[0]*n
        elif shape=='ends':cap=[m]+[0]*(n-2)+[m]
        elif shape in ['unit','sweep']:cap=[1]*n
        elif shape=='sparse':cap=[0 if rng.random()<.99 else rng.randrange(1,500) for _ in range(n)]
        elif shape=='large':cap=[100000]*n
        else:cap=[rng.randrange(3) for _ in range(n)]
        dist=[0 if shape=='zero' else 2 if shape=='warehouse' else rng.randrange(3) for _ in range(n-1)]+[1000000 if shape in ['warehouse','sparse'] else 2]
        if shape=='ends':q=[n//2+(i%2) for i in range(m)]
        elif shape=='unit':q=[n//2]*m
        elif shape=='sweep':q=[(i*97)%n+1 for i in range(m)]
        else:q=[rng.randrange(1,n+1) for _ in range(m)]
        return f'{n} {m}\n'+'\n'.join(' '.join(map(str,row)) for row in [cap,dist,q])+'\n'
    if mode=='assignment':
        if shape=='uniform':a=[[70]*n for _ in range(n)]
        elif shape=='diagonal':a=[[70 if i==j else 0 for j in range(n)] for i in range(n)]
        elif shape=='staircase':a=[[70 if j<=i else 0 for j in range(n)] for i in range(n)]
        elif shape=='rows':a=[[i%71]*n for i in range(n)]
        elif shape=='sparse':a=[[rng.randrange(68,71) if rng.random()<.03 else rng.randrange(3) for _ in range(n)] for _ in range(n)]
        elif shape=='two':a=[[rng.choice([0,70]) for _ in range(n)] for _ in range(n)]
        elif shape=='cycle':a=[[70 if j==(i+1)%n else 69 if i==j else 0 for j in range(n)] for i in range(n)]
        else:a=[[rng.randrange(71) for _ in range(n)] for _ in range(n)]
        return str(n)+'\n'+''.join(' '.join(map(str,row))+'\n' for row in a)
    if mode=='binary':
        m=recipe['m']
        if shape=='zero':rows=['0'*n]*5
        elif shape=='one':rows=['1'*n]*5
        elif shape=='alternating':rows=[('01'*n)[(i%2):(i%2)+n] for i in range(5)]
        else:rows=[''.join(rng.choices('01',k=n)) for _ in range(5)]
        if shape=='repeat':q=[(3,n//2+1)]*m
        elif shape=='ends':q=[(i%5+1,1 if i%2 else n) for i in range(m)]
        elif shape=='sweep':q=[(i%5+1,i%n+1) for i in range(m)]
        else:q=[(rng.randrange(1,6),rng.randrange(1,n+1)) for _ in range(m)]
        return f'{n} {m}\n'+'\n'.join(rows)+'\n'+''.join(f'{x} {y}\n' for x,y in q)
    if mode=='grid':
        m=recipe['m'];path=[]
        if shape=='empty':grid=['0'*n]*n;q=[rng.randrange(4) for _ in range(m)]
        elif shape=='checker':grid=[''.join('1' if (x+y)%2==0 else '0' for y in range(n)) for x in range(n)];q=[rng.randrange(4) for _ in range(m)]
        elif shape in ['snake','snake_reverse']:
            grid=[['0']*n for _ in range(n)]
            for x in range(0,n,2):
                columns=range(n) if (x//2)%2==0 else range(n-1,-1,-1)
                for y in columns:grid[x][y]='1';path.append((x,y))
                if x+2<n:grid[x+1][y]='1';path.append((x+1,y))
            if shape=='snake_reverse':path.reverse()
            moves={(-1,0):0,(1,0):1,(0,-1):2,(0,1):3}
            q=[moves[(b[0]-a[0],b[1]-a[1])] for a,b in zip(path,path[1:])]
            q=(q+[0]*m)[:m];grid=[''.join(row) for row in grid]
        else:
            vertical=shape=='vertical'
            grid=[''.join('1' if (y if vertical else x)%2==0 else '0' for y in range(n)) for x in range(n)]
            d=1 if vertical else 3
            if shape=='oscillate':q=[3,2]*(m//2)+[3]*(m%2)
            elif shape=='excursion':q=([3]*(n-1)+[2]*(n-1))*(m//max(1,2*n-2)+1);q=q[:m]
            else:q=[d]*(n-1)+[d^1]*(n-1)+[d]*m;q=q[:m]
        return f'{n} {m}\n'+'\n'.join(grid)+'\n'+'\n'.join(map(str,q))+'\n'
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
