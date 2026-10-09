"""Independent oracles and small exhaustive checks for six problem packages."""
from collections import deque
from pathlib import Path
import itertools
import json
import random
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PROBLEMS=[('simulation','character-x'),('recursion','recursive-maximum'),('trees','heap-tree-distance'),('data-structures','variable-lists'),('graphs','didu-hia-signifier-cycles'),('bitwise','signal-network')]
VARIANTS={slug:['std','alternative'] for _,slug in PROBLEMS}
VARIANTS['variable-lists']=['std']
VARIANTS['didu-hia-signifier-cycles']=['std','alternative-timestamps','alternative-pruning','alternative-doubling']

def character_oracle(text):
    lines=text.splitlines();answer=[]
    for c in lines[1:]:
        for i in range(8):
            row=[' ']*10
            for start in [i,7-i]:
                row[start:start+3]=[c]*3
            answer.append(''.join(row))
    return ''.join(row+'\n' for row in answer)

def maximum_oracle(text):
    return str(max(list(map(int,text.split()))[1:]))+'\n'

def distance_oracle(text):
    lines=text.splitlines();answer=[]
    for i,line in enumerate(lines[1:],1):
        a,b=[bin(int(x))[2:] for x in line.split()]
        common=0
        for x,y in zip(a,b):
            if x!=y:break
            common+=1
        answer.append(f'Case #{i}: {len(a)+len(b)-2*common}')
    return ''.join(row+'\n' for row in answer)

def lists_oracle(text):
    lines=iter(text.splitlines());n=int(next(lines));counts=list(map(int,next(lines).split()))
    containers=[deque() for _ in range(n)];owner={};value={};last=0;answer=[]
    for j,count in enumerate(counts):
        for _ in range(count):
            last+=1;containers[j].append(last);owner[last]=j;value[last]=last
    m=int(next(lines))
    for _ in range(m):
        op,identifier,*extra=map(int,next(lines).split())
        if op==1:
            if identifier not in owner:
                answer.append('NULL NULL NULL');continue
            row=containers[owner[identifier]];pos=row.index(identifier)
            answer.append(' '.join(str(value[row[k]]) if 0<=k<len(row) else 'NULL' for k in (pos-1,pos,pos+1)))
        elif op==2:
            if identifier in owner:
                containers[owner.pop(identifier)].remove(identifier);del value[identifier]
        elif op in (3,4):
            last+=1;owner[last]=identifier-1;value[last]=last
            if op==3:containers[identifier-1].appendleft(last)
            else:containers[identifier-1].append(last)
        elif identifier in owner:
            value[identifier]=extra[0]
    return ''.join(row+'\n' for row in answer)

def cycles_oracle(text,small=False):
    n,*target=map(int,text.split());target=[x-1 for x in target]
    if small:
        answer=0
        for start in range(n):
            seen=set();v=start
            while v not in seen:
                seen.add(v);v=target[v]
            answer+=v==start
        return str(answer)+'\n'
    # Iterative Kosaraju SCC decomposition, independent of cycle-length counting.
    reverse=[[] for _ in range(n)]
    for v,w in enumerate(target):reverse[w].append(v)
    seen=[False]*n;order=[]
    for start in range(n):
        path=[];v=start
        while not seen[v]:
            seen[v]=True;path.append(v);v=target[v]
        order.extend(reversed(path))
    seen=[False]*n;answer=0
    for start in reversed(order):
        if seen[start]:continue
        stack=[start];seen[start]=True;component=[]
        while stack:
            v=stack.pop();component.append(v)
            for w in reverse[v]:
                if not seen[w]:seen[w]=True;stack.append(w)
        if len(component)>1 or target[start]==start:answer+=len(component)
    return str(answer)+'\n'

def signal_oracle(text,small=False):
    answer=[]
    if small:
        bits=[0]*128
        for line in text.splitlines()[1:]:
            op,*args=map(int,line.split())
            if op==1:
                k=args[0]%128;bits=bits[k:]+bits[:k]
            elif op==2:
                answer.append(format(sum(bit*2**i for i,bit in enumerate(bits[:16])),'X'))
            else:
                l,r=args
                for i in range(l,r+1):bits[i]^=1
    else:
        state=0;mask=(1<<128)-1
        for line in text.splitlines()[1:]:
            op,*args=map(int,line.split())
            if op==1:
                k=args[0]%128;state=((state>>k)|(state<<(128-k)))&mask
            elif op==2:answer.append(format(state&65535,'X'))
            else:
                l,r=args;state^=((1<<(r-l+1))-1)<<l
    return ''.join(row+'\n' for row in answer)

ORACLES={'character-x':character_oracle,'recursive-maximum':maximum_oracle,'heap-tree-distance':distance_oracle,'variable-lists':lists_oracle,'didu-hia-signifier-cycles':cycles_oracle,'signal-network':signal_oracle}

