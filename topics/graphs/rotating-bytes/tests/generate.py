"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);mode=recipe['mode']
    if mode=='literal':return recipe['input']
    n=recipe['n'];shape=recipe['shape']
    if mode=='digits':
        k=recipe['k']
        if shape=='random':a=[rng.randrange(k) for _ in range(n)];a[0]=rng.randrange(1,k)
        elif shape=='zero':a=[1]+[0]*(n-1)
        elif shape=='one':a=[1]*n
        elif shape=='large':a=[k-1]*n
        elif shape=='no_carry':a=[rng.randrange((k+1)//2) for _ in range(n)];a[0]=1
        elif shape=='leading':a=[k-1]+[0]*(n-2)+[1]
        elif shape=='special':a=[1]+[k-2]*(n-2)+[k-1]
        else:a=[(n-i-1)%k for i in range(n)];a[0]=k-1
        return f'{n} {k}\n'+' '.join(map(str,a))+'\n'
    if mode=='queue':
        m=recipe['m']
        if shape=='random':s=''.join(rng.choices('01',k=m))
        elif shape=='push':s='0'*m
        elif shape=='pop':s='1'*m
        elif shape=='batch':s='0'*(m//2)+'1'*(m-m//2)
        else:s=(shape*(m//len(shape)+1))[:m]
        return f'{n} {m}\n'+s+'\n'
    if mode=='bst':
        # Median-first insertion keeps frequent searches shallow, as promised.
        values=[];work=[(-20000,20000)]
        while work:
            l,r=work.pop()
            if l>r:continue
            mid=(l+r)//2;values.append(mid);work.append((mid+1,r));work.append((l,mid-1))
        if shape=='extreme':values=[0,-2147483648,2147483647]+values[1:]
        ops=[];print_at=set((n-1)*i//9 for i in range(10))
        inserted=0
        for i in range(n):
            if i in print_at:ops.append('0')
            elif inserted<len(values):ops.append('1 '+str(values[inserted]));inserted+=1
            elif shape=='duplicate':ops.append(f'{1 if i%3 else 2} {values[i%127]}')
            elif shape=='root':ops.append(f'{1 if i%2 else 2} 0')
            elif shape=='missing':ops.append('2 '+str(1000000000+i))
            else:ops.append(f'{rng.choice([1,2,2])} {rng.randrange(-20000,20001)}')
        return str(n)+'\n'+'\n'.join(ops)+'\n'
    if mode=='heap':
        p=list(range(1,n+1))
        if shape not in ['chain','star']:rng.shuffle(p)
        edges=[]
        for i in range(1,n):
            j=i-1 if shape in ['chain','relabelled_chain'] else 0 if shape=='star' else (i-1)//2 if shape=='balanced' else rng.randrange(i)
            edges.append(f'{p[j]} {p[i]}\n')
        return f'{n} {p[0]}\n'+''.join(edges)
    if mode=='byte':
        m=recipe['m'];k=recipe['k']
        def label():return '0'*rng.randrange(1,6) if shape=='zero' else '01010' if shape=='chain' else ''.join(rng.choices('01',k=rng.randrange(1,6)))
        labels=[label() for _ in range(n)]
        if shape in ['star','ties']:labels=['0']*n
        starts=list(range(n-k+1,n+1));edges=[]
        for u in range(2,n+1):edges.append((u,u-1 if shape=='chain' else 1 if shape in ['star','ties'] else rng.randrange(1,u),label() if shape!='ties' else '0'))
        while len(edges)<m:
            if shape=='chain':u=n;v=n;s='11111'
            elif shape=='ties':u=rng.randrange(2,n+1);v=1;s='0'
            else:u=rng.randrange(1,n+1);v=rng.randrange(1,n+1);s=label()
            edges.append((u,v,s))
        rng.shuffle(edges)
        return f'{n} {m} {k}\n'+' '.join(labels)+'\n'+' '.join(map(str,starts))+'\n'+''.join(f'{u} {v} {s}\n' for u,v,s in edges)
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
