"""Validate the complete input contract of the R17 packages."""
from pathlib import Path
from decimal import Decimal
import re
import sys

def validate(slug,path):
    text = Path(path).read_text(encoding='ascii')
    if slug == 'sorting-pipeline':
        assert text.endswith('\n') and text.count('\n') == 1
        s = text[:-1]
        assert len(s) <= 100000
        assert re.fullmatch(r'[A-Za-z0-9.]*',s)
        for token in re.findall(r'[0-9.]+',s):
            assert re.fullmatch(r'(?:[0-9]+|[0-9]+\.[0-9]{0,2}|\.[0-9]{1,2})',token)
            assert Decimal(token) < 1000000
        return dict(length=len(s))
    if slug == 'robot-platforms':
        lines = text.splitlines()
        n,m = map(int,lines[0].split())
        assert 1 <= n <= 100000 and 1 <= m <= 100000 and len(lines) == m+1
        size=n;max_steps=0
        for line in lines[1:]:
            op,*args = map(int,line.split())
            assert 0 <= op <= 4
            assert len(args) == (1 if op in (2,3) else 0)
            if op in (2,3):
                assert abs(args[0]) <= 10**9
                if size:
                    r=args[0]%size
                    steps=min(r,size-r)
                    assert steps <= 500
                    max_steps=max(max_steps,steps)
            elif op==0:
                size=max(0,size-1)
            elif op==1:
                size+=1
        return dict(n=n,m=m,max_steps=max_steps)
    n,m,k,*values=map(int,text.split())
    assert slug == 'guess-common-divisor'
    assert 0 <= n//5 <= m <= n <= 1000 and len(values)==n
    assert 1 <= k <= 10**9 and all(1 <= x <= 10**9 for x in values)
    return dict(n=n,m=m,k=k)

if __name__ == '__main__':
    print(validate(sys.argv[1],Path(sys.argv[2])))
