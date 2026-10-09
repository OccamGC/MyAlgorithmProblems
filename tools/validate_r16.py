"""Validate input ranges without loading large graph edge lists."""
from pathlib import Path
import re

def validate(slug,path):
    with Path(path).open(encoding='ascii') as stream:
        if slug=='paper-tiger-sequence':
            initial=stream.readline().rstrip('\n')
            assert re.fullmatch('[A-Za-z0-9]{1,10}',initial)
            n,m=map(int,stream.readline().split());assert 0<=n<=70 and 0<=m<=n+1
            positions=[int(stream.readline()) for _ in range(n)]
            queries=[int(stream.readline()) for _ in range(m)]
            assert all(0<=p<=10**9 for p in positions)
            assert len(set(queries))==m and all(0<=q<=n for q in queries)
            lengths=[len(initial)]
            for _ in range(n):lengths.append(lengths[-1]+(lengths[-1]+4)//5)
            result=dict(n=n,m=m,initial=initial,positions=positions,queries=queries,output_characters=sum(lengths[q]+1 for q in queries),final_length=lengths[-1])
        elif slug=='simple-rail-network':
            n,m=map(int,stream.readline().split());assert 1<=n<=10**6 and 0<=m<=2*10**6
            negative_sum=0
            for _ in range(m):
                a,b,w=map(int,stream.readline().split())
                assert 1<=a<=n and 1<=b<=n and abs(w)<=10**9
                negative_sum+=min(w,0)
            result=dict(n=n,m=m,negative_sum=negative_sum)
        elif slug=='block-tower':
            n=int(stream.readline());assert 1<=n<=10
            names=[stream.readline().rstrip('\n') for _ in range(n+3)]
            assert all(re.fullmatch('[A-Za-z0-9_ ]{1,20}',s) for s in names)
            result=dict(n=n,names=names)
        else:
            T=int(stream.readline());assert 0<=T<=1000
            values=[int(stream.readline()) for _ in range(T)]
            assert all(abs(x)<=10**18 for x in values)
            result=dict(T=T,values=values)
        assert stream.read()==''
    return result
