"""Independent specifications, mathematical oracles and witness validation for R24."""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import itertools,math,sys
sys.set_int_max_str_digits(0)
PROBLEMS=[('number-theory','nested-geometric-sum'),('combinatorics','grox-sequence-1'),('combinatorics','square-sum-stacks'),('combinatorics','square-sum-capacity'),('combinatorics','ordered-tree-building')]
VARIANTS={s:(['std','alternative'] if s in ['grox-sequence-1','square-sum-stacks','square-sum-capacity'] else ['std']) for _,s in PROBLEMS}
P=1004535809

def validate(slug,text,group=None):
    words=text.split()
    if slug=='nested-geometric-sum':
        assert len(words)==3
        n,m,a=map(int,words);assert 1<=n<=2000000000 and 1<=m<=1000000 and 1<=a<=2000000000
        return dict(n=n,m=m,a=a)
    if slug=='grox-sequence-1':
        assert len(words)==4 and all(x.isdecimal() for x in words)
        a,b,c,n=map(int,words);assert 0<=a<=10**1000 and 0<=n<=10**1000 and 0<=b<=100000 and 0<=c<=1000
        return dict(a_digits=len(words[0]),b=b,c=c,n_digits=len(words[3]),exponent_zero=n==0)
    if slug=='square-sum-stacks':
        assert len(words)==1 and 1<=int(words[0])<=1000
        return dict(n=int(words[0]))
    if slug=='square-sum-capacity':
        t=int(words[0]);assert 1<=t<=1000 and len(words)==t+1 and len(text.encode('ascii'))<=600000
        for x in words[1:]:assert x.isdecimal() and 1<=int(x)<=2*10**100000
        return dict(queries=t,maximum_digits=max(map(len,words[1:])),input_bytes=len(text.encode('ascii')))
    assert slug=='ordered-tree-building' and len(words)==1
    n=int(words[0]);assert 0<=n<=1000000
    if group==1:assert n<=104
    if group==2:assert n<=3000
    return dict(n=n)

def geometric(text):
    n,m,a=map(int,text.split());p=2147483647
    if n<=5000:
        values=[sum(pow(a,i,p) for i in range(x,2*x+1))%p for x in range(1,n+1)] if n<=100 else [(pow(a,2*x+1,p)-pow(a,x,p))*pow(a-1,p-2,p)%p if a!=1 else x+1 for x in range(1,n+1)]
        weight=1;answer=0
        for t in range(n):
            answer=(answer+weight*values[n-t-1])%p
            weight=weight*(m+t)*pow(t+1,p-2,p)%p
        return str(answer)+'\n'
    if a==1:
        top=n+m;f=1;g=1
        for i in range(1,m+1):f=f*(n+i-1)%p;g=g*i%p
        c=f*pow(g,p-2,p)%p
        return str((c+c*top*pow(m+1,p-2,p))%p)+'\n'
    # Closed partial-fraction form, evaluated backwards with one factorial inverse.
    coefficients=[1]*m
    factorial=1
    product=1
    for t in range(1,m):
        product=product*(n+t-1)%p;factorial=factorial*t%p
        coefficients[t]=product
    inverse_factorial=pow(factorial,p-2,p)
    for t in range(m-1,0,-1):
        coefficients[t]=coefficients[t]*inverse_factorial%p
        inverse_factorial=inverse_factorial*t%p
    def repeated(q):
        ratio=q*pow(q-1,p-2,p)%p
        total=0
        for coefficient in coefficients:total=(total+coefficient)*ratio%p
        return (pow(ratio,m,p)*pow(q,n,p)-total)%p
    return str((a*repeated(a*a%p)-repeated(a))*pow(a-1,p-2,p)%p)+'\n'

