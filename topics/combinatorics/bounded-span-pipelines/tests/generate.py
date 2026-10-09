"""Deterministic standalone recipes and independent expected results."""
from pathlib import Path
import argparse,functools,io,itertools,json,math,random,subprocess

FLOAT=False
MOD=998244353
def free_count(length,k):
    small=[1]
    for n in range(1,k):small.append((small[-1]+sum(2*small[j]*small[n-j-2] for j in range(n-1)))%MOD)
    f=[1]
    for r in range(1,length+1):f.append((f[-1]+sum(2*f[r-span-1]*small[span-1] for span in range(1,min(k,r-1)+1)))%MOD)
    return f[-1]
def literal(n,k,pipes):
    partner={};weights={}
    for u,v,e in pipes:partner[u]=v;partner[v]=u;weights[u]=weights[v]=2-e
    def visit(left,chosen):
        if not left:return math.prod(weights.get(u,2) for u,v in chosen)
        u=left[0];total=visit(left[1:],chosen) if u not in partner else 0
        for v in left[1:]:
            if v-u>k:break
            if partner.get(u,v)!=v or partner.get(v,u)!=u:continue
            if any(a<u<b<v or u<a<v<b for a,b in chosen):continue
            total+=visit([x for x in left[1:] if x!=v],chosen+[(u,v)])
        return total
    return visit(list(range(1,n+1)),[])%MOD
def make_case(c):
    n=c['n'];k=c['k'];mode=c['mode'];rng=random.Random(c['seed'])
    if mode=='literal':pipes=[tuple(p) for p in c['pipes']];answer=literal(n,k,pipes)
    elif mode=='paired':
        pipes=[(i,i+1,rng.randrange(2)) for i in range(1,n,2)];answer=pow(2,sum(1-e for u,v,e in pipes),MOD)
    elif mode=='tiles':
        pipes=[(s,s+k,c['fixed']) for s in range(1,n-k+1,k+1)];block=(2-c['fixed'])*free_count(k-1,k)%MOD;answer=pow(block,len(pipes),MOD)*free_count(n%(k+1),k)%MOD
    elif mode=='free':pipes=[(1,2,1)];answer=free_count(n-2,k)
    return f'{n} {k} {len(pipes)}\n'+''.join(f'{u} {v} {e}\n' for u,v,e in pipes),f'{answer}\n'
def validate(text,group=None):
    stream=io.StringIO(text);n,k,m=map(int,stream.readline().split());assert 2<=n<=1000000 and 1<=k<=18 and 1<=m<=n//2
    # With m>=1, distinct endpoint heights make k=1 unrealizable.
    assert k>=2;used=set();intervals=[]
    for _ in range(m):
        row=list(map(int,stream.readline().split()));assert len(row)==3;u,v,e=row;assert 1<=u<=n and 1<=v<=n and u!=v and abs(u-v)<=k and e in [0,1] and u not in used and v not in used;used.update([u,v]);intervals.append((min(u,v),max(u,v)))
    assert not stream.read().strip();stack=[]
    for l,r in sorted(intervals):
        while stack and l>stack[-1]:stack.pop()
        assert not stack or r<stack[-1];stack.append(r)

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
