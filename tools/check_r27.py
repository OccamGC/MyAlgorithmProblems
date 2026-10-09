"""Input validation and independent small-instance oracles for R27."""
import itertools, math
from functools import lru_cache
PROBLEMS=[('greedy','digit-merge-extremes'),('data-structures','queue-with-stacks'),('data-structures','exact-search-tree'),('trees','lexicographic-heap-labels'),('graphs','rotating-bytes')]
VARIANTS={s:['std','alternative'] if s=='lexicographic-heap-labels' else ['std'] for _,s in PROBLEMS}
def validate(slug,text,group=None):
    it=iter(text.split())
    def integer():return int(next(it))
    if slug=='digit-merge-extremes':
        n=integer();k=integer();assert 2<=n<=10**6 and 2<=k<=10**9 and len(text.encode())<=21000000
        a=[integer() for _ in range(n)];assert a[0]>0 and all(0<=x<k for x in a);result=dict(n=n,k=k)
    elif slug=='queue-with-stacks':
        n=integer();m=integer();assert 2<=n<=10**9 and 0<=m<=4*10**6
        s=next(it) if m else '';assert len(s)==m and set(s)<=set('01');result=dict(n=n,m=m)
    elif slug=='exact-search-tree':
        m=integer();assert 0<=m<=10**5;prints=0
        for _ in range(m):
            t=integer();assert 0<=t<=2
            if t:assert -2**31<=integer()<2**31
            else:prints+=1
        assert prints<=10;result=dict(m=m,prints=prints)
    elif slug=='lexicographic-heap-labels':
        n=integer();root=integer();assert 2<=n<=500000 and 1<=root<=n
        dsu=list(range(n+1))
        def find(x):
            while dsu[x]!=x:dsu[x]=dsu[dsu[x]];x=dsu[x]
            return x
        for _ in range(n-1):
            a=integer();b=integer();assert 1<=a<=n and 1<=b<=n
            a=find(a);b=find(b);assert a!=b;dsu[a]=b
        result=dict(n=n,root=root)
    else:
        n=integer();m=integer();k=integer();assert 2<=n<=2*10**6 and 1<=m<=3*10**6 and 1<=k<n
        def binary(s):assert 1<=len(s)<=5 and set(s)<=set('01')
        for _ in range(n):binary(next(it))
        starts=[integer() for _ in range(k)];assert all(2<=s<=n for s in starts) and len(set(starts))==k
        head=[-1]*(n+1);dest=[];nxt=[]
        for e in range(m):
            u=integer();v=integer();assert 1<=u<=n and 1<=v<=n;binary(next(it));dest.append(u);nxt.append(head[v]);head[v]=e
        seen=bytearray(n+1);seen[1]=1;todo=[1]
        for v in todo:
            e=head[v]
            while e!=-1:
                u=dest[e]
                if not seen[u]:seen[u]=1;todo.append(u)
                e=nxt[e]
        assert any(seen[s] for s in starts)
        if group==1:assert n<=10 and m<=10
        if group==2:assert n<=1000 and m<=2000
        if group==3:assert n<=300000 and m<=500000
        result=dict(n=n,m=m,k=k)
    assert next(it,None) is None
    return result
def digits(text):
    n,k,*a=map(int,text.split());candidates=[]
    for i in range(n):
        for j in range(i+1,n):
            b=a.copy();s=b[i]+b[j];b[j]=s%k
            if s>=k:b[i]=1
            else:del b[i]
            while b[0]==0:del b[0]
            candidates.append(tuple(b))
    key=lambda b:(len(b),b)
    return '\n'.join(' '.join(map(str,b)) for b in [max(candidates,key=key),min(candidates,key=key)])+'\n'
