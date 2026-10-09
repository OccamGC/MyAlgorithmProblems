"""Input, scoring-group, and output checks for R6."""
import math
from pathlib import Path
import re

GROUP_SHARES = {'chaos-drone': (20,20,20,10,30), 'force-shield': (30,70),
                'vacuum-imploder': (100,), 'upgrade-toolkit': (100,),
                'nano-computer': (100,), 'cloning-vat': (100,)}


def validate_chaos(path):
    with path.open(encoding='utf-8') as source:
        n,m=map(int,source.readline().split())
        assert 1 <= n <= 300 and 0 <= m <= n*(n-1)//2
        names={}
        edges=set()
        for _ in range(m):
            a,b=source.readline().split()
            for value in (a,b):
                assert 1 <= len(value.encode('utf-8')) <= 80
                assert re.fullmatch(r'[A-Za-z0-9_\-\u3400-\u9fff]+',value)
                names.setdefault(value,len(names))
            u,v=sorted((names[a],names[b]))
            assert u != v and (u,v) not in edges
            edges.add((u,v))
        assert len(names) <= n and not source.read()
    parent=list(range(n))
    def find(u):
        while parent[u] != u:
            parent[u]=parent[parent[u]]
            u=parent[u]
        return u
    for u,v in edges:
        parent[find(u)]=find(v)
    vertices={}
    edge_counts={}
    for u in range(n):
        root=find(u)
        vertices[root]=vertices.get(root,0)+1
    for u,_ in edges:
        root=find(u)
        edge_counts[root]=edge_counts.get(root,0)+1
    return dict(n=n,m=m,forest=all(edge_counts.get(root,0)==size-1 for root,size in vertices.items()),
                unicyclic=all(edge_counts.get(root,0)==size for root,size in vertices.items()))


def validate_shield(path):
    with path.open(encoding='ascii') as source:
        n,m,r,s,a,b=map(int,source.readline().split())
        assert 1<=n<=500000 and 0<=a<=200000 and 0<=b<=200000
        assert 0<=m<3000 and 1<=r<=3000 and 0<=s<=3000
        small=n<=2000 and a<=1000 and b<=1000 and m<=30 and r<=30 and s<=30
        horizon=0
        for _ in range(n):
            x,t=map(int,source.readline().split())
            assert -1499<=x<=1500 and 1<=t<=3000
            small=small and -14<=x<=15 and t<=30
        for _ in range(a+b):
            l,h,t,k,amount=map(int,source.readline().split())
            assert -1499<=l<=h<=1500 and t>=1 and k>=1 and t+k-1<=3000 and 0<=amount<=1000
            small=small and -14<=l<=h<=15 and t+k-1<=30
            horizon=max(horizon,t+k-1)
        assert not source.read()
    return dict(n=n,M=m,R_s=r,S=s,A=a,B=b,horizon=horizon,small=small)


def validate_imploder(path):
    with path.open(encoding='ascii') as source:
        n,m=map(int,source.readline().split())
        assert 1<=n<=50000 and 1<=m<=50000
        for _ in range(n):
            x,y=map(int,source.readline().split())
            assert abs(x)<=10000 and abs(y)<=10000
        queries=0
        for _ in range(m):
            code,*args=map(int,source.readline().split())
            assert 0<=code<=7
            if code==7:
                assert len(args)==1 and 1<=args[0]<=n
                queries+=1
            else:
                assert len(args)==(3 if code in (0,1,6) else 2)
                l,r=args[:2]
                assert 1<=l<=r<=n
                if code<=1:
                    assert -100<=args[2]<=100
                if code==6:
                    assert 0<=args[2]<=360
        assert not source.read()
    return dict(n=n,m=m,queries=queries)


