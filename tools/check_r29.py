from pathlib import Path
import json,random,subprocess,collections,itertools,sys,time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R29'
RNG=random.Random(29031)
def run(slug,inp,name='std'):
    r=subprocess.run([str(OUT/f'{slug}-{name}.exe')],input=inp.encode(),capture_output=True,timeout=15)
    assert r.returncode==0,(slug,r.returncode,r.stderr.decode(errors='replace'),inp[:2000])
    return list(map(int,r.stdout.split()))
def war_brute(a,queries):
    a=a.copy()
    def count():return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))
    answer=[count()]
    for raw in queries:
        k=(answer[-1]+raw)%len(a) if raw<0 else raw-1
        chosen=[k]+[i for i in range(k+1,len(a)) if a[i]<a[k]]
        for i,v in zip(chosen,sorted(a[i] for i in chosen)):a[i]=v
        answer.append(count())
    return answer
def common_brute(n,weights,trees):
    best=0
    masks=[]
    for edges in trees:
        adj=[0]*n
        for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
        masks.append(adj)
    for chosen in range(1,1<<n):
        score=sum(weights[i] for i in range(n) if chosen>>i&1)
        if score<=best:continue
        for adj in masks:
            seen=chosen&-chosen;front=seen
            while front:
                bit=front&-front;front-=bit
                add=adj[bit.bit_length()-1]&chosen&~seen
                seen|=add;front|=add
            if seen!=chosen:break
        else:best=score
    return best
