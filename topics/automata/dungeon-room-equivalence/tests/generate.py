"""Deterministic standalone test recipes with verifiable expected results."""
from pathlib import Path
import argparse,collections,heapq,io,json,random,subprocess

def simple_classes(rows):
    k=len(rows[0]);rows=[[0]*k]+rows;colors=[0]+[1]*(len(rows)-1)
    while True:
        ids={};after=[]
        for u,row in enumerate(rows):
            key=(u!=0,tuple(colors[v] for v in row))
            if key not in ids:ids[key]=len(ids)
            after.append(ids[key])
        if after==colors:return len(ids)-1
        colors=after
def make_case(c):
    n=c['n'];k=c['k'];mode=c['mode'];r=random.Random(c['seed']);out=[f'{n} {k}'];rows=[]
    for u in range(1,n+1):
        if mode=='chain':row=[u-1]*k
        elif mode=='closed':row=[r.randint(1,n) for _ in range(k)]
        elif mode=='zero':row=[0]*k
        elif mode=='levels':
            level=(u-1)%c['levels']+1;row=[max(0,level-j-1) for j in range(k)]
        else:row=[r.randrange(n+1) for _ in range(k)];rows.append(row)
        out.append(' '.join(map(str,row)))
    answer=n if mode=='chain' else 1 if mode in ['closed','zero'] else c['levels'] if mode=='levels' else simple_classes(rows)
    return '\n'.join(out)+'\n',f'{answer}\n'
def validate(text,group=None):
    stream=io.StringIO(text);n,k=map(int,stream.readline().split());assert 1<=n<=200000 and 1<=k<=26 and n*k<=2000000
    for _ in range(n):
        row=list(map(int,stream.readline().split()));assert len(row)==k and all(0<=v<=n for v in row)
    assert not stream.read().strip()

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
