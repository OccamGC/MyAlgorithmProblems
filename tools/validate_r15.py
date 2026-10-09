"""Validate full-size R15 inputs without depending on the generators."""
from pathlib import Path

def validate(slug, path):
    with Path(path).open(encoding='ascii') as stream:
        header = list(map(int,stream.readline().split()))
        if slug == 'recursive-statistics':
            assert len(header)==1
            q = header[0]
            assert 0<=q<=100000
            values = [int(stream.readline()) for _ in range(q)]
            assert all(-1000000000<=v<=100000 for v in values)
            result = dict(q=q,maximum=max([0,*values]))
        elif slug == 'simple-merge':
            assert len(header)==2
            k,m = header
            assert 1<=k<=31 and m>=0
            total=0
            for _ in range(k):
                values=list(map(int,stream.readline().split()))
                size,a=values[0],values[1:]
                assert size>=1 and len(a)==size
                assert all(abs(v)<=1000000000 for v in a)
                assert all(x<=y for x,y in zip(a,a[1:])) or all(x>=y for x,y in zip(a,a[1:]))
                total+=size
            assert m<=total<=1000000
            result=dict(k=k,m=m,total=total)
        elif slug.startswith('interval-'):
            assert len(header)==1
            n=header[0]
            values=list(map(int,stream.readline().split()))
            assert 1<=n<=1000 and len(values)==n
            assert all(abs(v)<=1000000000 for v in values)
            result=dict(n=n,output_count=n*(n+1)//2)
        elif slug=='technology-tree':
            assert len(header)==2
            n,m=header
            assert 1<=n<=1000000 and 0<=m<=2000000
            duration=list(map(int,stream.readline().split()))
            assert len(duration)==n and all(-1<=v<=1000000000 for v in duration)
            active_edges=0
            self_loops=0
            for _ in range(m):
                fields=list(map(int,stream.readline().split()))
                assert len(fields)==2
                u,v=fields
                assert 1<=u<=n and 1<=v<=n
                active_edges+=duration[u-1]!=-1 and duration[v-1]!=-1
                self_loops+=u==v
            result=dict(n=n,m=m,active_edges=active_edges,self_loops=self_loops,completed=duration.count(-1))
        elif slug=='binary-traversals':
            assert len(header)==1
            n=header[0]
            assert 1<=n<=1000000
            pre=list(map(int,stream.readline().split()))
            ino=list(map(int,stream.readline().split()))
            assert len(pre)==len(ino)==n
            for values in [pre,ino]:
                seen=bytearray(n+1)
                for v in values:
                    assert 1<=v<=n and not seen[v]
                    seen[v]=1
            # Simulate opening nodes in preorder and closing them in inorder.
            stack=[]
            cursor=0
            for v in pre:
                stack.append(v)
                while stack and cursor<n and stack[-1]==ino[cursor]:
                    stack.pop()
                    cursor+=1
            assert cursor==n and not stack, 'incompatible traversals'
            result=dict(n=n,output_count=n)
        else:
            raise ValueError(slug)
        assert not stream.read().strip(), 'trailing input'
        return result
