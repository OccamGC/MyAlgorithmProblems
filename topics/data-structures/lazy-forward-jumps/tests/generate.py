"""Deterministic standalone test recipes with verifiable expected results."""
from pathlib import Path
import argparse,collections,heapq,io,json,random,subprocess

def make_case(c):
    n=c['n'];q=c['q'];group=c['group'];typ=1 if group<=2 else 2;r=random.Random(c['seed']);out=[f'{n} {q} {typ}',' '.join(['1']*(n+1))];answers=[];odd=even=total=0;current=1;a=min(n,24);batches=c.get('batches',100);length=max(1,q//batches);base=0
    for i in range(q):
        if group==1:
            update=i%3==0;position=a if update else (1000000000 if i%97==0 else 0)
            if update:current=[1,2,1000000000][(i//3)%3];value=current
        elif group in [2,3]:
            local=i%length;count=min(1000,length//2);update=local<count if group==2 else local<length-count
            position=r.randrange(n+1) if update or local%17 else 0;value=1
        else:
            if i%length==0:base=r.randrange(max(1,n-499))
            position=r.randint(base,min(n,base+500));update=bool(r.randrange(2));value=1
        if update:out.append(f'1 {position} {value}')
        else:
            out.append(f'2 {position}')
            answer=0 if position>n else n-position+1
            if group==1 and position<=a:answer=a-position+1+max(0,n-a-current+1)
            if (i+1)%2:odd^=answer
            else:even^=answer
            total+=answer
            if typ==2:answers.append(str(answer))
    expected='\n'.join(answers)+('\n' if answers else '') if typ==2 else f'{odd} {even} {total}\n'
    return '\n'.join(out)+'\n',expected
def validate(text,group=None):
    stream=io.StringIO(text);n,q,typ=map(int,stream.readline().split());assert 1<=n<=300000 and 0<=q<=6000000 and typ in [1,2]
    a=list(map(int,stream.readline().split()));assert len(a)==n+1 and all(1<=x<=1000000000 for x in a)
    updates=queries=sum_a=0;largest={1:[],2:[]};last=0;run=0;segments=0;low=high=None
    def finish(t,count):
        if not t:return
        heapq.heappush(largest[t],count)
        if len(largest[t])>100:heapq.heappop(largest[t])
    for _ in range(q):
        z=list(map(int,stream.readline().split()));assert z and z[0] in [1,2];t=z[0]
        if t==1:assert len(z)==3 and 0<=z[1]<=n and 1<=z[2]<=1000000000;updates+=1;sum_a+=z[1]
        else:assert len(z)==2 and 0<=z[1]<=1000000000;queries+=1
        if t!=last:finish(last,run);last=t;run=0
        run+=1;position=z[1]
        if low is None or max(high,position)-min(low,position)>500:segments+=1;low=high=position
        else:low=min(low,position);high=max(high,position)
    finish(last,run);assert not stream.read().strip()
    if group==1:assert typ==1 and sum_a<=50000000
    if group==2:assert typ==1 and updates<=100000 and updates-sum(largest[1])<=10
    if group==3:assert typ==2 and queries<=100000 and queries-sum(largest[2])<=10
    if group==4:assert typ==2 and q<=1000000 and segments<=100

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
