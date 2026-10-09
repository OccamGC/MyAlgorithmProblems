"""Independent small-input checks and input validation for five problem packages."""
from pathlib import Path
from functools import lru_cache
import collections, importlib.util, itertools, json, math, random, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/R30'
PROBLEMS = [('combinatorics','nested-linear-sum'),('combinatorics','monotone-sequence-count'),('dynamic-programming','optimal-search-tree'),('logic','monotone-unlocks'),('trees','diamond-hangers')]
MOD = 998244353

def run(slug, text, variant='std'):
    result = subprocess.run([str(OUT / f'{slug}-{variant}.exe')], input=text.encode(), capture_output=True, timeout=30)
    assert result.returncode == 0, (slug,result.stderr)
    return result.stdout.decode()

def load_generator(topic, slug):
    spec = importlib.util.spec_from_file_location('generator', ROOT/'topics'/topic/slug/'tests/generate.py')
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def unlock_oracle(text):
    lines = text.splitlines();N,M = map(int,lines[0].split())
    known = set(range(1,N+1))
    while True:
        add = set()
        for i,expr in enumerate(lines[1:]):
            boolean = re.sub(r'\d+',lambda m:'True' if int(m[0]) in known else 'False',expr)
            if eval(boolean.replace('&&',' and ').replace('||',' or '),{'__builtins__':{}},{}):
                add.add(N+i+1)
        if add <= known:break
        known |= add
    return ''.join(f'{int(i in known)}\n' for i in range(N+1,N+M+1))

@lru_cache(None)
def shapes(l,r):
    if l>r:return [((),())]
    result=[]
    for k in range(l,r+1):
        for left,ld in shapes(l,k-1):
            for right,rd in shapes(k+1,r):
                result.append(((k,)+left+right, (1,)+tuple(x+1 for x in ld+rd)))
    return result

def bst_oracle(weights):
    candidates=[]
    for order,depths in shapes(1,len(weights)):
        candidates.append((sum(weights[i-1]*d for i,d in zip(order,depths)),order))
    cost,order=min(candidates)
    return f'{cost}\n'+ ' '.join(map(str,order))+'\n'

def hanger_oracle(text):
    data=list(map(int,text.split()));n=data[0];pairs=[(0,0)]+list(zip(data[1::2],data[2::2]))
    child={v for pair in pairs for v in pair};root=next(i for i in range(1,n+1) if i not in child)
    coordinates=[];stack=[(root,0,0)];base=2*n+1
    while stack:
        u,h,x=stack.pop();coordinates.append((h,x,u));down,right=pairs[u]
        if down:stack.append((down,h+1,x))
        if right:stack.append((right,h,x+2*base**(n-h)))
    rows=collections.defaultdict(list)
    for h,x,u in sorted(coordinates):rows[h].append(u)
    return ''.join(' '.join(map(str,rows[h]))+'\n' for h in sorted(rows))

def validate(slug,text,group=3):
    if slug in ['nested-linear-sum','monotone-sequence-count']:
        values=list(map(int,text.split()));expected=4 if slug=='nested-linear-sum' else 2
        assert len(values)==expected
        n,m=values[:2]
        if expected==4:
            assert 1<=n<=10**7 and all(0<=v<=10**9 for v in values[1:])
            assert group!=1 or max(n,m)<=12
            assert group!=2 or m<=2000
        else:
            assert 1<=n<=2000 and 1<=m<=2000
            assert group!=1 or max(n,m)<=10
            assert group!=2 or min(n,m)<=50
        return values
    if slug=='optimal-search-tree':
        values=list(map(int,text.split()));n=values[0];assert 1<=n<=500 and len(values)==n+1
        assert all(0<=v<=10**9 for v in values[1:])
        assert group!=1 or n<=9
        assert group!=2 or n<=100
        return values[1:]
    if slug=='diamond-hangers':
        values=list(map(int,text.split()));n=values[0]
        assert 1<=n<=100000 and len(values)==2*n+1
        assert group!=1 or n<=20
        assert group!=2 or n<=1000
        indeg=[0]*(n+1);pairs=[(0,0)]+list(zip(values[1::2],values[2::2]))
        for pair in pairs[1:]:
            for x in pair:
                assert 0<=x<=n
                if x:indeg[x]+=1;assert indeg[x]<=1
        roots=[i for i in range(1,n+1) if not indeg[i]];assert len(roots)==1
        seen=set();stack=roots.copy()
        while stack:
            x=stack.pop();assert x not in seen;seen.add(x);stack.extend(v for v in pairs[x] if v)
        assert len(seen)==n
        return pairs
    lines=text.splitlines();assert len(lines)>=1
    N,M=map(int,lines[0].split());assert N>=0 and M>=0 and 1<=N+M<=200000 and len(lines)==M+1
    size=sum(map(len,lines[1:]));assert size<=1000000
    assert group!=1 or N+M<=20 and size<=1000
    assert group!=2 or N+M<=1000 and size<=10000
    for expression in lines[1:]:
        assert expression and all(ch in '0123456789&|() \t' for ch in expression)
        pos=0;need=True;depth=0
        for token in re.finditer(r'\d+|&&|\|\||[()]',expression):
            assert not expression[pos:token.start()].strip();pos=token.end();value=token[0]
            if value.isdigit():assert need and value[0]!='0' and len(value)<=6 and 1<=int(value)<=N+M;need=False
            elif value=='(':assert need;depth+=1
            elif value==')':assert not need and depth>0;depth-=1
            else:assert not need;need=True
        assert not need and depth==0 and not expression[pos:].strip()
    return N,M

