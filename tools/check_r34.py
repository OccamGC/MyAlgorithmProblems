"""R34 input validation and independent small-instance models."""
from pathlib import Path
import collections,heapq,importlib.util,itertools,json,random,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R34'
PROBLEMS=[('data-structures','dynamic-decreasing-stack'),('scheduling','shared-charger'),('trees','tolerance-paths'),('interactive','substring-permutation'),('data-structures','you-wrote-this-problem')]
MASK=(1<<64)-1
def module(path):
    spec=importlib.util.spec_from_file_location('r34_loaded',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
JUDGE=module(ROOT/'topics/interactive/substring-permutation/judge.py')
def run(slug,text,variant='std'):
    return subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,check=True,timeout=90).stdout.decode()
def encode_pairs(a,ops):
    current=a[:];last=0;lines=[f'{len(a)} {len(ops)}',' '.join(map(str,a))];answers=[]
    for op in ops:
        lines.append(' '.join(str((v&MASK)^last) for v in op))
        if op[0]==1:current[op[1]-1]=op[2]
        else:
            _,l,r,x,y=op;c=collections.Counter(current[l-1:r]);d=collections.Counter(current[x-1:y]);last=sum(v*d[k] for k,v in c.items());answers.append(last)
    return '\n'.join(lines)+'\n',answers
def validate(slug,text,group=3,answers=None):
    z=list(map(int,text.split()));assert z
    if slug=='substring-permutation':
        hidden=JUDGE.read_hidden(text);assert group!=1 or len(hidden)<=8;assert group!=2 or len(hidden)<=50;return hidden
    n,m=z[:2];at=2
    if slug=='shared-charger':
        assert 1<=n<=500000 and 1<=m<=500000 and len(z)==2+2*n
        a=z[2:2+n];b=z[2+n:];assert all(0<=v<=10**16 for v in a) and all(0<=v<=10**9 for v in b)
        assert group!=1 or n<=50 and m<=50 and max(b)<=5
        assert group!=2 or n<=200 and m<=200 and max(b)<=20
        assert group!=3 or n<=200 and m<=200
        assert group!=4 or n<=50000 and m<=50000
        return n,m,a,b
    if slug=='tolerance-paths':
        assert 1<=n<=1000 and 0<=m<=20000 and len(z)==2+2*(n-1)+2*n+2*m
        edges=[];parent=list(range(n))
        def find(x):
            while parent[x]!=x:x=parent[x]
            return x
        for _ in range(n-1):
            u,v=z[at:at+2];at+=2;assert 1<=u<=n and 1<=v<=n and find(u-1)!=find(v-1);parent[find(u-1)]=find(v-1);edges.append((u-1,v-1))
        bounds=[]
        for _ in range(n):
            l,r=z[at:at+2];at+=2;assert -10**9<=l<=r<=10**9;bounds.append((l,r))
        weights=[[] for _ in edges]
        for _ in range(m):
            e,w=z[at:at+2];at+=2;assert 1<=e<n and -10**9<=w<=10**9;weights[e-1].append(w)
        assert group!=1 or n<=8 and m<=15
        assert group!=2 or n<=100 and m<=1000
        return edges,bounds,weights
    limit=50000 if slug=='dynamic-decreasing-stack' else 100000
    assert 1<=n<=limit and 1<=m<=(50000 if slug=='dynamic-decreasing-stack' else 10000)
    assert group!=1 or n<=50 and m<=100
    assert group!=2 or n<=2000 and m<=2000
    a=z[at:at+n];at+=n;assert len(a)==n
    assert all((0 if slug=='dynamic-decreasing-stack' else -10**9)<=v<=10**9 for v in a)
    ops=[];last=0;query_count=0;current=a[:]
    for _ in range(m):
        if slug=='dynamic-decreasing-stack':
            t,x,y=z[at:at+3];at+=3;assert t in [1,2]
            assert 1<=x<=n and (0<=y<=10**9 if t==1 else x<=y<=n);ops.append((t,x,y))
        else:
            raw=z[at];at+=1;assert 0<=raw<=MASK;t=raw^last;assert t in [1,2];size=2 if t==1 else 4
            raw=z[at:at+size];at+=size;assert len(raw)==size and all(0<=v<=MASK for v in raw);v=[x^last for x in raw]
            if t==1:
                x,y=v;y=y if y<1<<63 else y-(1<<64);assert 1<=x<=n and abs(y)<=10**9;current[x-1]=y;ops.append((t,x,y))
            else:
                l,r,x,y=v;assert 1<=l<=r<=n and 1<=x<=y<=n;ops.append((t,*v))
                if answers is None:
                    c=collections.Counter(current[l-1:r]);d=collections.Counter(current[x-1:y]);last=sum(v*d[k] for k,v in c.items())
                else:last=int(answers[query_count]);assert 0<=last<=(r-l+1)*(y-x+1)
                query_count+=1
    assert at==len(z)
    assert answers is None or query_count==len(answers)
    return a,ops
def stack_oracle(text):
    a,ops=validate('dynamic-decreasing-stack',text);out=[]
    for t,x,y in ops:
        if t==1:a[x-1]=y
        else:
            stack=[]
            for v in a[x-1:y]:
                while stack and stack[-1]<=v:stack.pop()
                stack.append(v)
            out.append(len(stack))
    return out
def charger_brute(a,b,m):
    def feasible(power):
        states={tuple(a)}
        for minute in range(m):
            new=set()
            for state in states:
                for chosen in range(-1,len(a)):
                    nxt=tuple(state[i]+(power if i==chosen else 0)-b[i] for i in range(len(a)))
                    if min(nxt)>=0:new.add(tuple(min(v,(m-minute-1)*b[i]) for i,v in enumerate(nxt)))
            states=new
        return bool(states)
    for power in range(m*max(b,default=0)+1):
        if feasible(power):return power
    return -1
