"""Independent oracles, input validation and differential checks for R21."""
from pathlib import Path
from array import array
import heapq,itertools,json,math,random,subprocess
from check_candy_signed import candy_oracle, validate as validate_candy_signed

ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('strings','candy-brackets'),('number-theory','permutation-order'),('probability','grid-survival'),('graphs','nearest-terminal-sets'),('graphs','shortest-path-queries')]
VARIANTS={s:['std'] if s in ['candy-brackets','permutation-order'] else ['std','alternative'] for _,s in PROBLEMS}
MOD=7881299347898369

def candy_brute(text):
    rows=text.splitlines();n,m=map(int,rows[0].split())
    sequence=list(zip(map(int,rows[1].split()),map(int,rows[2].split())))
    def solve():
        best=0
        for i in range(len(sequence)):
            balance=weight=0
            for kind,value in sequence[i:]:
                balance+=(1 if kind==0 else -1 if kind==1 else 0);weight+=value
                if balance<0:break
                if balance==0:best=max(best,weight)
        return best
    answers=[solve()]
    for row in rows[3:]:
        side,kind,value=map(int,row.split())
        if side==0:sequence.insert(0,(kind,value))
        else:sequence.append((kind,value))
        answers.append(solve())
    return '\n'.join(map(str,answers))+'\n'

def permutation_oracle(text):
    values=list(map(int,text.split()));n=values[0];a=[x-1 for x in values[1:]];answer=1
    seen=bytearray(n)
    for start in range(n):
        if seen[start]:continue
        u=start;length=0
        while not seen[u]:seen[u]=1;length+=1;u=a[u]
        answer=math.lcm(answer,length)
    return str(answer%998244353)+'\n'

def walk_line(length,k):
    width=min(length,2*k+1);current=[1]*width;totals=[]
    for step in range(k+1):
        totals.append(sum(current)+(length-width)*(2**step))
        current=[(current[i-1] if i else 0)+(current[i+1] if i+1<width else 0) for i in range(width)]
    return totals

def grid_oracle(text):
    rows=text.splitlines();n,m,k=map(int,rows[0].split());grid=''.join(rows[1:])
    if '0' not in grid:
        a=walk_line(n,k);b=walk_line(m,k)
        total=sum(math.comb(k,t)*a[t]*b[k-t] for t in range(k+1))
    else:
        ids={p:i for i,p in enumerate(p for p,c in enumerate(grid) if c=='1')}
        neighbors=[]
        for p in ids:
            around=[]
            if p%m:around.append(p-1)
            if p%m+1<m:around.append(p+1)
            if p>=m:around.append(p-m)
            if p+m<n*m:around.append(p+m)
            neighbors.append([ids[x] for x in around if x in ids])
        current=[1]*len(ids)
        for _ in range(k):current=[sum(current[j] for j in adjacent) for adjacent in neighbors]
        total=sum(current)
    return str(total*pow(n*m*(4**k),-1,MOD)%MOD)+'\n'

def dijkstra(graph,sources):
    inf=10**30;distance=[inf]*len(graph);queue=[]
    for u in sources:distance[u]=0;queue.append((0,u))
    heapq.heapify(queue)
    while queue:
        weight,u=heapq.heappop(queue)
        if weight!=distance[u]:continue
        for v,c in graph[u].items():
            if weight+c<distance[v]:distance[v]=weight+c;heapq.heappush(queue,(weight+c,v))
    return distance

def graph_data(text,terminal=False):
    rows=text.splitlines();head=list(map(int,rows[0].split()));n,m=head[:2]
    labels=list(map(int,rows[1].split())) if terminal else None;offset=2 if terminal else 1
    graph=[{} for _ in range(n)]
    for row in rows[offset:offset+m]:
        u,v,c=map(int,row.split());u-=1;v-=1
        graph[u][v]=min(graph[u].get(v,10**30),c);graph[v][u]=min(graph[v].get(u,10**30),c)
    return graph,labels,rows[offset+m:]

