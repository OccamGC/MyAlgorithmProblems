"""Validate R7 ranges, score groups, outputs and selected closed-form cases."""
from pathlib import Path

PROBLEMS = (
    ('optimization','century-bomber'), ('trees','psychic-control-tree'),
    ('dynamic-programming','gene-mutation'), ('combinatorics','rhino-tank'),
    ('number-theory','redstone-clock'), ('data-structures','torch-light'),
    ('graphs','redstone-computer'), ('geometry','wheat-field'),
)
GROUP_SHARES = {slug:(100,) for _,slug in PROBLEMS}
GROUP_SHARES.update({'redstone-clock':(25,75), 'torch-light':(30,20,30,20), 'redstone-computer':(10,20,70)})

def century(path):
    values=list(map(int,path.read_bytes().split()))
    n,m,k,q=values[:4]
    assert 1<=n<=2000 and 1<=m<=2000 and 0<=k<=m and 0<=q<=30000
    assert len(values)==4+n+k+2*q
    assert all(0<=a<=9 for a in values[4:4+n])
    positions=values[4+n:4+n+k]
    assert len(set(positions))==k and all(1<=p<=m for p in positions)
    queries=values[4+n+k:]
    assert all(1<=l<=r<=n for l,r in zip(queries[::2],queries[1::2]))
    return dict(n=n,m=m,k=k,q=q)

def tree(path):
    values=list(map(int,path.read_bytes().split()))
    n=values[0]
    assert 1<=n<=100000 and len(values)==1+2*n+2*(n-1)
    weights=values[1:1+2*n:2]; control=values[2:1+2*n:2]
    assert all(1<=v<=5000 for v in weights) and sorted(control)==list(range(1,n+1))
    parent=list(range(n+1))
    def find(u):
        while parent[u]!=u:
            parent[u]=parent[parent[u]];u=parent[u]
        return u
    edge_values=values[1+2*n:]
    for u,v in zip(edge_values[::2],edge_values[1::2]):
        assert 1<=u<=n and 1<=v<=n and find(u)!=find(v)
        parent[find(u)]=find(v)
    return dict(n=n,total_weight=sum(weights),identity=control==list(range(1,n+1)))

def gene(path):
    values=list(map(int,path.read_bytes().split()))
    n,m,la,lb=values[:4]
    assert 2<=n<=30 and 2<=m<=30 and 1<=la<=20000 and 1<=lb<=20000
    assert len(values)==4+la+lb and all(0<=x<n for x in values[4:])
    assert la==1 or values[4]!=0
    assert lb==1 or values[4+la]!=0
    return dict(n=n,m=m,length_a=la,length_b=lb)

def rhino(path):
    values=list(map(int,path.read_bytes().split()))
    n,m=values[:2]
    assert 1<=n<=5 and 1<=m<=7 and len(values)==2+n*n*m
    assert all(0<=x<=100000 for x in values[2:])
    assert all(sum(values[i:i+m])>0 for i in range(2,len(values),m))
    return dict(n=n,m=m)

def clock(path):
    values=list(map(int,path.read_bytes().split()))
    assert len(values)==2
    n,a=values
    assert 1<=n<=10000000 and 1<=a<=10000000
    return dict(n=n,a=a)

def torch(path):
    with path.open() as stream:
        n,m=map(int,stream.readline().split())
        assert 1<=n<=2200 and 1<=m<=2200
        for _ in range(n):
            row=list(map(int,stream.readline().split()))
            assert len(row)==2*m
            assert all(abs(x)<=100000000 for x in row[::2])
            assert all(0<=r<=100000 for r in row[1::2])
        for _ in range(n):
            row=list(map(int,stream.readline().split()))
            assert len(row)==m and all(abs(x)<=10**15 for x in row)
        assert not stream.read().strip()
    return dict(n=n,m=m)

def computer(path):
    with path.open() as stream:
        n,m,k=map(int,stream.readline().split())
        assert 0<=n<=500 and 0<=m<=10000 and 1<=k<=150
        for _ in range(m):
            a,op,b,c=stream.readline().split()
            assert 1<=int(a)<=n and 1<=int(b)<=n and op in ('^','&','|')
            assert len(c)==k and set(c)<=set('01')
        assert not stream.read().strip()
    return dict(n=n,m=m,k=k)

