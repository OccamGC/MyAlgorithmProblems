"""Independent exact averaging, partition, output, and input checks for R39."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,itertools,json,random,subprocess
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'build/R39';D=ROOT/'topics/greedy/single-member-household'
spec=importlib.util.spec_from_file_location('recipe',D/'tests/generate.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
def potential(a,others):
    for x in sorted(others):
        if x>a:a=(a+x)/2
    return a
def optimum(values):
    a=values[0];others=values[1:];A=potential(a,others);q=len(others)
    if not q:return [A,F(0),F(0),1,1,1,1]
    b=min(others);rich=b>a
    if rich:b=(a+b)/2
    O=sum(values)-A
    gap=max(A-b,O-A,O-2*b) if q>=2 else abs(A-O)
    strict=A*q>O
    return [A,gap,A-b,1,int(strict),1,int(strict)]
def partitions(items):
    if not items:yield [];return
    a,*rest=items
    for p in partitions(rest):
        yield [[a]]+p
        for i in range(len(p)):yield p[:i]+[[a]+p[i]]+p[i+1:]
def prescribed(values):
    a=values[0];out=[]
    for x in sorted(values[1:]):
        if x>a:a=(a+x)/2;out.append(a)
        else:out.append(x)
    return a,out

def main():
    rng=random.Random(39001);checked=0;partition_cases=0
    for n in range(2,7):
        for case in range(400):
            values=[F(rng.randint(1,12),rng.randint(1,4)) for _ in range(n)];want=potential(values[0],values[1:])
            for mask in range(1,1<<n):
                ids=[i for i in range(n) if mask>>i&1]
                if len(ids)<2:continue
                mean=sum(values[i] for i in ids)/len(ids);after=[mean if i in ids else x for i,x in enumerate(values)];assert potential(after[0],after[1:])<=want;checked+=1
            A,out=prescribed(values);answer=optimum(values);assert A==answer[0]
            largest=F(0)
            for parts in partitions(out):
                wealth=[A]+[sum(g) for g in parts];largest=max(largest,max(wealth)-min(wealth))
            assert largest==answer[1];partition_cases+=1
    print('subset averages and outsider partitions passed',flush=True)
    def check(rows):
        text=str(len(rows))+'\n'+''.join(f'{p} {m}\n' for p,m in rows);gen.validate(text);expected=gen.literal(rows);assert gen.histogram(rows)==expected
        out=subprocess.check_output([str(B/'single-member-household-std.exe')],input=text.encode()).decode();assert gen.matches(out,'\n'.join(map(str,expected)))
    rng=random.Random(39003)
    for i in range(600):check([(1,rng.randint(1,20))]+[(rng.randint(1,20),rng.randint(1,100)) for _ in range(rng.randrange(8))])
    grid=0
    for a,b,v,p in itertools.product(range(1,9),range(1,9),range(1,9),[1,2,3,7,20]):
        if b<=a<v:check([(1,a),(1,b),(p,p*v)]);grid+=1
    for q in [1,2,20,100,500]:check([(1,3),(1,2)]+[(20,80)]*q)
    check([(1,3),(1,2),(1,5)])
    bad=['0\n','1\n2 1\n','1\n1 0\n','2\n1 1\n21 1\n','2\n1 1\n1 1000001\n','1\n1 1\n2 2\n']
    for text in bad:
        try:gen.validate(text)
        except (AssertionError,ValueError,IndexError):pass
        else:raise AssertionError(('invalid input accepted',text))
    expected='7\n0\n0\n1\n1\n1\n1\n'
    for invalid in [expected+'1\n',expected.replace('7','1000000014',1),expected.replace('7','-1',1),expected[:-2]+'2\n','text']:
        assert not gen.matches(invalid,expected)
    result={'seed':39001,'arbitrary_subset_averages':checked,'exhaustive_outsider_partitions':partition_cases,'cpp_random_exact_fraction':600,'cpp_threshold_grid':grid,'cpp_near_equality':5,'cpp_exact_equality':1,'rejected_invalid_inputs':len(bad),'rejected_invalid_outputs':5};(B/'small-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8',newline='\n');print(result,flush=True)
if __name__=='__main__':main()