def transform(values,inverse=False):
    n=len(values);j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:j^=bit;bit>>=1
        j^=bit
        if i<j:values[i],values[j]=values[j],values[i]
    size=2
    while size<=n:
        root=pow(3,(P-1)//size,P)
        if inverse:root=pow(root,P-2,P)
        powers=[1]*(size//2)
        for k in range(1,len(powers)):powers[k]=powers[k-1]*root%P
        for start in range(0,n,size):
            for offset,w in enumerate(powers):
                x=values[start+offset];y=values[start+offset+size//2]*w%P
                values[start+offset]=(x+y)%P;values[start+offset+size//2]=(x-y)%P
        size*=2
    if inverse:
        inv=pow(n,P-2,P)
        values[:]=[v*inv%P for v in values]

@lru_cache(maxsize=6)
def strand_coefficients(b,c):
    degree=2*(b+c);length=1
    while length<=degree:length*=2
    first=[0]*length;second=[0]*length
    value=1
    for i in range(b+1):
        first[2*i]=value
        value=value*(b-i)*pow(i+1,P-2,P)%P
    # Explicit trinomial expansion; different from the C++ quadratic multiplication.
    fact=[1]*(c+1)
    for i in range(1,c+1):fact[i]=fact[i-1]*i%P
    inverse=[pow(x,P-2,P) for x in fact]
    powers=[pow(2,i,P) for i in range(c+1)]
    for i in range(c+1):
        for j in range(c-i+1):
            k=c-i-j
            coefficient=fact[c]*inverse[i]%P*inverse[j]%P*inverse[k]%P*powers[k]%P
            second[2*i+k]=(second[2*i+k]+(-coefficient if j%2 else coefficient))%P
    transform(first);transform(second)
    first=[a*b%P for a,b in zip(first,second)];transform(first,True)
    return first[:degree+1]

def grox_small(a,b,c,n):
    # Labelled positions: choose the places occupied by each added letter type.
    values=[pow(a,i,P) for i in range(n+1)]
    for count,allowed in [(b,lambda j:j%2==0),(c,lambda j:j==0 or j%2==1)]:
        for _ in range(count):values=[sum(math.comb(i,j)*values[i-j] for j in range(i+1) if allowed(j))%P for i in range(n+1)]
    return values[n]

def grox(text):
    a,b,c,n=map(int,text.split())
    if n<=20 and b+c<=30:return str(grox_small(a,b,c,n))+'\n'
    if n==0:return '1\n'
    exp=n%(P-1);total=0
    for i,coefficient in enumerate(strand_coefficients(b,c)):
        base=(a-b-c+i)%P
        total=(total+coefficient*(pow(base,exp,P) if base else 0))%P
    return str(total*pow(pow(2,b+c,P),P-2,P)%P)+'\n'

def stack_witness(text):
    n=int(text);columns=[[] for _ in range(n)];size=n;start=0;value=(n+1)**2//2-1
    if n%2==0:
        for column in columns:column.append(value);value-=1
        size-=1
    while size>1:
        for i in range(start+size-1,start-1,-1):columns[i].append(value);value-=1
        for i in range(start,start+size):columns[i].append(value);value-=1
        start+=1;size-=2
    columns[start].append(1)
    return ''.join(' '.join(map(str,row))+'\n' for row in columns)

def check_stack_output(text,output):
    n=int(text);lines=output.strip().splitlines();assert len(lines)==n
    target=(n+1)**2//2-1;seen=bytearray(target+1);count=0
    for line in lines:
        values=list(map(int,line.split()));assert values
        for value in values:assert 1<=value<=target and not seen[value];seen[value]=1;count+=1
        for higher,lower in zip(values,values[1:]):
            assert higher>lower
            s=higher+lower;assert math.isqrt(s)**2==s
    assert count==target and all(seen[1:])

def capacity(text):return ''.join(str((int(n)+1)**2//2-1)+'\n' for n in text.split()[1:])
def tree(text):
    n=int(text);p=998244353
    if n<=2:return '1\n'
    # Pair consecutive factors; independent modular product organization.
    values=list(range(1,n))
    while len(values)>1:values=[values[i]*values[i+1]%p if i+1<len(values) else values[i] for i in range(0,len(values),2)]
    return str(pow(n,n-2,p)*values[0]%p)+'\n'
ORACLES=dict(zip([s for _,s in PROBLEMS],[geometric,grox,stack_witness,capacity,tree]))
def check_output(slug,text,output,expected=None):
    if slug=='square-sum-stacks':check_stack_output(text,output)
    else:assert output.split()==(expected if expected is not None else ORACLES[slug](text)).split(),(slug,text[:100],output[:100],(expected or '')[:100])
