"""Reproducible test inputs. Python standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(recipe):
    rng=random.Random(recipe['seed'])
    mode=recipe['mode']
    if mode=='literal':return recipe['input']
    shape=recipe['shape']
    n=recipe.get('n',0)
    if mode=='war':
        m=recipe['m']
        if shape=='increasing':a=list(range(n))
        elif shape=='descending':a=list(range(n,0,-1))
        elif shape=='equal':a=[-1000000000]*n
        elif shape=='two':a=[1]*(n-1)+[0]
        elif shape=='layers':a=[(i%997)-498 for i in range(n)]
        elif shape=='repeat':a=([2,2,1,0]*n)[:n]
        elif shape=='permutation':a=list(range(n));rng.shuffle(a)
        else:a=[rng.randrange(-1000000000,1000000001) for _ in range(n)]
        if shape=='two':q=list(range(1,min(n,m)+1))+[1]*max(0,m-n)
        elif shape=='repeat':q=[1]*m
        elif shape=='descending':q=[n-i%n for i in range(m)]
        else:q=[rng.randrange(-1000000000,0) if i%2 else rng.randrange(1,n+1) for i in range(m)]
        return f'{n} {m}\n'+' '.join(map(str,a))+'\n'+'\n'.join(map(str,q))+'\n'
    if mode=='common':
        m=recipe['m']
        if shape=='positive':weights=[1000000000]*n
        elif shape=='negative':weights=[-rng.randrange(1,1000000001) for _ in range(n)]
        elif shape=='flow64':weights=[1000000000 if i<n//2 else -1000000000 for i in range(n)]
        else:weights=[rng.randrange(-1000000000,1000000001) for _ in range(n)]
        def tree(kind,perm):
            ret=[]
            for i in range(1,n):
                p=i-1 if kind in ['chain','flow64'] else 0 if kind=='star' else (i-1)//2 if kind=='balanced' else rng.randrange(i)
                ret.append((perm[p],perm[i]))
            return ret
        rows=[]
        same=None
        for j in range(m):
            if shape in ['chain','star','balanced','flow64'] and same is not None:edges=same
            else:
                perm=list(range(1,n+1))
                if shape not in ['chain','star','balanced','flow64']:rng.shuffle(perm)
                edges=tree(shape,perm);same=edges
            rows.extend(f'{u} {v}\n' for u,v in edges)
        return f'{n} {m}\n'+' '.join(map(str,weights))+'\n'+''.join(rows)
    if mode=='battle':
        initial=[1,1,1]
        prices=[1000000000,1000000000,1,1,1]
        if shape in ['events','wide','head']:
            initial[2]=2 if shape!='head' else 1
            prices=[1000000000,1000000000,5000000 if shape=='wide' else 1,1000000000,5000000 if shape=='wide' else 1]
            enemies=[[5000,5000000,5000000 if shape=='head' else 1,5000000] for _ in range(n)]
        elif shape=='no_damage':
            initial=[5000000,5000000,1];prices=[1,1000000000,1,1000000000,1]
            enemies=[[5000,5000000,5000000,5000000] for _ in range(n)]
        elif shape=='steps':
            initial=[5000000,1,1];prices=[1,1000000000,1,1000000000,5000000]
            enemies=[[rng.randrange(1,5001),rng.randrange(1,5000001),rng.randrange(1,5000001),rng.randrange(1,5000001)] for _ in range(n)]
        elif shape=='ties':
            initial=[1,1,2];prices=[1,1,1,1,1]
            enemies=[[1,1,1,2] for _ in range(n)]
        elif shape=='mixed':
            initial=[1000000,1000000,1000000];prices=[123456789,1000000000,1,987654321,1]
            enemies=[[rng.randrange(1,5001),rng.randrange(1,5000001),rng.randrange(1,5000001),rng.randrange(1,5000001)] for _ in range(n)]
        else:
            initial=[3,1,2];prices=[2,7,3,11,2]
            enemies=[[rng.randrange(1,5001),rng.randrange(1,5000001),1,rng.randrange(1,5000001)] for _ in range(n)]
        return str(n)+'\n'+' '.join(map(str,initial))+'\n'+' '.join(map(str,prices))+'\n'+''.join(' '.join(map(str,e))+'\n' for e in enemies)
    if mode=='plot':
        ops=[]
        if shape=='reuse':
            while len(ops)+204<=n:
                ops.extend((1,i-1,i,i%3) for i in range(1,201))
                ops.extend([(3,200),(2,1),(1,0,1,100000),(2,1)])
            ops.extend([(3,0)]*(n-len(ops)))
        elif shape=='comb':
            depth=(n-1000)//2
            for i in range(1,depth+1):
                parent=0 if i==1 else 2*i-3
                ops.extend([(1,parent,2*i-1,rng.randrange(100001)),(1,2*i-1,2*i,rng.randrange(100001))])
            leaves=list(range(2,2*depth+1,2))
            ops.extend((3,leaves[i%len(leaves)]) for i in range(n-len(ops)))
        elif shape=='chain':
            length=n//2
            for i in range(1,length+1):ops.append((1,i-1,i,0))
            ops.append((1,0,100000,0))
            ops.extend((3,length if i%2 else 100000) for i in range(n-len(ops)))
        else:
            inserts=n-1000
            children=[0]*(inserts+1)
            for i in range(1,inserts+1):
                parent=0 if shape in ['star','equal','delete_root'] else (i-1)//2 if shape=='balanced' else rng.randrange(i)
                value=0 if shape=='equal' else 100000 if shape=='star' else rng.randrange(100001)
                ops.append((1,parent,i,value));children[parent]+=1
            leaves=[i for i in range(inserts+1) if children[i]==0]
            ops.extend((3,leaves[i%len(leaves)]) for i in range(n-len(ops)))
            if shape=='delete_root':ops[-1]=(2,0)
        assert len(ops)==n
        return str(n)+'\n'+''.join(' '.join(map(str,op))+'\n' for op in ops)
    raise ValueError(mode)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text(encoding='utf-8'))
    recipes=[x for x in plan['cases'] if args.case is None or x['id']==args.case]
    if not recipes:parser.error('unknown case: '+str(args.case))
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for recipe in recipes:
        path=args.out_dir/(recipe['id']+'.in')
        path.write_text(generate(recipe),'ascii',newline='\n')
        if args.std:
            with path.open('rb') as inp,path.with_suffix('.out').open('wb') as out:
                subprocess.run([str(args.std.resolve())],stdin=inp,stdout=out,check=True)
    print('Generated',len(recipes),'input(s)')
if __name__=='__main__':main()