def wheat(path):
    values=list(map(int,path.read_bytes().split()))
    n,m,k=values[:3]
    assert 1<=n<=100000 and 1<=m<=100000 and 0<=k<=200 and len(values)==3+2*k
    assert all(1<=x<=n and 1<=y<=m for x,y in zip(values[3::2],values[4::2]))
    return dict(n=n,m=m,k=k)

VALIDATORS=dict(zip((slug for _,slug in PROBLEMS),(century,tree,gene,rhino,clock,torch,computer,wheat)))

def validate_group(slug,spec,dimensions):
    group=spec['group']
    if slug=='redstone-clock' and group==1:
        assert dimensions['n']<=1000000
    elif slug=='torch-light':
        assert max(dimensions['n'],dimensions['m'])<=(80,300,1500,2200)[group-1]
    elif slug=='redstone-computer' and group<=2:
        assert dimensions['k']==1 and dimensions['n']<=(20,50)[group-1]

def check_computer(input_path,tokens,reference=None):
    with input_path.open() as stream:
        n,m,k=map(int,stream.readline().split())
        if tokens==[b'No']:
            if reference is not None:
                assert reference==[b'No']
            return
        assert len(tokens)==n and all(len(x)==k and set(x)<={48,49} for x in tokens)
        values=[int(x,2) for x in tokens]
        for _ in range(m):
            a,op,b,c=stream.readline().split()
            u,v=values[int(a)-1],values[int(b)-1]
            assert (u^v if op=='^' else u&v if op=='&' else u|v)==int(c,2)

def check_output(slug,path,dimensions):
    tokens=path.read_bytes().split()
    if slug=='redstone-computer':
        check_computer(path.with_suffix('.in'),tokens)
        if path.stem in ('late-impossible','medium-impossible','sample-3'):
            assert tokens==[b'No']
        else:
            assert tokens!=[b'No']
        return
    assert all(t.isdigit() for t in tokens),path
    values=list(map(int,tokens))
    n=dimensions['n']
    count=dimensions['m'] if slug=='century-bomber' else n if slug=='psychic-control-tree' else 2 if slug=='redstone-clock' else 1
    assert len(values)==count
    if slug=='century-bomber':
        assert all(v<=9*dimensions['q']*dimensions['k'] for v in values)
        if path.stem=='maximum-full': assert values==[9*dimensions['q']*(j+1) for j in range(dimensions['m'])]
        if path.stem in ('zero-values','no-starts','sample-3'): assert not any(values)
    elif slug=='psychic-control-tree':
        assert values[0]==0 and all(v<=dimensions['total_weight'] for v in values)
        if dimensions['identity'] or path.stem=='maximum-star': assert not any(values)
        if path.stem=='maximum-chain':
            data=list(map(int,path.with_suffix('.in').read_bytes().split()))
            control=data[2:1+2*n:2]
            low=n; high=1
            for i in range(n-1,-1,-1):
                low=min(low,control[i]); high=max(high,control[i])
                assert values[i]==(high-low+1-(n-i))*5000
    elif slug in ('gene-mutation','rhino-tank'):
        assert values[0]<1000000007
        if slug=='gene-mutation':
            if path.stem in ('equal-base','long-standard','all-maximal'): assert values==[0]
            if path.stem=='zero-standard':
                data=list(map(int,path.with_suffix('.in').read_bytes().split()))
                result=0
                for digit in data[4+dimensions['length_a']:]: result=(result*n+digit)%1000000007
                assert values==[result]
        elif path.stem=='fixed-valid': assert values==[1]
        elif path.stem in ('fixed-invalid','one-color','sample-3'): assert values==[0]
    elif slug=='redstone-clock':
        assert all(v<1<<47 for v in values)
    elif slug=='torch-light':
        assert 0<=values[0]<=n*dimensions['m']
        if path.stem in ('large-cover','maximum-cover'): assert values==[(n*dimensions['m']+1)//2]
        if path.stem=='medium-point': assert values==[n*dimensions['m']]
    elif slug=='wheat-field':
        assert values[0]<=min(n,dimensions['m'])
        if path.stem=='empty': assert values==[min(n,dimensions['m'])]
