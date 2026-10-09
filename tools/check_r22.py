"""Independent R22 oracles and validation; only formal C++ programs are timed."""
from pathlib import Path
from functools import lru_cache
import bisect,itertools,json,math,random,subprocess
ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('optimization','queen-of-hearts-card-soldiers'),('graphs','lattice-completion'),('logic','lattice-recognition'),('combinatorics','sublattice-count'),('recursion','fractional-recurrence')]
VARIANTS={s:['std','alternative'] for _,s in PROBLEMS}
VARIANTS['sublattice-count'].append('brute');VARIANTS['fractional-recurrence']=['std']
def lines(values):return ''.join(str(x)+'\n' for x in values)

def card_oracle(text):
    values=list(map(int,text.split()));points=sorted(zip(values[1::2],values[2::2]));tails=[]
    for _,armor in points:
        value=-armor;index=bisect.bisect_left(tails,value)
        if index==len(tails):tails.append(value)
        else:tails[index]=value
    return str(len(tails))+'\n'
def card_brute(points):
    answer=0
    for mask in range(1<<len(points)):
        if mask.bit_count()<=answer:continue
        chosen=[points[i] for i in range(len(points)) if mask>>i&1]
        if all((a<c and b>d) or (a>c and b<d) for (a,b),(c,d) in itertools.combinations(chosen,2)):answer=len(chosen)
    return str(answer)+'\n'

def completions(text):
    values=list(map(int,text.split()));t=values[0];at=1;arrays=[]
    for _ in range(t):n=values[at];at+=1;arrays.append([x-1 for x in values[at:at+n]]);at+=n
    assert at==len(values)
    return arrays
def completion_oracle(text):
    answers=[]
    for a in completions(text):
        parent=list(range(len(a)));size=[1]*len(a);ok=True
        def find(u):
            while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
            return u
        for i,j in enumerate(a):
            u=find(i);v=find(j)
            if u==v:
                if a[j]!=i:ok=False;break
            else:
                if size[u]<size[v]:u,v=v,u
                parent[v]=u;size[u]+=size[v]
        answers.append('Y' if ok else 'N')
    return lines(answers)

def matrices(text):
    values=list(map(int,text.split()));at=1;result=[]
    for _ in range(values[0]):
        n=values[at];at+=1;a=[values[at+i*n:at+(i+1)*n] for i in range(n)];at+=n*n;result.append(a)
    assert at==len(values)
    return result
def is_lattice(a):
    n=len(a);full=(1<<n)-1
    rows=[sum(value<<j for j,value in enumerate(row)) for row in a]
    columns=[sum(a[i][j]<<i for i in range(n)) for j in range(n)]
    for i in range(n):
        if not a[i][i]:return False
        for j in range(n):
            if a[i][j] and rows[j]&~rows[i]:return False
    for i in range(n):
        for j in range(i,n):
            up=rows[i]&rows[j];down=columns[i]&columns[j]
            # Directly enumerate every candidate from the mathematical definition.
            if not any(up>>k&1 and (up&~rows[k])==0 for k in range(n)):return False
            if not any(down>>k&1 and (down&~columns[k])==0 for k in range(n)):return False
    return True
def recognition_oracle(text):return lines('Y' if is_lattice(a) else 'N' for a in matrices(text))

def table(text):
    values=list(map(int,text.split()));n=values[0];assert len(values)==1+n*n
    return [[x-1 for x in values[1+i*n:1+(i+1)*n]] for i in range(n)]
def sublattice_brute(a):
    n=len(a);answer=0
    for mask in range(1,1<<n):
        selected=[i for i in range(n) if mask>>i&1]
        answer+=all(mask>>a[i][j]&1 and mask>>a[j][i]&1 for i in selected for j in selected)
    return str(answer)+'\n'
def sublattice_oracle(text):
    a=table(text)
    if len(a)<=10:return sublattice_brute(a)
    return subprocess.check_output([str(ROOT/'build/bin/sublattice-count-brute.exe')],input=text.encode('ascii'),timeout=120).decode('ascii').replace('\r\n','\n')

