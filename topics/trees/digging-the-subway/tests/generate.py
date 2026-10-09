"""Deterministic recipes with independent result checks."""
from pathlib import Path
import argparse,functools,io,itertools,json,math,random,subprocess

FLOAT=False
def parse(text):
    a=list(map(int,text.split()));n,k=a[:2];marks=a[2:2+k];edges=[tuple(a[i:i+3]) for i in range(2+k,len(a),3)];return n,marks,edges
def validate(text,group=None):
    n,marks,edges=parse(text);assert 2<=n<=1000 and 1<=len(marks)<=n and len(set(marks))==len(marks) and all(1<=u<=n for u in marks) and len(edges)==n-1
    parent=list(range(n+1))
    def find(u):
        while u!=parent[u]:parent[u]=parent[parent[u]];u=parent[u]
        return u
    for e in edges:
        assert len(e)==3;u,v,w=e;assert 1<=u<=n and 1<=v<=n and 1<=w<=100 and find(u)!=find(v);parent[find(u)]=find(v)
def literal(n,marks,edges):
    # Enumerate unions of actual permitted paths, without the subtree lemma.
    graph=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):graph[u-1].append((v-1,i));graph[v-1].append((u-1,i))
    paths={0}
    for root in marks:
        stack=[(root-1,-1,0)]
        while stack:
            u,p,mask=stack.pop();paths.add(mask)
            stack.extend((v,u,mask|(1<<e)) for v,e in graph[u] if v!=p)
    states={0};full=(1<<(n-1))-1;values=[]
    while full not in states:
        states={a|b for a in states for b in paths};values.append(max(sum(w for i,(_,_,w) in enumerate(edges) if a>>i&1) for a in states))
    return values
def rooted(n,root,edges):
    # Independent single-source oracle: merge concave marginal-gain lists.
    graph=[[] for _ in range(n)]
    for u,v,w in edges:graph[u-1].append((v-1,w));graph[v-1].append((u-1,w))
    parent=[-1]*n;order=[root-1];lists=[[] for _ in range(n)]
    for u in order:
        for v,w in graph[u]:
            if v!=parent[u]:parent[v]=u;order.append(v)
    for u in reversed(order):
        for v,w in graph[u]:
            if v==parent[u]:continue
            a=lists[v] or [0];a[0]+=w;lists[u].extend(a)
        lists[u].sort(reverse=True)
    return list(itertools.accumulate(lists[root-1]))
def star(n,marks,edges):
    yes=sorted((w for u,v,w in edges if v in marks),reverse=True);no=sorted((w for u,v,w in edges if v not in marks),reverse=True);a=[0]+list(itertools.accumulate(yes));b=[0]+list(itertools.accumulate(no));ans=[];total=sum(w for u,v,w in edges)
    for i in range(1,n):
        best=0
        for y in range(min(len(no),i)+1):
            x=min(len(yes),2*i-y)
            if 1 not in marks and x==0:continue
            best=max(best,a[x]+b[y])
        ans.append(best)
        if best==total:break
    return ans
def make_case(c):
    rng=random.Random(c['seed']);mode=c['mode']
    if mode=='literal':text=c['input'];n,marks,edges=parse(text);ans=literal(n,marks,edges)
    else:
        n=c['n'];marks=c.get('marks',[1]);edges=[]
        if mode=='star':
            marks=[v for v in range(2,n+1) if v%2==0] if c.get('mixed') else list(range(2,n+1));edges=[(1,v,rng.randint(1,100)) for v in range(2,n+1)];ans=star(n,set(marks),edges)
        else:
            for v in range(2,n+1):
                u=v-1 if mode=='chain' else v//2 if mode=='binary' else rng.randrange(1,v)
                edges.append((u,v,rng.randint(1,100)))
            ans=rooted(n,marks[0],edges)
        text=f'{n} {len(marks)}\n'+' '.join(map(str,marks))+'\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)
    return text,str(len(ans))+'\n'+'\n'.join(map(str,ans))+'\n'

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
            out=subprocess.check_output([str(a.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n');assert matches(out.decode(),expected),c['id'];f.with_suffix('.out').write_bytes(out)
if __name__=='__main__':main()
