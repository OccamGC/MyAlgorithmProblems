"""Independent validators and small-instance oracles for batch R28."""
from collections import deque
from functools import lru_cache
from itertools import permutations
MOD=998244353
def validate(slug,text):
    t=text.split();it=iter(t)
    def read():return int(next(it))
    if slug=='tree-demolition':
        n=read();assert 1<=n<=500000
        p=[read() for _ in range(n)];assert all(abs(x)<=1000000 for x in p)
        parent=list(range(n));edges=[]
        def find(u):
            while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
            return u
        for _ in range(n-1):
            u=read()-1;v=read()-1;assert 0<=u<n and 0<=v<n
            a=find(u);b=find(v);assert a!=b;parent[a]=b;edges.append((u,v))
        result=(p,edges)
    elif slug=='line-capacity-transport':
        n=read();m=read();assert 1<=n<=100000 and 1<=m<=100000
        cap=[read() for _ in range(n)];dist=[read() for _ in range(n)];q=[read()-1 for _ in range(m)]
        assert all(0<=x<=100000 for x in cap) and all(0<=x<=2 for x in dist[:-1]) and 0<=dist[-1]<=1000000
        assert all(0<=x<n for x in q);result=(cap,dist,q)
    elif slug=='time-management-and-team-sports':
        n=read();assert 0<=n<=500
        a=[[read() for _ in range(n)] for _ in range(n)]
        assert all(0<=x<=70 for row in a for x in row);result=a
    elif slug=='dynamic-binary-bounds':
        n=read();m=read();assert 1<=n<=10000 and 0<=m<=10000
        rows=[next(it) for _ in range(5)];assert all(len(s)==n and set(s)<={'0','1'} for s in rows)
        q=[(read()-1,read()) for _ in range(m)]
        assert all(0<=x<5 and 1<=y<=n for x,y in q);result=(rows,q)
    elif slug=='grid-forest-matching':
        n=read();m=read();assert 1<=n<=400 and 0<=m<=1000000
        grid=[next(it) for _ in range(n)];assert all(len(row)==n and set(row)<={'0','1'} for row in grid)
        seen=set()
        for x in range(n):
            for y in range(n):
                if grid[x][y]=='0' or (x,y) in seen:continue
                stack=[(x,y,-1,-1)];seen.add((x,y))
                while stack:
                    a,b,px,py=stack.pop()
                    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        c=a+dx;d=b+dy
                        if 0<=c<n and 0<=d<n and grid[c][d]=='1' and (c,d)!=(px,py):
                            assert (c,d) not in seen,'road graph has a cycle'
                            seen.add((c,d));stack.append((c,d,a,b))
        q=[read() for _ in range(m)];assert all(0<=x<=3 for x in q);result=(grid,q)
    else:raise ValueError(slug)
    assert next(it,None) is None,'extra input tokens'
    return result
def demolition_oracle(data):
    p,edges=data;n=len(p);adj=[[] for _ in p]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    parent=[-1]*n;order=[0];children=[0]*n
    for u in order:
        for v in adj[u]:
            if v!=parent[u]:parent[v]=u;children[u]|=1<<v;order.append(v)
    @lru_cache(None)
    def solve(mask):
        if mask==(1<<n)-1:return 0,()
        answer=None
        for u in range(n):
            if not(mask>>u&1) and children[u]&mask==children[u]:
                value,sequence=solve(mask|1<<u);candidate=(value+p[u]*mask.bit_count(),(u+1,)+sequence)
                if answer is None or candidate[0]>answer[0] or candidate[0]==answer[0] and candidate[1]<answer[1]:answer=candidate
        return answer
    value,sequence=solve(0);return [value,*sequence]
def transport_oracle(data):
    cap,dist,q=data;n=len(cap);cap=cap+[len(q)];position=[0]
    for d in dist:position.append(position[-1]+d)
    states={(0,)*(n+1):0};answer=[]
    for p in q:
        nxt={}
        for state,cost in states.items():
            for i in range(n+1):
                if state[i]<cap[i]:
                    row=list(state);row[i]+=1;row=tuple(row);value=cost+abs(position[p]-position[i])
                    nxt[row]=min(nxt.get(row,10**30),value)
        states=nxt;answer.append(min(states.values()))
    return answer
def assignment_oracle(a):
    n=len(a);answer=(0,)*71
    for perm in permutations(range(n)):
        counts=[0]*71
        for i,j in enumerate(perm):counts[70-a[i][j]]+=1
        answer=max(answer,tuple(counts))
    return list(answer)
def binary_oracle(data):
    rows,q=data;values=[int(s,2) for s in rows]
    def count():
        A,B,C,D,E=values;answer=[0]*4
        for a in range(A+1):
            for b in range(B+1):
                answer[((a&b)<=C)+((a^b)<=D)+((a|b)<=E)]+=1
        return [x%MOD for x in answer]
    answer=count()
    for x,y in q:values[x]^=1<<(y-1);answer+=count()
    return answer
def grid_oracle(data):
    grid,q=data;n=len(grid);positions=[(x,y) for x in range(n) for y in range(n) if grid[x][y]=='1'];answer=[len(positions)]
    for d in q:
        dx,dy=[(-1,0),(1,0),(0,-1),(0,1)][d]
        positions=[(x+dx,y+dy) for x,y in positions if 0<=x+dx<n and 0<=y+dy<n and grid[x+dx][y+dy]=='1']
        answer.append(len(positions))
    return answer
ORACLES=dict(zip(['tree-demolition','line-capacity-transport','time-management-and-team-sports','dynamic-binary-bounds','grid-forest-matching'],[demolition_oracle,transport_oracle,assignment_oracle,binary_oracle,grid_oracle]))

