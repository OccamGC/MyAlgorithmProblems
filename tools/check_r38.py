"""Independent small models and validator checks for R38. Compile binaries into build/R38 first."""
from pathlib import Path
import argparse,importlib.util,itertools,json,math,random,subprocess
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'build/R38';rng=random.Random(380019)
PATHS=[('search','garden-click-coefficient'),('combinatorics','bounded-span-pipelines'),('graphs','nether-portal'),('trees','digging-the-subway'),('graphs','snow-white')]
def load(i):
    t,s=PATHS[i];spec=importlib.util.spec_from_file_location('recipe',ROOT/'topics'/t/s/'tests/generate.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def run(slug,text):return subprocess.check_output([str(B/(slug+'.exe'))],input=text.encode(),timeout=30).decode()
def pipe_oracle(n,k,pipes):
    partner={};weights={}
    for u,v,e in pipes:partner[u]=v;partner[v]=u;weights[u]=weights[v]=2-e
    def enumerate_all(left,chosen):
        if not left:
            return math.prod(weights.get(u,2) for u,v in chosen)
        u=left[0];total=0
        if u not in partner:total+=enumerate_all(left[1:],chosen)
        for v in left[1:]:
            if v-u>k:break
            if partner.get(u,v)!=v or partner.get(v,u)!=u:continue
            if any(a<u<b<v or u<a<v<b for a,b in chosen):continue
            total+=enumerate_all([x for x in left[1:] if x!=v],chosen+[(u,v)])
        return total
    return enumerate_all(list(range(1,n+1)),[])%998244353
def portal_oracle(data):
    rows=[list(map(int,r.split())) for r in data.splitlines()];n,m=rows[0];sw,sx,sy,tw,tx,ty=rows[1];steps=rows[2];p=[(sw,sx,sy,sw,sx,sy,-10**30,0)]+[tuple(r) for r in rows[3:]]+[(tw,tx,ty,tw,tx,ty,-10**30,0)]
    reachable={0}
    for _ in range(n+2):
        for u in list(reachable):
            for v in range(n+2):
                if p[u][3]==p[v][0]:reachable.add(v)
    if n+1 not in reachable:return 'YouNeedOpPermission'
    if steps[tw-1]<0:return 'NegativeInfinity'
    d=[10**30]*(n+2);d[0]=0
    for iteration in range(100000):
        before=d.copy()
        for u in range(n+2):
            if before[u]==10**30:continue
            for v in range(n+2):
                if p[u][3]!=p[v][0]:continue
                candidate=p[v][6] if steps[p[u][3]-1]<0 else max(p[v][6],before[u]+p[u][7]+steps[p[u][3]-1]*(abs(p[u][4]-p[v][1])+abs(p[u][5]-p[v][2])))
                d[v]=min(d[v],candidate)
        if d==before:return str(d[-1])
    raise AssertionError('oracle did not converge')
def subway_oracle(n,marks,edges):
    adj=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):adj[u].append((v,i));adj[v].append((u,i))
    paths=set()
    for s in marks:
        stack=[(s,-1,0)]
        while stack:
            u,p,mask=stack.pop();paths.add(mask)
            for v,e in adj[u]:
                if v!=p:stack.append((v,u,mask|(1<<e)))
    weight=[0]*(1<<(n-1))
    for mask in range(1,len(weight)):
        bit=mask&-mask;weight[mask]=weight[mask^bit]+edges[bit.bit_length()-1][2]
    reached={0};answers=[]
    while (1<<(n-1))-1 not in reached:
        reached={mask|p for mask in reached for p in paths};answers.append(max(weight[v] for v in reached))
    return [len(answers)]+answers
def components(n,edges):
    reach=[1<<i for i in range(n)]
    for u,v in edges:reach[u]|=1<<v
    for k in range(n):
        for i in range(n):
            if reach[i]>>k&1:reach[i]|=reach[k]
    ids=[];reps=[]
    for u in range(n):
        c=next((i for i,v in enumerate(reps) if reach[u]>>v&1 and reach[v]>>u&1),len(reps))
        if c==len(reps):reps.append(u)
        ids.append(c)
    return reach,ids,reps
def formula(n,h,edges):
    reach,ids,reps=components(n,edges);ind=[0]*len(reps);out=ind.copy()
    for u,v in edges:
        if ids[u]!=ids[v]:out[ids[u]]=1;ind[ids[v]]=1
    levels=sorted(set(h));counts={x:[0,0] for x in levels}
    for c,u in enumerate(reps):counts[h[u]][0]+=not ind[c];counts[h[u]][1]+=not out[c]
    if len(levels)==1:return 0 if len(reps)==1 else max(counts[levels[0]])
    for x in levels[1:]:
        if not any(h[u]>=x>h[v] for u,v in edges):return None
    a,b=counts[levels[0]];c,d=counts[levels[-1]]
    return sum(max(a,b) for a,b in counts.values())+1-(b>a)-(c>d)
