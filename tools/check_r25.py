"""Independent input validation and mathematical checks for R25."""
from array import array
from functools import lru_cache
import itertools

PROBLEMS=[('optimization','postal-facilities'),('graphs','downhill-routes'),('dynamic-programming','energy-limited-routes'),('data-structures','little-y-segment-tree'),('trees','ancestor-depth-counts')]
VARIANTS={s:['std','alternative'] if s in ['postal-facilities','little-y-segment-tree','ancestor-depth-counts'] else ['std'] for _,s in PROBLEMS}
VARIANTS['little-y-segment-tree'].append('alternative-binary-lifting')

def validate(slug,text,group=None):
    a=list(map(int,text.split()))
    if slug=='postal-facilities':
        n,m=a[:2];assert 1<=n<=2000 and 1<=m<=min(1000,n) and len(a)==n+2 and all(0<=x<=10**8 for x in a[2:])
        return dict(n=n,m=m)
    if slug in ['downhill-routes','energy-limited-routes']:
        n,m=a[:2];shift=2 if slug=='downhill-routes' else 3
        assert 0<=n<=100000 and 0<=m<=100000 and len(a)==shift+n+2*m
        if shift==3:assert 0<=a[2]<=30
        if group==1 and slug=='downhill-routes':assert n<=300 and m<=300
        assert all(abs(x)<=100000 for x in a[shift:shift+n]) and all(1<=x<=n for x in a[shift+n:])
        return dict(n=n,m=m,**(dict(energy=a[2]) if shift==3 else {}))
    if slug=='little-y-segment-tree':
        n,m=a[:2];assert 1<=n<=500000 and 1<=m<=500000 and len(a)==n+2+2*m
        assert all(0<=x<=10**9 for x in a[2:n+2])
        assert all(1<=l<=r<=n for l,r in zip(a[n+2::2],a[n+3::2]))
        return dict(n=n,m=m)
    n=a[0];assert 1<=n<=2000000 and len(a)==n
    p=[0,0]+a[1:];assert all(1<=x<=n for x in p[2:])
    seen=bytearray(n+1);seen[1]=2
    for start in range(2,n+1):
        u=start
        while seen[u]==0:seen[u]=1;u=p[u]
        assert seen[u]==2,'parent cycle'
        u=start
        while seen[u]==1:seen[u]=2;u=p[u]
    return dict(n=n)