def charger_heap(a,b,m):
    def feasible(power):
        q=[(a[i]//b[i],i,a[i]) for i in range(len(a)) if a[i]<m*b[i]];heapq.heapify(q)
        for t in range(m):
            if not q:return True
            deadline,i,energy=heapq.heappop(q)
            if deadline<t:return False
            energy+=power
            if energy<m*b[i]:heapq.heappush(q,(energy//b[i],i,energy))
        return not q
    high=max([0]+[m*y-x for x,y in zip(a,b)])
    if not feasible(high):return -1
    low=0
    while low<high:
        mid=(low+high)//2
        if feasible(mid):high=mid
        else:low=mid+1
    return low
def noise_oracle(text):
    edges,bounds,weights=validate('tolerance-paths',text);n=len(bounds);adj=[[] for _ in range(n)]
    for e,(u,v) in enumerate(edges):adj[u].append((v,e));adj[v].append((u,e))
    answers=[]
    for start in range(n):
        reached={start};stack=[(start,-1,None)]
        # Enumerate all feasible edge-weight assignments, not intervals or binary search.
        while stack:
            u,parent,previous=stack.pop()
            for v,e in adj[u]:
                if v==parent:continue
                for w in set(weights[e]):
                    if previous is None or bounds[u][0]<=w-previous<=bounds[u][1]:reached.add(v);stack.append((v,u,w))
        answers.append(len(reached))
    return answers
def main():
    rng=random.Random(340061);counts={s:0 for _,s in PROBLEMS}
    for test in range(300):
        n=rng.choice([1,2,20,227,500]);m=100;a=[rng.randrange(10) for _ in range(n)];ops=[]
        for _ in range(m):
            if rng.randrange(3)==0:ops.append((1,rng.randint(1,n),rng.choice([0,10**9,rng.randrange(10)])))
            else:l,r=sorted([rng.randint(1,n),rng.randint(1,n)]);ops.append((2,l,r))
        text=f'{n} {m}\n'+' '.join(map(str,a))+'\n'+''.join(' '.join(map(str,op))+'\n' for op in ops);expected=list(map(str,stack_oracle(text)))
        for v in ['std','alternative']:assert run('dynamic-decreasing-stack',text,v).split()==expected,(test,v)
        counts['dynamic-decreasing-stack']+=1
    for test in range(250):
        n=rng.randint(1,3);m=rng.randint(1,4);a=[rng.randrange(10) for _ in range(n)];b=[rng.randrange(4) for _ in range(n)]
        expected=charger_brute(a,b,m);assert expected==charger_heap(a,b,m)
        text=f'{n} {m}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'
        for v in ['std','alternative']:assert run('shared-charger',text,v).split()==[str(expected)],(test,text,v,expected)
        counts['shared-charger']+=1
    for test in range(250):
        n=rng.randint(1,8);m=0 if n==1 else rng.randrange(16);edges=[(rng.randrange(v),v) for v in range(1,n)];bounds=[sorted([rng.randrange(-4,5),rng.randrange(-4,5)]) for _ in range(n)];special=[(rng.randrange(n-1)+1,rng.randrange(-5,6)) for _ in range(m)]
        text=f'{n} {m}\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges)+''.join(f'{l} {r}\n' for l,r in bounds)+''.join(f'{e} {w}\n' for e,w in special)
        assert run('tolerance-paths',text).split()==list(map(str,noise_oracle(text))),(test,text)
        counts['tolerance-paths']+=1
    maximum=0
    for n in range(1,7):
        for p in itertools.permutations(range(1,n+1)):
            text=f'{n}\n'+' '.join(map(str,p))+'\n';output=list(map(int,run('substring-permutation',text,'simulate').split()));assert output[:-1]==list(p);maximum=max(maximum,output[-1]);counts['substring-permutation']+=1
    for test in range(150):
        n=rng.choice([99,100,101,119,120]);p=list(range(1,n+1));rng.shuffle(p)
        result=JUDGE.run(OUT/'substring-permutation-std.exe',p);maximum=max(maximum,result['queries']);counts['substring-permutation']+=1
        if test<25:
            for query in result['trace']:
                q=query['query'];dp=[0]*(n+1);best=0
                for x in q:
                    nxt=[0]*(n+1)
                    for j,y in enumerate(p,1):
                        if x==y:nxt[j]=dp[j-1]+1;best=max(best,nxt[j])
                    dp=nxt
                assert best==query['reply']
    for test in range(300):
        n=rng.choice([1,2,50,399,400,401,801,1601]);a=[rng.randrange(-8,9) for _ in range(n)];ops=[]
        for i in range(100):
            if rng.randrange(2):ops.append((1,rng.randint(1,n),rng.choice([-10**9,10**9,rng.randrange(-8,9)])))
            else:
                l,r=sorted([rng.randint(1,n),rng.randint(1,n)]);x,y=sorted([rng.randint(1,n),rng.randint(1,n)])
                if i%4==0:l=x=1;r=y=n
                ops.append((2,l,r,x,y))
        text,answers=encode_pairs(a,ops);validate('you-wrote-this-problem',text,answers=answers)
        assert run('you-wrote-this-problem',text).split()==list(map(str,answers)),(test,text)
        counts['you-wrote-this-problem']+=1
    report={'status':'passed','independent_inputs':counts,'maximum_interactive_queries_seen':maximum,'actual_pipe_interactions':150,'lcs_oracle_independent_dp_sessions':25}
    (OUT/'small-checks.json').write_text(json.dumps(report,indent=2)+'\n','utf-8');print(report,flush=True)
if __name__=='__main__':main()
