"""Independent small-instance oracles for the eight R9 reference programs."""
import heapq
import itertools
import json
import math
import os
import random
import subprocess
from collections import deque
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(2026092909)
MOD = 1000000007

def run(slug, data):
    program = ROOT/'build/bin'/(slug + ('.exe' if os.name == 'nt' else ''))
    result = subprocess.run([str(program)],input=data.encode(),capture_output=True,check=True,timeout=30)
    return list(map(int,result.stdout.split()))

def melon_oracle(grid):
    n,m=len(grid),len(grid[0])
    vines=[(x,y) for x in range(n) for y in range(m) if grid[x][y]=='l']
    choices=[]
    for x,y in vines:
        choices.append([a*m+b for a,b in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=a<n and 0<=b<m and grid[a][b]=='o'])
    results=[]
    def visit(i,used,unmatched):
        if i==len(choices):
            if all(all(v in used for v in choices[u]) for u in unmatched):
                results.append(len(used))
            return
        visit(i+1,used,unmatched+[i])
        for v in choices[i]:
            if v not in used:visit(i+1,used|{v},unmatched)
    visit(0,set(),[])
    return min(results),max(results)

def check_melon():
    count=0
    grids=[''.join(x) for x in itertools.product('lox',repeat=6)]
    for text in grids:
        grid=[text[:3],text[3:]]
        lo,hi=melon_oracle(grid)
        for kind,answer in ((0,hi),(1,lo)):
            data=f'2 3 {kind}\n'+'\n'.join(grid)+'\n'
            assert run('melon-planting',data)==[answer],data
            count+=1
    for _ in range(120):
        grid=[''.join(RNG.choice('lloox') for _ in range(4)) for _ in range(3)]
        if sum(row.count('l') for row in grid)>8:continue
        lo,hi=melon_oracle(grid)
        for kind,answer in ((0,hi),(1,lo)):
            data=f'3 4 {kind}\n'+'\n'.join(grid)+'\n'
            assert run('melon-planting',data)==[answer],data
            count+=1
    return count

def wool_oracle(a,b,p,t,effects,flock_items,cells):
    start=cells.index('S'); all_sheared=(1<<p)-1
    dist={(start,0,0):0};queue=[(0,start,0,0)]
    def relax(cost,pos,mask,carry):
        state=(pos,mask,carry)
        if cost<dist.get(state,10**30):
            dist[state]=cost;heapq.heappush(queue,(cost,*state))
    while queue:
        cost,pos,mask,carry=heapq.heappop(queue)
        if dist[pos,mask,carry]!=cost:continue
        if mask==all_sheared and carry==0:return cost
        step=max(1,t+sum(value for i,value in enumerate(effects) if carry>>i&1))
        x,y=divmod(pos,b)
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<a and 0<=ny<b and cells[nx*b+ny]!='B':relax(cost+step,nx*b+ny,mask,carry)
        if cells[pos].isdigit():
            flock=int(cells[pos])
            if not(mask>>flock&1):relax(cost,pos,mask|(1<<flock),carry|flock_items[flock])
        if cells[pos]=='C':
            sub=carry
            while sub:
                sub=(sub-1)&carry
                relax(cost,pos,mask,sub)
    raise AssertionError('unreachable')

def check_wool():
    for _ in range(180):
        a,b=RNG.choice([(2,3),(2,4),(3,3)])
        p=RNG.randint(1,min(4,a*b-2));k=2;t=RNG.randint(1,12)
        effect=[RNG.randint(-5,5) for _ in range(k)]
        counts=[RNG.choice([(1,0),(0,1),(1,1)]) for _ in range(p)]
        cells=['S','C']+[str(i) for i in range(p)]+['E']*(a*b-p-2)
        RNG.shuffle(cells)
        pieces=[];items=[]
        for row in counts:
            mask=0
            for j,cnt in enumerate(row):
                for _ in range(cnt):mask|=1<<len(pieces);pieces.append(effect[j])
            items.append(mask)
        answer=wool_oracle(a,b,p,t,pieces,items,cells)
        data=f'{a} {b} {p} {k} {t}\n'+' '.join(map(str,effect))+'\n'+'\n'.join(' '.join(map(str,row)) for row in counts)+'\n'+'\n'.join(' '.join(cells[i*b:(i+1)*b]) for i in range(a))+'\n'
        assert run('potion-wool',data)==[answer],(data,answer)
    return 180

