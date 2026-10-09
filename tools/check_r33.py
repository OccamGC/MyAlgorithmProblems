"""Independent small models, input validators, and checks for the five R33 problems."""
from pathlib import Path
import collections,hashlib,heapq,importlib.util,itertools,json,math,random,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R33'
PROBLEMS=[('permutations','lexicographic-jump'),('combinatorics','anonymous-leaf-orders'),('combinatorics','labeled-leaf-orders'),('constructive','mind-swap-restoration'),('number-theory','dynamic-polynomial-geometric-sum')]
P=1000000007;Q=998244353
def module(path):
    spec=importlib.util.spec_from_file_location('r33_loaded',path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
def load_generator(topic,slug):return module(ROOT/'topics'/topic/slug/'tests/generate.py')
CHECKER=module(ROOT/'topics/constructive/mind-swap-restoration/checker.py')
def validate(slug,text,group=3):
    if slug=='mind-swap-restoration':
        n,used,soul=CHECKER.read_input(text)
        assert group!=1 or n<=8 and len(used)<=20
        assert group!=2 or n<=2000 and len(used)<=2000
        return n,used,soul
    values=list(map(int,text.split()))
    if slug.endswith('leaf-orders'):
        assert len(values)==2;n,m=values;assert 0<=n<=100000 and 0<=m<=100000
        assert group!=1 or n<=8
        assert group!=2 or n<=1000
        return n,m
    if slug=='lexicographic-jump':
        T=values[0];assert 1<=T<=100000;position=1;total=0;cases=[]
        for _ in range(T):
            n,k=values[position:position+2];position+=2;a=values[position:position+n];position+=n
            assert n>=1 and 0<=k<2**31 and len(a)==n and set(a)==set(range(1,n+1));total+=n
            assert group!=1 or n<=8
            assert group!=2 or n<=2000
            cases.append((a,k))
        assert total<=2000000 and position==len(values)
        return cases
    n,m,k,a=values[:4];assert 1<=n<=10**9 and 1<=m<=10000 and 1<=k<=200 and 0<=a<P
    assert group!=1 or n<=20 and m<=30 and k<=4
    assert group!=2 or n<=1000 and m<=300 and k<=30
    b=values[4:5+k];assert len(b)==k+1 and all(0<=x<P for x in b);position=5+k;ops=[]
    for _ in range(m):
        t=values[position];position+=1
        if t==1:
            n2=values[position];position+=1;assert 1<=n2<=10**9
            assert group!=1 or n2<=20
            assert group!=2 or n2<=1000
            ops.append((t,n2))
        else:
            assert t==2;j,x=values[position:position+2];position+=2;assert 0<=j<=k and 0<=x<P;ops.append((t,j,x))
    assert position==len(values)
    return n,a,b,ops
def run(slug,text,variant='std'):
    return subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,check=True,timeout=60).stdout.decode()
def permutation_oracle(a,k):
    remaining=sorted(a);rank=0
    for i,x in enumerate(a):rank=rank*(len(a)-i)+remaining.index(x);remaining.remove(x)
    rank=(rank+k)%math.factorial(len(a));remaining=sorted(a);answer=[]
    for i in range(len(a)-1,-1,-1):digit,rank=divmod(rank,math.factorial(i));answer.append(remaining.pop(digit))
    return answer
def leaf_oracle(n,m):
    if n<=2:return int(n==m)
    if not 2<=m<n:return 0
    t=n-m;stirling=[1]+[0]*t
    for _ in range(n-2):
        for j in range(t,0,-1):stirling[j]=(j*stirling[j]+stirling[j-1])%Q
        stirling[0]=0
    return math.comb(n,m)%Q*math.factorial(t)%Q*stirling[t]%Q*(math.factorial(n-1)%Q)%Q
def direct_sum(text):
    n,a,b,ops=validate('dynamic-polynomial-geometric-sum',text);answers=[]
    def evaluate():
        total=0;power=1
        for i in range(1,n+1):
            power=power*a%P;value=0
            for c in b[::-1]:value=(value*i+c)%P
            total=(total+power*value)%P
        return str(total)
    answers.append(evaluate())
    for op in ops:
        if op[0]==1:n=op[1]
        else:b[op[1]]=op[2]
        answers.append(evaluate())
    return answers