def verify(slug,text,expected=None):
    if expected is None:expected=ORACLES[slug](text)
    for variant in VARIANTS[slug]:
        program=ROOT/'build/bin'/f'{slug}-{variant}.exe'
        result=subprocess.check_output([str(program)],input=text.encode('ascii'),timeout=15).replace(b'\r\n',b'\n')
        assert result==expected.encode('ascii'),(slug,variant,text[:1000],expected[:1000],result[:1000])

def main():
    rng=random.Random(2026100119);counts={}
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    batches=['0\n']+[str(len(chars[i:i+20]))+'\n'+'\n'.join(chars[i:i+20])+'\n' for i in range(0,len(chars),20)]
    for text in batches:verify('character-x',text)
    counts['character-x']=dict(input_batches=len(batches),distinct_characters=62)
    print('character-x: all 62 characters and empty batch passed',flush=True)
    cases=[]
    for n in range(1,5):cases.extend(itertools.product([-1,0,1],repeat=n))
    cases.extend(tuple(rng.randint(-10**9,10**9) for _ in range(rng.randint(1,100))) for _ in range(150))
    for values in cases:verify('recursive-maximum',str(len(values))+'\n'+' '.join(map(str,values))+'\n')
    counts['recursive-maximum']=len(cases)
    print('recursive-maximum:',len(cases),'batches passed',flush=True)
    pairs=list(itertools.product(range(1,129),repeat=2))
    # BFS on the finite tree supplies an independent oracle for all small pairs.
    distances={}
    for start in range(1,129):
        queue=deque([start]);distance={start:0}
        while queue:
            v=queue.popleft()
            for w in (v//2,2*v,2*v+1):
                if 1<=w<=128 and w not in distance:distance[w]=distance[v]+1;queue.append(w)
        for end,value in distance.items():distances[start,end]=value
    text=str(len(pairs))+'\n'+''.join(f'{a} {b}\n' for a,b in pairs)
    expected=''.join(f'Case #{i}: {distances[pair]}\n' for i,pair in enumerate(pairs,1))
    assert distance_oracle(text)==expected
    verify('heap-tree-distance',text,expected)
    large=[(rng.randint(1,10**18),rng.randint(1,10**18)) for _ in range(2000)]
    verify('heap-tree-distance',str(len(large))+'\n'+''.join(f'{a} {b}\n' for a,b in large))
    counts['heap-tree-distance']=dict(bfs_pairs=len(pairs),large_pairs=len(large))
    print('heap-tree-distance: BFS and 64-bit comparisons passed',flush=True)
    for _ in range(250):
        n=rng.randint(1,5);sizes=[rng.randint(1,5) for _ in range(n)];last=sum(sizes);ops=[]
        for j in range(60):
            op=rng.randint(1,5)
            if op in (3,4):args=[rng.randint(1,n)];last+=1
            else:args=[rng.choice([-10**9,-1,0,10**9,rng.randint(1,last+5)])]
            if op==5:args.append(rng.randint(-10**9,10**9))
            ops.append(' '.join(map(str,[op]+args)))
        verify('variable-lists',f'{n}\n'+ ' '.join(map(str,sizes))+f'\n{len(ops)}\n'+'\n'.join(ops)+'\n')
    counts['variable-lists']=dict(input_batches=250,operations=15000)
    print('variable-lists: 250 independent deque simulations passed',flush=True)
    cases=[()]
    for n in range(1,5):cases.extend(itertools.product(range(1,n+1),repeat=n))
    cases.extend(tuple(rng.randint(1,n) for _ in range(n)) for n in [rng.randint(1,60) for _ in range(150)])
    for values in cases:
        text=str(len(values))+'\n'+''.join(str(v)+'\n' for v in values)
        expected=cycles_oracle(text,True)
        assert cycles_oracle(text)==expected
        verify('didu-hia-signifier-cycles',text,expected)
    counts['didu-hia-signifier-cycles']=len(cases)
    print('didu-hia-signifier-cycles:',len(cases),'batches passed',flush=True)
    ops=[]
    for l in range(128):
        for r in range(l,128):ops.extend([f'3 {l} {r}','2',f'1 {l-64}'])
    for k in range(-256,257):ops.extend([f'3 {abs(k)%128} {abs(k)%128}',f'1 {k}','2'])
    text=str(len(ops))+'\n'+'\n'.join(ops)+'\n'
    expected=signal_oracle(text,True);assert expected==signal_oracle(text)
    verify('signal-network',text,expected)
    verify('signal-network','0\n')
    counts['signal-network']=dict(intervals=8256,signed_rotations=513,operations=len(ops),empty_batch=True)
    print('signal-network: every interval and signed shifts passed',flush=True)
    (ROOT/'build/R19/checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
