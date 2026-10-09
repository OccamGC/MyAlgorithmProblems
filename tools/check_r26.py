"""Input checks and independent small oracles for the five R26 problems."""
from functools import lru_cache
from fractions import Fraction
import itertools, math

PROBLEMS=[('dynamic-programming','distinct-tile-runs'),('dynamic-programming','prefix-tile-groups'),('number-theory','old-yd-disjoint-set'),('data-structures','minimum-weighted-subarrays'),('data-structures','clue-generator')]
VARIANTS={s:['std'] if i<2 else ['std','alternative'] for i,(_,s) in enumerate(PROBLEMS)}

def validate(slug,text,group=None):
    it=iter(map(int,text.split()))
    if slug=='distinct-tile-runs':
        n,m,k=next(it),next(it),next(it);assert all(1<=v<=5000000 for v in (n,m,k))
        for _ in range(k):
            a,b,c=next(it),next(it),next(it);assert 1<=a<=10**9 and 1<=b<=m and 1<=c<=n
        result=dict(n=n,m=m,k=k)
    elif slug=='prefix-tile-groups':
        n=next(it);assert 1<=n<=5000000
        for _ in range(n):assert 1<=next(it)<=10**9
        result=dict(n=n)
    elif slug=='old-yd-disjoint-set':
        A,B,C,D,m=[next(it) for _ in range(5)];assert all(1<=v<=10**9 for v in (A,C,D)) and 1<=m<=5
        q=[next(it) for _ in range(m)];assert all(3<=B<=v<=10**7 for v in q)
        result=dict(B=B,m=m,maximum_n=max(q))
    else:
        n=next(it);limit=10**7 if slug=='minimum-weighted-subarrays' else 10**5;assert 1<=n<=limit
        m=next(it) if slug=='clue-generator' else None
        for _ in range(n):assert abs(next(it))<=10**9
        if m is not None:
            assert 1<=m<=10**5
            for _ in range(2*m):assert 0<=next(it)<=10**9
        result=dict(n=n,**(dict(m=m) if m is not None else {}))
    assert next(it,None) is None
    return result

def local_sets(x):return x>=0 and x not in (1,2,5)
def runs_subsets(a):
    runs=[tuple(range(i,i+k)) for k in [3,5] for i in range(len(a)-k+1)]
    def visit(i):
        if i==len(runs):return all(map(local_sets,a))
        if visit(i+1):return True
        r=runs[i]
        if all(a[j]>0 for j in r):
            for j in r:a[j]-=1
            answer=visit(i+1)
            for j in r:a[j]+=1
            if answer:return True
        return False
    return visit(0)

def tiles_a(text):
    n,m,k,*data=map(int,text.split());kinds={}
    for a,b,c in zip(data[::3],data[1::3],data[2::3]):
        row=kinds.setdefault(b,{})
        row[c]=row.get(c,0)+a
    for row in kinds.values():
        keys=sorted(row);segment=[];prev=-2
        for r in keys:
            if r!=prev+1:
                if segment and not runs_subsets(segment):return '0\n'
                segment=[]
            segment.append(row[r]);prev=r
        if segment and not runs_subsets(segment):return '0\n'
    return '1\n'

@lru_cache(None)
def partition(a,pair):
    if not any(a):return pair==0
    i=next(i for i,x in enumerate(a) if x);b=list(a)
    if b[i]>=3:
        b[i]-=3
        if partition(tuple(b),pair):return True
        b[i]+=3
    if pair and b[i]>=2:
        b[i]-=2
        if partition(tuple(b),0):return True
        b[i]+=2
    if i+2<len(b) and b[i+1] and b[i+2]:
        for j in range(i,i+3):b[j]-=1
        if partition(tuple(b),pair):return True
    return False

def tiles_b(text):
    n,*a=map(int,text.split())
    out=''.join(f'{int(partition(tuple(a[:i]),0))} {int(partition(tuple(a[:i]),1))}\n' for i in range(1,n+1))
    partition.cache_clear()
    return out

def recurrence(text):
    A,B,C,D,m,*q=map(int,text.split());mod=1000000007
    # Recursive expansion with an exact Taylor rational; no terminal-path formula.
    e_lower=sum((Fraction(1,math.factorial(k)) for k in range(31)),Fraction(0))
    def solve(n):
        @lru_cache(None)
        def f(a,b):
            if Fraction(n-a-B)<b*e_lower:return A
            return (C*f(a+1,b)+D*f(a,b+1))%mod
        return f(0,0)
    return ''.join(str(solve(n))+'\n' for n in q)

def minimum(text):
    n,*a=map(int,text.split());answer=0
    for l in range(n):
        total=0;lowest=10**10
        for r in range(l,n):total+=a[r];lowest=min(lowest,a[r]);answer+=total*lowest
    return str(answer)+'\n'

def zero(text):
    n,m,*data=map(int,text.split());a=data[:n];answer=0;out=[]
    for u,v in zip(data[n::2],data[n+1::2]):
        l,r=sorted(((u^answer)%n,(v^answer)%n));answer=0
        for i in range(l,r+1):
            total=0
            for j in range(i,r+1):
                total+=a[j]
                if total==0:answer+=j-i+1
        out.append(str(answer))
    return '\n'.join(out)+'\n'

ORACLES=dict(zip([s for _,s in PROBLEMS],[tiles_a,tiles_b,recurrence,minimum,zero]))
def check_output(slug,text,output,expected=None):
    assert output.split()==(expected if expected is not None else ORACLES[slug](text)).split(),(slug,text[:300],output[:300],str(expected)[:300])
