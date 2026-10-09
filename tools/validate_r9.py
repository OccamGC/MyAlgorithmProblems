"""Validate R9 input contracts, score groups and output shapes."""
import math
import re
from collections import deque
from fractions import Fraction

PROBLEMS=(('graphs','melon-planting'),('dynamic-programming','potion-wool'),('number-theory','agricultural-ratios'),('data-structures','lottery-plugin'),('strings','sign-recognition'),('trees','timber'),('trees','spice-routes'),('data-structures','colony-trade'))
GROUP_SHARES={slug:(100,) for _,slug in PROBLEMS}
GROUP_SHARES['melon-planting']=(20,30,20,30)

def melon(path):
    tokens=path.read_text().split();n,m,tp=map(int,tokens[:3]);rows=tokens[3:]
    assert n>=1 and m>=1 and tp in (0,1) and len(rows)==n
    assert all(len(row)==m and set(row)<=set('lox') for row in rows)
    p=sum(row.count('l') for row in rows)
    assert n*m<=(1000 if tp==0 else 100) and (tp==0 or p<=18)
    return dict(n=n,m=m,tp=tp,vines=p)

def wool(path):
    tokens=iter(path.read_text().split());a,b,p,k,t=[int(next(tokens)) for _ in range(5)]
    assert 1<=a<=10 and 1<=b<=10 and 1<=p<=10 and 1<=k<=50 and 1<=t<=10**6
    effects=[int(next(tokens)) for _ in range(k)]
    assert all(-100<=x<=100 for x in effects)
    for _ in range(p):
        row=[int(next(tokens)) for _ in range(k)]
        assert all(0<=x<=10 for x in row) and sum(row)>=1
    cells=list(tokens)
    assert len(cells)==a*b and cells.count('S')==1 and 1<=cells.count('C')<=10
    assert set(cells)<=set('SBCE')|set(map(str,range(p)))
    assert all(cells.count(str(i))==1 for i in range(p))
    seen={cells.index('S')};queue=deque(seen)
    while queue:
        x,y=divmod(queue.popleft(),b)
        for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            pos=u*b+v
            if 0<=u<a and 0<=v<b and cells[pos]!='B' and pos not in seen:seen.add(pos);queue.append(pos)
    assert all(i in seen for i,value in enumerate(cells) if value=='C' or value.isdigit())
    return dict(a=a,b=b,p=p,k=k,t=t,chests=cells.count('C'))

def ratios(path):
    tokens=path.read_text().split();n=int(tokens[0]);assert 1<=n<=10 and len(tokens)==1+2*n
    total=Fraction(0);answer=1;maximum=0
    for a,b in zip(tokens[1::2],tokens[2::2]):
        assert re.fullmatch(r'[01]\.[0-9]*',a) and re.fullmatch(r'[0-9]+',b)
        assert len(a)+len(b)<=200
        whole,finite=a.split('.');scale=10**len(finite)
        value=Fraction(int(whole))+Fraction(int(finite or '0'),scale)+Fraction(int(b),scale*(10**len(b)-1))
        assert 0<=value<=1
        total+=value;answer=math.lcm(answer,value.denominator);maximum=max(maximum,len(a)+len(b))
    assert 0<total<=1
    return dict(n=n,maximum_length=maximum,expected=str(answer))

def lottery(path):
    values=list(map(int,path.read_bytes().split()));A,B,C,n,m,q,k=values[:7]
    assert all(0<=v<=10**9 for v in (A,B,C))
    assert 1<=n<=3500000 and 0<=m<=4000000 and 0<=q<=200000 and 0<=k<=200000 and q+k<=m
    assert len(values)==7+q+2*k
    queries=values[7:7+q];events=values[7+q::2];people=values[8+q::2]
    assert all(1<=i<=m for i in queries+events) and all(1<=i<=n for i in people)
    assert all(x<y for x,y in zip(queries,queries[1:])) and all(x<y for x,y in zip(events,events[1:]))
    assert len(set(queries+events))==q+k
    return dict(n=n,m=m,q=q,k=k)

