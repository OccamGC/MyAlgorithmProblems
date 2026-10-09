"""Independent determinant expansion and matrix-power recurrence checks."""
import itertools
import json
import math
import random
from pathlib import Path
from check_r14 import run

ROOT=Path(__file__).resolve().parents[1]

def multiply(a,b,p):
    size=len(a);c=[[0]*size for _ in a]
    for i in range(size):
        for k in range(size):
            for j in range(size):c[i][j]=(c[i][j]+a[i][k]*b[k][j])%p
    return c

def matrix_recurrence(beta,a,coeff,n):
    p=1000000007;k=len(coeff)-1;size=k+2
    matrix=[[0]*size for _ in range(size)];matrix[0][0]=beta%p
    for j in range(k+1):matrix[0][j+1]=sum(coeff[i]*math.comb(i,j) for i in range(j,k+1))%p
    for i in range(k+1):
        for j in range(i+1):matrix[i+1][j+1]=math.comb(i,j)
    result=[[int(i==j) for j in range(size)] for i in range(size)]
    while n:
        if n&1:result=multiply(result,matrix,p)
        matrix=multiply(matrix,matrix,p);n>>=1
    return (result[0][0]*a+result[0][1])%p

def cyclic(a,b,p):
    n=len(a);result=[0]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[(i+j)%n]=(result[(i+j)%n]+x*y)%p
    return result

def determinant(a):
    n=len(a);p=1004535809;one=[1]+[0]*(n-1)
    powers=[[one] for _ in a]
    for i in range(n):
        for _ in range(n-1):powers[i].append(cyclic(powers[i][-1],a[i],p))
    answer=[0]*n
    for permutation in itertools.permutations(range(n)):
        inversions=sum(permutation[i]>permutation[j] for i in range(n) for j in range(i+1,n))
        term=one
        for row,column in enumerate(permutation):term=cyclic(term,powers[column][row],p)
        for i,x in enumerate(term):answer[i]=(answer[i]+(-x if inversions%2 else x))%p
    return answer

def main():
    rng=random.Random(202609301401);counts={}
    for prime,root in [(1004535809,3),(1005060097,5)]:
        assert all(prime%d for d in range(2,math.isqrt(prime)+1))
        rem=prime-1;factors=[];d=2
        while d*d<=rem:
            if rem%d==0:
                factors.append(d)
                while rem%d==0:rem//=d
            d+=1
        if rem>1:factors.append(rem)
        assert all(pow(root,(prime-1)//q,prime)!=1 for q in factors)
    counts['prime_and_primitive_root_pairs']=2
    count=0
    for beta in [0,1,-1,2,-1000000000,1000000000]:
        for k in range(5):
            a=rng.randrange(-10**9,10**9+1);coeff=[rng.randrange(-10**9,10**9+1) for _ in range(k+1)]
            indices=[0,1,999999937,1000000000]
            text=f'{len(indices)} {beta} {k}\n'+' '.join(map(str,[a,*coeff]))+'\n'+''.join(f'0 {n}\n' for n in indices)
            assert run('grox-sequence-6',text)==[matrix_recurrence(beta,a,coeff,n) for n in indices]
            count+=1
    counts['large_index_matrix_models']=count
    count=0
    for k in range(3):
        n=1<<k
        for _ in range(20):
            a=[[rng.randrange(1000) for _ in range(n)] for _ in range(n)]
            text=f'{k}\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n'
            assert run('grox-sequence-7',text)==determinant(a)
            count+=1
    counts['direct_determinants']=count
    (ROOT/'build/R14-formulas.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')
    print(counts)

if __name__=='__main__':main()
