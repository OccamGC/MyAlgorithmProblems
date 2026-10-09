"""Validate R18 input formats, ranges and geometry scoring groups."""
from pathlib import Path
import re
import sys

def validate(slug,path,group=None):
    text=Path(path).read_text(encoding='ascii');lines=text.splitlines()
    if slug=='acceleration-orders' or slug.startswith('rectangle-'):
        T=int(lines[0]);assert 0<=T<=(10000 if slug=='acceleration-orders' else 1000)
        assert len(lines)==T+1
        dims=set()
        allowed={1:{2},2:{1},3:{0},4:{0,1},5:{0,2},6:{1,2},7:{0,1,2}}
        for line in lines[1:]:
            row=list(map(int,line.split()))
            assert len(row)==(2 if slug=='acceleration-orders' else 8)
            assert all(abs(x)<=(10000 if slug=='acceleration-orders' else 10**9) for x in row)
            if slug.startswith('rectangle-'):
                for i in [0,4]:
                    dim=int(row[i]!=row[i+2])+int(row[i+1]!=row[i+3]);dims.add(dim)
                    if slug=='rectangle-intersection-type' and group:
                        assert dim in allowed[group],(path,group,row)
        return dict(T=T,dimensions=sorted(dims))
    if slug=='matrix-mixer':
        n,m,K=map(int,lines[0].split());initial_n=n
        assert 1<=n<=20 and 1<=m<=20 and 1<=K<=1000 and len(lines)==n+K+1
        for line in lines[1:n+1]:
            values=list(map(int,line.split()));assert len(values)==m and all(0<=v<=10**9 for v in values)
        invalid=0
        for line in lines[n+1:]:
            op,*args=map(int,line.split());assert op in [1,2,3]
            assert len(args)==(0 if op==3 else 2)
            assert all(abs(x)<=30 for x in args)
            if op==3:n,m=m,n
            else:
                bound=n if op==1 else m
                invalid+=not all(1<=x<=bound for x in args)
        return dict(n=initial_n,cells=len(lines[1].split())*initial_n,K=K,invalid_operations=invalid)
    if slug=='skewer-substrings':
        s=lines[0];M=int(lines[1]);assert re.fullmatch('[a-z]{1,1000}',s) and 1<=M<=1000 and len(lines)==M+2
        for line in lines[2:]:
            l,r,t=line.split();assert 1<=int(l)<=int(r)<=len(s) and re.fullmatch('[a-z]{1,40}',t)
        return dict(N=len(s),M=M)
    assert slug=='cat-selection'
    n,k,*values=map(int,text.split())
    assert 0<=k<=n<=25 and len(values)==n and all(abs(v)<=1000 for v in values)
    return dict(n=n,k=k)

if __name__=='__main__':
    print(validate(sys.argv[1],Path(sys.argv[2])))