def sign(path):
    tokens=path.read_text().split();n,q=map(int,tokens[:2]);assert 1<=n<=5 and 1<=q<=5
    assert len(tokens)==2+n+2*q
    strings=tokens[2:2+n]
    assert all(1<=len(s)<=50000 and re.fullmatch('[a-z]+',s) for s in strings)
    queries=list(map(int,tokens[2+n:]));assert all(1<=l<=r<=10**10 for l,r in zip(queries[::2],queries[1::2]))
    return dict(n=n,q=q,total_length=sum(map(len,strings)),max_answer=sum(len(s)*(len(s)+1)//2 for s in strings),all_equal=len(set(strings))==1 and n>1)

def forest(n,edges):
    parent=list(range(n+1))
    def find(u):
        while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
        return u
    for u,v in edges:
        assert 1<=u<=n and 1<=v<=n
        x,y=find(u),find(v);assert x!=y;parent[x]=y

def timber(path):
    values=list(map(int,path.read_bytes().split()));n,m=values[:2]
    assert 1<=n<=500000 and 0<=m<=n-1 and len(values)==2+2*m
    forest(n,list(zip(values[2::2],values[3::2])))
    return dict(n=n,m=m,components=n-m)

def spice(path):
    values=list(map(int,path.read_bytes().split()));n=values[0];assert 1<=n<=100000
    edges=[values[i:i+4] for i in range(1,1+4*(n-1),4)]
    assert all(len(edge)==4 and 0<=edge[2]<=edge[3]<=100000 and edge[3]>=1 for edge in edges)
    forest(n,[(u,v) for u,v,_,_ in edges])
    pos=1+4*(n-1);a=values[pos];low=values[pos+1:pos+1+a];pos+=a+1;b=values[pos];high=values[pos+1:]
    assert 0<=a<=n and 0<=b<=2 and len(low)==a and len(high)==b and all(1<=v<=n for v in low+high)
    expected=None
    if not a or not b:expected=0
    elif set(low)&set(high):expected=1
    elif all(q==0 for _,_,q,_ in edges):expected=1
    elif all(q==p for _,_,q,p in edges):expected=0
    return dict(n=n,a=a,b=b,expected=expected)

def trade(path):
    with path.open() as stream:
        n,m=map(int,stream.readline().split());assert 1<=n<=300000 and 1<=m<=300000
        initial=list(map(int,stream.readline().split()));assert len(initial)==2*n
        assert all(0<=c<=10**9 for c in initial[::2]) and all(0<=p<=10**5 for p in initial[1::2])
        queries=0;maximum_changes=0
        for _ in range(m):
            op=list(map(int,stream.readline().split()));assert op and op[0] in (1,2,3,4)
            if op[0]<=2:
                assert len(op)==2 and 0<=op[1]<=(1000 if op[0]==1 else 10**18)
                queries+=op[0]==2
            else:
                assert len(op)==3 and 1<=op[1]<=n and 0<=op[2]<=(10**5 if op[0]==3 else 10**9)
                maximum_changes+=op[0]==4
        assert not stream.read().strip()
    return dict(n=n,m=m,query_count=queries,price_changes=maximum_changes)

VALIDATORS=dict(zip((slug for _,slug in PROBLEMS),(melon,wool,ratios,lottery,sign,timber,spice,trade)))

def validate_group(slug,spec,d):
    if slug=='melon-planting':
        group=spec['group'];assert d['tp']==(group>=3)
        if group in (1,3):assert d['n']==1

def check_output(slug,path,d):
    tokens=path.read_bytes().split()
    assert all(re.fullmatch(rb'\d+',s) for s in tokens)
    values=list(map(int,tokens))
    if slug=='timber':
        assert values and 1<=values[0]<=d['n'] and len(values)==1+2*values[0]
        pairs=list(zip(values[1::2],values[2::2]));assert pairs[-1]==(d['n'],d['components'])
        assert all(1<=cut<=d['n'] and 1<=trees<=min(k,d['components']) for k,(cut,trees) in enumerate(pairs,1))
        gains=[pairs[0][0]]+[b[0]-a[0] for a,b in zip(pairs,pairs[1:])]
        assert all(x>=y>0 for x,y in zip(gains,gains[1:]))
        if d['m']==0:assert pairs==[(i,i) for i in range(1,d['n']+1)]
    elif slug in ('lottery-plugin','sign-recognition','colony-trade'):
        assert len(values)==d.get('q',d.get('query_count'))
        limit=d['n'] if slug=='lottery-plugin' else d['max_answer'] if slug=='sign-recognition' else 1000000006
        assert all(0<=v<=limit for v in values)
        if d.get('all_equal'):assert not any(values)
    else:
        assert len(values)==1
        if slug=='melon-planting':assert values[0]<=d['vines']
        elif slug=='agricultural-ratios':assert str(values[0])==d['expected']
        elif slug=='spice-routes':
            assert values[0]<1000000007
            if d['expected'] is not None:assert values[0]==d['expected']