def integer_root(x):
    if x==0:return 0
    target=x**4;value=1<<((target.bit_length()+4)//5)
    while True:
        candidate=(4*value+target//(value**4))//5
        if candidate>=value:break
        value=candidate
    while value**5>target:value-=1
    while (value+1)**5<=target:value+=1
    return value
def function_oracle(text):
    values=list(map(int,text.split()))[1:]
    @lru_cache(None)
    def f(x):
        if x==0:return 0
        return 3*f(max(integer_root(x)-1,0))+2*f(x//2)+x
    return ' '.join(str(f(x)) for x in values)+'\n'
ORACLES=dict(zip([s for _,s in PROBLEMS],[card_oracle,completion_oracle,recognition_oracle,sublattice_oracle,function_oracle]))

def validate(slug,text,group=None):
    values=list(map(int,text.split()))
    if slug=='queen-of-hearts-card-soldiers':
        n=values[0];assert 0<=n<=10**6 and len(values)==1+2*n and all(abs(x)<=10**9 for x in values[1:])
        if group==1:assert n<=20
        if group==2:assert n<=2000
        return dict(n=n)
    if slug=='lattice-completion':
        assert 0<=values[0]<=400000;arrays=completions(text);total=0
        for a in arrays:assert 1<=len(a)<=200000 and all(0<=x<len(a) for x in a);total+=len(a)
        assert total<=400000;return dict(T=len(arrays),total_N=total,maximum_N=max(map(len,arrays),default=0))
    if slug=='lattice-recognition':
        assert 0<=values[0]<=50000;arrays=matrices(text);total=0
        for a in arrays:assert 1<=len(a)<=50 and all(x in [0,1] for row in a for x in row);total+=len(a)
        assert total<=50000;return dict(T=len(arrays),total_n=total,maximum_n=max(map(len,arrays),default=0))
    if slug=='fractional-recurrence':
        n=values[0];assert 1<=n<=100000 and len(values)==n+1 and all(0<=x<=10**9 for x in values[1:]);return dict(N=n,maximum=max(values[1:]))
    a=table(text);n=len(a);assert 1<=n<=22 and all(0<=x<n for row in a for x in row)
    join=[[a[min(i,j)][max(i,j)] for j in range(n)] for i in range(n)]
    meet=[[a[max(i,j)][min(i,j)] for j in range(n)] for i in range(n)]
    for i in range(n):
        assert a[i][i]==i
        for j in range(n):
            assert join[i][meet[i][j]]==i and meet[i][join[i][j]]==i
            for k in range(n):
                assert join[join[i][j]][k]==join[i][join[j][k]]
                assert meet[meet[i][j]][k]==meet[i][meet[j][k]]
    relation=[[join[i][j]==j for j in range(n)] for i in range(n)]
    @lru_cache(None)
    def height(v):return 1+max((height(u) for u in range(n) if u!=v and relation[u][v]),default=0)
    return dict(n=n,height=max(height(i) for i in range(n)))

def run_case(slug,text,expected=None):
    validate(slug,text);expected=ORACLES[slug](text) if expected is None else expected
    for variant in VARIANTS[slug]:
        actual=subprocess.check_output([str(ROOT/'build/bin'/f'{slug}-{variant}.exe')],input=text.encode('ascii'),timeout=120).decode('ascii').replace('\r\n','\n')
        assert actual==expected,(slug,variant,text[:400],actual[:400],expected[:400])

def encode_matrices(items):return str(len(items))+'\n'+''.join(str(len(a))+'\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n' for a in items)
def encode_functions(items):return str(len(items))+'\n'+''.join(str(len(a))+'\n'+lines(x+1 for x in a) for a in items)
def encode_table(a):return str(len(a))+'\n'+'\n'.join(' '.join(str(x+1) for x in row) for row in a)+'\n'

def main():
    rng=random.Random(2026100122);report={};count=0
    points=list(itertools.product([-1,0,1],repeat=2))
    for n in range(5):
        for sequence in itertools.combinations_with_replacement(points,n):
            text=str(n)+'\n'+''.join(f'{a} {b}\n' for a,b in sequence);expected=card_brute(sequence)
            assert card_oracle(text)==expected;run_case('queen-of-hearts-card-soldiers',text,expected);count+=1
    for _ in range(100):
        n=rng.randrange(13);sequence=[(rng.randrange(-5,6),rng.randrange(-5,6)) for _ in range(n)]
        run_case('queen-of-hearts-card-soldiers',str(n)+'\n'+''.join(f'{a} {b}\n' for a,b in sequence),card_brute(sequence))
    report['queen-of-hearts-card-soldiers']=dict(exhaustive_point_multisets=count,random_subset_enumerations=100);print('Card checks passed',flush=True)
    all_lattices={};total=0
    for n in range(1,5):
        chunk=[];answers=[];valid=[]
        for mask in range(1<<(n*n)):
            a=[[mask>>(i*n+j)&1 for j in range(n)] for i in range(n)];answer=is_lattice(a)
            if answer:valid.append(mask)
            chunk.append(a);answers.append('Y' if answer else 'N');total+=1
            if len(chunk)*n>=48000:
                run_case('lattice-recognition',encode_matrices(chunk),lines(answers));chunk=[];answers=[]
        if chunk:run_case('lattice-recognition',encode_matrices(chunk),lines(answers))
        all_lattices[n]=valid
    report['lattice-recognition']=dict(exhaustive_relation_matrices=total,largest_n=4);print('Relation checks passed',flush=True)
    count=0
    for n in range(1,5):
        arrays=[];answers=[]
        for a in itertools.product(range(n),repeat=n):
            required=sum(1<<(i*n+a[i]) for i in range(n));forbidden=0
            for i,j in enumerate(a):
                if not(required>>(j*n+i)&1):forbidden|=1<<(j*n+i)
            exists=any((mask&required)==required and not(mask&forbidden) for mask in all_lattices[n])
            arrays.append(a);answers.append('Y' if exists else 'N');count+=1
        text=encode_functions(arrays);expected=lines(answers);assert completion_oracle(text)==expected;run_case('lattice-completion',text,expected)
    report['lattice-completion']=dict(exhaustive_function_graphs=count,oracle='enumerated all lattice-representing extension relations through n=4');print('Completion checks passed',flush=True)
    count=0
    for n,masks in all_lattices.items():
        for mask in masks:
            a=[[mask>>(i*n+j)&1 for j in range(n)] for i in range(n)]
            if any(i!=j and a[i][j] and a[j][i] for i in range(n) for j in range(n)):continue
            operation=[]
            for i in range(n):
                row=[]
                for j in range(n):
                    if i<=j:
                        bounds=[k for k in range(n) if a[i][k] and a[j][k]];v=next(k for k in bounds if all(a[k][z] for z in bounds))
                    else:
                        bounds=[k for k in range(n) if a[k][i] and a[k][j]];v=next(k for k in bounds if all(a[z][k] for z in bounds))
                    row.append(v)
                operation.append(row)
            run_case('sublattice-count',encode_table(operation),sublattice_brute(operation));count+=1
    report['sublattice-count']=dict(all_labeled_lattices_through_n4=count,oracle='enumeration of every nonempty subset');print('Sublattice checks passed',flush=True)
    values=list(range(10001))+[t**5+d for t in range(1,64) for d in [-1,0,1] if 0<=t**5+d<=10**9]+[rng.randrange(10**9+1) for _ in range(1000)]
    run_case('fractional-recurrence',str(len(values))+'\n'+' '.join(map(str,values))+'\n')
    report['fractional-recurrence']=dict(exact_integer_recurrence_queries=len(values),oracle='Python arbitrary-precision integer Newton root and exact recurrence')
    (ROOT/'build/R22/checks.json').write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