def terminals_oracle(text):
    graph,labels,_=graph_data(text,True);d=dijkstra(graph,[i for i,c in enumerate(labels) if c==0])
    answer=min((d[i] for i,c in enumerate(labels) if c==1),default=10**30)
    return str(-1 if answer==10**30 else answer)+'\n'

def queries_oracle(text):
    graph,_,rows=graph_data(text);cache={};answer=[]
    for row in rows:
        u,v=map(int,row.split());u-=1;v-=1
        if u not in cache:cache[u]=dijkstra(graph,[u])
        distance=cache[u][v];answer.append(str(-1 if distance==10**30 else distance))
    return '\n'.join(answer)+'\n'

ORACLES=dict(zip([s for _,s in PROBLEMS],[candy_oracle,permutation_oracle,grid_oracle,terminals_oracle,queries_oracle]))

def validate(slug,text,group=None):
    rows=text.splitlines()
    if slug=='candy-brackets':
        return validate_candy_signed(text,group)
    if slug=='permutation-order':
        assert len(rows)==2;n=int(rows[0]);assert 1<=n<=10**6
        a=list(map(int,rows[1].split()));assert len(a)==n and len(set(a))==n and min(a)==1 and max(a)==n
        return dict(N=n)
    if slug=='grid-survival':
        n,m,k=map(int,rows[0].split());assert 1<=n*m<=10**6 and n>=1 and m>=1 and 0<=k<=25
        assert len(rows)==n+1 and all(len(row)==m and set(row)<={'0','1'} for row in rows[1:])
        return dict(n=n,m=m,k=k,roads=sum(row.count('1') for row in rows[1:]))
    terminal=slug=='nearest-terminal-sets'
    head=list(map(int,rows[0].split()));n,m=head[:2];assert 1<=n<=500000 and 1<=m<=500000
    offset=2 if terminal else 1
    if terminal:
        labels=list(map(int,rows[1].split()));assert len(labels)==n and set(labels)<={0,1,2} and len(rows)==m+2
        if group in [1,2]:assert labels.count(0)<=1 and labels.count(1)<=1
        if group==1:assert n<=500
    else:
        q=head[2];assert 1<=q<=500000 and (q==1 or n<=500) and len(rows)==m+q+1
        if group in [1,2]:assert q==1
        if group in [2,3]:assert n<=500
        for row in rows[offset+m:]:
            u,v=map(int,row.split());assert 1<=u<=n and 1<=v<=n
    for row in rows[offset:offset+m]:
        u,v,c=map(int,row.split());assert 1<=u<=n and 1<=v<=n and 0<=c<=10**9
    return dict(n=n,m=m,**({'S':labels.count(0),'T':labels.count(1)} if terminal else {'q':q}))

def run_case(slug,text,expected=None):
    validate(slug,text)
    expected=ORACLES[slug](text) if expected is None else expected
    for variant in VARIANTS[slug]:
        actual=subprocess.check_output([str(ROOT/'build/bin'/f'{slug}-{variant}.exe')],input=text.encode('ascii'),timeout=60).decode('ascii').replace('\r\n','\n')
        assert actual==expected,(slug,variant,text[:300],actual[:300],expected[:300])

def floyd_oracle(n,edges):
    d=[[10**30]*n for _ in range(n)]
    for i in range(n):d[i][i]=0
    for u,v,c in edges:d[u][v]=min(d[u][v],c);d[v][u]=min(d[v][u],c)
    for k in range(n):
        for i in range(n):
            for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return d

