"""Deterministic standalone test recipes with verifiable expected results."""
from pathlib import Path
import argparse,collections,heapq,io,json,random,subprocess

def solve_and_validate(text):
    stream=io.StringIO(text);n,m,k,t=map(int,stream.readline().split());assert 2<=n<=100000 and 1<=m<=100000 and 1<=k<=50000 and 0<=t<=100
    adj={};ds={1:0};heap=[];count=m;deleted=0;answers=[]
    def relax(v,value):
        if value<ds.get(v,t+1):ds[v]=value;heapq.heappush(heap,(value,v))
    def add(edge):
        u,v,x,y=edge;assert 1<=u<=n and 1<=v<=n and u!=v and 0<=x<=10000 and y in [0,1]
        adj.setdefault(u,[]).append((v,x));relax(v,ds.get(u,t+1)+x)
        if y:adj.setdefault(v,[]).append((u,x));relax(u,ds.get(v,t+1)+x)
    def propagate():
        while heap:
            cost,u=heapq.heappop(heap)
            if ds.get(u)!=cost:continue
            for v,x in adj.get(u,[]):relax(v,cost+x)
    for _ in range(m):
        edge=list(map(int,stream.readline().split()));assert len(edge)==4;add(edge)
    heapq.heappush(heap,(0,1));propagate()
    for c in range(1,k+1):
        raw=list(map(int,stream.readline().split()));assert len(raw)==4 and all(0<=v<2**30 for v in raw)
        key=(deleted+3)*(c+37)%998244353;add([v^key for v in raw]);count+=1;propagate();clear=ds.get(n,t+1)<=t;answers.append(str(int(clear)))
        if clear:deleted+=count;count=0;adj={};ds={1:0}
    assert not stream.read().strip();return answers
def validate(text,group=None):return solve_and_validate(text)
def small_distance(n,edges):
    ds=[10**20]*n;ds[0]=0
    for _ in range(n-1):
        changed=False
        for u,v,x,y in edges:
            if ds[u-1]+x<ds[v-1]:ds[v-1]=ds[u-1]+x;changed=True
            if y and ds[v-1]+x<ds[u-1]:ds[u-1]=ds[v-1]+x;changed=True
        if not changed:break
    return ds[-1]
def make_case(c):
    n=c['n'];m=c['m'];k=c['k'];t=c['threshold'];mode=c['mode'];rng=random.Random(c['seed']);initial=[];packets=[];flags=[]
    def edge():
        u,v=rng.sample(range(1,n+1),2);return (u,v,rng.choice([0,1,10000,rng.randrange(101)]),rng.randrange(2))
    for i in range(m):
        if mode=='random':initial.append(edge())
        elif mode=='decreases':initial.append((2,3+i%(n-3),0,0))
        elif mode=='initial' and i==0:initial.append((1,n,0,0))
        else:initial.append((1,2,10000,i%2))
    edges=initial.copy()
    for i in range(k):
        if mode=='random':packet=edge();edges.append(packet);clear=small_distance(n,edges)<=t
        elif mode=='decreases':packet=(1,2,max(0,100-i) if i<=100 else 10000,i%2);clear=False
        elif mode=='never':packet=(1,n,t+1,i%2);clear=False
        elif mode=='resets':packet=(1,n,0,i%2);clear=True
        elif mode=='initial':packet=(2,1,10000,0);clear=i==0
        else:
            j=i%3;packet=[(1,2,0,0),(2,3,0,1),(3,n,t,0)][j];clear=j==2
        packets.append(packet);flags.append(int(clear))
        if mode=='random' and clear:edges=[]
    out=[f'{n} {m} {k} {t}']+[' '.join(map(str,e)) for e in initial];count=m;deleted=0
    for i,(e,clear) in enumerate(zip(packets,flags),1):
        key=(deleted+3)*(i+37)%998244353;out.append(' '.join(str(v^key) for v in e));count+=1
        if clear:deleted+=count;count=0
    return '\n'.join(out)+'\n',' '.join(map(str,flags))+'\n'

def generate(c):return make_case(c)[0]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'));p.add_argument('--out-dir',type=Path,required=True);p.add_argument('--case',action='append');p.add_argument('--std',type=Path);a=p.parse_args()
    plan=json.loads(a.plan.read_text('utf-8'));ids={c['id'] for c in plan['cases']}
    if a.case and not set(a.case)<=ids:p.error('unknown case ID')
    a.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if a.case and c['id'] not in a.case:continue
        text,expected=make_case(c);validate(text,c['group']);f=a.out_dir/(c['id']+'.in');f.write_text(text,'utf-8',newline='\n')
        if a.std:
            out=subprocess.check_output([str(a.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n')
            assert out.split()==expected.encode().split(),c['id'];f.with_suffix('.out').write_bytes(out)
if __name__=='__main__':main()
