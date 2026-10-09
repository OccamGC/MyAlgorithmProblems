"""Deterministic data, exact small Fraction oracle, and independent histogram checks."""
from pathlib import Path
from fractions import Fraction
import argparse,io,itertools,json,random,subprocess
MOD=1000000007
SCALE=232792560
def parse(text):
    stream=io.StringIO(text);n=int(stream.readline());rows=[tuple(map(int,stream.readline().split())) for _ in range(n)];assert not stream.read().strip();return n,rows
def validate(text,group=None):
    n,rows=parse(text);assert 1<=n<=1000000 and len(rows)==n and all(len(row)==2 and 1<=row[0]<=20 and 1<=row[1]<=1000000 for row in rows) and rows[0][0]==1
def residue(x):
    x=Fraction(x);return x.numerator%MOD*pow(x.denominator,-1,MOD)%MOD
def literal(rows):
    # Expand actual people, use exact rationals, then evaluate each statistic.
    initial=Fraction(rows[0][1]);a=initial;others=[]
    for v in sorted(Fraction(m,p) for p,m in rows[1:] for _ in range(p)):
        if v>a:a=(a+v)/2;others.append(a)
        else:others.append(v)
    if not others:return [residue(a),0,0,1,1,1,1]
    b=min(others);outside=sum(others);q=len(others);gap=abs(a-outside) if q==1 else max(a-b,outside-2*b,outside-a);strict=int(a*q>outside)
    return [residue(a),residue(gap),residue(a-b),1,strict,1,strict]
def histogram(rows):
    # Group by exact integer-scaled means, then sum contributions BACKWARD.
    initial=rows[0][1];counts={};total=0;q=0;low=None;high=None;has_lower=False
    for p,m in rows[1:]:
        v=m*(SCALE//p);counts[v]=counts.get(v,0)+p;total+=m;q+=p;low=v if low is None else min(low,v);high=v if high is None else max(high,v);has_lower|=v<initial*SCALE
    if q==0:return [initial,0,0,1,1,1,1]
    rich=high>initial*SCALE;b=Fraction(low,SCALE)
    if b>initial:b=(initial+b)/2
    tail=1;answer=0;invscale=pow(SCALE,-1,MOD)
    for v,p in sorted(counts.items(),reverse=True):
        if v<=initial*SCALE:break
        decay=pow((MOD+1)//2,p,MOD);answer=(answer+v%MOD*invscale%MOD*(1-decay)%MOD*tail)%MOD;tail=tail*decay%MOD
    answer=(answer+initial*tail)%MOD;outside=(total+initial-answer)%MOD
    if not rich:
        gap=abs(Fraction(initial-total)) if q==1 else max(Fraction(initial)-b,Fraction(total)-2*b,Fraction(total-initial));gap=residue(gap);strict=int(has_lower)
    elif q==1:gap=0;strict=0
    else:
        threshold=2*b;maximum=Fraction(high,SCALE)
        if maximum<=threshold:at_least=False
        elif maximum/2>=threshold:at_least=True
        else:
            # Used only for small recipes with an ambiguous branch.
            assert q<=10000,'provide a structural large-case branch certificate'
            a=Fraction(initial)
            for v,p in sorted(counts.items()):
                v=Fraction(v,SCALE)
                if v>initial:a=v+(a-v)/2**p
            at_least=a>=threshold
        gap=(outside-(2*residue(b) if at_least else answer))%MOD;strict=1
    return [answer,gap,(answer-residue(b))%MOD,1,strict,1,strict]
def make_case(c):
    mode=c['mode'];rng=random.Random(c['seed'])
    if mode=='literal':text=c['input'];n,rows=parse(text);return text,'\n'.join(map(str,literal(rows)))+'\n'
    n=c['n'];rows=[]
    if mode=='equal':rows=[(1,2)]+[(i%20+1,2*(i%20+1)) for i in range(1,n)]
    elif mode=='poor':rows=[(1,1000000)]+[(rng.randint(1,20),rng.randint(1,1000000)) for _ in range(n-1)]
    elif mode=='same-rich':rows=[(1,1)]+[(20,60)]*(n-1)
    elif mode=='near':rows=[(1,3),(1,2)]+[(20,80)]*(n-2)
    elif mode=='exact':rows=[(1,3),(1,5)]+[(1,2)]*(n-2)
    elif mode=='random':rows=[(1,1)]+[(rng.randint(1,20),rng.randint(1,1000000)) for _ in range(n-1)]
    elif mode=='reverse':rows=[(1,1)]+[(i%20+1,1000000-i%1000000) for i in range(1,n)]
    else:raise ValueError(mode)
    text=str(n)+'\n'+''.join(f'{p} {m}\n' for p,m in rows)
    if mode=='exact':answer=[4,(sum(m for p,m in rows)-8)%MOD,2,1,1,1,1]
    else:answer=histogram(rows)
    return text,'\n'.join(map(str,answer))+'\n'
def generate(c):return make_case(c)[0]
def matches(actual,expected):
    try:
        values=list(map(int,actual.split()));return len(values)==7 and all(0<=x<MOD for x in values[:3]) and all(x in [0,1] for x in values[3:]) and values==list(map(int,expected.split()))
    except ValueError:return False
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'));p.add_argument('--out-dir',type=Path,required=True);p.add_argument('--case',action='append');p.add_argument('--std',type=Path);a=p.parse_args();plan=json.loads(a.plan.read_text('utf-8'));ids={c['id'] for c in plan['cases']}
    if a.case and not set(a.case)<=ids:p.error('unknown case ID')
    a.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if a.case and c['id'] not in a.case:continue
        text,expected=make_case(c);validate(text,c['group']);f=a.out_dir/(c['id']+'.in');f.write_text(text,'utf-8',newline='\n')
        if a.std:
            out=subprocess.check_output([str(a.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n');assert matches(out.decode(),expected),c['id'];f.with_suffix('.out').write_bytes(out)
if __name__=='__main__':main()
