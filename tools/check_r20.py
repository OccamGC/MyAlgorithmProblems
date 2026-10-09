"""Independent checks for the three retained R20 problem packages."""
from pathlib import Path
from collections import deque
from functools import lru_cache
import itertools
import json
import random
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('strings','spiral-numbers'),('simulation','side-scrolling-field-theory'),('combinatorics','holy-palanquin-confectionery')]
VARIANTS={'spiral-numbers':['std','alternative'],'side-scrolling-field-theory':['std'],'holy-palanquin-confectionery':['std','alternative-knapsack','alternative-search']}

def palindrome_oracle(text):
    return ''.join(('Y' if str(int(s))==str(int(s))[::-1] else 'N')+'\n' for s in text.split()[1:])

def circle_oracle(text,stepwise=False):
    rows=text.splitlines();n,m=map(int,rows[0].split())
    people=deque((int(x.split()[0]),x.split()[1]) for x in rows[1:1+n]);answer=[]
    # The first deque entry is the holder. Moving to the next displayed index
    # is a left rotation of the sequence, independent of modular-index code.
    turns={0:{0:1,1:-1},1:{0:-1,1:1}}
    for row in rows[1+n:]:
        d,p=map(int,row.split());sign=turns[people[0][0]][d]
        if stepwise:
            for _ in range(p):people.rotate(sign)
        else:people.rotate(sign*p)
        answer.append(people[0][1])
    assert len(answer)==m
    return '\n'.join(answer)+'\n'

def restock_oracle(text):
    x=int(text)
    @lru_cache(None)
    def count(price,remaining):
        if price>x:return (1,remaining)
        ways=total=0
        for quantity in range(remaining//price+1):
            a,b=count(price+1,remaining-quantity*price)
            ways+=a;total+=b
        return ways,total
    return str(count(1,x)[1]%998244353)+'\n'

ORACLES={'spiral-numbers':palindrome_oracle,'side-scrolling-field-theory':circle_oracle,'holy-palanquin-confectionery':restock_oracle}

def validate(slug,text,group=None):
    rows=text.splitlines()
    if slug=='spiral-numbers':
        t=int(rows[0]);assert 1<=t<=1000 and len(rows)==t+1
        assert all(1<=len(s)<=18 and set(s)<=set('0123456789') and int(s)<10**18 for s in rows[1:])
        return dict(T=t,max_length=max(map(len,rows[1:])))
    if slug=='holy-palanquin-confectionery':
        assert len(rows)==1
        x=int(rows[0]);assert 0<=x<=80
        return dict(value=x)
    assert slug=='side-scrolling-field-theory',slug
    n,m=map(int,rows[0].split());assert 1<=n<=30000 and 1<=m<=30000 and len(rows)==1+n+m
    facing=[]
    for row in rows[1:1+n]:
        f,c=row.split();assert f in ['0','1'] and len(c)==1 and 'A'<=c<='Z';facing.append(int(f))
    total=pos=0;nowrap=True
    for row in rows[1+n:]:
        d,p=map(int,row.split());assert d in [0,1] and 0<=p<=10**9
        total+=p;nextpos=pos+(p if d!=facing[pos] else -p)
        nowrap &= 0<=nextpos<n;pos=nextpos%n
    if group in [1,2]:assert total<=4000000
    if group==1:assert nowrap
    return dict(N=n,M=m,total_steps=total,no_wrapping=nowrap)

def run_case(slug,text,expected=None):
    validate(slug,text)
    expected=ORACLES[slug](text) if expected is None else expected
    for variant in VARIANTS[slug]:
        path=ROOT/'build/bin'/f'{slug}-{variant}.exe'
        actual=subprocess.check_output([str(path)],input=text.encode('ascii'),timeout=30).decode('ascii').replace('\r\n','\n')
        assert actual==expected,(slug,variant,text[:300],actual[:300],expected[:300])

def main():
    report={};rng=random.Random(2026100120)
    strings=[''.join(t) for length in range(1,6) for t in itertools.product('012',repeat=length)]
    strings += [str(rng.randrange(10**18)).zfill(18) for _ in range(5000)]
    for i in range(0,len(strings),1000):
        chunk=strings[i:i+1000];run_case('spiral-numbers',str(len(chunk))+'\n'+'\n'.join(chunk)+'\n')
    report['spiral-numbers']={'exhaustive_alphabet_012_length_1_to_5':363,'random_18_digit_strings':5000}
    for iteration in range(200):
        n=rng.randint(1,20);m=100
        text=f'{n} {m}\n'+''.join(f'{rng.randrange(2)} {chr(65+rng.randrange(26))}\n' for _ in range(n))+''.join(f'{rng.randrange(2)} {rng.randrange(201)}\n' for _ in range(m))
        run_case('side-scrolling-field-theory',text,circle_oracle(text,True))
    report['side-scrolling-field-theory']={'independent_stepwise_batches':200,'operations':20000}
    for x in range(81):run_case('holy-palanquin-confectionery',f'{x}\n')
    report['holy-palanquin-confectionery']={'all_legal_budgets':81}
    dest=ROOT/'build/R20/checks.json';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
