"""Independent reference models and validators for R31."""
from pathlib import Path
import importlib.util,itertools,json,random,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R31'
PROBLEMS=[('simulation','memory-functions'),('parsing','small-integer-calculator'),('selection','nearest-median'),('combinatorics','strand-length-range'),('selection','generated-budget-selection')]
MOD=1000000007

def load_generator(topic,slug):
    spec=importlib.util.spec_from_file_location('generator',ROOT/'topics'/topic/slug/'tests/generate.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def validate(slug,text,group=3):
    if slug=='small-integer-calculator':
        expr=text.rstrip('\r\n');assert expr and len(expr)<=100000 and '\n' not in expr
        assert group!=1 or len(expr)<=30
        assert group!=2 or len(expr)<=1000
        need=True;depth=0
        for char in expr:
            if char in '0123456789':assert need;need=False
            elif char=='(':assert need;depth+=1
            elif char==')':assert not need and depth>0;depth-=1
            elif need:assert char in '+-~'
            else:assert char in '+-*/%<>';need=True
        assert not need and depth==0
        return expr
    tokens=list(map(int,text.split()))
    if slug=='nearest-median':
        n,k=tokens[:2];assert 1<=k<=n<=10**6 and len(tokens)==n+2 and all(abs(a)<10**9 for a in tokens[2:])
        assert group!=1 or n<=20
        assert group!=2 or n<=10000
        return tokens[2:],k
    if slug=='strand-length-range':
        M=tokens[0];assert 1<=M<=100000 and len(tokens)==3*M+1
        queries=list(zip(tokens[1::3],tokens[2::3],tokens[3::3]))
        for L,R,K in queries:
            assert 1<=L<=R<=10**9 and 1<=K<=10**9
            assert group!=1 or M<=20 and R<=8 and K<=2
            assert group!=2 or M<=1000 and R<=10000
        return queries
    if slug=='generated-budget-selection':
        assert len(tokens)==6;n,A,B,C,D,L=tokens
        assert 1<=n<=20000000 and all(abs(x)<=10**9 for x in tokens[1:]) and D!=0
        assert group!=1 or n<=20
        assert group!=2 or n<=100000
        return tokens
    n=tokens[0];assert 1<=n<=1000;sizes=tokens[1:n+1];S=sum(sizes)
    assert len(sizes)==n and min(sizes)>=1 and S<=1000
    initial=tokens[n+1:n+1+S];assert len(initial)==S and all(x in [0,1] for x in initial)
    k=tokens[n+1+S];assert 1<=k<=50000;pos=n+S+2;operations=[]
    assert group!=1 or S<=20 and k<=100
    assert group!=2 or S<=100 and k<=1000
    for _ in range(k):
        kind=tokens[pos];length=3 if kind==2 else 5;op=tokens[pos:pos+length];pos+=length
        assert kind in [0,1,2] and len(op)==length
        assert 0<=op[1]<n and abs(op[2])<=10**9
        if kind==0:assert op[3] in [0,1] and 0<=op[4]<=10**9
        if kind==1:assert 0<=op[3]<n and abs(op[4])<=10**9
        operations.append(op)
    assert pos==len(tokens)
    return sizes,initial,operations

def memory_oracle(text):
    sizes,data,ops=validate('memory-functions',text);starts=[0]+list(itertools.accumulate(sizes));S=len(data);out=[]
    for op in ops:
        kind,a,offset=op[:3];begin=starts[a]+offset;access=[];pending=[];error=None
        if kind==0:
            value,count=op[3:]
            if count and (begin<0 or begin+count>S):error='overflow'
            elif count:
                access=[(a,p) for p in range(begin,begin+count)];pending=[(p,value) for _,p in access]
            result='true'
        else:
            if kind==1:destarray=op[3];dest=starts[destarray]+op[4]
            p=begin;source=[];target=[]
            while True:
                q=dest+p-begin if kind==1 else p
                if not 0<=p<S or not 0<=q<S:error='overflow';break
                source.append(p);access.append((a,p))
                if kind==1:target.append(q);access.append((destarray,q))
                if data[p]==0:break
                p+=1
            if error is None:
                if kind==1 and set(source)&set(target):error='overwrite'
                elif kind==1:pending=list(zip(target,[data[x] for x in source]));result='true'
                else:result=str(len(source)-1)
        if error:out.append(error);continue
        warning=any(not starts[array]<=p<starts[array+1] for array,p in access)
        for p,v in pending:data[p]=v
        out.append(('w' if warning else '')+result)
    return '\n'.join(out)+'\n'

def wrap(value):return (value+2**31)%2**32-2**31
def trunc_div(a,b):return (abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1)

def calculator_oracle(text):
    # Independent recursive precedence-climbing model, only used on shallow inputs.
    expr=text.strip();pos=0;levels={'<':1,'>':1,'+':2,'-':2,'*':3,'/':3,'%':3}
    def parse(level=1):
        nonlocal pos
        char=expr[pos];pos+=1
        if char in '+-~':
            a=parse(4);value=a if char=='+' else wrap(-a) if char=='-' else wrap(~a)
        elif char=='(':
            value=parse();assert expr[pos]==')';pos+=1
        else:value=int(char)
        while pos<len(expr) and expr[pos] in levels and levels[expr[pos]]>=level:
            op=expr[pos];pos+=1;b=parse(levels[op]+1);a=value
            if op=='+':value=wrap(a+b)
            elif op=='-':value=wrap(a-b)
            elif op=='*':value=wrap(a*b)
            elif op=='/':value=wrap(trunc_div(a,b))
            elif op=='%':value=wrap(a-trunc_div(a,b)*b)
            elif op=='<':value=int(a<b)
            else:value=int(a>b)
        return value
    try:result=parse();assert pos==len(expr);return str(result)+'\n'
    except ZeroDivisionError:return 'Runtime Error\n'

def median_oracle(text):
    values,k=validate('nearest-median',text);ordered=sorted(values);n=len(values)
    twice=ordered[(n-1)//2]+ordered[n//2]
    return str(sum(sorted(values,key=lambda a:(abs(2*a-twice),-a))[:k]))+'\n'

def dna_orbits(n,K):
    classes=set()
    for seq in itertools.product(range(2*K),repeat=n):
        reverse=tuple(x^1 for x in seq[::-1]);classes.add(min(seq,reverse))
    return len(classes)

def dna_formula(text):
    def prefix(n,q):
        def geometric(n):
            return n%MOD if q==1 else (pow(q,n+1,MOD)-q)*pow(q-1,MOD-2,MOD)%MOD
        return (geometric(n)+geometric(n//2))*500000004%MOD
    return ''.join(str((prefix(R,2*K%MOD)-prefix(L-1,2*K%MOD))%MOD)+'\n' for L,R,K in validate('strand-length-range',text))

def sequence(text):
    n,A,B,C,D,L=validate('generated-budget-selection',text);out=[]
    for _ in range(n):
        product=A*B;A=C+product-trunc_div(product,D)*D;out.append(A)
    return out,L

def budget_oracle(text,exhaustive=False):
    values,L=sequence(text)
    if exhaustive:
        best=0
        for mask in range(1<<len(values)):
            if sum(v for i,v in enumerate(values) if mask>>i&1)<=L:best=max(best,mask.bit_count())
    else:
        total=0;best=0
        for i,v in enumerate(sorted(values),1):
            total+=v
            if total<=L:best=i
    return str(best)+'\n'

def run(slug,text,variant):
    p=subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,timeout=45)
    assert p.returncode==0,(slug,variant,p.stderr);return p.stdout.decode()

def main():
    rng=random.Random(313131);counts={s:0 for _,s in PROBLEMS}
    def check(slug,text,answer):
        validate(slug,text)
        for variant in (['std'] if slug=='small-integer-calculator' else ['std','alternative']):
            result=run(slug,text,variant);assert result.split()==answer.split(),(slug,variant,text[:2000],result[:2000],answer[:2000])
        counts[slug]+=1
    gen=load_generator('simulation','memory-functions')
    for seed in range(180):
        text=gen.generate({'seed':seed,'sizes':[rng.randint(1,5) for _ in range(rng.randint(1,5))],'k':100,'mode':'random'})
        check('memory-functions',text,memory_oracle(text))
    def expression(depth):
        if depth==0:return str(rng.randrange(10))
        kind=rng.randrange(4)
        if kind==0:return rng.choice('+-~')+expression(depth-1)
        if kind==1:return '('+expression(depth-1)+')'
        return expression(depth-1)+rng.choice('+-*/%<>')+expression(depth-1)
    for _ in range(350):
        text=expression(rng.randint(1,6))+'\n';check('small-integer-calculator',text,calculator_oracle(text))
    for text in ['3<2<1','9*9*9*9*9*9*9*9*9*9*9','(2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2*2)/(-1)','-7%3','-~1','--~~-~(5)+++--(3*(6+7)*4)*2/(2+2)+(1>(((2))))']:
        check('small-integer-calculator',text+'\n',calculator_oracle(text))
    for _ in range(240):
        n=rng.randint(1,60);k=rng.randint(1,n);values=[rng.choice([rng.randint(-9,9),-999999999,999999999]) for _ in range(n)]
        text=f'{n} {k}\n'+' '.join(map(str,values))+'\n';check('nearest-median',text,median_oracle(text))
    for K in range(1,4):
        counts_by_length=[0]+[dna_orbits(n,K) for n in range(1,7)]
        queries=[(L,R,K) for L in range(1,7) for R in range(L,7)]
        text=str(len(queries))+'\n'+''.join(f'{L} {R} {K}\n' for L,R,K in queries)
        answer=''.join(str(sum(counts_by_length[L:R+1])%MOD)+'\n' for L,R,K in queries)
        check('strand-length-range',text,answer)
    for _ in range(50):
        queries=[]
        for j in range(20):
            L=rng.randint(1,10**9);R=rng.randint(L,10**9);K=rng.choice([1,500000004,10**9,rng.randint(1,10**9)]);queries.append((L,R,K))
        text='20\n'+''.join(f'{L} {R} {K}\n' for L,R,K in queries);check('strand-length-range',text,dna_formula(text))
    for _ in range(220):
        values=[rng.randint(1,12),rng.randint(-100,100),rng.randint(-100,100),rng.randint(-100,100),rng.choice([i for i in range(-100,101) if i]),rng.randint(-200,300)]
        text=' '.join(map(str,values))+'\n';check('generated-budget-selection',text,budget_oracle(text,True))
    (OUT/'small-checks.json').write_text(json.dumps({'status':'passed','independent_inputs':counts,'memory_operations':18000,'dna_exhaustive_orbit_queries':63},indent=2)+'\n','utf-8')
    print(counts,flush=True)
if __name__=='__main__':main()
