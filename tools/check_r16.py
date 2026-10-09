"""Independent small-case oracles for the four R16 problems."""
from collections import deque
from pathlib import Path
import itertools,json,random,subprocess
ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('strings','paper-tiger-sequence'),('graphs','simple-rail-network'),('recursion','block-tower'),('logic','circuit-board-test')]

def run(slug,variant,text):
    return subprocess.check_output([str(ROOT/'build/bin'/f'{slug}-{variant}.exe')],input=text.encode('ascii'),timeout=30).replace(b'\r\n',b'\n').decode('ascii')

def paper_oracle(initial,positions,queries):
    versions=[initial]
    for p in positions:
        s=versions[-1]; added=(len(s)+4)//5
        versions.append(''.join(s[(p+i)%len(s)] for i in range(added))+s)
    return ''.join(versions[i]+'\n' for i in queries)

def graph_oracle(n,edges):
    best=None
    for mask in range(1<<len(edges)):
        adjacency=[[] for _ in range(n)]
        total=0
        for i,(a,b,w) in enumerate(edges):
            if mask>>i&1:
                adjacency[a-1].append(b-1); adjacency[b-1].append(a-1); total+=w
        seen={0}; stack=[0]
        while stack:
            for y in adjacency[stack.pop()]:
                if y not in seen: seen.add(y);stack.append(y)
        if len(seen)==n and (best is None or total<best): best=total
    return 'bad idea\n' if best is None else str(best)+'\n'

def hanoi_bfs(n):
    start=(0,)*n; goal=(1,)*n
    parent={start:None}; queue=deque([start])
    while goal not in parent:
        state=queue.popleft()
        top=[next((d for d in range(n) if state[d]==p),n) for p in range(3)]
        for a,b in itertools.permutations(range(3),2):
            if top[a]<top[b]:
                nxt=list(state); nxt[top[a]]=b; nxt=tuple(nxt)
                if nxt not in parent:
                    parent[nxt]=(state,top[a],a,b);queue.append(nxt)
    moves=[]; state=goal
    while state!=start:
        state,d,a,b=parent[state]; moves.append((d,a,b))
    return moves[::-1]

def check_hanoi(n,names,blocks,output):
    stacks=[list(range(n)),[],[]]
    lines=output.splitlines()
    assert len(lines)==(1<<n)-1
    for line in lines:
        matches=[]
        for a,b in itertools.permutations(range(3),2):
            if stacks[a]:
                disk=stacks[a][-1]
                if (not stacks[b] or stacks[b][-1]<disk) and line==f'Move {blocks[disk]} from {names[a]} to {names[b]}.': matches.append((a,b))
        assert len(matches)==1,(line,matches)
        a,b=matches[0]; stacks[b].append(stacks[a].pop())
    assert stacks==[[],list(range(n)),[]]

def main():
    rng=random.Random(2026093017)
    counts={}
    original_paper_cases=0
    for case in range(390):
        n=rng.randrange(19) if case<350 else rng.randrange(40,71)
        initial=''.join(rng.choice('aAZ09') for _ in range(rng.randrange(1,11)))
        positions=[rng.randrange(10**9+1) for _ in range(n)]
        queries=rng.sample(range(n+1),rng.randrange(n+2)) if case<350 else [n,*rng.sample(range(n),min(n,3))]
        text=initial+'\n'+f'{n} {len(queries)}\n'+''.join(str(x)+'\n' for x in positions+queries)
        expected=paper_oracle(initial,positions,queries)
        variants=['std','alternative']+(['original'] if n<=54 else [])
        original_paper_cases+=n<=54
        for variant in variants:
            assert run('paper-tiger-sequence',variant,text)==expected,(case,variant)
    counts['paper_cases']=390
    counts['original_paper_cases']=original_paper_cases
    print('Paper suffix and streaming programs agree with explicit copies.',flush=True)
    for case in range(500):
        n=rng.randrange(1,8);m=rng.randrange(11)
        edges=[(rng.randrange(1,n+1),rng.randrange(1,n+1),rng.randrange(-7,9)) for _ in range(m)]
        text=f'{n} {m}\n'+''.join(f'{a} {b} {w}\n' for a,b,w in edges)
        expected=graph_oracle(n,edges)
        for variant in ['std','alternative','original']:
            assert run('simple-rail-network',variant,text).strip()==expected.strip(),(case,variant,n,edges)
    counts['graph_subset_cases']=500
    print('Rail programs agree with exhaustive edge subsets.',flush=True)
    bfs={n:hanoi_bfs(n) for n in range(1,8)}
    for n,moves in bfs.items(): assert len(moves)==(1<<n)-1
    for case in range(120):
        n=case%10+1
        names=[f' Platform {i}  ' for i in range(3)]
        blocks=[f' B{i}_'+''.join(rng.choice('aZ09_ ') for _ in range(7))+' ' for i in range(n)]
        text=str(n)+'\n'+'\n'.join(names+blocks)+'\n'
        outputs=[run('block-tower',v,text) for v in ['std','alternative','original']]
        assert len(set(outputs))==1
        check_hanoi(n,names,blocks,outputs[0])
        if n<=7:
            expected=''.join(f'Move {blocks[n-1-d]} from {names[a]} to {names[b]}.\n' for d,a,b in bfs[n])
            assert outputs[0]==expected
    counts.update(hanoi_cases=120,hanoi_bfs_sizes=list(bfs))
    print('Tower moves are legal, optimal and preserve complete names.',flush=True)
    values=list(range(-10000,10001))+[rng.randrange(-10**18,10**18+1) for _ in range(2000)]
    values += [sign*x for sign in [-1,1] for x in [10**18,10**18-1,2**53-1,2**53,2**53+1]]
    for start in range(0,len(values),1000):
        batch=values[start:start+1000]
        text=str(len(batch))+'\n'+'\n'.join(map(str,batch))+'\n'
        expected=''.join('T\n' if x>0 and x**3<3000 and x*x>=10 and (x*x>2000 or x*x<700) else 'F\n' for x in batch)
        for variant in ['std','alternative','original']:
            assert run('circuit-board-test',variant,text)==expected
    for variant in ['std','alternative','original']: assert run('circuit-board-test',variant,'0\n')==''
    counts['predicate_values']=len(values)
    (ROOT/'build/R16-checks.json').write_text(json.dumps(dict(seed=2026093017,**counts),indent=2)+'\n',encoding='utf-8')
    print(counts,flush=True)

if __name__=='__main__':main()
