"""Deterministic standalone recipes and independent expected results."""
from pathlib import Path
import argparse,functools,io,itertools,json,math,random,subprocess

FLOAT=True
def score(n,m,A,layout,soil,decimal=False):
    if decimal:
        from decimal import Decimal,localcontext
        num=Decimal
    else:num=float
    s=num(str(soil));effects=[]
    for i in range(n*m):
        neighbors=sum(p=='N' and i!=j and abs(i//m-j//m)<=1 and abs(i%m-j%m)<=1 for j,p in enumerate(layout));effects.append(s*(1+num('.2')*neighbors*s))
    cursor=num(1);cps=num(1);cpc=num(0);cps_loss=num(1);cpc_loss=num(1);bloom=num(0)
    for p,f in zip(layout,effects):
        if p=='B':cps+=num('.01')*f
        if p=='T':cpc+=num('.02')*f
        if p=='W':bloom+=num('.002')*f
        if p=='D':cps+=num('.03')*f;cpc_loss*=1-num('.05')*f
        if p=='G':cursor+=num('.01')*f;cpc+=num('.04')*f;cps_loss*=1-num('.01')*f
    milk=num('.04')*A*num('1.05')**2*num('1.1')*bloom;kitty=num(1)
    for a,e in [('.05',1),('.1',2),('.115',1),('.125',2),('.15',2),('.175',2),('.2',5)]:kitty*=(1+num(a)*milk)**e
    return (num('.956')+num('.044')*cursor)*kitty*cps*cps_loss*cpc*cpc_loss
@functools.lru_cache(None)
def optimum(n,m,A,alphabet='BTWNG'):
    # Enumerate complete layouts (not the C++ mask/partial-sum traversal).
    best=-1;best_layout=None;best_soil=None
    for layout in itertools.product(alphabet,repeat=n*m):
        for soil in [1,1.25]:
            value=score(n,m,A,layout,soil)
            if value>best:best=value;best_layout=layout;best_soil=soil
    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec=60;return str(score(n,m,A,best_layout,best_soil,True)),''.join(best_layout),best_soil
def make_case(c):return f"{c['n']} {c['m']} {c['A']}\n",c['expected']+'\n'
def validate(text,group=None):
    v=list(map(int,text.split()));assert len(v)==3;n,m,A=v;assert n>=1 and m>=1 and n*m<=8 and 0<=A<=1000

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
