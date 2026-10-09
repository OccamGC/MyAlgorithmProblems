"""Deterministic standalone test recipes with verifiable expected results."""
from pathlib import Path
import argparse,collections,heapq,io,json,random,subprocess

def literal(s):
    import itertools
    choices=[]
    for q in itertools.combinations(range(len(s)),4):
        if ''.join(s[i] for i in q)=='1212':choices.append(q)
    def conflict(a,b):return bool(set(a)&set(b)) or any(x<u<y<v or u<x<v<y for x,y in [(a[0],a[1]),(a[2],a[3])] for u,v in [(b[0],b[1]),(b[2],b[3])])
    masks=[sum(1<<j for j,b in enumerate(choices) if j<=i or conflict(a,b)) for i,a in enumerate(choices)]
    def exists(mask,count):
        if not count:return True
        if mask.bit_count()<count:return False
        while mask:
            bit=mask&-mask;i=bit.bit_length()-1;mask^=bit
            if exists(mask&~masks[i],count-1):return True
        return False
    for count in range(len(s)//4,-1,-1):
        if exists((1<<len(choices))-1,count):return count
def make_case(c):
    mode=c['mode']
    if mode=='literal':s=c['s'];answer=literal(s)
    elif mode=='ones':s='1'*c['n'];answer=0
    elif mode=='alternating':s='12'*(c['n']//2);answer=c['n']//4
    elif mode=='nested':s='1'*(c['n']//2)+'2'*(c['n']//2);answer=0
    elif mode=='chains':s='1'*c['a']+'2'*c['a']+'1'*c['b']+'2'*c['b'];answer=min(c['a'],c['b'])
    elif mode=='rooted':s='1'*c['a']+'12'*c['b']+'2'*c['a'];answer=c['b']//2
    elif mode=='unmatched':s='1'*c['a']+'12'*c['b'];answer=c['b']//2
    elif mode=='closing':s='2'*c['a']+'12'*c['b'];answer=c['b']//2
    return f'{len(s)}\n{s}\n',f'{answer}\n'
def validate(text,group=None):
    tokens=text.split();assert tokens;n=int(tokens[0]);assert 0<=n<=10000000
    if n==0:assert len(tokens)==1
    else:assert len(tokens)==2 and len(tokens[1])==n and set(tokens[1])<={'1','2'}

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
