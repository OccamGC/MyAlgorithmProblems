"""Check both two-household references against exact full-state search."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import json
import random
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'topics/greedy/town-editing-simoleons-3'
OUT=ROOT/'build/R41'
spec=importlib.util.spec_from_file_location('gen_r41',D/'tests/generate.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
from oracle import exact_answer, schedule_answer, residue
PROGRAMS=[OUT/f'{D.name}-{variant}.exe' for variant in ['std','alternative-affine']]


def check(rows,values):
    text=gen.as_text(rows);gen.validate(text)
    expected=''.join(str(x)+'\n' for x in values)
    for exe in PROGRAMS:
        actual=subprocess.check_output([str(exe)],input=text.encode()).decode()
        assert gen.matches(actual,expected),(exe,rows[:5],actual[:200],expected[:200])


def main():
    rng=random.Random(41001)
    rows=[];answers=[]
    for k in range(1,31):
        for l in range(1,31):
            for m1,m2 in [(k,9*l),(rng.randrange(101),rng.randrange(101)),(0,1000000000)]:
                row=(k,m1,l,m2);value=residue(exact_answer(row))
                assert schedule_answer(row)==value,(row,value)
                rows.append(row);answers.append(value)
    for k in [1,2,1000000]:
        for m in [0,1,1000000000]:rows.append((k,m,0,0));answers.append(m)
    check(rows,answers);small=len(rows)
    rows=[(rng.randint(1,1000000),rng.randrange(1000000001),rng.randint(1,1000000),rng.randrange(1000000001)) for _ in range(2000)]
    check(rows,[schedule_answer(row) for row in rows])
    # The losing branch must be chosen using exact ratios, never residues.
    equal=[(k,k*999,l,l*999) for k,l in [(1,1000000),(1000000,1),(999999,1000000),(1000000,999999)]]
    check(equal,[row[1] for row in equal])
    invalid=['','0\n','100001\n','1\n0 0\n1 1\n','1\n1 1\n0 1\n',
             '1\n1000001 1\n1 1\n','1\n1 1\n1000001 1\n','1\n1 -1\n1 1\n',
             '1\n1 1\n1 1000000001\n','1\n1 1\n-1 0\n','2\n1 1\n1 1\n',
             '1\n1 1\n1 1\nextra\n','1\n1 1 1 1\n']
    for index,text in enumerate(invalid):
        try:gen.validate(text)
        except (ValueError,OverflowError):pass
        else:raise AssertionError(('invalid accepted',text))
        path=OUT/'invalid.in';path.write_text(text,encoding='utf-8')
        for flags in [[],['-O']]:
            result=subprocess.run([sys.executable,*flags,str(D/'tests/validate.py'),str(path)],capture_output=True)
            assert result.returncode!=0,(index,flags)
    for text in ['', '-1', '1000000007', '1 2', '0.5','nan','x']:
        assert not gen.matches(text,'1\n'),text
    # Literal four-move witness, using original household money and identities.
    households=[{'T1','T2'},{'O1','O2'}];money=[F(2),F(18)]
    history=[]
    for person,source in [('T1',0),('O1',1),('T2',0),('O2',1)]:
        dest=1-source;carried=money[source]/len(households[source])
        households[source].remove(person);households[dest].add(person)
        money[source]-=carried;money[dest]+=carried
        assert sum(money)==20
        history.append(list(map(str,money)))
    assert households[1]=={'T1','T2'} and money[1]==F(98,9)
    output={'seed':41001,'exact_population_pairs':900,'exact_cases':small,
            'large_matrix_cases':2000,'equal_ratio_boundaries':4,'invalid_inputs':len(invalid),
            'invalid_outputs':7,'sample_witness_household_money':history,'all_passed':True}
    (OUT/'small-checks.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
