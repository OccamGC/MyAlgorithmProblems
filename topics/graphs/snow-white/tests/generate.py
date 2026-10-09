"""Deterministic recipes with independent result checks."""
from pathlib import Path
import argparse,functools,io,itertools,json,math,random,subprocess

FLOAT=False
def parse(text):
    stream=io.StringIO(text);n,m=map(int,stream.readline().split());h=list(map(int,stream.readline().split()));edges=[tuple(int(x)-1 for x in stream.readline().split()) for _ in range(m)];assert not stream.read().strip();return n,m,h,edges
def validate(text,group=None):
    n,m,h,edges=parse(text);assert 1<=n<=500000 and 1<=m<=2000000 and len(h)==n and all(-10**9<=x<=10**9 for x in h)
    assert all(len(e)==2 and all(0<=x<n for x in e) and h[e[0]]>=h[e[1]] for e in edges)
def scc(n,edges):
    # Independent iterative Tarjan, in contrast to the reference's Kosaraju.
    graph=[[] for _ in range(n)]
    for u,v in edges:graph[u].append(v)
    discovery=[-1]*n;low=[0]*n;active=bytearray(n);stack=[];ids=[-1]*n;count=0;clock=0
    for root in range(n):
        if discovery[root]>=0:continue
        discovery[root]=low[root]=clock;clock+=1;stack.append(root);active[root]=1;frames=[(root,0)]
        while frames:
            u,j=frames[-1]
            if j<len(graph[u]):
                v=graph[u][j];frames[-1]=(u,j+1)
                if discovery[v]<0:
                    discovery[v]=low[v]=clock;clock+=1;stack.append(v);active[v]=1;frames.append((v,0))
                elif active[v]:low[u]=min(low[u],discovery[v])
            else:
                frames.pop()
                if frames:low[frames[-1][0]]=min(low[frames[-1][0]],low[u])
                if low[u]==discovery[u]:
                    while True:
                        v=stack.pop();active[v]=0;ids[v]=count
                        if v==u:break
                    count+=1
    return ids,count
def optimum(n,h,edges):
    ids,count=scc(n,edges)
    if count==1:return 0,0
    incoming=bytearray(count);outgoing=bytearray(count);level=sorted(set(h));index={x:i for i,x in enumerate(level)};diff=[0]*(len(level)+1);ch=[0]*count
    for u in range(n):ch[ids[u]]=h[u]
    for u,v in edges:
        if ids[u]!=ids[v]:incoming[ids[v]]=1;outgoing[ids[u]]=1
        if h[u]>h[v]:diff[index[h[v]]+1]+=1;diff[index[h[u]]+1]-=1
    active=0
    for i in range(1,len(level)):
        active+=diff[i]
        if active==0:return None
    counts={x:[0,0] for x in level}
    for u in range(count):counts[ch[u]][0]+=not incoming[u];counts[ch[u]][1]+=not outgoing[u]
    if len(level)==1:return 0,max(counts[level[0]])
    a,b=counts[level[0]];c,d=counts[level[-1]]
    return level[-1]-level[0],sum(max(a,b) for a,b in counts.values())+1-(b>a)-(c>d)
def check_output(text,output):
    try:
        n,m,h,edges=parse(text);want=optimum(n,h,edges);v=list(map(int,output.split()))
        if want is None:return v==[-1]
        cost,k=v[:2]
        if (cost,k)!=want or len(v)!=2+2*k:return False
        added=[(v[i]-1,v[i+1]-1) for i in range(2,len(v),2)]
        if not all(0<=u<n and 0<=w<n and u!=w and h[u]<=h[w] for u,w in added):return False
        return sum(h[w]-h[u] for u,w in added)==cost and scc(n,edges+added)[1]==1
    except (ValueError,IndexError,AssertionError):return False
def make_case(c):
    mode=c['mode'];rng=random.Random(c['seed'])
    if mode=='literal':return c['input'],''
    n=c['n'];m=c.get('m',n-1)
    if mode=='chain':h=[i*4000-10**9 for i in range(n)];edges=[(i,i-1) for i in range(1,n)]
    elif mode=='same':h=[10**9]*n;edges=[(i,i-1) for i in range(1,n)]
    elif mode=='isolates':h=[0]*n;edges=[(0,0)]
    elif mode=='cycle':h=[-10**9]*n;edges=[(i,(i+1)%n) for i in range(n)]
    elif mode=='gap':h=[i for i in range(n)];edges=[(i,i-1) for i in range(1,n) if i!=n//2]
    elif mode=='layers':
        h=[(i%5)*500000000-10**9 for i in range(n)];edges=[(4,0)]
        while len(edges)<m:
            u=rng.randrange(n);v=rng.randrange(n)
            if h[u]<h[v]:u,v=v,u
            edges.append((u,v))
    else:raise ValueError(mode)
    while len(edges)<m:edges.append(edges[rng.randrange(len(edges))])
    return f'{n} {len(edges)}\n'+' '.join(map(str,h))+'\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges),''

def generate(c):return make_case(c)[0]
def matches(actual,expected):
    if FLOAT:
        import math
        try:
            tokens=actual.split();x=float(tokens[0]);y=float(expected)
            return len(tokens)==1 and math.isfinite(x) and abs(x-y)<=1e-9*max(1,abs(y))
        except (ValueError,IndexError):return False
    return actual.split()==expected.split()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'));p.add_argument('--out-dir',type=Path,required=True);p.add_argument('--case',action='append');p.add_argument('--std',type=Path);a=p.parse_args()
    plan=json.loads(a.plan.read_text('utf-8'));ids={c['id'] for c in plan['cases']}
    if a.case and not set(a.case)<=ids:p.error('unknown case ID')
    a.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if a.case and c['id'] not in a.case:continue
        text,expected=make_case(c);validate(text,c['group']);f=a.out_dir/(c['id']+'.in');f.write_text(text,'utf-8',newline='\n')
        if a.std:
            out=subprocess.check_output([str(a.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n');assert check_output(text,out.decode()),c['id'];f.with_suffix('.out').write_bytes(out)
if __name__=='__main__':main()
