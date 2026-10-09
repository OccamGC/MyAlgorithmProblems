"""Validate complete formal inputs against the published R19 contracts."""
from pathlib import Path

def validate(slug,path,group=None):
    lines=Path(path).read_text(encoding='ascii').splitlines()
    n=int(lines[0])
    if slug=='character-x':
        assert 0<=n<=20 and len(lines)==n+1
        assert all(len(c)==1 and c.isascii() and c.isalnum() for c in lines[1:])
    elif slug=='recursive-maximum':
        assert 1<=n<=100 and len(lines)==2
        values=list(map(int,lines[1].split()));assert len(values)==n
        assert all(abs(v)<=10**9 for v in values)
    elif slug=='heap-tree-distance':
        assert 1<=n<=10**5 and len(lines)==n+1
        for line in lines[1:]:
            values=list(map(int,line.split()));assert len(values)==2 and all(1<=v<=10**18 for v in values)
    elif slug=='didu-hia-signifier-cycles':
        assert 0<=n<=10**5 and len(lines)==n+1
        assert all(1<=int(v)<=n for v in lines[1:])
    elif slug=='variable-lists':
        assert 1<=n<=500
        sizes=list(map(int,lines[1].split()));assert len(sizes)==n and all(1<=c<=1000 for c in sizes)
        m=int(lines[2]);assert 1<=m<=500000 and len(lines)==m+3
        for line in lines[3:]:
            values=list(map(int,line.split()));op=values[0]
            assert 1<=op<=5 and len(values)==(3 if op==5 else 2)
            if op in (3,4):assert 1<=values[1]<=n
            else:assert all(abs(v)<=10**9 for v in values[1:])
        return dict(n=n,initial_items=sum(sizes),m=m)
    elif slug=='signal-network':
        assert 0<=n<=2000000 and len(lines)==n+1
        for line in lines[1:]:
            values=list(map(int,line.split()));op=values[0]
            assert 1<=op<=3 and len(values)=={1:2,2:1,3:3}[op]
            if op==1:assert abs(values[1])<=10**9
            if op==3:assert 0<=values[1]<=values[2]<=127
    else:raise ValueError(slug)
    return dict(count=n)