def validate_toolkit(path):
    with path.open(encoding='ascii') as source:
        n=int(source.readline())
        assert 0<=n<=1000
        capacities=[]
        for i in range(1,n+1):
            k,v=map(int,source.readline().split())
            assert 0<=k<=1000 and 0<=v<=1000
            capacities.append(min(k,v//i))
        assert not source.read()
    return dict(n=n,total_capacity=sum(capacities),capacities=capacities)


def validate_nano(path):
    with path.open(encoding='ascii') as source:
        n,q=map(int,source.readline().split())
        assert 1<=n<=100000 and 1<=q<=100000
        values=list(map(int,source.readline().split()))
        assert len(values)==n and all(0<=value<=65536 for value in values)
        queries=0
        for _ in range(q):
            code,l,r=map(int,source.readline().split())
            assert code in (1,2)
            if code==1:
                assert 1<=l<=r<=n
                queries+=1
            else:
                assert 1<=l<=n and 0<=r<=65536
        assert not source.read()
    return dict(n=n,q=q,queries=queries)


def validate_clone(path):
    with path.open(encoding='ascii') as source:
        q=int(source.readline())
        assert 1<=q<=1000000
        total=0
        maximum=0
        for _ in range(q):
            n,m,text=source.readline().split()
            n,m=int(n),int(m)
            assert n>=1 and n%2 and 0<=m<=n and len(text)==n and set(text)<=set('0123')
            total+=n
            maximum=max(maximum,n)
        assert total<=1000000 and not source.read()
    return dict(q=q,total_length=total,max_length=maximum)


VALIDATORS={'chaos-drone':validate_chaos,'force-shield':validate_shield,
            'vacuum-imploder':validate_imploder,'upgrade-toolkit':validate_toolkit,
            'nano-computer':validate_nano,'cloning-vat':validate_clone}


def validate_group(slug,spec,d):
    if slug=='chaos-drone':
        if spec['group']==1:
            assert d['n']<=10 and d['m']<=20
        if spec['group']==2:
            assert d['forest']
        if spec['group']==3:
            assert d['unicyclic']
        if spec['group']==4:
            assert d['m']==d['n']*(d['n']-1)//2
    if slug=='force-shield' and spec['group']==1:
        assert d['small']


def check_output(slug,path,d):
    if slug=='cloning-vat':
        with path.with_suffix('.in').open(encoding='ascii') as source, path.open(encoding='ascii') as answer:
            q=int(source.readline())
            for _ in range(q):
                n,m,text=source.readline().split()
                n,m=int(n),int(m)
                half=n//2
                actual=answer.readline().rstrip('\n')
                different=sum(text[i]!=text[i+half+1] for i in range(half))
                if different>m:
                    assert actual=='failed'
                else:
                    assert len(actual)==n and set(actual)<=set('0123')
                    assert actual[:half]==actual[half+1:]
                    assert sum(a!=b for a,b in zip(text,actual))==m
                    if path.stem=='all-change':
                        assert actual=='1'*n
                    if path.stem=='no-change':
                        assert actual==text
            assert not answer.read()
        return
    lines=path.read_text(encoding='ascii').splitlines()
    tokens=' '.join(lines).split()
    if slug=='vacuum-imploder':
        assert len(lines)==d['n']+d['queries'] and all(len(line.split())==2 for line in lines)
        values=list(map(float,tokens))
        assert all(math.isfinite(value) for value in values)
        if path.stem in ('rotations','translations','queries','reflections'):
            with path.with_suffix('.in').open() as source:
                n,m=map(int,source.readline().split())
                points=[tuple(map(int,source.readline().split())) for _ in range(n)]
                if path.stem=='queries':
                    expected=[points[int(source.readline().split()[1])-1] for _ in range(m)]+points
                elif path.stem=='translations':
                    expected=[(x+100*((m+1)//2),y+100*(m//2)) for x,y in points]
                elif path.stem=='reflections':
                    assert m%4==0
                    expected=points
                else:
                    angle=math.radians(m%360)
                    expected=[(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle)) for x,y in points]
            flat=[value for point in expected for value in point]
            assert len(values)==len(flat) and all(abs(a-b)<=1e-5 for a,b in zip(values,flat))
        return
    assert all(re.fullmatch(r'-?\d+',token) for token in tokens)
    values=list(map(int,tokens))
    if slug=='chaos-drone':
        assert len(lines)==len(values)==1 and (d['n']+1)//2<=values[0]<=d['n']
        if d['m']==0:
            assert values[0]==d['n']
        if d['m']==d['n']*(d['n']-1)//2:
            assert values[0]==(d['n']+1)//2
        if path.stem=='star':
            assert values[0]==d['n']-1
    elif slug=='force-shield':
        assert len(lines)==len(values)==1 and abs(values[0])<=6*10**17
        known={'sample-negative':-37,'zero-span':0,'maximum':0,'no-events':0,
               'repairs-only':-300000000000000000,'maximum-damage':299999966600000000}
        if path.stem in known:
            assert values==[known[path.stem]],(path,values)
    elif slug=='upgrade-toolkit':
        modulus=100000007
        assert len(lines)==1 and len(values)==d['total_capacity']+1
        assert all(0<=value<modulus for value in values)
        assert values==values[::-1] and values[0]==values[-1]==1
        assert sum(values)%modulus==math.prod(c+1 for c in d['capacities'])%modulus
        if path.stem=='ones':
            assert values==[math.comb(d['n'],k)%modulus for k in range(d['n']+1)]
    elif slug=='nano-computer':
        assert len(lines)==len(values)==d['queries']
        assert all(0<=value<=131071*d['n']*(d['n']+1)//2 for value in values)
        if path.stem=='zero':
            assert set(values)<={0}
        if path.stem=='high-bit':
            assert set(values)=={((d['n']+1)**2//4)*65536}