def main():
    rng=random.Random(300513);counts={slug:0 for _,slug in PROBLEMS}
    def check(slug,text,answer,variants=('std','alternative')):
        validate(slug,text)
        for variant in variants:
            actual=run(slug,text,variant)
            assert actual.split()==answer.split(),(slug,variant,text[:2000],actual[:2000],answer[:2000])
        counts[slug]+=1
    for n in range(1,7):
        for m in range(0,8):
            for k,c in [(0,0),(1,0),(0,1),(7,3)]:
                expected=sum(k*seq[0]+c for seq in itertools.combinations_with_replacement(range(1,m+1),n))%MOD
                check('nested-linear-sum',f'{n} {m} {k} {c}\n',str(expected))
    for _ in range(120):
        n=rng.randint(1,100);m=rng.choice([rng.randrange(100),MOD+rng.randrange(-100,101),10**9]);k=rng.randrange(10**9+1);c=rng.randrange(10**9+1)
        answer=(k*math.comb(n+m,n+1)+c*math.comb(n+m-1,n))%MOD if m else 0
        check('nested-linear-sum',f'{n} {m} {k} {c}\n',str(answer))
    for n in range(1,13):
        for m in range(1,13):
            dp=[1]*m
            for _ in range(n-1):dp=list(itertools.accumulate(dp))
            check('monotone-sequence-count',f'{n} {m}\n',str(sum(dp)%MOD))
    for _ in range(70):
        n=rng.randint(1,2000);m=rng.randint(1,2000)
        check('monotone-sequence-count',f'{n} {m}\n',str(math.comb(n+m-1,n)%MOD))
    for n in range(1,7):
        for values in itertools.product([0,1],repeat=n):
            check('optimal-search-tree',f'{n}\n'+' '.join(map(str,values))+'\n',bst_oracle(values))
    for _ in range(100):
        n=rng.randint(1,8);weights=[rng.choice([0,1,rng.randint(1,10**9)]) for _ in range(n)]
        check('optimal-search-tree',f'{n}\n'+' '.join(map(str,weights))+'\n',bst_oracle(weights))
    for _ in range(300):
        N=rng.randrange(5);M=rng.randint(1,15)
        def expression(depth):
            if depth==0 or rng.randrange(3)==0:return str(rng.randint(1,N+M))
            return '('+expression(depth-1)+rng.choice(['&&','||'])+expression(depth-1)+')'
        text=f'{N} {M}\n'+'\n'.join(expression(3) for _ in range(M))+'\n'
        check('monotone-unlocks',text,unlock_oracle(text),('std',))
    for text in ['2 1\n1||3&&2\n','0 0\n','0 1\n1\n','1 2\n1&&1\n3||2\n']:
        if text=='0 0\n':continue
        check('monotone-unlocks',text,unlock_oracle(text),('std',))
    gen=load_generator('trees','diamond-hangers')
    for seed in range(320):
        text=gen.generate({'n':rng.randint(1,25),'mode':rng.choice(['random','down','right','balanced','zigzag']),'seed':seed})
        check('diamond-hangers',text,hanger_oracle(text))
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'small-checks.json').write_text(json.dumps({'status':'passed','independent_inputs':counts},indent=2)+'\n','utf-8')
    print(counts,flush=True)
if __name__=='__main__':main()
