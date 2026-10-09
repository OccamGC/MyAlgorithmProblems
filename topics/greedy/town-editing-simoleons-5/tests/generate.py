"""Deterministic wealth-level recipes, exact fractions, and generic matrix checks."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import argparse
import io
import json
import random
import subprocess

MOD=1000000007
HALF=(MOD+1)//2


def parse(text):
    stream=io.StringIO(text);first=stream.readline().split()
    if len(first)!=1:raise ValueError('expected n')
    n=int(first[0])
    if not 2<=n<=1000000:raise ValueError('n out of range')
    rows=[];levels=set()
    for i in range(n):
        fields=stream.readline().split()
        if len(fields)!=2:raise ValueError('expected population and money')
        p,m=map(int,fields)
        if not (1<=p<=20 if i==0 else 0<=p<=1000000):raise ValueError('population out of range')
        if not 0<=m<=1000000000 or (p==0 and m!=0):raise ValueError('invalid money')
        if i==0:k,initial=p,m
        elif p and m*k>initial*p:
            d=gcd(m,p);levels.add((m//d,p//d))
            if len(levels)>3:raise ValueError('more than three richer wealth levels')
        rows.append((p,m))
    if n<k+len(levels)+1:raise ValueError('insufficient fixed slots')
    if stream.read().strip():raise ValueError('extra input')
    return rows


def validate(text,group=None):parse(text)


def as_text(rows):return str(len(rows))+'\n'+''.join(f'{p} {m}\n' for p,m in rows)


def groups(rows):
    k,initial=rows[0];counts={}
    for p,m in rows[1:]:
        if p and m*k>initial*p:
            d=gcd(m,p);key=(m//d,p//d);counts[key]=counts.get(key,0)+p
    return sorted(((F(a,b),count) for (a,b),count in counts.items()))


def exact(rows):
    k,m=rows[0];values=[F(m,k)]*k
    for value,count in groups(rows):
        for _ in range(count):
            v=value
            for i in range(k):values[i]=v=(values[i]+v)/2
    answer=sum(values)
    return answer.numerator%MOD*pow(answer.denominator,-1,MOD)%MOD


def matrix(rows):
    k,m=rows[0];values=[m*pow(k,-1,MOD)%MOD]*k
    b=[[0]*k for _ in range(k)]
    for col in range(k):
        carry=0
        for i in range(k):carry=(carry+(i==col))*HALF%MOD;b[i][col]=carry
    grouped=groups(rows)
    powers=[b]
    for _ in range(max((count.bit_length() for _,count in grouped),default=1)-1):
        a=powers[-1]
        powers.append([[sum(a[i][s]*a[s][j] for s in range(j,i+1))%MOD if j<=i else 0 for j in range(k)] for i in range(k)])
    for mean,count in grouped:
        v=mean.numerator*pow(mean.denominator,-1,MOD)%MOD;z=[(x-v)%MOD for x in values];bit=0
        while count:
            if count&1:z=[sum(powers[bit][i][j]*z[j] for j in range(i+1))%MOD for i in range(k)]
            count>>=1;bit+=1
        values=[(x+v)%MOD for x in z]
    return sum(values)%MOD


def rows_for(c):
    if c['mode']=='literal':return [tuple(row) for row in c['rows']]
    n,k,m=c['n'],c['k'],c['money'];rng=random.Random(c['seed']);rows=[(k,m)];mode=c['mode']
    if mode=='poor':return rows+[(rng.randint(20,1000000),rng.randrange(1000000001)) for _ in range(n-1)]
    if mode=='modulus':
        for value,total in [(1,MOD-1),(2,MOD),(3,MOD+1)]:
            while total:
                p=min(total,1000000);rows.append((p,p*value));total-=p
        rows += [(1000000,0)]*(n-len(rows));return rows
    if mode=='groups':
        levels=c['levels']
        for i in range(n-1):
            if c.get('mixed') and i%11==0:rows.append((0,0));continue
            if c.get('mixed') and i%11==1:rows.append((rng.randint(1,1000000),0));continue
            a,b=levels[rng.randrange(len(levels))];scale=rng.randint(1,min(1000000//b,1000000000//a));rows.append((b*scale,a*scale))
        return rows
    raise ValueError(mode)


def generate(c):return as_text(rows_for(c))


def make_case(c):
    rows=rows_for(c);answer=exact(rows) if c.get('oracle')=='exact' else matrix(rows)
    return as_text(rows),str(answer)+'\n'


def matches(actual,expected):
    try:
        a=list(map(int,actual.split()));return len(a)==1 and 0<=a[0]<MOD and a==list(map(int,expected.split()))
    except ValueError:return False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True);parser.add_argument('--case',action='append');parser.add_argument('--std',type=Path)
    args=parser.parse_args();plan=json.loads(args.plan.read_text(encoding='utf-8'));ids={c['id'] for c in plan['cases']}
    if args.case and not set(args.case)<=ids:parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:continue
        text,expected=make_case(c);validate(text,c['group']);p=args.out_dir/(c['id']+'.in');p.write_text(text,encoding='utf-8',newline='\n')
        if args.std:
            output=subprocess.check_output([str(args.std.resolve())],input=text.encode()).replace(b'\r\n',b'\n')
            if not matches(output.decode(),expected):raise ValueError('wrong reference output: '+c['id'])
            p.with_suffix('.out').write_bytes(output)


if __name__=='__main__':main()
