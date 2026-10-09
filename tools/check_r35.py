"""Independent models and input validation for the final five-problem batch."""
from pathlib import Path
import collections,heapq,importlib.util,itertools,json,math,random,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R35';P=1000000007
PROBLEMS=[('constructive','lower-weight-imperfect-non-matching'),('data-structures','batched-rectangle-maximum'),('probability','unique-substring-hits'),('trees','path-neighborhood-updates'),('graphs','closed-edge-survey')]
def module(path):
    spec=importlib.util.spec_from_file_location('r35_loaded',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
CHECKER=module(ROOT/'topics/constructive/lower-weight-imperfect-non-matching/checker.py')
def run(slug,text,variant='std'):
    return subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode('ascii'),capture_output=True,check=True,timeout=180).stdout.decode()
def validate(slug,text,group=None):
    if slug=='lower-weight-imperfect-non-matching':
        n,edges,b=CHECKER.read_input(text);assert group!=1 or n<=8 and len(edges)<=15;assert group!=2 or n<=1000 and len(edges)<=3000;return n,edges,b
    if slug=='unique-substring-hits':
        tokens=text.split();assert len(tokens)>=3;n=int(tokens[0]);q=int(tokens[1]);s=tokens[2];targets=list(map(int,tokens[3:]));assert 1<=n<=100000 and 1<=q<=500 and len(s)==n and len(targets)==q and all(33<=ord(c)<=126 for c in s) and all(0<=x<=10**18 for x in targets)
        assert group!=1 or n<=20
        assert group!=2 or n<=2000
        return s,targets
    z=list(map(int,text.split()));assert z
    if slug=='batched-rectangle-maximum':
        n,m,q=z[:3];assert n>=1 and m>=1 and n*m<=10000000 and 1<=q<=100000
        a=z[3:3+n*m];assert len(a)==n*m and all(abs(v)<=20000 for v in a);at=3+n*m;ops=[];runs=0;last=0
        for _ in range(q):
            t,x1,y1,x2,y2=z[at:at+5];at+=5;assert t in [1,2] and 1<=x1<=x2<=n and 1<=y1<=y2<=m
            op=[t,x1,y1,x2,y2]
            if t==1:
                v=z[at];at+=1;assert abs(v)<=20000;op.append(v);runs+=last!=1
            last=t;ops.append(op)
        assert at==len(z) and runs<=20
        assert group!=1 or n*m<=100 and q<=100
        assert group!=2 or n*m<=100000 and q<=5000
        return n,m,a,ops
    n,m=z[:2];at=2
    if slug=='closed-edge-survey':
        assert 2<=n<=100000 and n-1<=m<=200000 and len(z)==2+3*m;edges=[];degree=[0]*n;parent=list(range(n))
        def find(u):
            while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
            return u
        for _ in range(m):
            u,v,w=z[at:at+3];at+=3;assert 1<=u<=n and 1<=v<=n and u!=v and 0<=w<=1000;u-=1;v-=1;edges.append((u,v,w));degree[u]+=1;degree[v]+=1;parent[find(u)]=find(v)
        assert len({find(u) for u in range(n)})==1;odd=sum(d%2 for d in degree);assert m==n-1 or odd<=20
        assert group!=1 or m==n-1
        assert group!=2 or m>=n and odd==0
        assert group!=3 or m>=n and odd<=20
        return n,edges
    assert 1<=n<=100000 and 1<=m<=100000;edges=[];parent=list(range(n))
    def find(u):
        while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
        return u
    for _ in range(n-1):
        u,v=z[at:at+2];at+=2;assert 1<=u<=n and 1<=v<=n and find(u-1)!=find(v-1);parent[find(u-1)]=find(v-1);edges.append((u-1,v-1))
    ops=[]
    for _ in range(m):
        t,a=z[at:at+2];at+=2;assert 1<=t<=12 and 1<=a<=n;op=[t,a]
        if (t-1)%3!=2:
            b=z[at];at+=1;assert 1<=b<=n;op.append(b)
        if t<=6:
            v=z[at];at+=1;assert abs(v)<=100000000;op.append(v)
        ops.append(op)
    assert at==len(z)
    assert group!=1 or n<=30 and m<=100
    assert group!=2 or n<=2000 and m<=2000
    return n,edges,ops
def grid_oracle(text):
    n,m,a,ops=validate('batched-rectangle-maximum',text);out=[]
    for t,x1,y1,x2,y2,*v in ops:
        cells=[(i-1)*m+j-1 for i in range(x1,x2+1) for j in range(y1,y2+1)]
        if t==1:
            for k in cells:a[k]+=v[0]
        else:out.append(str(max(a[k] for k in cells)))
    return out
def rational_answer(target,distinct,unique):
    numerator=target*distinct;g=math.gcd(numerator,unique);numerator//=g;denominator=unique//g
    return -1 if denominator%P==0 else numerator%P*pow(denominator,P-2,P)%P
def substring_oracle(text):
    s,targets=validate('unique-substring-hits',text);c=collections.Counter(s[i:j] for i in range(len(s)) for j in range(i+1,len(s)+1));d=len(c);u=sum(v==1 for v in c.values());return [str(rational_answer(t,d,u)) for t in targets]
