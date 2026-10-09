"""Literal small models, cutoff perturbations and reproducible table checks."""
from pathlib import Path
import collections,functools,importlib.util,itertools,json,math,random,re,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R36';P=1000000007
PROBLEMS=[('data-structures','bounded-conveyor'),('combinatorics','white-cell-board'),('number-theory','box-gcd-prefix-sum'),('number-theory','monotone-gcd-sum'),('number-theory','falling-factorial-binomial-sum')]
def module(path):
    spec=importlib.util.spec_from_file_location('loaded_r36',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def run(slug,text,variant='std'):
    return subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,check=True,timeout=180).stdout.decode().split()
def queue_oracle(text):
    lines=text.splitlines();n,m=map(int,lines[0].split());q=collections.deque();out=[]
    for line in lines[1:]:
        z=list(map(int,line.split()))
        if z[0]==1:
            if len(q)<n:q.append(z[1])
        elif q:out.append(str(q.popleft()))
    return out
def phi_array(n):
    a=list(range(n+1))
    for p in range(2,n+1):
        if a[p]==p:
            for j in range(p,n+1,p):a[j]-=a[j]//p
    return a
def direct_box(n,m):
    a=phi_array(n);s=[0]
    for i in range(1,n+1):s.append((s[-1]+pow(i,m,P))%P)
    return sum(a[d]*(d*s[n//d-1]+(n-d*(n//d)+1)*pow(n//d,m,P)) for d in range(1,n+1))%P
def direct_monotone(n,m):
    a=phi_array(n);b=[0,1]
    for q in range(2,n+1):b.append(b[-1]*(q+m-1)*pow(q-1,-1,P)%P)
    return sum(a[d]*b[n//d] for d in range(1,n+1))%P
def falling(n,k):
    if k>n:return 0
    if k<=2000000:
        a=1
        for i in range(n-k+1,n+1):a=a*i%P
    elif P-1-n<=100 and n-k<=100:
        a=P-1
        for i in range(n+1,P):a=a*pow(i,-1,P)%P
        a=a*pow(math.factorial(n-k),-1,P)%P
    else:return None
    return a*pow(2,n-k,P)%P
def main():
    rng=random.Random(3601);counts={s:0 for _,s in PROBLEMS}
    for _ in range(300):
        n=rng.randrange(25);ops=[rng.choice(['2',f'1 {rng.choice([0,-2147483648,2147483647,rng.randrange(-100,101)])}']) for i in range(200)]
        text=f'{n} {len(ops)}\n'+'\n'.join(ops)+'\n';assert run(PROBLEMS[0][1],text)==queue_oracle(text);counts[PROBLEMS[0][1]]+=1
    board=list(map(int,run(PROBLEMS[1][1],'')))
    assert list(map(int,run(PROBLEMS[1][1],'','alternative')))==board
    for n in range(1,5):
        lines=[sum(1<<(i*n+j) for j in range(n)) for i in range(n)]+[sum(1<<(i*n+j) for i in range(n)) for j in range(n)]
        lines += [sum(1<<(i*n+i) for i in range(n)),sum(1<<(i*n+n-1-i) for i in range(n))]
        answer=sum(all(mask&line for line in lines) for mask in range(1<<(n*n)))
        assert board[n]==answer
    counts[PROBLEMS[1][1]]=1+2+16+512+65536
    for n in range(1,7):
        for m in range(1,6):
            box=sum(math.gcd(*xs) for t in range(1,n+1) for xs in itertools.product(range(1,t+1),repeat=m))%P
            mono=sum(math.gcd(*xs) for xs in itertools.combinations_with_replacement(range(1,n+1),m))%P
            for j,want in [(2,box),(3,mono)]:
                assert run(PROBLEMS[j][1],f'{n} {m}\n')==[str(want)];counts[PROBLEMS[j][1]]+=1
    for _ in range(150):
        n=rng.randint(1,3000);m=rng.choice([1,2,3,100000,rng.randint(1,60)])
        for j,oracle in [(2,direct_box),(3,direct_monotone)]:
            want=oracle(n,m)
            for variant in (['std','cutoff-small'] if m<80 else ['std']):
                assert run(PROBLEMS[j][1],f'{n} {m}\n',variant)==[str(want)],(j,n,m,variant,want)
            counts[PROBLEMS[j][1]]+=1
    for n in range(1,30):
        for k in range(1,n+3):
            want=sum(math.prod(range(i-k+1,i+1))*math.comb(n,i) for i in range(1,n+1))%P
            for variant in ['std','alternative']:assert run(PROBLEMS[4][1],f'{n} {k}\n',variant)==[str(want)]
            counts[PROBLEMS[4][1]]+=1
    for _ in range(100):
        n=rng.randint(1,10**9);k=rng.randrange(1,1000)
        for variant in ['std','alternative']:assert run(PROBLEMS[4][1],f'{n} {k}\n',variant)==[str(falling(n,k))]
        counts[PROBLEMS[4][1]]+=1
    negative=0
    for topic,slug in PROBLEMS:
        gen=module(ROOT/'topics'/topic/slug/'tests/generate.py')
        bad=['1'] if slug=='white-cell-board' else ['','-1 1\n','1000000001 1\n','1 0 2\n']
        if slug=='bounded-conveyor':bad=['1 1\n','1 1\n3\n','0 1\n1 2147483648\n','1 1\n2 3\n']
        for text in bad:
            try:gen.validate(text)
            except (AssertionError,ValueError,IndexError):negative+=1
            else:raise AssertionError((slug,text))
    report={'independent_small_checks':counts,'negative_input_checks':negative,'cutoff_variant':'B=80 for m<80; large m checked with production bound'}
    (OUT/'small-checks.json').write_text(json.dumps(report,indent=2)+'\n','utf-8',newline='\n');print(report,flush=True)
if __name__=='__main__':main()
