"""Validate the full published ranges and exact input arities of batch R14."""
import re
from pathlib import Path

PROBLEMS=(('combinatorics','grox-sequence-4'),('combinatorics','grox-sequence-5a'),('combinatorics','grox-sequence-5b'),('linear-algebra','grox-sequence-6'),('linear-algebra','grox-sequence-7'),('sorting','gnome-sort'))
GROUP_SHARES={slug:(100,) for _,slug in PROBLEMS}

def validate(slug,path):
    raw=Path(path).read_bytes().split()
    assert all(re.fullmatch(rb'-?\d+',v) for v in raw),(slug,'non-integer token')
    values=list(map(int,raw))
    if slug=='grox-sequence-4':
        n=values[0];assert 0<=n<2**20 and len(values)==2*n+3
        assert all(0<=v<=10**9 for v in values[1:])
        return {'n':n,'output_count':3}
    if slug=='grox-sequence-5a':
        assert len(values)==3;n,k,p=values
        assert 0<=n<=10**1000 and 0<=k<=3000 and 1<=p<=2*10**9
        return {'digits':len(raw[0]),'k':k,'modulus':p,'output_count':1}
    if slug=='grox-sequence-5b':
        assert len(values)==2;n,k=values
        assert 0<=n<=10**9 and 0<=k<=100000
        return {'n':n,'k':k,'output_count':1}
    if slug=='grox-sequence-6':
        Q,b,k=values[:3];assert 1<=Q<=500 and abs(b)<=10**9 and 0<=k<=200
        at=3;assert len(values)>=at+k+2
        assert all(abs(v)<=10**9 for v in values[at:at+k+2]);at+=k+2
        queries=0
        for _ in range(Q):
            assert at<len(values);op=values[at];at+=1;assert op in (0,1)
            count=k+2 if op else 1;assert at+count<=len(values)
            if op:assert all(abs(v)<=10**9 for v in values[at:at+count])
            else:assert 0<=values[at]<=10**9;queries+=1
            at+=count
        assert at==len(values)
        return {'Q':Q,'beta':b,'k':k,'output_count':queries}
    if slug=='grox-sequence-7':
        k=values[0];assert 0<=k<=9;n=1<<k
        assert len(values)==1+n*n and all(0<=v<=999 for v in values[1:])
        return {'k':k,'n':n,'output_count':n}
    if slug=='gnome-sort':
        n=values[0];assert 2<=n<=500000 and len(values)==1+2*n
        assert all(abs(v)<=10**9 for v in values[1:])
        assert len(set(zip(values[1::2],values[2::2])))==n
        return {'n':n,'output_count':1}
    raise ValueError(slug)

VALIDATORS={slug:(lambda path,s=slug:validate(s,path)) for _,slug in PROBLEMS}

def validate_group_case(slug,spec,dimensions):
    assert spec['group']==1

def check_output(slug,path,dimensions):
    raw=Path(path).read_bytes().split();assert len(raw)==dimensions['output_count']
    assert all(v.isdigit() for v in raw)
    modulus={'grox-sequence-4':1004535809,'grox-sequence-5a':dimensions.get('modulus'),'grox-sequence-5b':1005060097,'grox-sequence-6':1000000007,'grox-sequence-7':1004535809}.get(slug)
    if modulus is not None:assert all(0<=int(v)<modulus for v in raw)
    else:assert 0<=int(raw[0])<=dimensions['n']**2-1