def battle_brute(initial,prices,enemies):
    hp,am,atk=initial;ch,cd,vd,ca,va=prices
    low=max([0]+[(d+1-atk+va-1)//va for k,h,d,a in enemies])
    high=max([0]+[(d+h-atk+va-1)//va for k,h,d,a in enemies])
    dmax=max([0]+[(a-am+vd-1)//vd for k,h,d,a in enemies])
    best=None
    for x in range(low,high+1):
        attack=atk+x*va
        for y in range(dmax+1):
            defence=am+y*vd
            damage=sum(k*((h+attack-d-1)//(attack-d))*max(a-defence,0) for k,h,d,a in enemies)
            health=max(hp,damage+1)
            candidate=((health-hp)*ch+y*cd+x*ca,health,defence,attack)
            if best is None or candidate<best:best=candidate
    return list(best)
def battle_input(initial,prices,enemies):
    return str(len(enemies))+'\n'+' '.join(map(str,initial))+'\n'+' '.join(map(str,prices))+'\n'+''.join(' '.join(map(str,e))+'\n' for e in enemies)
def plot_brute(operations):
    parent={0:None};value={0:0};children={0:set()};answers=[]
    for op in operations:
        t,a=op[:2]
        if t==1:
            _,a,b,c=op;parent[b]=a;value[b]=c;children[b]=set();children[a].add(b)
        elif t==2:
            if parent[a] is not None:children[parent[a]].remove(a)
            stack=[a]
            while stack:
                u=stack.pop();stack.extend(children.pop(u));del parent[u];del value[u]
        else:
            def reverse_path(v):
                ret=[]
                while v is not None:ret.append(value[v]);v=parent[v]
                return ret
            word=reverse_path(a);longest=0
            for b in parent:
                if b==a or children[b]:continue
                other=reverse_path(b);length=0
                while length<min(len(word),len(other)) and word[length]==other[length]:length+=1
                longest=max(longest,length)
            answers.append(len(word)-longest)
    return answers
def random_plot(count):
    alive={0:None};child={0:set()};free=[];next_id=1;ops=[]
    for i in range(count):
        pick=RNG.random()
        if pick<.49 or len(alive)==1 and pick<.8:
            a=RNG.choice(list(alive))
            if free and RNG.random()<.75:b=free.pop(RNG.randrange(len(free)))
            else:b=next_id;next_id+=1
            c=RNG.choice([0,1,2,100000,RNG.randrange(8)])
            ops.append((1,a,b,c));alive[b]=a;child[b]=set();child[a].add(b)
        elif pick<.73 and len(alive)>1:
            a=RNG.choice([u for u in alive if u]);ops.append((2,a));child[alive[a]].remove(a);stack=[a]
            while stack:
                u=stack.pop();stack.extend(child.pop(u));del alive[u];free.append(u)
        else:
            a=RNG.choice([u for u in alive if not child[u]]);ops.append((3,a))
    if RNG.random()<.1:ops.append((2,0))
    return ops
def main():
    results={}
    for t in range(700):
        n=RNG.randrange(1,22);a=[RNG.randrange(-6,7) for _ in range(n)]
        queries=[RNG.randrange(1,n+1) if RNG.random()<.5 else RNG.randrange(-10**9,0) for _ in range(RNG.randrange(1,80))]
        inp=f'{n} {len(queries)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(map(str,queries))+'\n'
        want=war_brute(a,queries);got=run('selective-suffix-sort',inp)
        assert got==want,('war',inp,want,got)
    results['selective-suffix-sort']={'actual_array_sort_cases':700,'passed':True};print('war 700 passed',flush=True)
    for t in range(400):
        n=RNG.randrange(1,12);m=RNG.randrange(1,6)
        weights=[RNG.choice([RNG.randrange(-20,21),10**9,-10**9]) for _ in range(n)]
        trees=[]
        for _ in range(m):
            order=RNG.sample(range(n),n);trees.append([(order[i],order[RNG.randrange(i)]) for i in range(1,n)])
        inp=f'{n} {m}\n'+' '.join(map(str,weights))+'\n'+''.join(f'{u+1} {v+1}\n' for edges in trees for u,v in edges)
        want=[common_brute(n,weights,trees)];got=run('common-tree-subset',inp)
        assert got==want,('common',inp,want,got)
    results['common-tree-subset']={'all_vertex_subset_cases':400,'passed':True};print('common 400 passed',flush=True)
    ways=[0]*20001;ways[0]=1
    power=1
    while power<=20000:
        for s in range(power,20001):ways[s]=(ways[s]+ways[s-power])%10**9
        power*=2
    samples=list(range(120))+RNG.sample(range(120,20001),280)
    for n in samples:
        got=run('binary-power-partitions',str(n)+'\n')
        assert got==[ways[n]],('partitions',n,ways[n],got)
    results['binary-power-partitions']={'coin_change_cases':len(samples),'passed':True};print('partitions 400 passed',flush=True)
    for t in range(600):
        initial=tuple(RNG.randrange(1,14) for _ in range(3))
        prices=tuple(RNG.randrange(1,12) for _ in range(5))
        enemies=[tuple(RNG.randrange(1,14) for _ in range(4)) for _ in range(RNG.randrange(1,8))]
        if t%4==0:
            prices=tuple(RNG.choice([1,10**9,RNG.randrange(1,100)]) if i in (0,1,3) else prices[i] for i in range(5))
        inp=battle_input(initial,prices,enemies);want=battle_brute(initial,prices,enemies)
        for name in ['std','alternative-heap']:
            got=run('battle-upgrades',inp,name)
            assert got==want,('battle',name,inp,want,got)
    results['battle-upgrades']={'exhaustive_upgrade_pairs_cases':600,'programs':2,'passed':True};print('battle 600 passed',flush=True)
    for t in range(600):
        ops=random_plot(RNG.randrange(1,130));inp=str(len(ops))+'\n'+''.join(' '.join(map(str,op))+'\n' for op in ops)
        want=plot_brute(ops);got=run('dynamic-path-independence',inp)
        assert got==want,('plot',inp,want,got)
    results['dynamic-path-independence']={'explicit_leaf_strings_cases':600,'passed':True};print('plot 600 passed',flush=True)
    (OUT/'small-checks.json').write_text(json.dumps(results,indent=2)+'\n','utf-8')
if __name__=='__main__':main()

def validate(slug,inp):
    lines=inp.strip().splitlines();tokens=list(map(int,inp.split()));pos=0
    def take():
        nonlocal pos
        assert pos<len(tokens);v=tokens[pos];pos+=1;return v
    if slug=='selective-suffix-sort':
        n=take();m=take();assert 1<=n<=100000 and 1<=m<=100000
        a=[take() for _ in range(n)];assert all(-10**9<=v<=10**9 for v in a)
        queries=[take() for _ in range(m)];assert all(-10**9<=q<=-1 or 1<=q<=n for q in queries)
        data=(a,queries)
    elif slug=='common-tree-subset':
        n=take();m=take();assert 1<=n<=20000 and 1<=m<=5
        weights=[take() for _ in range(n)];assert all(abs(v)<=10**9 for v in weights);trees=[]
        for _ in range(m):
            parent=list(range(n))
            def find(u):
                while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
                return u
            edges=[]
            for i in range(n-1):
                u=take()-1;v=take()-1;assert 0<=u<n and 0<=v<n
                x=find(u);y=find(v);assert x!=y;parent[x]=y;edges.append((u,v))
            trees.append(edges)
        data=(n,weights,trees)
    elif slug=='binary-power-partitions':
        n=take();assert 0<=n<=2**63-1;data=n
    elif slug=='battle-upgrades':
        n=take();assert 1<=n<=5000
        initial=tuple(take() for _ in range(3));prices=tuple(take() for _ in range(5))
        assert all(1<=v<=5000000 for v in initial)
        assert all(1<=prices[i]<=10**9 for i in [0,1,3]) and all(1<=prices[i]<=5000000 for i in [2,4])
        enemies=[tuple(take() for _ in range(4)) for _ in range(n)]
        assert all(1<=e[0]<=5000 and all(1<=v<=5000000 for v in e[1:]) for e in enemies)
        data=(initial,prices,enemies)
    else:
        n=take();assert 1<=n<=100000;operations=[];alive={0:None};children={0:set()}
        for _ in range(n):
            t=take();a=take();assert 0<=a<=100000 and a in alive
            if t==1:
                b=take();c=take();assert 0<=b<=100000 and b not in alive and 0<=c<=100000
                alive[b]=a;children[b]=set();children[a].add(b);operations.append((t,a,b,c))
            elif t==2:
                if alive[a] is not None:children[alive[a]].remove(a)
                stack=[a]
                while stack:
                    u=stack.pop();stack.extend(children.pop(u));del alive[u]
                operations.append((t,a))
            else:
                assert t==3 and not children[a];operations.append((t,a))
        data=operations
    assert pos==len(tokens),(slug,pos,len(tokens))
    return data

def oracle(slug,data):
    if slug=='selective-suffix-sort':return war_brute(*data)
    if slug=='common-tree-subset':return [common_brute(*data)]
    if slug=='battle-upgrades':return battle_brute(*data)
    if slug=='dynamic-path-independence':return plot_brute(data)
    n=data;ways=[1]+[0]*n;p=1
    while p<=n:
        for j in range(p,n+1):ways[j]=(ways[j]+ways[j-p])%10**9
        p*=2
    return [ways[n]]

