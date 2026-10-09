"""Input validators and independent reference models for R32."""
from pathlib import Path
import collections,importlib.util,itertools,json,math,random,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R32'
out=OUT
rng=random.Random(320071)
PROBLEMS=[('number-theory','apostle-luke-password'),('trees','giant-christmas-tree'),('parsing','short-circuit-calculator'),('data-structures','old-y-segment-tree'),('dynamic-programming','limited-refueling')]
MEMORY_MB={'apostle-luke-password':128,'giant-christmas-tree':1024,'short-circuit-calculator':128,'old-y-segment-tree':1024,'limited-refueling':128}

def load_generator(topic,slug):
    spec=importlib.util.spec_from_file_location('generator',ROOT/'topics'/topic/slug/'tests/generate.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

levels={'?':1,'||':2,'&&':3,'|':4,'^':5,'&':6,'==':7,'!=':7,'<':8,'>':8,'<=':8,'>=':8,'<<':9,'>>':9,'+':10,'-':10,'*':11,'/':11,'%':11}

def run(slug,text,variant='std'):
 p=subprocess.run([str(out/f'{slug}-{variant}.exe')],input=text.encode(),capture_output=True,timeout=30);assert p.returncode==0,(slug,p.returncode,text[:500]);return p.stdout.decode().split()

def tree_oracle(N,edges,queries):
 adjacent=[[] for _ in range(N)];state=[]
 for i,(u,v,s) in enumerate(edges):adjacent[u].append((v,i));adjacent[v].append((u,i));state.append(s)
 results=[]
 for a,b in queries:
  parents={a:(a,-1)};queue=[a]
  for u in queue:
   for v,i in adjacent[u]:
    if v not in parents:parents[v]=(u,i);queue.append(v)
  while b!=a:
   b,i=parents[b];state[i]=0
  best=0
  for start in range(N):
   distance={start:0};queue=[start]
   for u in queue:
    for v,i in adjacent[u]:
     if state[i] and v not in distance:distance[v]=distance[u]+1;queue.append(v)
   best=max(best,max(distance.values()))
  results.append(str(best))
 return results

def wrap(x):return (x+2**31)%2**32-2**31

def calculator_oracle(text):
 tokens=re.findall(r'\d+|<<|>>|<=|>=|==|!=|&&|\|\||[^\s]',text);pos=0
 def parse(level=1):
  nonlocal pos
  token=tokens[pos];pos+=1
  if token in ['+','-','!','~']:node=('u'+token,parse(12))
  elif token=='(':node=parse();assert tokens[pos]==')';pos+=1
  else:node=int(token)
  while pos<len(tokens) and tokens[pos] in levels and levels[tokens[pos]]>=level:
   operator=tokens[pos];pos+=1
   if operator=='?':
    yes=parse();assert tokens[pos]==':';pos+=1;no=parse(2);node=('?',node,yes,no)
   else:node=(operator,node,parse(levels[operator]+1))
  return node
 root=parse();assert pos==len(tokens)
 def evaluate(node):
  if isinstance(node,int):return node
  operator=node[0];a=evaluate(node[1])
  if operator=='u+':return a
  if operator=='u-':return wrap(-a)
  if operator=='u!':return int(not a)
  if operator=='u~':return wrap(~a)
  if operator=='?':return evaluate(node[2] if a else node[3])
  if operator=='&&' and not a:return 0
  if operator=='||' and a:return 1
  b=evaluate(node[2])
  if operator in ['&&','||']:return int(bool(b))
  if operator=='+':return wrap(a+b)
  if operator=='-':return wrap(a-b)
  if operator=='*':return wrap(a*b)
  if operator in ['/','%']:
   q=(abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1);return wrap(q if operator=='/' else a-q*b)
  if operator=='<<':return wrap(a<<(b&31))
  if operator=='>>':return a>>(b&31)
  if operator=='<':return int(a<b)
  if operator=='>':return int(a>b)
  if operator=='<=':return int(a<=b)
  if operator=='>=':return int(a>=b)
  if operator=='==':return int(a==b)
  if operator=='!=':return int(a!=b)
  if operator=='&':return wrap(a&b)
  if operator=='^':return wrap(a^b)
  if operator=='|':return wrap(a|b)
  raise AssertionError(operator)
 try:return [str(evaluate(root))]
 except ZeroDivisionError:return ['Segmentfault']

def expression(depth):
 if depth==0:return str(rng.choice([0,1,2,31,32,33,1000000000,rng.randrange(100)]))
 kind=rng.randrange(5)
 if kind==0:return rng.choice(['+','-','!','~'])+expression(depth-1)
 if kind==1:return '('+expression(depth-1)+')'
 if kind==2:return expression(depth-1)+'?'+expression(depth-1)+':'+expression(depth-1)
 return expression(depth-1)+rng.choice([x for x in levels if x!='?'])+expression(depth-1)

def validate(slug,text,group=3):
    if slug=='short-circuit-calculator':
        expr=text.removesuffix('\n').removesuffix('\r');assert 1<=len(expr)<=200000
        assert '\n' not in expr and '\r' not in expr
        assert group!=1 or len(expr)<=60
        assert group!=2 or len(expr)<=5000
        position=0;need=True;questions=[0];tokens=[]
        for match in re.finditer(r'[0-9]+|<<|>>|<=|>=|==|!=|&&|\|\||[()+\-~!*/%<>&^|?:]',expr):
            assert not expr[position:match.start()].strip(' \t');position=match.end();token=match[0];tokens.append(token)
            if token[0].isdigit():
                value=token.lstrip('0') or '0';assert need and len(value)<=10 and int(value)<=10**9;need=False
            elif token=='(':assert need;questions.append(0)
            elif token==')':assert not need and len(questions)>1 and questions[-1]==0;questions.pop()
            elif token=='?':assert not need;questions[-1]+=1;need=True
            elif token==':':assert not need and questions[-1]>0;questions[-1]-=1;need=True
            elif need:assert token in ['+','-','!','~']
            else:assert token in levels and token!='?';need=True
        assert tokens and not need and questions==[0] and not expr[position:].strip(' \t')
        return expr
    data=list(map(int,text.split()))
    if slug=='apostle-luke-password':
        assert len(data)==4;N,G,k,b=data
        assert 1<=N<=5000 and 0<=G<=100000 and 1<=k<=10**9 and 0<=b<=10**14
        maximum=k*(G+N-1)+b
        assert group!=1 or maximum<=60
        assert group!=2 or maximum<=10**7
        return data
    if slug=='old-y-segment-tree':
        N,M=data[:2];assert 1<=N<=50000 and 1<=M<=50000 and len(data)==2+N+2*M
        assert all(0<=v<=10**9 for v in data[2:N+2]) and all(0<=v<2**31 for v in data[N+2:])
        assert group!=1 or N<=30 and M<=100
        assert group!=2 or N<=2000 and M<=2000
        return data[2:N+2],list(zip(data[N+2::2],data[N+3::2]))
    if slug=='limited-refueling':
        N,L,R=data[:3];assert 1<=L<=2000 and 0<=N<=L and (R==-1 or 1<=R<=L) and len(data)==3+3*N
        stations=list(zip(data[3::3],data[4::3],data[5::3]));assert len({x for x,c,s in stations})==N
        assert all(0<=x<L and 0<=c<=10**9 and 0<=s<=10**9 for x,c,s in stations)
        assert group!=1 or L<=12
        assert group!=2 or L<=200
        return L,R,stations
    N,M=data[:2];assert 2<=N<=100000 and 1<=M<=200000 and len(data)==2+3*(N-1)+2*M
    assert group!=1 or N<=30 and M<=100
    assert group!=2 or N<=2000 and M<=2000
    edge_end=2+3*(N-1);edges=list(zip(data[2:edge_end:3],data[3:edge_end:3],data[4:edge_end:3]));parent=list(range(N+1))
    def root(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    for u,v,s in edges:
        assert 1<=u<=N and 1<=v<=N and s in [0,1];a=root(u);b=root(v);assert a!=b;parent[a]=b
    queries=list(zip(data[edge_end::2],data[edge_end+1::2]));assert all(1<=u<=N and 1<=v<=N for u,v in queries)
    return N,[(u-1,v-1,s) for u,v,s in edges],[(u-1,v-1) for u,v in queries]

def refuel_oracle(text):
    L,R,stations=validate('limited-refueling',text);capacity=L if R==-1 else R;stations.sort();costs={0:0};stops={0:0};previous=0
    for x,price,stock in stations+[(L,0,0)]:
        distance=x-previous;costs={f-distance:c for f,c in costs.items() if f>=distance};stops={f-distance:c for f,c in stops.items() if f>=distance}
        newcost={};newstops={}
        for f,c in costs.items():
            for q in range(min(stock,capacity-f)+1):newcost[f+q]=min(newcost.get(f+q,10**20),c+q*price)
        for f,c in stops.items():
            for q in range(min(stock,capacity-f)+1):newstops[f+q]=min(newstops.get(f+q,10**20),c+(q>0))
        costs=newcost;stops=newstops;previous=x
    return [str(min(costs.values(),default=-1)),str(min(stops.values(),default=-1))]

def stack_oracle(text):
    values,queries=validate('old-y-segment-tree',text);last=0;answers=[];n=len(values)
    for u,v in queries:
        left,right=sorted([(u^last)%n,(v^last)%n]);stack=[]
        for value in values[left:right+1]:
            while stack and stack[-1]<=value:stack.pop()
            stack.append(value)
        last=len(stack);answers.append(str(last))
    return answers

def main():
    counts={slug:0 for _,slug in PROBLEMS}
    def check(slug,text,expected):
        validate(slug,text)
        for variant in ['std','alternative']:assert run(slug,text,variant)==expected,(slug,variant,text[:1000],expected[:30])
        counts[slug]+=1
    for p in range(61):
        f=math.factorial(p-1) if p else 1
        answer=math.isqrt((math.factorial(p)*(f+2)+p)//p**3)-f//p if p else 0
        check('apostle-luke-password',f'1 0 1 {p}\n',[str(answer)])
    for _ in range(120):
        N=rng.randint(1,30);G=rng.randint(0,100);k=rng.randint(1,1000);b=rng.randint(0,1000000);total=0;expected=[]
        for j in range(G,G+N):
            p=k*j+b;total+=p==1 or p>=2 and all(p%d for d in range(2,math.isqrt(p)+1));expected.append(str(total))
        check('apostle-luke-password',f'{N} {G} {k} {b}\n',expected)
    for _ in range(220):
        N=rng.randint(2,35);M=rng.randint(1,50);edges=[(i,rng.randrange(i),rng.randrange(2)) for i in range(1,N)];queries=[(rng.randrange(N),rng.randrange(N)) for _ in range(M)]
        text=f'{N} {M}\n'+''.join(f'{u+1} {v+1} {s}\n' for u,v,s in edges)+''.join(f'{u+1} {v+1}\n' for u,v in queries)
        check('giant-christmas-tree',text,tree_oracle(N,edges,queries))
    examples=['1?0:1?2:3','1?1?2:3:4','0?1/0:2','1?2:1/0','(1/0)?2:3','0&&1/0||3','1||1/0','0|1/0','15<<33','-5>>1','1<<-1','0000007 + 2','+++++-----1','(1000000000*3)/(-1)']
    for text in examples+[expression(rng.randint(1,5)) for _ in range(400)]:check('short-circuit-calculator',text+'\n',calculator_oracle(text))
    gen=load_generator('data-structures','old-y-segment-tree')
    for seed in range(200):
        text,expected=gen.make_case({'n':rng.randint(1,60),'m':rng.randint(1,100),'shape':rng.choice(['random','equal','zigzag','decreasing']),'alphabet':10,'seed':seed})
        answer=stack_oracle(text);assert answer==expected.split();check('old-y-segment-tree',text,answer)
    for _ in range(300):
        L=rng.randint(1,10);R=rng.choice([-1]+list(range(1,L+1)));N=rng.randint(0,L);stations=[(x,rng.randrange(10),rng.randrange(L+2)) for x in rng.sample(range(L),N)]
        text=f'{N} {L} {R}\n'+''.join(f'{x} {c} {s}\n' for x,c,s in stations);check('limited-refueling',text,refuel_oracle(text))
    (OUT/'small-checks.json').write_text(json.dumps({'status':'passed','independent_inputs':counts},indent=2)+'\n','utf-8');print(counts,flush=True)
if __name__=='__main__':main()