def decode_tree(code):
    n=len(code)+2;degree=[1]*n
    for x in code:degree[x]+=1
    leaves=[i for i,d in enumerate(degree) if d==1];heapq.heapify(leaves);edges=[]
    for x in code:
        u=heapq.heappop(leaves);edges.append(tuple(sorted((u,x))));degree[u]-=1;degree[x]-=1
        if degree[x]==1:heapq.heappush(leaves,x)
    edges.append(tuple(sorted(leaves)));return edges
def main():
    rng=random.Random(330089);counts={s:0 for _,s in PROBLEMS}
    permutations=[]
    for n in range(1,7):
        ordered=list(itertools.permutations(range(1,n+1)))
        for i,a in enumerate(ordered):
            for k in [0,1,2,23,len(ordered)-1,len(ordered),2**31-1]:permutations.append((a,k,ordered[(i+k)%len(ordered)]))
    for _ in range(350):
        n=rng.choice([7,8,12,13,14,25,100]);a=list(range(1,n+1));rng.shuffle(a);k=rng.randrange(2**31)
        if rng.randrange(4)==0:a.sort(reverse=True)
        permutations.append((a,k,permutation_oracle(a,k)))
    text=str(len(permutations))+'\n'+''.join(f'{len(a)} {k}\n'+ ' '.join(map(str,a))+'\n' for a,k,ans in permutations);validate('lexicographic-jump',text)
    expected=[str(x) for a,k,ans in permutations for x in ans]
    for v in ['std','alternative']:assert run('lexicographic-jump',text,v).split()==expected,v
    counts['lexicographic-jump']=len(permutations)
    for n in range(9):
        for m in range(n+3):
            answer=leaf_oracle(n,m)
            for slug in ['labeled-leaf-orders','anonymous-leaf-orders']:
                expected=answer if slug.startswith('labeled') or n<=2 else answer*pow(math.factorial(m),Q-2,Q)%Q
                assert run(slug,f'{n} {m}\n').split()==[str(expected)],(slug,n,m,expected);counts[slug]+=1
    canonical_counts={}
    for n in range(2,6):
        orbits=collections.defaultdict(set);labeled=collections.Counter()
        for code in itertools.product(range(n),repeat=n-2):
            edges=decode_tree(code);degree=collections.Counter(x for e in edges for x in e);leaves=[x for x in range(n) if degree[x]<=1];m=len(leaves)
            for order in itertools.permutations(edges):
                labeled[m]+=1;forms=[]
                for renamed in itertools.permutations(leaves):
                    mapping=dict(zip(leaves,renamed));forms.append(tuple(tuple(sorted(mapping.get(x,x) for x in e)) for e in order))
                orbits[m].add(min(forms))
        for m in range(n+1):
            assert run('labeled-leaf-orders',f'{n} {m}\n').split()==[str(labeled[m])]
            assert run('anonymous-leaf-orders',f'{n} {m}\n').split()==[str(len(orbits[m]))]
        canonical_counts[n]={m:len(x) for m,x in orbits.items()}
    for _ in range(250):
        n=rng.randint(1,40);pairs=list(itertools.combinations(range(1,n+1),2));rng.shuffle(pairs);pairs=pairs[:rng.randrange(min(200,len(pairs))+1)]
        text=f'{n} {len(pairs)}\n'+''.join(f'{u} {v}\n' for u,v in pairs)
        for variant in ['std','alternative']:CHECKER.check(text,run('mind-swap-restoration',text,variant))
        counts['mind-swap-restoration']+=1
    for case in range(300):
        n=rng.randint(1,30);k=rng.randint(1,8);a=rng.choice([0,1,2,P-1,rng.randrange(P)]);m=rng.randint(1,20);b=[rng.randrange(P) for _ in range(k+1)]
        ops=[f'1 {rng.randint(1,30)}' if rng.randrange(2) else f'2 {rng.randrange(k+1)} {rng.randrange(P)}' for _ in range(m)]
        text=f'{n} {m} {k} {a}\n'+' '.join(map(str,b))+'\n'+'\n'.join(ops)+'\n';expected=direct_sum(text)
        for variant in ['std','alternative']:assert run('dynamic-polynomial-geometric-sum',text,variant).split()==expected,(case,text,variant)
        counts['dynamic-polynomial-geometric-sum']+=1
    (OUT/'small-checks.json').write_text(json.dumps({'independent_inputs':counts,'anonymous_order_orbits':canonical_counts,'status':'passed'},indent=2)+'\n','utf-8');print(counts,flush=True)
if __name__=='__main__':main()