def queue(text):
    # Dijkstra over complete stack configurations with input/output time windows.
    import heapq
    parts=text.split();n=int(parts[0]);s=parts[2] if int(parts[1]) else '';waiting=0;needed=0
    for c in s:
        if c=='0':waiting+=1
        elif waiting:waiting-=1;needed+=1
    n=min(n,max(2,needed));states={tuple([()]*n):0};pushed=0;popped=0
    for c in s:
        nxt={}
        if c=='0' and pushed<needed:
            pushed+=1
            for state,cost in states.items():
                for i in range(n):
                    a=list(state);a[i]+=(pushed,);a=tuple(sorted(a));nxt[a]=min(nxt.get(a,10**9),cost+1)
        elif c=='1' and popped<pushed:
            popped+=1
            for state,cost in states.items():
                for i,x in enumerate(state):
                    if x and x[-1]==popped:a=list(state);a[i]=x[:-1];a=tuple(sorted(a));nxt[a]=min(nxt.get(a,10**9),cost+1)
        else:continue
        states=nxt;heap=[(c,s) for s,c in states.items()];heapq.heapify(heap)
        while heap:
            cost,state=heapq.heappop(heap)
            if states[state]!=cost:continue
            for i,x in enumerate(state):
                if not x:continue
                for j in range(n):
                    if i==j:continue
                    a=list(state);a[i]=x[:-1];a[j]+=(x[-1],);a=tuple(sorted(a))
                    if states.get(a,10**9)>cost+2:states[a]=cost+2;heapq.heappush(heap,(cost+2,a))
    return str(min(states.values()))+'\n'
def bst(text):
    it=iter(map(int,text.split()));m=next(it);root=None;out=[]
    # Node = [key, multiplicity, left, right]. No ordered index.
    def insert(t,x):
        if t is None:return [x,1,None,None]
        if x==t[0]:t[1]+=1
        else:
            side=2 if x<t[0] else 3;t[side]=insert(t[side],x)
        return t
    def remove(t,x):
        if t is None:return None
        if x!=t[0]:
            side=2 if x<t[0] else 3;t[side]=remove(t[side],x);return t
        t[1]-=1
        if t[1]:return t
        if t[2] is None:return t[3]
        if t[3] is None:return t[2]
        s=t[3]
        while s[2] is not None:s=s[2]
        t[0],t[1]=s[0],s[1];s[1]=1;t[3]=remove(t[3],s[0]);return t
    def preorder(t):return [] if t is None else [t[0]]+preorder(t[2])+preorder(t[3])
    for _ in range(m):
        t=next(it)
        if t==0:out.append(' '.join(map(str,preorder(root))))
        elif t==1:root=insert(root,next(it))
        else:root=remove(root,next(it))
    return ''.join(s+'\n' for s in out)
def read_tree(text):
    n,r,*data=map(int,text.split());adj=[[] for _ in range(n+1)]
    for u,v in zip(data[::2],data[1::2]):adj[u].append(v);adj[v].append(u)
    parent=[0]*(n+1);order=[r]
    for u in order:
        for v in adj[u]:
            if v!=parent[u]:parent[v]=u;order.append(v)
    return n,parent,order
def heap_labels(text):
    n,parent,_=read_tree(text);best=None;a=[0]*(n+1)
    def go(t):
        nonlocal best
        if t>n:
            b=tuple(a[1:])
            if best is None or b>best:best=b
            return
        for u in range(1,n+1):
            if a[u]==0 and (parent[u]==0 or a[parent[u]]):a[u]=t;go(t+1);a[u]=0
    go(1);return best
def rank(a):
    v=sum(sum(x<a[i] for x in a[i+1:])*math.factorial(len(a)-i-1) for i in range(len(a)))
    return f'{v%100000007} {v%100000009}\n'
def heap(text):return rank(heap_labels(text))
def byte(text):
    it=iter(text.split());n,m,k=[int(next(it)) for _ in range(3)];labels=[next(it) for _ in range(n)];starts=[int(next(it))-1 for _ in range(k)];adj=[[] for _ in range(n)]
    for _ in range(m):u=int(next(it))-1;v=int(next(it))-1;s=next(it);adj[u].append((v,s))
    best=None
    def visit(u,path,text):
        nonlocal best
        if u==0:
            key=(len(text),text,tuple(reversed(path)))
            if best is None or key<best:best=key
            return
        for v,s in adj[u]:
            if v not in path and (best is None or len(text)+len(s)+len(labels[v])<=best[0]):visit(v,path+[v],text+s+labels[v])
    for s in starts:visit(s,[s],labels[s])
    return best[1]+'\n'+' '.join(str(x+1) for x in reversed(best[2]))+'\n'
ORACLES=dict(zip([s for _,s in PROBLEMS],[digits,queue,bst,heap,byte]))
def check_output(slug,text,output,expected=None):
    want=ORACLES[slug](text) if expected is None else expected
    if slug=='exact-search-tree':assert [x.split() for x in output.splitlines()]==[x.split() for x in want.splitlines()],(text,want,output)
    else:assert output.split()==want.split(),(slug,text[:2000],want[:2000],output[:2000])
