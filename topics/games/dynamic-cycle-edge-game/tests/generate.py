"""Deterministic standalone test recipes with verifiable expected results."""
from pathlib import Path
import argparse,collections,heapq,io,json,random,subprocess

def result(n,minimum,first,last):
    if not n:return 0
    return int(minimum>0 and n%2==1 or first%2==1 or (n-1-last)%2==1)
def literal(a):
    if not a:return 0
    v=min(a);return result(len(a),v,a.index(v),len(a)-1-a[::-1].index(v))
def make_case(c):
    mode=c['mode'];n=c['n'];q=c['q'];r=random.Random(c['seed'])
    a=[2,5,3,0] if mode=='sample' else [2,2,2,3] if mode=='counter' else [c.get('value',2)]*n if mode in ['uniform','positive'] or c.get('zero') else [r.randrange(101) for _ in range(n)]
    if c.get('zero'):a=[0]*n
    out=[f'{n} {q}',' '.join(map(str,a))];answers=[str(literal(a))]
    if mode in ['change','append','pop']:
        lo=[(v,i) for i,v in enumerate(a)];hi=[(v,-i) for i,v in enumerate(a)];heapq.heapify(lo);heapq.heapify(hi);left=0;right=n-1
        for j in range(q):
            if mode=='change':
                p=r.randrange(n);v=r.randrange(101);a[p]=v;out.append(f'1 {p+1} {v}');heapq.heappush(lo,(v,p));heapq.heappush(hi,(v,-p))
            elif mode=='append':
                v=r.randrange(101);p=len(a);a.append(v);n+=1;right+=1;out.append(f'2 {n} {v}');heapq.heappush(lo,(v,p));heapq.heappush(hi,(v,-p))
            else:
                if j%2:out.append(f'3 {n}');right-=1
                else:out.append('3 1');left+=1
                n-=1
            if not n:answers.append('0');continue
            while lo and (not left<=lo[0][1]<=right or a[lo[0][1]]!=lo[0][0]):heapq.heappop(lo)
            while hi and (not left<=-hi[0][1]<=right or a[-hi[0][1]]!=hi[0][0]):heapq.heappop(hi)
            answers.append(str(result(n,lo[0][0],lo[0][1]-left,-hi[0][1]-left)))
    elif mode=='uniform':
        for j in range(q):
            op=r.choice([1,2,3]) if n else 2;p=r.randint(1,n+(op==2))
            if op==1:out.append(f'1 {p} 2')
            elif op==2:out.append(f'2 {p} 2');n+=1
            else:out.append(f'3 {p}');n-=1
            answers.append(str(n%2))
    else:
        for j in range(q):
            op=r.choice([1,2,3]) if a else 2
            if len(a)>80:op=3
            p=r.randrange(len(a)+(op==2));v=r.randrange(4)
            if op==1:a[p]=v;out.append(f'1 {p+1} {v}')
            elif op==2:a.insert(p,v);out.append(f'2 {p+1} {v}')
            else:a.pop(p);out.append(f'3 {p+1}')
            answers.append(str(literal(a)))
    return '\n'.join(out)+'\n','\n'.join(answers)+'\n'
def validate(text,group=None):
    stream=io.StringIO(text);n,q=map(int,stream.readline().split());assert 0<=n<=100000 and 0<=q<=100000
    a=list(map(int,stream.readline().split()));assert len(a)==n and all(0<=v<=100 for v in a)
    for _ in range(q):
        z=list(map(int,stream.readline().split()));assert z and z[0] in [1,2,3]
        if z[0]==1:assert len(z)==3 and 1<=z[1]<=n and 0<=z[2]<=100
        elif z[0]==2:assert len(z)==3 and 1<=z[1]<=n+1 and 0<=z[2]<=100;n+=1
        else:assert len(z)==2 and 1<=z[1]<=n;n-=1
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