def tree_oracle(text):
    n,edges,ops=validate('path-neighborhood-updates',text);adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    parent=[-1]*n;order=[0]
    for u in order:
        for v in adj[u]:
            if v!=parent[u]:parent[v]=u;order.append(v)
    descendant=[{u} for u in range(n)]
    for u in order[:0:-1]:descendant[parent[u]]|=descendant[u]
    def path(a,b):
        prev={a:-1};queue=[a]
        for u in queue:
            if u==b:break
            for v in adj[u]:
                if v not in prev:prev[v]=u;queue.append(v)
        result=set()
        while b!=-1:result.add(b);b=prev[b]
        return result
    a=[0]*n;out=[]
    for op in ops:
        t=op[0];region=(t-1)%3;action=(t-1)//3
        if region==2:vertices=descendant[op[1]-1]
        else:
            route=path(op[1]-1,op[2]-1);vertices=route if region==0 else {v for u in route for v in adj[u]}-route
        if action==0:
            for u in vertices:a[u]+=op[-1]
        elif action==1:
            for u in vertices:a[u]=op[-1]
        elif action==2:out.append(str(max(a[u] for u in vertices)) if vertices else 'EMPTY')
        else:out.append(str(sum(a[u] for u in vertices)))
    return out
def route_oracle(text):
    n,edges=validate('closed-edge-survey',text);m=len(edges);adj=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):adj[u].append((v,w,1<<i));adj[v].append((u,w,1<<i))
    distance={(0,0):0};queue=[(0,0,0)]
    while queue:
        d,u,mask=heapq.heappop(queue)
        if distance.get((u,mask))!=d:continue
        if u==0 and mask==(1<<m)-1:return ['1',str(d)]
        for v,w,bit in adj[u]:
            state=(v,mask|bit);nd=d+w
            if nd<distance.get(state,10**100):distance[state]=nd;heapq.heappush(queue,(nd,*state))
    raise AssertionError('unreachable')
def main():
    rng=random.Random(350079);counts={s:0 for _,s in PROBLEMS}
    for case in range(250):
        n=rng.randint(1,8);edges=[(v,rng.randrange(v),rng.randrange(10)) for v in range(1,n)]
        edges += [(rng.randrange(n),rng.randrange(n),rng.randrange(10)) for _ in range(rng.randrange(8))]
        text=f'{n} {len(edges)}\n'+''.join(f'{u+1} {v+1} {w}\n' for u,v,w in edges);answer=CHECKER.check(text,run('lower-weight-imperfect-non-matching',text));assert answer['score']==100 and answer['distance']==answer['baseline'];counts['lower-weight-imperfect-non-matching']+=1
    for case in range(300):
        n=rng.randint(1,8);m=rng.randint(1,8);a=[rng.randint(-20,20) for _ in range(n*m)];ops=[]
        for i in range(60):
            x1,x2=sorted([rng.randint(1,n),rng.randint(1,n)]);y1,y2=sorted([rng.randint(1,m),rng.randint(1,m)]);t=1 if i%4<2 else 2;op=[t,x1,y1,x2,y2]
            if t==1:op.append(rng.choice([-20000,20000,rng.randint(-20,20)]))
            ops.append(op)
        text=f'{n} {m} {len(ops)}\n'+' '.join(map(str,a))+'\n'+''.join(' '.join(map(str,op))+'\n' for op in ops);assert run('batched-rectangle-maximum',text).split()==grid_oracle(text),(case,text);counts['batched-rectangle-maximum']+=1
    strings=[''.join(p) for n in range(1,9) for p in itertools.product('ab',repeat=n)]
    strings += [''.join(rng.choice('aabC09!~\\') for _ in range(rng.randint(1,35))) for _ in range(150)]
    for s in strings:
        targets=[0,1,4,2**31,10**18,P];text=f'{len(s)} {len(targets)}\n{s}\n'+'\n'.join(map(str,targets))+'\n';expected=substring_oracle(text)
        for v in ['std','alternative']:assert run('unique-substring-hits',text,v).split()==expected,(s,v,expected)
        counts['unique-substring-hits']+=1
    a,b,c=11879,2,84166;s='a'*a+'b'*b+'c'*c;d=a*b+b*c+a*c+a+b+c;u=a*b+b*c+a*c+3;assert u==P
    targets=[0,1,4,P,2*P,P*(P-15),10**18];text=f'{len(s)} {len(targets)}\n{s}\n'+'\n'.join(map(str,targets))+'\n';validate('unique-substring-hits',text);expected=[str(rational_answer(t,d,u)) for t in targets]
    for v in ['std','alternative']:assert run('unique-substring-hits',text,v).split()==expected,v
    counts['unique-substring-hits']+=1
    singular={'length':len(s),'D':d,'U':u,'expected':expected}
    for case in range(350):
        n=rng.choice([1,2,8,25,50]);edges=[(v,rng.randrange(v)) for v in range(1,n)];rng.shuffle(edges);ops=[]
        for i in range(120):
            t=i%12+1;a=rng.randrange(n)+1;op=[t,a]
            if (t-1)%3!=2:op.append(rng.randrange(n)+1)
            if t<=6:op.append(rng.choice([-100000000,100000000,0,rng.randrange(-100,101)]))
            ops.append(op)
        text=f'{n} {len(ops)}\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges)+''.join(' '.join(map(str,op))+'\n' for op in ops)
        assert run('path-neighborhood-updates',text).split()==tree_oracle(text),(case,text);counts['path-neighborhood-updates']+=1
    for case in range(250):
        n=rng.randint(2,7);edges=[(v,rng.randrange(v),rng.randrange(6)) for v in range(1,n)]
        for _ in range(rng.randrange(5)):
            u,v=rng.sample(range(n),2);edges.append((u,v,rng.randrange(6)))
        text=f'{n} {len(edges)}\n'+''.join(f'{u+1} {v+1} {w}\n' for u,v,w in edges);assert run('closed-edge-survey',text).split()==route_oracle(text),(case,text);counts['closed-edge-survey']+=1
    result={'status':'passed','independent_inputs':counts,'singular_denominator_counts':singular}
    (OUT/'small-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');print(result,flush=True)
if __name__=='__main__':main()
