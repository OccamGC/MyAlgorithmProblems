"""Independent mathematical checks and input validation for R23."""
from pathlib import Path
from functools import lru_cache
import json,math
ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('number-theory','arithmetic-geometric-sum'),('combinatorics','nested-polynomial-sum'),('combinatorics','paired-strand-count'),('combinatorics','general-paired-strands'),('dynamic-programming','unlabeled-distributions')]
VARIANTS={slug:['std','alternative'] for _,slug in PROBLEMS}
VARIANTS['general-paired-strands']=['std']
MOD=1000000007;PRIME=2147483647

@lru_cache(maxsize=1024)
def geometric_query(l,r,a,b,c,d):
    length=r-l+1
    if length<=16:
        return sum((a+b*i)*pow(c,d+b*i,MOD) for i in range(l,r+1))%MOD
    q=pow(c,b,MOD)
    if q==1:return (a*length+b*(l+r)*length//2)*pow(c,d,MOD)%MOD
    # Double a prefix, then optionally append its next power.
    count=0;power=1;plain=0;weighted=0
    for bit in bin(length)[2:]:
        weighted=(weighted*(1+power)+count*(power*plain%MOD))%MOD
        plain=plain*(1+power)%MOD
        power=power*power%MOD;count*=2
        if bit=='1':
            weighted=(weighted+count*power)%MOD
            plain=(plain+power)%MOD
            power=power*q%MOD;count+=1
    return pow(c,d,MOD)*pow(q,l,MOD)*((a+b*l)*plain+b*weighted)%MOD

def geometric(text):
    v=list(map(int,text.split()));m=v[0]
    return ''.join(str(geometric_query(*v[1+6*i:7+6*i]))+'\n' for i in range(m))

def combination(n,k,p):
    if k<0 or k>n:return 0
    k=min(k,n-k);num=den=1
    for i in range(1,k+1):num=num*(n-k+i)%p;den=den*i%p
    return num*pow(den,p-2,p)%p

def polynomial(text):
    v=list(map(int,text.split()));n,m,k=v[:3];a=v[3:]
    if n==1:return str(sum(a)%PRIME)+'\n'
    base=combination(n+m-1,m,PRIME)
    answer=a[0]*base%PRIME
    # Independent falling-binomial expansion using Stirling numbers.
    row=[0]*(k+1);row[0]=1;weights=[0]*(k+1)
    for degree in range(1,k+1):
        row=[0]+[(row[j-1]+j*row[j])%PRIME for j in range(1,k+1)]
        for j in range(1,degree+1):weights[j]=(weights[j]+a[degree]*row[j])%PRIME
    value=base*(n+m)%PRIME*pow(n,PRIME-2,PRIME)%PRIME
    factorial=1
    for j in range(1,k+1):
        value=value*(n-j+1)%PRIME*pow(m+j,PRIME-2,PRIME)%PRIME
        factorial=factorial*j%PRIME
        answer=(answer+weights[j]*factorial*value)%PRIME
    return str(answer)+'\n'

@lru_cache(maxsize=4096)
def fixed_dna_query(n):
    numerator=pow(4,n,2*MOD)
    if n%2==0:numerator+=pow(4,n//2,2*MOD)
    return numerator%(2*MOD)//2

def fixed_dna(text):
    v=list(map(int,text.split()));answer=0
    for n in v[1:]:answer^=fixed_dna_query(n)
    return str(answer)+'\n'

@lru_cache(maxsize=4096)
def general_dna_query(n,k,p):
    value=k*pow(2*k,n-1,p)
    if n%2==0:value+=k*pow(2*k,n//2-1,p)
    return value%p

def general_dna(text):
    v=list(map(int,text.split()));answer=0
    for i in range(v[0]):answer^=general_dna_query(*v[1+3*i:4+3*i])
    return str(answer)+'\n'

def partitions(text):
    n,m=map(int,text.split());values=[1]+[0]*n
    for total in range(1,n+1):
        value=0;k=1
        while k*(3*k-1)//2<=total:
            sign=1 if k%2 else -1
            value+=sign*values[total-k*(3*k-1)//2]
            if k*(3*k+1)//2<=total:value+=sign*values[total-k*(3*k+1)//2]
            k+=1
        values[total]=value%MOD
    for part in range(m+1,n+1):
        for total in range(n,part-1,-1):values[total]=(values[total]-values[total-part])%MOD
    return ''.join(str(value)+'\n' for value in values[1:])

ORACLES=dict(zip([s for _,s in PROBLEMS],[geometric,polynomial,fixed_dna,general_dna,partitions]))

def validate(slug,text,group=None):
    values=list(map(int,text.split()))
    assert text.endswith('\n')
    if group is not None:assert group==1
    if slug=='arithmetic-geometric-sum':
        m=values[0];assert 1<=m<=100000 and len(values)==1+6*m
        for i in range(m):
            l,r,a,b,c,d=values[1+6*i:7+6*i]
            assert 1<=l<=r<=1000000000 and all(1<=x<=1000000000 for x in [a,b,c,d])
        return dict(m=m)
    if slug=='nested-polynomial-sum':
        n,m,k=values[:3]
        assert 1<=n<=2000000000 and 1<=m<=10000000 and 0<=k<=300
        assert len(values)==4+k and all(1<=a<=2000000000 for a in values[3:])
        return dict(n=n,m=m,k=k)
    if slug=='paired-strand-count':
        m=values[0];assert 1<=m<=500000 and len(values)==m+1
        assert all(1<=n<=1000000000 for n in values[1:])
        return dict(m=m)
    if slug=='general-paired-strands':
        m=values[0];assert 1<=m<=500000 and len(values)==1+3*m
        assert all(1<=v<=1000000000 for v in values[1:])
        return dict(M=m)
    n,m=values;assert 1<=n<=5000 and 1<=m<=5000
    return dict(n=n,m=m)
