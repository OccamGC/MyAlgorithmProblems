"""Count literal loop calls and enumerate all small shuffle histories independently."""
from pathlib import Path
import itertools
import json
import random
import subprocess

ROOT=Path(__file__).resolve().parents[1]
MOD=998244353
PROBLEMS=[
 ('number-theory','power-call-count',[]),
 ('probability','shuffle-expectation',['direct-expectation','element-probabilities']),
 ('probability','shuffle-distribution',['element-probabilities']),
]

def binary_oracle(bits):
    exponent=int(bits,2)
    count=0
    while exponent:
        if exponent%2:
            count+=1
        exponent//=2
        if exponent:
            count+=1
    return count

def enumerate_locations(n):
    counts=[[0]*n for _ in range(n)]
    for choices in itertools.product(range(n),repeat=n):
        array=list(range(n))
        for i,j in enumerate(choices):
            array[i],array[j]=array[j],array[i]
        for i,source in enumerate(array):
            counts[i][source]+=1
    return counts

def distribution_oracle(a,counts):
    n=len(a)
    inverse=pow(n**n,MOD-2,MOD)
    answer=[[0]*n for _ in range(n)]
    for i in range(n):
        for source,value in enumerate(a):
            answer[i][value-1]+=counts[i][source]
    return [[x*inverse%MOD for x in row] for row in answer]

def run(slug,variant,text):
    output=subprocess.check_output([str(ROOT/'build/bin'/f'{slug}-{variant}.exe')],input=text.encode(),timeout=20)
    return list(map(int,output.split()))

def main():
    rng=random.Random(2026093016)
    strings=[''.join(bits) for n in range(1,11) for bits in itertools.product('01',repeat=n)]
    strings += ['0'*rng.randrange(20)+''.join(rng.choice('01') for _ in range(rng.randrange(1,1000))) for _ in range(500)]
    text=str(len(strings))+'\n'+'\n'.join(strings)+'\n'
    answers=[binary_oracle(s) for s in strings]
    assert run('power-call-count','std',text)==answers
    assert run('power-call-count','original',text)==answers
    assert run('power-call-count','std','0\n')==[]
    # The approved modulus bound leaves exponent reduction unchanged.
    reduction_cases=0
    for modulus in [2,3,5,7,11,101]:
        for exponent in range(modulus-1):
            assert exponent%(modulus-1)==exponent
            assert binary_oracle(bin(exponent)[2:])==binary_oracle(bin(exponent%(modulus-1))[2:])
            reduction_cases+=1
    assert binary_oracle('10')==2 and 2%(3-1)==0
    matrix_cases=0
    history_counts={}
    for n in range(1,7):
        locations=enumerate_locations(n)
        history_counts[n]=n**n
        arrays=list(itertools.product(range(1,n+1),repeat=n)) if n<=4 else [tuple(rng.randrange(1,n+1) for _ in range(n)) for _ in range(100)]
        arrays.extend([tuple(range(1,n+1)),tuple([1]*n),tuple([n]*n)])
        for a in arrays:
            text=f'{n}\n'+' '.join(map(str,a))+'\n'
            matrix=distribution_oracle(a,locations)
            expected=[sum((j+1)*row[j] for j in range(n))%MOD for row in matrix]
            flat=[v for row in matrix for v in row]
            for variant in ['std','alternative-element-probabilities']:
                assert run('shuffle-distribution',variant,text)==flat,(n,a,variant)
            for variant in ['std','alternative-direct-expectation','alternative-element-probabilities']:
                assert run('shuffle-expectation',variant,text)==expected,(n,a,variant)
            if matrix_cases<100:
                assert run('shuffle-expectation','original',text)==expected
            assert all(sum(row)%MOD==1 for row in matrix)
            assert [sum(row[j] for row in matrix)%MOD for j in range(n)]==[a.count(j+1) for j in range(n)]
            assert sum(expected)%MOD==sum(a)%MOD
            matrix_cases+=1
        print('Enumerated all histories for n =',n,flush=True)
    report=dict(seed=2026093016,binary_queries=len(strings),empty_query_files=1,valid_reduction_cases=reduction_cases,shuffle_inputs=matrix_cases,enumerated_history_counts=history_counts,program_comparisons_per_shuffle=5,original_expectation_comparisons=100)
    (ROOT/'build/R15-followup-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