def ratio_value(prefix,period):
    # Sum the terminating prefix and a geometric series independently.
    whole,finite=prefix.split('.')
    scale=10**len(finite)
    return Fraction(int(whole))+Fraction(int(finite or '0'),scale)+Fraction(int(period),scale*(10**len(period)-1))

def ratio_answer(rows):
    return math.lcm(*(ratio_value(a,b).denominator for a,b in rows))

def check_ratios():
    for i in range(300):
        n=RNG.randint(1,10);rows=[]
        for _ in range(n):
            length=RNG.randint(0,4 if i<200 else 90)
            period_length=RNG.randint(1,4 if i<200 else 100)
            rows.append(('0.0'+''.join(str(RNG.randrange(10)) for _ in range(length)),''.join(str(RNG.randrange(10)) for _ in range(period_length))))
        if all(ratio_value(*row)==0 for row in rows):rows[0]=('0.0','1')
        answer=ratio_answer(rows)
        if i<30:
            assert all(answer*ratio_value(*row)==int(answer*ratio_value(*row)) for row in rows)
        data=str(n)+'\n'+'\n'.join(a+' '+b for a,b in rows)+'\n'
        assert run('agricultural-ratios',data)==[answer],data
    return 300

def lottery_answer(A,B,C,n,m,queries,changes):
    active={i:i for i in range(1,n+1)};answer=[]
    for event in range(1,m+1):
        A=(A*B+C)%n+1;t=A
        if event in queries:
            answer.append(min(active,key=lambda i:(abs(active[i]-t),active[i],i if active[i]>t else -i)) if active else 0)
        elif event in changes:active[changes[event]]=t
        else:active.pop(t,None)
    return answer

def check_lottery():
    for _ in range(300):
        n=RNG.randint(1,25);m=RNG.randint(0,100)
        A,B,C=[RNG.choice([0,1,10**9,RNG.randrange(10**9)]) for _ in range(3)]
        query=[];changes={}
        for i in range(1,m+1):
            kind=RNG.randrange(3)
            if kind==0:query.append(i)
            elif kind==1:changes[i]=RNG.randint(1,n)
        data=f'{A} {B} {C}\n{n} {m} {len(query)} {len(changes)}\n'+' '.join(map(str,query))+'\n'+' '.join(f'{i} {d}' for i,d in changes.items())+'\n'
        assert run('lottery-plugin',data)==lottery_answer(A,B,C,n,m,set(query),changes),data
    return 300

def sign_answer(strings,queries):
    owners={}
    occurrences=[]
    for owner,s in enumerate(strings):
        for i in range(len(s)):
            for j in range(i+1,len(s)+1):
                piece=s[i:j];owners.setdefault(piece,set()).add(owner);occurrences.append(piece)
    return [sum(l<=len(piece)<=r and len(owners[piece])==1 for piece in occurrences) for l,r in queries]

def check_sign():
    for _ in range(300):
        strings=[''.join(RNG.choice('abc') for _ in range(RNG.randint(1,10))) for _ in range(RNG.randint(1,5))]
        queries=[sorted([RNG.randint(1,12),RNG.choice([RNG.randint(1,12),10**10])]) for _ in range(5)]
        data=f'{len(strings)} 5\n'+'\n'.join(strings)+'\n'+'\n'.join(f'{l} {r}' for l,r in queries)+'\n'
        assert run('sign-recognition',data)==sign_answer(strings,queries),data
    return 300

def timber_answer(n,edges):
    graph=[[] for _ in range(n)]
    for u,v in edges:graph[u].append(v);graph[v].append(u)
    parent=[-1]*n;root=[0]*n
    for start in range(n):
        if parent[start]!=-1:continue
        parent[start]=start;root[start]=start;queue=[start]
        for u in queue:
            for v in graph[u]:
                if parent[v]==-1:parent[v]=u;root[v]=start;queue.append(v)
    paths=[]
    for u in range(n):
        mask=1<<u
        while parent[u]!=u:u=parent[u];mask|=1<<u
        paths.append(mask)
    best=[(-1,n+1)]*(n+1)
    for selected in range(1,1<<n):
        cover=0;trees=set()
        for u in range(n):
            if selected>>u&1:cover|=paths[u];trees.add(root[u])
        k=selected.bit_count();candidate=(cover.bit_count(),-len(trees))
        best[k]=max(best[k],candidate)
    need=next(k for k in range(1,n+1) if best[k][0]==n)
    return [need]+[value for pair in best[1:need+1] for value in (pair[0],-pair[1])]

