"""Independent mathematical/simulation oracles for the six R18 packages."""
from pathlib import Path
from decimal import Decimal
from functools import lru_cache
import itertools
import json
import random
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('arithmetic','acceleration-orders'),('geometry','rectangle-intersection'),
          ('geometry','rectangle-intersection-type'),('simulation','matrix-mixer'),
          ('strings','skewer-substrings'),('dynamic-programming','cat-selection')]
VARIANTS={slug: (['std'] if slug=='acceleration-orders' else
                ['std','alternative-projection','alternative-center'] if slug.startswith('rectangle-') else
                ['std','alternative']) for _,slug in PROBLEMS}

def acceleration_oracle(text):
    T,*values=map(int,text.split())
    return ''.join(f'{abs(Decimal(a)*Decimal(t)*Decimal(t)/2):.1f}\n' for a,t in zip(values[::2],values[1::2]))

def geometry_dimension(values):
    # Probe all endpoints and all open cells of the endpoint arrangement.
    dimensions=[]
    for axis in range(2):
        a,b,c,d=[values[i+axis] for i in (0,2,4,6)]
        endpoints=sorted({a,b,c,d})
        probes=[2*x for x in endpoints]+[x+y for x,y in zip(endpoints,endpoints[1:])]
        common={x for x in probes if min(a,b)*2<=x<=max(a,b)*2 and min(c,d)*2<=x<=max(c,d)*2}
        if not common:
            return -1
        dimensions.append(int(len(common)>1))
    return sum(dimensions)

def rectangle_oracle(text,classification=False):
    lines=text.splitlines();result=[]
    for line in lines[1:]:
        value=geometry_dimension(list(map(int,line.split())))
        result.append(['None','Point','Edge','Area'][value+1] if classification else
                      'Intersection Found' if value>=0 else 'Intersection Not Found')
    return ''.join(x+'\n' for x in result)

def mixer_oracle(text):
    lines=iter(text.splitlines());n,m,K=map(int,next(lines).split())
    grid=[list(map(int,next(lines).split())) for _ in range(n)]
    output=[]
    for line in lines:
        op,*args=map(int,line.split())
        if op==3:
            grid=[list(row) for row in zip(*grid[::-1])]
        else:
            a,b=args;limit=len(grid) if op==1 else len(grid[0])
            if not (1<=a<=limit and 1<=b<=limit):
                output.append('Invalid arguments!');continue
            if op==1:
                grid[a-1],grid[b-1]=grid[b-1],grid[a-1]
            else:
                for row in grid:
                    row[a-1],row[b-1]=row[b-1],row[a-1]
        output.extend(' '.join(map(str,row)) for row in grid)
    return ''.join(x+'\n' for x in output)

def substring_oracle(text):
    lines=text.splitlines();s=lines[0];out=[]
    for line in lines[2:]:
        left,right,t=line.split();left=int(left)-1;right=int(right)
        count=sum(s.startswith(t,i) for i in range(left,right-len(t)+1))
        out.append(count)
    return ''.join(f'{x}\n' for x in out)

def cat_oracle(text,brute=False):
    n,k,*values=map(int,text.split())
    if brute:
        best=None
        for chosen in itertools.combinations(values,k):
            score=0
            for value in chosen:
                score=score*3+value
            best=score if best is None else max(best,score)
        return f'{best}\n'
    @lru_cache(None)
    def solve(start,remaining):
        if remaining==0:
            return 0
        if n-start<remaining:
            return -10**30
        return max(solve(start+1,remaining),values[start]*3**(remaining-1)+solve(start+1,remaining-1))
    return f'{solve(0,k)}\n'

ORACLES={'acceleration-orders':acceleration_oracle,
         'rectangle-intersection':rectangle_oracle,
         'rectangle-intersection-type':lambda text:rectangle_oracle(text,True),
         'matrix-mixer':mixer_oracle,'skewer-substrings':substring_oracle,'cat-selection':cat_oracle}

def verify(slug,text,expected=None):
    expected=ORACLES[slug](text) if expected is None else expected
    for variant in VARIANTS[slug]:
        exe=ROOT/'build/bin'/f'{slug}-{variant}.exe'
        actual=subprocess.check_output([str(exe)],input=text.encode('ascii'),timeout=30).replace(b'\r\n',b'\n').decode('ascii')
        assert actual==expected,(slug,variant,text[:4000],expected[:4000],actual[:4000])

def main():
    rng=random.Random(2026093018)
    counts={}
    pairs=list(itertools.product(range(-20,21),repeat=2))+list(itertools.product([-10000,-1,0,1,10000],repeat=2))
    verify('acceleration-orders',str(len(pairs))+'\n'+''.join(f'{a} {t}\n' for a,t in pairs))
    verify('acceleration-orders','0\n');counts['acceleration-orders']=len(pairs)
    print('acceleration-orders',len(pairs),'queries passed',flush=True)
    rectangles=list(itertools.product(range(-1,2),repeat=8))
    rectangles += [tuple(rng.randrange(-10**9,10**9+1) for _ in range(8)) for _ in range(1000)]
    rectangles += [(-1,-1,-5,-5,-2,-1,-2,-2)]
    assert geometry_dimension(rectangles[-1])==1
    for slug in ['rectangle-intersection','rectangle-intersection-type']:
        for offset in range(0,len(rectangles),1000):
            batch=rectangles[offset:offset+1000]
            verify(slug,str(len(batch))+'\n'+''.join(' '.join(map(str,row))+'\n' for row in batch))
        verify(slug,'0\n');counts[slug]=len(rectangles)
        print(slug,len(rectangles),'geometric queries passed',flush=True)
    for _ in range(240):
        n=rng.randrange(1,7);m=rng.randrange(1,7);K=30
        lines=[f'{n} {m} {K}']+[' '.join(str(rng.randrange(10**9+1)) for _ in range(m)) for _ in range(n)]
        for j in range(K):
            op=rng.randrange(1,4)
            lines.append(str(op)+(f' {rng.randrange(-2,8)} {rng.randrange(-2,8)}' if op<3 else ''))
        verify('matrix-mixer','\n'.join(lines)+'\n')
    counts['matrix-mixer']=240
    print('matrix-mixer 240 input batches passed',flush=True)
    for _ in range(200):
        s=''.join(rng.choice('abc') for _ in range(rng.randrange(1,101)))
        lines=[s,'40']
        for j in range(40):
            l=rng.randrange(1,len(s)+1);r=rng.randrange(l,len(s)+1)
            t=''.join(rng.choice('abc') for _ in range(rng.randrange(1,41)))
            lines.append(f'{l} {r} {t}')
        verify('skewer-substrings','\n'.join(lines)+'\n')
    counts['skewer-substrings']=dict(input_batches=200,queries=8000)
    print('skewer-substrings 8000 queries passed',flush=True)
    count=0
    for n in range(4):
        for values in itertools.product([-1,0,1],repeat=n):
            for k in range(n+1):
                text=f'{n} {k}\n'+' '.join(map(str,values))+'\n'
                verify('cat-selection',text,cat_oracle(text,True));count+=1
    for _ in range(180):
        n=rng.randrange(15);k=rng.randrange(n+1)
        text=f'{n} {k}\n'+' '.join(str(rng.randrange(-1000,1001)) for _ in range(n))+'\n'
        verify('cat-selection',text,cat_oracle(text,True));count+=1
    counts['cat-selection']=count
    print('cat-selection',count,'subset-enumeration batches passed',flush=True)
    (ROOT/'build/R18/checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
