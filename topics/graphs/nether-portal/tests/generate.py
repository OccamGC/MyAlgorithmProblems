"""Deterministic standalone recipes and independent expected results."""
from pathlib import Path
import argparse,functools,io,itertools,json,math,random,subprocess

FLOAT=False
def literal(text):
    rows=[list(map(int,r.split())) for r in text.splitlines()];n,m=rows[0];sw,sx,sy,tw,tx,ty=rows[1];steps=rows[2];p=[(sw,sx,sy,sw,sx,sy,-10**30,0)]+[tuple(r) for r in rows[3:]]+[(tw,tx,ty,tw,tx,ty,-10**30,0)];reachable={0}
    for _ in range(n+2):
        for u in list(reachable):
            for v in range(n+2):
                if p[u][3]==p[v][0]:reachable.add(v)
    if n+1 not in reachable:return 'YouNeedOpPermission'
    if steps[tw-1]<0:return 'NegativeInfinity'
    d=[10**30]*(n+2);d[0]=0
    for iteration in range(1000000):
        before=d.copy()
        for u in range(n+2):
            if before[u]==10**30:continue
            for v in range(n+2):
                if p[u][3]!=p[v][0]:continue
                candidate=p[v][6] if steps[p[u][3]-1]<0 else max(p[v][6],before[u]+p[u][7]+steps[p[u][3]-1]*(abs(p[u][4]-p[v][1])+abs(p[u][5]-p[v][2])))
                d[v]=min(d[v],candidate)
        if d==before:return str(d[-1])
    raise AssertionError('small oracle iteration bound exceeded')
def make_case(c):
    mode=c['mode'];rng=random.Random(c['seed'])
    if mode=='literal':text=c['input'];return text,literal(text)+'\n'
    if mode=='random':
        n=20;m=5;point=lambda:(rng.randint(1,m),rng.randint(-3,3),rng.randint(-3,3));a=point();b=point();steps=[rng.randint(-2,3) for _ in range(m)];portals=[point()+point()+(rng.randint(-10,10),rng.randint(-10,10)) for _ in range(n)]
    else:
        n=3000;m=200;a=(1,0,0);b=(200,0,0);steps=[0]*m;portals=[]
        for i in range(n):
            w=i%200+1;dest=w%200+1;delta=0;opening=-10000
            if mode=='negative':delta=-1
            elif mode=='slow-cycle':delta=-1 if w==200 else 0
            elif mode=='positive':delta=10000;opening=10000
            elif mode=='unreachable':dest=1;steps[-1]=-1
            elif mode=='infinity':steps[-1]=-1
            elif mode=='reset':steps[99]=-1;delta=123;opening=-10000
            elif mode=='coordinates':steps=[10]*m;delta=0;opening=-10000
            portals.append((w,-10000 if mode=='coordinates' else 0,0,dest,10000 if mode=='coordinates' else 0,0,opening,delta))
        if mode=='coordinates':a=(1,-10000,0);b=(200,10000,0)
    text=f'{n} {m}\n'+' '.join(map(str,a+b))+'\n'+' '.join(map(str,steps))+'\n'+''.join(' '.join(map(str,p))+'\n' for p in portals)
    if mode=='random':answer=literal(text)
    else:answer={'negative':'-10001','slow-cycle':'-10000','positive':'2000000','unreachable':'YouNeedOpPermission','infinity':'NegativeInfinity','reset':str(-10000+100*123),'coordinates':str(198*200000)}[mode]
    return text,answer+'\n'
def validate(text,group=None):
    stream=io.StringIO(text);n,m=map(int,stream.readline().split());assert 0<=n<=3000 and 1<=m<=200
    positions=list(map(int,stream.readline().split()));assert len(positions)==6
    def point(w,x,y):assert 1<=w<=m and -10000<=x<=10000 and -10000<=y<=10000
    point(*positions[:3]);point(*positions[3:]);steps=list(map(int,stream.readline().split()));assert len(steps)==m and all(-10<=t<=10 for t in steps);counts=[0]*(m+1)
    for _ in range(n):
        row=list(map(int,stream.readline().split()));assert len(row)==8;point(*row[:3]);point(*row[3:6]);assert all(-10000<=v<=10000 for v in row[6:]);counts[row[0]]+=1
    assert max(counts)<=50 and not stream.read().strip()

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