def brute(n,h,edges):
    want=formula(n,h,edges)
    if want is None:return None
    possible=[(u,v) for u in range(n) for v in range(n) if u!=v and h[u]<=h[v] and (u,v) not in edges];cost=max(h)-min(h)
    for k in range(min(want,len(possible))+1):
        for adds in itertools.combinations(possible,k):
            if sum(h[v]-h[u] for u,v in adds)!=cost:continue
            if components(n,edges+list(adds))[0][0]==(1<<n)-1 and len(components(n,edges+list(adds))[2])==1:return k,adds
    return 'formula impossible'

def main():
    counts={};mods=[load(i) for i in range(5)]
    for n,m in [(1,1),(1,2),(1,3),(2,2)]:
        for a in [0,200,1000]:
            want,*_=mods[0].optimum(n,m,a,'EBTWNDG');reduced,*_=mods[0].optimum(n,m,a)
            assert abs(float(want)-float(reduced))<=1e-12;assert mods[0].matches(run('garden-click-coefficient-std',f'{n} {m} {a}\n'),want)
    counts[PATHS[0][1]]=12;print('garden: all seven plant types on 12 small boards',flush=True)
    for case in range(450):
        n=rng.randint(2,11);k=rng.randint(2,18);used=set();pipes=[]
        for _ in range(n):
            u,v=sorted(rng.sample(range(1,n+1),2))
            if v-u>k or u in used or v in used or any(a<u<b<v or u<a<v<b for a,b,e in pipes):continue
            used|={u,v};pipes.append((u,v,rng.randrange(2)))
        if not pipes:pipes=[(1,2,1)]
        text=f'{n} {k} {len(pipes)}\n'+''.join(f'{u} {v} {e}\n' for u,v,e in pipes);assert int(run('bounded-span-pipelines-std',text))==pipe_oracle(n,k,pipes)
    counts[PATHS[1][1]]=450;print('pipes: 450 direct matching enumerations',flush=True)
    for case in range(1200):
        n=rng.randrange(12);m=rng.randint(1,5);point=lambda:(rng.randint(1,m),rng.randint(-3,3),rng.randint(-3,3));a=point();b=point();steps=[rng.randint(-2,3) for _ in range(m)];rows=[f'{n} {m}',' '.join(map(str,a+b)),' '.join(map(str,steps))]
        for _ in range(n):rows.append(' '.join(map(str,point()+point()+(rng.randint(-10,10),rng.randint(-10,10)))))
        text='\n'.join(rows)+'\n';want=portal_oracle(text)
        for variant in ['std','alternative-deadline']:assert run('nether-portal-'+variant,text).split()==[want]
    counts[PATHS[2][1]]=1200;print('portals: 1200 literal fixed points for both programs',flush=True)
    for case in range(1000):
        n=rng.randint(2,10);marks=rng.sample(range(n),rng.randint(1,n));edges=[(u,rng.randrange(u),rng.randint(1,100)) for u in range(1,n)];text=f'{n} {len(marks)}\n'+' '.join(str(u+1) for u in marks)+'\n'+''.join(f'{u+1} {v+1} {w}\n' for u,v,w in edges)
        assert list(map(int,run('digging-the-subway-std',text).split()))==subway_oracle(n,marks,edges)
    counts[PATHS[3][1]]=1000;print('tree: 1000 direct path-union enumerations',flush=True)
    for case in range(2500):
        n=rng.randint(1,40);h=[rng.randint(-3,3) for _ in range(n)];edges=[(u,v) for u in range(n) for v in range(n) if h[u]>=h[v] and rng.random()<.12] or [(0,0)];text=f'{n} {len(edges)}\n'+' '.join(map(str,h))+'\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges);out=run('snow-white-std',text);assert mods[4].check_output(text,out);want=formula(n,h,edges)
        assert (list(map(int,out.split()))==[-1]) if want is None else int(out.split()[1])==want
    for case in range(300):
        n=rng.randint(2,5);h=[rng.randrange(3) for _ in range(n)];edges=[(u,v) for u in range(n) for v in range(n) if u!=v and h[u]>=h[v] and rng.random()<.25];want=formula(n,h,edges);actual=brute(n,h,edges)
        assert actual is None if want is None else actual!='formula impossible' and actual[0]==want
    counts[PATHS[4][1]]={'construction_graphs':2500,'exhaustive_optima':300};print('height: 2500 constructions and 300 exhaustive optima',flush=True)
    bad=[['0 1 0\n','3 3 0\n','1 1 1001\n'],['2 1 1\n1 2 1\n','3 2 2\n1 2 1\n2 3 0\n'],['0 1\n1 0 0 1 0 0\n11\n'],['1001 1\n1\n','2 1\n1\n1 2 0\n','3 2\n1 1\n1 2 1\n2 3 1\n'],['2 1\n0 1\n1 2\n','1 1\n1000000001\n1 1\n']]
    rejected=0
    for mod,cases in zip(mods,bad):
        for text in cases:
            try:mod.validate(text)
            except (AssertionError,ValueError,IndexError):rejected+=1
            else:raise AssertionError(('accepted invalid input',text))
    result={'seed':380019,'independent_inputs_or_states':counts,'invalid_inputs_rejected':rejected};(B/'small-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8',newline='\n');print(result,flush=True)
if __name__=='__main__':main()
