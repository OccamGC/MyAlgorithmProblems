"""Independent enumeration, recurrence, and polynomial models for batch R14."""
from pathlib import Path
import itertools
import json
import math
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (
    ('combinatorics','grox-sequence-4'), ('combinatorics','grox-sequence-5a'),
    ('combinatorics','grox-sequence-5b'), ('linear-algebra','grox-sequence-6'),
    ('linear-algebra','grox-sequence-7'), ('sorting','gnome-sort'),
)

def oracle(slug,text):
    tokens=text.split()
    if slug == 'grox-sequence-4':
        n=int(tokens[0]);a=list(map(int,tokens[1:n+2]));b=list(map(int,tokens[n+2:]))
        ans=[0,0,0]
        for i in range(n+1):
            for j in range(n-i+1):
                for at in (i^j,i|j,i&j):ans[at%3]+=a[i]*b[j]
        return [v%1004535809 for v in ans]
    if slug in {'grox-sequence-5a','grox-sequence-5b'}:
        n,k=map(int,tokens[:2]);p=int(tokens[2]) if slug.endswith('5a') else 1005060097
        return [sum(math.comb(n,i)*pow(i,k,p) for i in range(1,n+1))%p]
    if slug == 'grox-sequence-6':
        stream=iter(map(int,tokens));Q,b,k=next(stream),next(stream),next(stream)
        a=next(stream);coeff=[next(stream) for _ in range(k+1)];ans=[];p=1000000007
        for _ in range(Q):
            op=next(stream)
            if op==1:a=next(stream);coeff=[next(stream) for _ in range(k+1)]
            else:
                n=next(stream);value=a
                for t in range(1,n+1):value=(b*value+sum(c*pow(t,i,p) for i,c in enumerate(coeff)))%p
                ans.append(value%p)
        return ans
    if slug == 'grox-sequence-7':
        k=int(tokens[0]);n=1<<k;p=1004535809
        a=[list(map(int,tokens[1+i*n:1+(i+1)*n])) for i in range(n)]
        # Exact cyclic polynomial multiplication, without transforms/evaluation.
        ans=[1]+[0]*(n-1)
        for i in range(n):
            for j in range(i+1,n):
                difference=[(a[j][t]-a[i][t])%p for t in range(n)];out=[0]*n
                for x,c in enumerate(ans):
                    for y,d in enumerate(difference):out[(x+y)%n]=(out[(x+y)%n]+c*d)%p
                ans=out
        return ans
    if slug == 'gnome-sort':
        n=int(tokens[0]);a=[tuple(map(int,tokens[1+2*i:3+2*i])) for i in range(n)]
        position=0;count=0
        while True:
            if position==0:position+=1
            count+=1
            if a[position]<a[position-1]:
                a[position],a[position-1]=a[position-1],a[position];position-=1;continue
            if position==n-1:break
            position+=1
        return [count]
    raise ValueError(slug)

def run(slug,text,suffix=''):
    output=subprocess.check_output([str(ROOT/'build/bin'/f'{slug}{suffix}.exe')],input=text.encode(),timeout=30)
    return list(map(int,output.split()))

def main():
    rng=random.Random(2026093014);counts={s:0 for _,s in PROBLEMS}
    def check(slug,text,expected=None):
        expected=oracle(slug,text) if expected is None else expected
        actual=run(slug,text)
        assert actual==expected,(slug,text,actual,expected)
        if slug=='grox-sequence-4':assert run(slug,text,'-alternative')==expected
        counts[slug]+=1
    for n in list(range(32))+[32,33,63,64,65,127,128,129]:
        for mode in range(3):
            a=[rng.randrange(1000000001) if mode else int(i==n) for i in range(n+1)]
            b=[rng.randrange(1000000001) if mode else 1000000000 for i in range(n+1)]
            check('grox-sequence-4',f'{n}\n'+ ' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n')
    moduli=[1,2,3,4,6,8,12,16,32,64,96,10007,1000000007,1073741824,2000000000]
    for n in range(17):
        for k in [0,1,2,3,7,16,31]:
            check('grox-sequence-5a',f'{n} {k} {rng.choice(moduli)}\n')
            check('grox-sequence-5b',f'{n} {k}\n')
    for p in moduli:
        for n in [0,1,2,3,7,8,15,16,31,32,63]:
            for k in [0,1,4]:check('grox-sequence-5a',f'{n} {k} {p}\n')
    for _ in range(120):
        n=rng.randrange(81);k=rng.randrange(121)
        check('grox-sequence-5a',f'{n} {k} {rng.choice(moduli)}\n')
        check('grox-sequence-5b',f'{n} {k}\n')
    # Huge decimal exponents for k=0,1,2 have exact elementary binomial moments.
    for digits in [1,9,100,1000,1001]:
        n=10**(digits-1) if digits>1 else 0
        for p in moduli:
            for k in [0,1,2]:
                if k==0:expected=(pow(2,n,p)-1)%p
                elif n==0:expected=0
                elif k==1:expected=n*pow(2,n-1,p)%p
                elif n==1:expected=1%p
                else:expected=n*(n-1)*pow(2,n-2,p)%p+n*pow(2,n-1,p)%p
                check('grox-sequence-5a',f'{n} {k} {p}\n',[expected%p])
    for b in [0,1,-1,2,-2,1000000000,-1000000000]:
        for k in [0,1,2,5,10,200]:
            a=rng.randrange(-1000000000,1000000001);c=[rng.randrange(-1000000000,1000000001) for _ in range(k+1)]
            rows=[f'8 {b} {k}', ' '.join(map(str,[a,*c])),'0 0','0 1','0 2','0 15']
            rows+=['1 '+' '.join(map(str,[rng.randrange(-10,11),*[rng.randrange(-10,11) for _ in c]])), '0 0','0 7','0 21']
            check('grox-sequence-6','\n'.join(rows)+'\n')
    for _ in range(120):
        k=rng.randrange(9);b=rng.randrange(-5,6);rows=[f'12 {b} {k}',' '.join(map(str,[rng.randrange(-20,21) for _ in range(k+2)]))]
        for _ in range(12):
            if rng.randrange(4)==0:rows.append('1 '+' '.join(map(str,[rng.randrange(-20,21) for _ in range(k+2)])))
            else:rows.append(f'0 {rng.randrange(41)}')
        check('grox-sequence-6','\n'.join(rows)+'\n')
    for k in range(4):
        n=1<<k
        for _ in range(35):
            a=[[rng.randrange(1000) for _ in range(n)] for _ in range(n)]
            if rng.randrange(5)==0 and n>1:a[-1]=a[0].copy()
            check('grox-sequence-7',f'{k}\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n')
    for n in range(2,8):
        permutations=list(itertools.permutations(range(n)))
        if len(permutations)>200:rng.shuffle(permutations);permutations=permutations[:200]
        for order in permutations:
            text=f'{n}\n'+'\n'.join(f'{i//2} {i%2}' for i in order)+'\n';check('gnome-sort',text)
    for _ in range(150):
        n=rng.randrange(2,41);values=rng.sample([(x,y) for x in range(-10,11) for y in range(-10,11)],n)
        check('gnome-sort',f'{n}\n'+'\n'.join(f'{x} {y}' for x,y in values)+'\n')
    (ROOT/'build/R14-checks.json').write_text(json.dumps({'seed':2026093014,'cases':counts,'total':sum(counts.values())},indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts,indent=2),flush=True)
    print('Total:',sum(counts.values()),flush=True)

if __name__=='__main__':main()