def postal_naive(text):
    n,m,*x=map(int,text.split());x.sort();prev=[0]+[10**30]*n
    for k in range(m):
        cur=[10**30]*(n+1)
        for r in range(k+1,n+1):
            cur[r]=min(prev[l]+sum(abs(y-x[(l+r-1)//2]) for y in x[l:r]) for l in range(k,r))
        prev=cur
    return str(prev[n])+'\n'

def postal(text):
    # SMAWK, independently of the divide-and-conquer implementations.
    n,m,*x=map(int,text.split());x.sort();p=[0]+list(itertools.accumulate(x));inf=10**30
    prev=[0]+[inf]*n
    for k in range(1,m+1):
        def value(r,l):
            if l>=r:return inf
            mid=(l+r-1)//2
            return prev[l]+x[mid]*(2*mid-l-r+2)+p[r]+p[l]-2*p[mid+1]
        def smawk(rows,cols):
            if not rows:return {}
            reduced=[]
            for c in cols:
                while reduced and value(rows[len(reduced)-1],c)<value(rows[len(reduced)-1],reduced[-1]):reduced.pop()
                if len(reduced)<len(rows):reduced.append(c)
            answer=smawk(rows[1::2],reduced);index={c:i for i,c in enumerate(reduced)};lo=0
            for i in range(0,len(rows),2):
                hi=index[answer[rows[i+1]]] if i+1<len(rows) else len(reduced)-1
                row=rows[i];best=lo
                for j in range(lo+1,hi+1):
                    if value(row,reduced[j])<value(row,reduced[best]):best=j
                answer[row]=reduced[best];lo=hi
            return answer
        choices=smawk(list(range(k,n+1)),list(range(k-1,n)))
        cur=[inf]*(n+1)
        for r,l in choices.items():cur[r]=value(r,l)
        prev=cur
    return str(prev[n])+'\n'

def graph(text,energy=False):
    a=list(map(int,text.split()));n,m=a[:2];start=3 if energy else 2
    h=a[start:start+n];edges=list(zip(a[start+n::2],a[start+n+1::2]))
    return n,m,(a[2] if energy else 0),h,[(u-1,v-1) for u,v in edges]

def downhill(text):
    n,m,e,h,edges=graph(text);adj=[[] for _ in range(n)]
    for u,v in edges:
        if h[u]>h[v]:adj[u].append(v)
        if h[v]>h[u]:adj[v].append(u)
    ways=[1]*n
    for u in sorted(range(n),key=h.__getitem__):ways[u]=(1+sum(ways[v] for v in adj[u]))%998246353
    return str(sum(ways)%998246353)+'\n'

def energy(text):
    # Forward propagation by exact energy spent, starting once at each vertex.
    n,m,budget,h,edges=graph(text,True);adj=[set() for _ in range(n)];mod=998244353
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    dp=[array('I',[0])*n for _ in range(budget+1)];dp[0]=array('I',[1])*n
    order=sorted(range(n),key=h.__getitem__,reverse=True)
    for spent in range(budget+1):
        for u in order:
            count=dp[spent][u]
            for v in adj[u]:
                cost=0 if h[v]<h[u] else 1 if h[v]==h[u] else 2
                if spent+cost<=budget:dp[spent+cost][v]=(dp[spent+cost][v]+count)%mod
    return str(sum(map(sum,dp))%mod)+'\n'

def stack_naive(text):
    a=list(map(int,text.split()));n,m=a[:2];x=a[2:2+n];answers=[]
    for l,r in zip(a[2+n::2],a[3+n::2]):
        s=[]
        for v in x[l-1:r]:
            while s and s[-1]<=v:s.pop()
            s.append(v)
        answers.append(len(s))
    return ''.join(str(x)+'\n' for x in answers)

def stack(text):
    # A query follows previous-strictly-greater links from its right endpoint.
    a=list(map(int,text.split()));n,m=a[:2];x=[10**10]+a[2:2+n];prev=array('I',[0])*(n+1);s=[0]
    for i in range(1,n+1):
        while x[s[-1]]<=x[i]:s.pop()
        prev[i]=s[-1];s.append(i)
    jump=[prev]
    for _ in range(1,n.bit_length()):
        p=jump[-1];jump.append(array('I',(p[p[i]] for i in range(n+1))))
    answer=[]
    for l,r in zip(a[2+n::2],a[3+n::2]):
        count=1
        for k in range(len(jump)-1,-1,-1):
            if jump[k][r]>=l:r=jump[k][r];count+=1<<k
        answer.append(str(count))
    return '\n'.join(answer)+'\n'

def tree_small(text):
    a=list(map(int,text.split()));n=a[0];p=[0,0]+a[1:];anc=[set() for _ in range(n+1)];depth=[0]*(n+1)
    for u in range(1,n+1):
        v=u
        while v:anc[u].add(v);v=p[v]
        depth[u]=len(anc[u])-1
    rows=[]
    for u in range(1,n+1):
        row=[0,0,0]
        for v in range(1,n+1):row[(depth[v]>depth[u])-(depth[v]<depth[u])+1]+=len(anc[u]&anc[v])
        rows.append(' '.join(map(str,row)))
    return '\n'.join(rows)+'\n'

ORACLES=dict(zip([s for _,s in PROBLEMS],[postal,downhill,energy,stack,tree_small]))
def check_output(slug,text,output,expected=None):
    assert output.split()==(expected if expected is not None else ORACLES[slug](text)).split(),(slug,text[:100],output[:100],str(expected)[:100])