def check_timber():
    for _ in range(300):
        n=RNG.randint(1,11)
        labels=list(range(n));RNG.shuffle(labels)
        edges=[(labels[i],labels[RNG.randrange(i)]) for i in range(1,n) if RNG.randrange(4)]
        data=f'{n} {len(edges)}\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges)
        assert run('timber',data)==timber_answer(n,edges),data
    return 300

def spice_answer(n,edges,low,high):
    answer=0
    for mask in range(1<<(n-1)):
        parent=list(range(n));probability=1
        def find(u):
            while u!=parent[u]:u=parent[u]
            return u
        for i,(u,v,q,p) in enumerate(edges):
            if mask>>i&1:
                parent[find(u)]=find(v);probability=probability*(p-q)*pow(p,-1,MOD)%MOD
            else:probability=probability*q*pow(p,-1,MOD)%MOD
        if any(find(u)==find(v) for u in low for v in high):answer=(answer+probability)%MOD
    return answer

def check_spice():
    for _ in range(300):
        n=RNG.randint(1,9);edges=[]
        for v in range(1,n):
            p=RNG.randint(1,6);edges.append((RNG.randrange(v),v,RNG.randint(0,p),p))
        low=[RNG.randrange(n) for _ in range(RNG.randint(0,n))];high=[RNG.randrange(n) for _ in range(RNG.randint(0,2))]
        data=str(n)+'\n'+''.join(f'{u+1} {v+1} {q} {p}\n' for u,v,q,p in edges)+str(len(low))+'\n'+' '.join(str(u+1) for u in low)+'\n'+str(len(high))+'\n'+' '.join(str(u+1) for u in high)+'\n'
        assert run('spice-routes',data)==[spice_answer(n,edges,low,high)],data
    return 300

def trade_answer(prices,production,operations):
    prices=list(prices);production=list(production);stock=[0]*len(prices);answer=[]
    for op in operations:
        if op[0]==1:stock=[x+p*op[1] for x,p in zip(stock,production)]
        elif op[0]==2:
            k=op[1];value=0
            for i in sorted(range(len(prices)),key=lambda i:(prices[i],i),reverse=True):
                sold=min(k,stock[i]);k-=sold;stock[i]-=sold;value+=sold*prices[i]
            answer.append(value%MOD)
        elif op[0]==3:production[op[1]-1]=op[2]
        else:prices[op[1]-1]=op[2]
    return answer

def check_trade():
    for _ in range(500):
        n=RNG.randint(1,15);m=RNG.randint(1,100)
        prices=[RNG.choice([0,1,5,10**9,RNG.randint(1,100)]) for _ in range(n)]
        production=[RNG.choice([0,1,10**5,RNG.randint(1,20)]) for _ in range(n)]
        operations=[]
        for _ in range(m):
            kind=RNG.randint(1,4)
            if kind==1:operations.append((1,RNG.choice([0,1,1000,RNG.randint(1,1000)])))
            elif kind==2:operations.append((2,RNG.choice([0,1,10**18,RNG.randint(1,100000)])))
            else:operations.append((kind,RNG.randint(1,n),RNG.choice([0,1,10**5 if kind==3 else 10**9,RNG.randint(1,20)])))
        data=f'{n} {m}\n'+' '.join(f'{c} {p}' for c,p in zip(prices,production))+'\n'+'\n'.join(' '.join(map(str,op)) for op in operations)+'\n'
        assert run('colony-trade',data)==trade_answer(prices,production,operations),data
    return 500

def main():
    results={}
    for slug,check in [('melon-planting',check_melon),('potion-wool',check_wool),('agricultural-ratios',check_ratios),('lottery-plugin',check_lottery),('sign-recognition',check_sign),('timber',check_timber),('spice-routes',check_spice),('colony-trade',check_trade)]:
        results[slug]=check();print(slug,results[slug],'passed',flush=True)
    (ROOT/'build/R9-checks.json').write_text(json.dumps({'seed':2026092909,'comparisons':results},indent=2)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':main()
