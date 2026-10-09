"""Verify multi-member wealth maximization with exact arithmetic and matrices."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
import importlib.util
import json
import random
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'topics/greedy/town-editing-simoleons-2'
OUT=ROOT/'build/R40'
spec=importlib.util.spec_from_file_location('recipes_r40',D/'tests/generate.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
PROGRAMS=[OUT/f'town-editing-simoleons-2-{v}.exe' for v in ['std','alternative-forward']]


def potential(target,others):
    target=sorted(target,reverse=True)
    for v in sorted(others):
        for i in range(len(target)):
            if v>target[i]:target[i]=v=(v+target[i])/2
    return sum(target)


def check(rows,expected):
    text=gen.as_text(rows);gen.validate(text)
    for exe in PROGRAMS:
        actual=subprocess.check_output([str(exe)],input=text.encode()).decode()
        assert gen.matches(actual,str(expected)),(exe,rows,expected,actual)


def main():
    rng=random.Random(40001)
    for _ in range(720):
        rows=[(rng.randint(1,20),rng.randint(1,200))]
        rows += [(rng.randint(1,6),rng.randint(1,50)) for _ in range(rng.randint(0,8))]
        expected=gen.literal(rows)
        assert gen.grouped_matrix(rows)==expected
        check(rows,expected)
    potential_checks=0
    subsets=[ids for size in range(2,5) for ids in combinations(range(4),size)]
    for values in product(range(1,5),repeat=4):
        x=list(map(F,values));before=potential(x[:2],x[2:])
        for ids in subsets:
            y=x[:];average=sum(x[i] for i in ids)/len(ids)
            for i in ids:y[i]=average
            assert potential(y[:2],y[2:])<=before
            potential_checks+=1
    for _ in range(2000):
        k=rng.randint(1,4);q=rng.randint(1,5)
        x=[F(rng.randint(-20,20),rng.randint(1,7)) for _ in range(k+q)]
        before=potential(x[:k],x[k:])
        for _ in range(12):
            ids=rng.sample(range(k+q),rng.randint(2,k+q));y=x[:]
            average=sum(x[i] for i in ids)/len(ids)
            for i in ids:y[i]=average
            assert potential(y[:k],y[k:])<=before
            potential_checks+=1
    large=0
    for k in [1,2,3,7,20]:
        for copies in [1,1001,1024]:
            rows=[(k,1)]+[(1000000,999999)]*copies
            check(rows,gen.grouped_matrix(rows));large+=1
    invalid=['0\n','1000001\n','1\n0 0\n','1\n21 1\n','1\n1 0\n',
             '2\n1 1\n1000001 1\n','1\n1 1000001\n','1\n1 1 1\n','2\n1 1\n','1\n1 1\n2 2\n']
    for i,text in enumerate(invalid):
        try:gen.validate(text)
        except (ValueError,OverflowError):pass
        else:raise AssertionError(text)
        f=OUT/'invalid.in';f.write_text(text,encoding='ascii')
        for flags in [[],['-O']]:
            assert subprocess.run([sys.executable,*flags,str(D/'tests/validate.py'),str(f)],capture_output=True).returncode!=0
    for text in ['', '-1',str(gen.MOD),'1 2','nan','8.0']:
        assert not gen.matches(text,'8')
    assert gen.matches('8\n','8')
    record=dict(seed=40001,exact_fraction_and_matrix_inputs=720,
                arbitrary_subset_potential_checks=potential_checks,
                generic_matrix_large_population_inputs=large,
                rejected_invalid_inputs=len(invalid),rejected_invalid_outputs=6)
    (OUT/'small-checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
