"""Independent exact oracles and randomized verification for R17."""
from pathlib import Path
from decimal import Decimal
import itertools
import json
import math
import random
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = [('strings','sorting-pipeline'), ('data-structures','robot-platforms'),
            ('number-theory','guess-common-divisor')]

def pipeline_oracle(text):
    tokens = re.findall(r'[0-9.]+|[A-Za-z]',text)
    integers = sum(int(x.lstrip('0') or '0') for x in tokens if x[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' and '.' not in x)
    decimals = sum((Decimal(x) for x in tokens if '.' in x), Decimal(0))
    lower = ''.join(x.lower() for x in tokens if x.isupper())
    upper = ''.join(x.upper() for x in tokens if x.islower())
    return f'{integers}\n{decimals:.2f}\n{lower}\n{upper}\n'

def robot_oracle(text):
    lines = text.splitlines()
    n,m = map(int,lines[0].split())
    items = list(range(1,n+1))
    current = 0
    last = n
    out = []
    for line in lines[1:]:
        op,*args = map(int,line.split())
        if op == 0 and items:
            items.pop(current)
            current = current % len(items) if items else 0
        elif op == 1:
            last += 1
            items.insert(current+1 if items else 0,last)
        elif op in (2,3) and items:
            current = (current + (args[0] if op==2 else -args[0])) % len(items)
        elif op == 4:
            out.append(items[current] if items else -1)
    return ''.join(f'{x}\n' for x in out)

def divisor_oracle(text):
    n,m,k,*values = map(int,text.split())
    if m == 0:
        return f'{k}\n'
    # Enumerate all m-position subsets, then all divisors of their gcd.
    best = 1
    for subset in itertools.combinations(values,m):
        g = math.gcd(*subset)
        for d in range(1,math.isqrt(g)+1):
            if g % d == 0:
                for candidate in (d,g//d):
                    if candidate <= k:
                        best = max(best,candidate)
    return f'{best}\n'

ORACLES = dict(zip((s for _,s in PROBLEMS),[pipeline_oracle,robot_oracle,divisor_oracle]))

def verify(slug,text,expected=None):
    if expected is None:
        expected = ORACLES[slug](text)
    for variant in ['std','alternative']:
        exe = ROOT/'build/bin'/f'{slug}-{variant}.exe'
        actual = subprocess.check_output([str(exe)],input=text.encode('ascii'),timeout=30).replace(b'\r\n',b'\n').decode('ascii')
        assert actual == expected, (slug,variant,text,expected,actual)

def main():
    rng = random.Random(2026093017)
    counts = {}
    for _,slug in PROBLEMS:
        count = 0
        if slug == 'sorting-pipeline':
            for text in ['\n','0\n','.0\n','0.\n','.01\n','0x3F666.\n','66ccff3f3f3f3f\n','999999.99A999999\n','AazZ\n']:
                verify(slug,text);count+=1
            for _ in range(300):
                text=''
                for j in range(rng.randrange(100)):
                    token=rng.choice([str(rng.randrange(10**6)),f'.{rng.randrange(100):02}',f'{rng.randrange(10**6)}.',f'{rng.randrange(10**6)}.{rng.randrange(100):02}'])
                    text+=token+rng.choice('aAzZ')
                verify(slug,text+'\n');count+=1
        elif slug == 'robot-platforms':
            for _ in range(350):
                n=rng.randrange(1,20);m=150
                lines=[f'{n} {m}']
                for j in range(m):
                    op=rng.randrange(5)
                    lines.append(str(op)+(f' {rng.choice([-10**9,10**9,rng.randrange(-100,101)])}' if op in (2,3) else ''))
                verify(slug,'\n'.join(lines)+'\n');count+=1
        else:
            for _ in range(400):
                n=rng.randrange(10);m=rng.randrange(n//5,n+1);k=rng.randrange(1,201)
                text=f'{n} {m} {k}\n'+' '.join(str(rng.randrange(1,201)) for _ in range(n))+'\n'
                verify(slug,text);count+=1
            # Any sample wholly within the first 800 positions misses divisor 2.
            text='1000 200 2\n'+' '.join(map(str,[1]*800+[2]*200))+'\n'
            verify(slug,text,'2\n');count+=1
        counts[slug]=count
        print(slug,count,'independent checks passed',flush=True)
    (ROOT/'build/R17/checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
