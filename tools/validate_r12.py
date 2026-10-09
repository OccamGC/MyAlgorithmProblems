"""Input constraints and output-shape checks for R12."""
import math
import re
import sys
from functools import lru_cache
from pathlib import Path

PROBLEMS = (
    ('number-theory','factorial-recovery'), ('trees','dynamic-directory'),
    ('data-structures','gran-forest'), ('data-structures','crystal-list'),
    ('data-structures','contract-summoning'), ('data-structures','canister-sequence'),
)
GROUP_SHARES = {slug:(100,) for _,slug in PROBLEMS}
if hasattr(sys,'set_int_max_str_digits'): sys.set_int_max_str_digits(0)

@lru_cache(maxsize=None)
def factorial_text(n):
    return str(math.factorial(n))

class Forest:
    def __init__(self,n): self.parent=list(range(n+1))
    def find(self,v):
        while self.parent[v]!=v:
            self.parent[v]=self.parent[self.parent[v]]
            v=self.parent[v]
        return v
    def join(self,a,b):
        a=self.find(a);b=self.find(b)
        assert a!=b,'Input contains a cycle'
        self.parent[a]=b

def read_line(stream,count):
    line=stream.readline()
    assert line, 'Missing input line'
    tokens=line.split()
    assert len(tokens)==count,(count,len(tokens))
    assert all(re.fullmatch(r'-?\d+',token) for token in tokens)
    return list(map(int,tokens))

def validate(slug,path):
    with Path(path).open(encoding='ascii') as stream:
        if slug=='factorial-recovery':
            n,k=read_line(stream,2)
            assert 0<=n<=500000
            suffix=stream.readline().rstrip('\r\n')
            expected=factorial_text(n)
            assert max(0,len(expected)-15)<=k<=len(expected)
            assert len(suffix)==k and all('0'<=c<='9' for c in suffix)
            assert suffix==(expected[-k:] if k else '')
            assert not stream.read().strip()
            return dict(n=n,k=k,digits=len(expected),outputs=1)
        header=list(map(int,stream.readline().split()))
        n=header[0]
        outputs=0
        output_types=[]
        if slug=='dynamic-directory':
            assert len(header)==2
            m=header[1];assert 2<=n<=200000 and 0<=m<=200000
            forest=Forest(n)
            for _ in range(n-1):
                a,b,v=read_line(stream,3)
                assert 1<=a<=n and 1<=b<=n and abs(v)<=10000
                forest.join(a,b)
            total_k=0
            for _ in range(m):
                row=list(map(int,stream.readline().split()));assert row
                op=row[0];assert 1<=op<=4
                if op==4:
                    k=row[1];assert 1<=k<=200000 and len(row)==k+2
                    assert len(set(row[2:]))==k and all(1<=v<=n for v in row[2:])
                    total_k+=k;outputs+=1
                elif op==2:
                    assert len(row)==2 and 1<=row[1]<=n
                else:
                    assert len(row)==4 and all(1<=v<=n for v in row[1:3]) and abs(row[3])<=10000
            assert total_k<=200000
            extra=dict(m=m,total_k=total_k)
        elif slug=='gran-forest':
            assert len(header)==3
            m,q=header[1:];assert 1<=n<=500000 and 0<=m<n and 1<=q<=10000
            assert all(abs(v)<=10000 for v in read_line(stream,n))
            forest=Forest(n)
            for _ in range(m):
                a,b=read_line(stream,2)
                assert 1<=a<=n and 1<=b<=n
                forest.join(a,b)
            for _ in range(q):
                op,a,b,v=read_line(stream,4)
                assert 1<=op<=4 and 1<=a<=n and 1<=b<=n and forest.find(a)==forest.find(b)
                assert abs(v)<=(10000 if op<=2 else 100000000)
                if op>=3:outputs+=1;output_types.append(op)
            extra=dict(m=m,q=q,output_types=output_types)
        elif slug=='crystal-list':
            assert len(header)==3
            k,m=header[1:];assert 0<=n<=500000 and 0<=k<=500000 and 0<=m<=100000
            assert all(1<=v<=k for v in read_line(stream,n))
            assert all(1<=v<=50000 for v in read_line(stream,k))
            for _ in range(m):
                row=list(map(int,stream.readline().split()));assert row
                if row[0]==0:
                    assert len(row)==4
                    l,r,c=row[1:];assert 1<=l<=r<=n and 1<=c<=k
                    outputs+=1
                else:
                    assert row[0]==1 and len(row)==3 and 1<=row[1]<=k and 1<=row[2]<=50000
            extra=dict(k=k,m=m)
        elif slug=='contract-summoning':
            assert len(header)==4 and 1<=n<=100000
            assert all(0<=v<=1000000000 for v in header[1:])
            for _ in range(n):
                assert all(0<=v<=1000000000 for v in read_line(stream,6))
            outputs=1;extra={}
        else:
            assert slug=='canister-sequence' and len(header)==2
            m=header[1];assert 1<=n<=200000 and 1<=m<=200000
            assert all(1<=v<=1000000000 for v in read_line(stream,n))
            for _ in range(m):
                row=list(map(int,stream.readline().split()));assert len(row)>=3
                op,l,r=row[:3];assert 1<=op<=4
                if op==3:
                    assert len(row)==4 and 1<=l<=n and 1<=r<=n-l+1 and 1<=row[3]<=n-r+1
                else:
                    assert 1<=l<=r<=n and len(row)==(4 if op==1 else 3)
                    if op==1:assert 1<=row[3]<=1000000000
                    if op==4:outputs+=1
            extra=dict(m=m)
        assert not stream.read().strip(),'Extra input tokens'
        return dict(n=n,outputs=outputs,**extra)

VALIDATORS={slug:(lambda path,slug=slug:validate(slug,path)) for _,slug in PROBLEMS}

def validate_group(slug,spec,dimensions):
    assert slug in VALIDATORS and spec['group']==1

def check_output(slug,path,dimensions):
    tokens=Path(path).read_text(encoding='ascii').split()
    assert len(tokens)==dimensions['outputs']
    assert all(re.fullmatch(r'-?\d+',v) for v in tokens)
    if slug=='factorial-recovery':
        assert tokens==[factorial_text(dimensions['n'])]
        return
    values=list(map(int,tokens));n=dimensions['n']
    if slug=='dynamic-directory':assert all(abs(v)<=(n-1)*10000 for v in values)
    elif slug=='gran-forest':
        assert all(0<=v<=n if op==3 else abs(v)<=n*10000*(dimensions['q']+1) for v,op in zip(values,dimensions['output_types']))
    elif slug=='crystal-list':assert all(0<=v<=n*49999 for v in values)
    elif slug=='contract-summoning':
        assert 0<=values[0]<=n
        known={'none':0,'antichain':2,'one':1,'chain':n,'reverse-chain':n,'all':n,'duplicates':n}
        if Path(path).stem in known:assert values[0]==known[Path(path).stem]
    else:assert all(1<=v<=n for v in values)
