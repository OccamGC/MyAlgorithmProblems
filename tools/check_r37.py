"""Independent small models for equivalence, graph resets, jumps, packing and games."""
from pathlib import Path
from functools import lru_cache
import argparse,heapq,importlib.util,itertools,json,random,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R37'
PROBLEMS=[('automata','dungeon-room-equivalence'),('graphs','encrypted-reset-network'),('data-structures','lazy-forward-jumps'),('strings','noncrossing-1212-packing'),('games','dynamic-cycle-edge-game')]
def run(slug,text,variant='std'):
    return subprocess.run([str(OUT/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,check=True,timeout=180).stdout.decode().split()
def dungeon(a):
    k=len(a[0]);a=[[0]*k]+a;colors=[0]+[1]*(len(a)-1)
    while True:
        labels={};after=[]
        for u,row in enumerate(a):
            key=(u!=0,tuple(colors[v] for v in row))
            if key not in labels:labels[key]=len(labels)
            after.append(labels[key])
        if after==colors:return len(labels)-1
        colors=after
def distance(n,edges):
    adj=[[] for _ in range(n)]
    for u,v,x,y in edges:
        adj[u-1].append((v-1,x))
        if y:adj[v-1].append((u-1,x))
    ds=[10**30]*n;ds[0]=0;q=[(0,0)]
    while q:
        d,u=heapq.heappop(q)
        if d!=ds[u]:continue
        for v,w in adj[u]:
            if d+w<ds[v]:ds[v]=d+w;heapq.heappush(q,(d+w,v))
    return ds[-1]
def encrypt(n,initial,packets,threshold):
    out=[f'{n} {len(initial)} {len(packets)} {threshold}']+[' '.join(map(str,e)) for e in initial];edges=initial.copy();deleted=0;answers=[]
    for c,edge in enumerate(packets,1):
        key=(deleted+3)*(c+37)%998244353;out.append(' '.join(str(v^key) for v in edge));edges.append(edge)
        clear=distance(n,edges)<=threshold;answers.append(str(int(clear)))
        if clear:deleted+=len(edges);edges=[]
    return '\n'.join(out)+'\n',answers
def jumps(values,ops,typ):
    a=values.copy();n=len(a)-1;odd=even=total=0;answers=[]
    for i,op in enumerate(ops,1):
        if op[0]==1:a[op[1]]=op[2]
        else:
            u=op[1];value=0
            while u<=n:u+=a[u];value+=1
            if i%2:odd^=value
            else:even^=value
            total+=value;answers.append(str(value))
    return answers if typ==2 else list(map(str,[odd,even,total]))
def packing(s):
    choices=[]
    for q in itertools.combinations(range(len(s)),4):
        if ''.join(s[i] for i in q)=='1212':choices.append((sum(1<<i for i in q),[(q[0],q[1]),(q[2],q[3])]))
    def conflict(a,b):return bool(a[0]&b[0]) or any(x<u<y<v or u<x<v<y for x,y in a[1] for u,v in b[1])
    conflicts=[sum(1<<j for j,b in enumerate(choices) if j<=i or conflict(a,b)) for i,a in enumerate(choices)]
    def search(mask,need):
        if not need:return True
        if mask.bit_count()<need:return False
        while mask:
            bit=mask&-mask;i=bit.bit_length()-1;mask^=bit
            if search(mask&~conflicts[i],need-1):return True
        return False
    for target in range(min(s.count('1'),s.count('2'))//2,-1,-1):
        if search((1<<len(choices))-1,target):return target
@lru_cache(None)
def game(a):
    n=len(a)
    if not n:return False
    for e in set([0,n-1]):
        for v in range(a[e]):
            b=list(a);b[e]=v
            b=b[1:]+b[:1] if e==0 else b[-1:]+b[:-1]
            if not game(tuple(b)):return True
    return False
def game_formula(a):
    n=len(a)
    if not n:return False
    minimum=min(a)
    if minimum>0 and n%2:return True
    return a.index(minimum)%2==1 or a[::-1].index(minimum)%2==1
def forest_model(s):
    stack=[[0,0]]
    for c in s:
        if c=='1':stack.append([0,0])
        elif len(stack)>1:
            total,term=stack.pop();size=total+1;d=1+max(total%2,term-total);stack[-1][0]+=size;stack[-1][1]=max(stack[-1][1],size+d)
    while len(stack)>1:
        total,term=stack.pop();stack[-1][0]+=total;stack[-1][1]=max(stack[-1][1],term)
    total,term=stack[0];return (total-max(total%2,term-total))//2
def exhaustive_packing():
    count=0
    for n in range(13):
        for a in itertools.product('12',repeat=n):
            s=''.join(a);assert forest_model(s)==packing(s),s;count+=1
    result={'literal_packing_vs_python_forest_model':count};(OUT/'packing-exhaustive.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
def validation_checks():
    bad=[['0 1\n','1 0\n\n','1 1\n2\n','2 1\n0\n'],['2 1 1 101\n1 2 0 0\n0 0 0 0\n','2 1 1 1\n1 1 0 0\n0 0 0 0\n','2 1 1 1\n1 2 0 0\n1073741824 0 0 0\n'],['1 0 1\n0 1\n','1 1 1\n1 1\n1 2 1\n','1 1 1\n1 1\n2 1000000001\n'],['3\n120\n','2\n1\n','-1\n\n'],['0 1\n\n3 1\n','0 1\n\n2 2 0\n','1 0\n101\n']];count=0
    for (topic,slug),texts in zip(PROBLEMS,bad):
        p=ROOT/'topics'/topic/slug/'tests/generate.py';spec=importlib.util.spec_from_file_location('validation_r37',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for text in texts:
            try:m.validate(text)
            except (AssertionError,ValueError,IndexError):count+=1
            else:raise AssertionError((slug,text))
    result={'invalid_inputs_rejected':count};(OUT/'validation-boundaries.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
def main():
    rng=random.Random(3701);counts={s:0 for _,s in PROBLEMS}
    for _ in range(350):
        n=rng.randint(1,35);k=rng.randint(1,6);a=[[rng.randrange(n+1) for j in range(k)] for i in range(n)]
        text=f'{n} {k}\n'+'\n'.join(' '.join(map(str,row)) for row in a)+'\n';assert run(PROBLEMS[0][1],text)==[str(dungeon(a))];counts[PROBLEMS[0][1]]+=1
    for _ in range(200):
        n=rng.randint(2,12);threshold=rng.randint(0,100)
        def edge():
            u,v=rng.sample(range(1,n+1),2);return (u,v,rng.choice([0,1,10000,rng.randrange(101)]),rng.randrange(2))
        initial=[edge() for i in range(rng.randint(1,25))];packets=[edge() for i in range(70)];text,expected=encrypt(n,initial,packets,threshold)
        assert run(PROBLEMS[1][1],text)==expected,(text,expected);counts[PROBLEMS[1][1]]+=1
    for _ in range(300):
        n=rng.randint(1,60);q=rng.randrange(150);typ=rng.choice([1,2]);a=[rng.randint(1,n+3) for i in range(n+1)];ops=[]
        for i in range(q):ops.append([1,rng.randrange(n+1),rng.choice([1,1000000000,rng.randrange(1,n+2)])] if rng.randrange(2) else [2,rng.choice([1000000000,rng.randrange(n+5)])])
        text=f'{n} {q} {typ}\n'+' '.join(map(str,a))+'\n'+'\n'.join(' '.join(map(str,op)) for op in ops)+'\n'
        expected=jumps(a,ops,typ)
        for v in ['std','alternative']:
            if (OUT/f'{PROBLEMS[2][1]}-{v}.exe').exists():assert run(PROBLEMS[2][1],text,v)==expected,(text,expected,v)
        counts[PROBLEMS[2][1]]+=1
    inputs=[''.join(a) for n in range(10) for a in itertools.product('12',repeat=n)]
    inputs+=[''.join(rng.choice('12') for i in range(rng.randrange(10,17))) for _ in range(150)]
    inputs+=['11221122111112222122']
    for s in inputs:
        assert run(PROBLEMS[3][1],f'{len(s)}\n{s}\n')==[str(packing(s))],s;counts[PROBLEMS[3][1]]+=1
    a=[];ops=[];expected=['0']
    for n in range(7):
        while len(a)<n:a.append(0);ops.append([2,len(a),0]);expected.append(str(int(game(tuple(a)))))
        for b in itertools.product(range(4),repeat=n):
            for i,v in enumerate(b):
                if a[i]!=v:a[i]=v;ops.append([1,i+1,v]);expected.append(str(int(game(tuple(a)))))
            assert game(tuple(a))==game_formula(a)
            counts[PROBLEMS[4][1]]+=1
    # Exercise deletion and insertion at both ends and inside the sequence.
    for _ in range(1000):
        op=rng.choice([1,2,3]) if a else 2
        if op==1:
            i=rng.randrange(len(a));v=rng.randrange(4);a[i]=v;ops.append([1,i+1,v])
        elif op==2 and len(a)<6 or not a:
            i=rng.randrange(len(a)+1);v=rng.randrange(4);a.insert(i,v);ops.append([2,i+1,v])
        else:
            i=rng.randrange(len(a));a.pop(i);ops.append([3,i+1])
        expected.append(str(int(game(tuple(a)))))
    text=f'0 {len(ops)}\n\n'+'\n'.join(' '.join(map(str,op)) for op in ops)+'\n';assert len(ops)<=100000
    assert run(PROBLEMS[4][1],text)==expected
    result={'independent_inputs_or_states':counts,'cycle_update_outputs':len(expected),'literal_game_states':game.cache_info().currsize}
    (OUT/'small-checks.json').write_text(json.dumps(result,indent=2)+'\n','utf-8',newline='\n');print(result,flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--packing-exhaustive',action='store_true');parser.add_argument('--validation-only',action='store_true');args=parser.parse_args()
    if args.packing_exhaustive:exhaustive_packing()
    elif args.validation_only:validation_checks()
    else:main();validation_checks()