def main():
    rng=random.Random(2026100121);report={};count=0
    for n in range(6):
        for types in itertools.product(range(3),repeat=n):
            weights=[rng.choice([-4000000000,-1,0,1,4000000000]) for _ in types]
            text=f'{n} 0\n'+' '.join(map(str,types))+'\n'+' '.join(map(str,weights))+'\n'
            expected=candy_brute(text);assert expected==candy_oracle(text);run_case('candy-brackets',text,expected);count+=1
    for _ in range(200):
        n=rng.randrange(10);m=20
        text=f'{n} {m}\n'+' '.join(str(rng.randrange(3)) for _ in range(n))+'\n'+' '.join(str(rng.choice([-4000000000,-1,0,1,4000000000])) for _ in range(n))+'\n'+''.join(f'{rng.randrange(2)} {rng.randrange(3)} {rng.randrange(-4000000000,4000000001)}\n' for _ in range(m))
        expected=candy_brute(text);assert expected==candy_oracle(text);run_case('candy-brackets',text,expected)
    report['candy-brackets']=dict(exhaustive_type_strings=count,random_update_batches=200,operations=4000,formal_oracle='offline sibling-atom activation and maximum-subarray DSU')
    count=0
    for n in range(1,7):
        for a in itertools.permutations(range(n)):
            b=list(range(n));step=0
            while True:
                nxt=[0]*n
                for i in range(n):nxt[a[i]]=b[i]
                b=nxt;step+=1
                if b==list(range(n)):break
            text=str(n)+'\n'+' '.join(str(x+1) for x in a)+'\n';expected=str(step)+'\n'
            assert expected==permutation_oracle(text);run_case('permutation-order',text,expected);count+=1
    report['permutation-order']=dict(exhaustive_permutations=count,formal_oracle='arbitrary precision integer LCM')
    count=0
    for n,m in [(1,1),(1,3),(2,2),(2,3)]:
        for mask in range(1<<(n*m)):
            grid=['1' if mask>>i&1 else '0' for i in range(n*m)]
            for k in range(4):
                total=0
                for start in range(n*m):
                    for moves in itertools.product(range(4),repeat=k):
                        i,j=divmod(start,m);valid=grid[start]=='1'
                        for move in moves:
                            di,dj=[(-1,0),(1,0),(0,-1),(0,1)][move];i+=di;j+=dj
                            if not (0<=i<n and 0<=j<m) or grid[i*m+j]=='0':valid=False;break
                        total+=valid
                text=f'{n} {m} {k}\n'+'\n'.join(''.join(grid[i*m:(i+1)*m]) for i in range(n))+'\n'
                expected=str(total*pow(n*m*4**k,-1,MOD)%MOD)+'\n';assert grid_oracle(text)==expected
                run_case('grid-survival',text,expected);count+=1
    report['grid-survival']=dict(exhaustive_grid_step_cases=count,formal_oracle='exact integer walks; separable full rectangles')
    for slug in ['nearest-terminal-sets','shortest-path-queries']:
        for iteration in range(200):
            n=rng.randint(1,12);m=rng.randint(1,50);edges=[(rng.randrange(n),rng.randrange(n),rng.choice([0,1,10**9,rng.randrange(100)])) for _ in range(m)]
            d=floyd_oracle(n,edges);edge_text=''.join(f'{u+1} {v+1} {c}\n' for u,v,c in edges)
            if slug=='nearest-terminal-sets':
                labels=[rng.randrange(3) for _ in range(n)];answer=min((d[u][v] for u in range(n) for v in range(n) if labels[u]==0 and labels[v]==1),default=10**30)
                text=f'{n} {m}\n'+' '.join(map(str,labels))+'\n'+edge_text;expected=str(-1 if answer==10**30 else answer)+'\n'
            else:
                text=f'{n} {m} {n*n}\n'+edge_text+''.join(f'{u+1} {v+1}\n' for u in range(n) for v in range(n))
                expected=''.join(str(-1 if x==10**30 else x)+'\n' for row in d for x in row)
            assert ORACLES[slug](text)==expected;run_case(slug,text,expected)
        report[slug]=dict(random_multigraphs=200,small_oracle='independent Floyd-Warshall',formal_oracle='Python heap Dijkstra after parallel-edge minimization')
    (ROOT/'build/R21/checks.json').write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
