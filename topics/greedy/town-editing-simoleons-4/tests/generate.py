"""Deterministic recipes and several reference oracles for one empty slot."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse
import io
import json
import random
import subprocess

MOD=1000000007
HALF=(MOD+1)//2


def parse(text):
    stream=io.StringIO(text);first=stream.readline().split()
    if len(first)!=1:raise ValueError('expected n')
    n=int(first[0])
    if not 2<=n<=1000000:raise ValueError('n out of range')
    rows=[];empty=False
    for i in range(n):
        fields=stream.readline().split()
        if len(fields)!=2:raise ValueError('expected population and money')
        p,m=map(int,fields)
        if not (1<=p<=1000000 if i==0 else p in (0,1)):raise ValueError('population out of range')
        if not 0<=m<=1000000000 or (p==0 and m!=0):raise ValueError('invalid money')
        empty|=p==0;rows.append((p,m))
    if not empty:raise ValueError('at least one initial empty household is required')
    if stream.read().strip():raise ValueError('extra input')
    return rows


def validate(text,group=None):parse(text)


def as_text(rows):return str(len(rows))+'\n'+''.join(f'{p} {m}\n' for p,m in rows)


def exact(rows):
    k,m=rows[0];values=[F(m,k)]*k
    for v in sorted(F(m,p) for p,m in rows[1:] if p):
        for i in range(k):
            if v>values[i]:values[i]=v=(v+values[i])/2
    answer=sum(values)
    return answer.numerator%MOD*pow(answer.denominator,-1,MOD)%MOD


def grid(rows):
    k,m=rows[0];values=[m*pow(k,-1,MOD)%MOD]*k
    for v in sorted(m for p,m in rows[1:] if p and m*k>rows[0][1]):
        for i in range(k):values[i]=v=(values[i]+v)*HALF%MOD
    return sum(values)%MOD


def matrix(rows):
    k,m=rows[0];a=m*pow(k,-1,MOD)%MOD
    values=sorted(v for p,v in rows[1:] if p and v*k>m);r=len(values)
    if r>30:raise ValueError('matrix oracle is for at most 30 richer outsiders')
    z=[(v-a)%MOD for v in values];initial=sum(z)
    b=[[0]*r for _ in range(r)]
    for col in range(r):
        carry=0
        for i in range(r):carry=(carry+(i==col))*HALF%MOD;b[i][col]=carry
    while k:
        if k&1:z=[sum(b[i][j]*z[j] for j in range(r))%MOD for i in range(r)]
        b=[[sum(b[i][t]*b[t][j] for t in range(j,i+1))%MOD if j<=i else 0 for j in range(r)] for i in range(r)]
        k>>=1
    return (m+initial-sum(z))%MOD


def grouped_tail(rows):
    # Column-wise tail formula: independent of the row-wise coefficient sum.
    k,m=rows[0];counts=Counter(v for p,v in rows[1:] if p and v*k>m)
    inv=[0,1]+[0]*max(0,k-1)
    for j in range(2,k+1):inv[j]=MOD-MOD//j*inv[MOD%j]%MOD
    a=m*inv[k]%MOD;answer=m;before=0;previous=k
    for value,count in sorted(counts.items(),reverse=True):
        before+=count;choose=1;half=1;tail=k
        for j in range(1,k):
            choose=choose*(before+j-1)%MOD*inv[j]%MOD;half=half*HALF%MOD
            tail=(tail+(k-j)*choose*half)%MOD
        tail=tail*pow(HALF,before,MOD)%MOD
        answer=(answer+(value-a)*(previous-tail))%MOD;previous=tail
    return answer


def factorial_oracle(rows):
    # Same proved coefficient identity, evaluated by factorials rather than recurrence.
    k,m=rows[0];values=sorted((v for p,v in rows[1:] if p and v*k>m),reverse=True)
    r=len(values)
    if not r:return m
    end=k+r-1;factorial=[1]*(end+1)
    for i in range(1,end+1):factorial[i]=factorial[i-1]*i%MOD
    inverse=[1]*(end+1);inverse[end]=pow(factorial[end],-1,MOD)
    for i in range(end,0,-1):inverse[i-1]=inverse[i]*i%MOD
    a=m*pow(k,-1,MOD)%MOD;prefix=0;half=pow(HALF,k,MOD);answer=m
    for d,v in enumerate(values):
        c=factorial[k+d-1]*inverse[k-1]%MOD*inverse[d]%MOD*half%MOD
        prefix=(prefix+c)%MOD;answer=(answer+(v-a)*(1-prefix))%MOD;half=half*HALF%MOD
    return answer


def rows_for(c):
    if c['mode']=='literal':return [tuple(row) for row in c['rows']]
    n,k,m=c['n'],c['k'],c['money'];rng=random.Random(c['seed'])
    rows=[(k,m)];mode=c['mode']
    if mode=='poor':rows += [(1,rng.randrange(1001)) for _ in range(n-2)]
    elif mode=='few':rows += [(1,1),(1,17),(1,1000000000)]+[(0,0)]*(n-5)
    elif mode=='same':rows += [(1,1000000000)]*(n-2)
    elif mode=='groups':rows += [(1,rng.choice(c['values'])) for _ in range(n-2)]
    elif mode=='random':rows += [(1,rng.randrange(1000000001)) for _ in range(n-2)]
    elif mode=='distinct':rows += [(1,(i*104729)%1000000001) for i in range(n-2)]
    else:raise ValueError(mode)
    rows.append((0,0));return rows


def generate(c):return as_text(rows_for(c))


def make_case(c):
    rows=rows_for(c);kind=c['oracle']
    if kind=='exact':answer=exact(rows)
    elif kind=='initial':answer=rows[0][1]
    elif kind=='matrix':answer=matrix(rows)
    elif kind=='tail':answer=grouped_tail(rows)
    elif kind=='grid':answer=grid(rows)
    elif kind=='factorial':answer=factorial_oracle(rows)
    else:raise ValueError(kind)
    return as_text(rows),str(answer)+'\n'


def matches(actual,expected):
    try:
        a=list(map(int,actual.split()));b=list(map(int,expected.split()))
        return len(a)==1 and 0<=a[0]<MOD and a==b
    except ValueError:return False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True);parser.add_argument('--case',action='append');parser.add_argument('--std',type=Path)
    args=parser.parse_args();plan=json.loads(args.plan.read_text(encoding='utf-8'));ids={c['id'] for c in plan['cases']}
    if args.case and not set(args.case)<=ids:parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:continue
        text,expected=make_case(c);validate(text,c['group']);p=args.out_dir/(c['id']+'.in');p.write_text(text,encoding='utf-8',newline='\n')
        if args.std:
            output=subprocess.check_output([str(args.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n')
            if not matches(output.decode(),expected):raise ValueError('wrong reference output: '+c['id'])
            p.with_suffix('.out').write_bytes(output)


if __name__=='__main__':main()
