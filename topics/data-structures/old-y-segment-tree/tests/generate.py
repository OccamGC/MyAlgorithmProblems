"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def make_case(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];shape=case['shape']
    if shape=='increasing':values=list(range(n))
    elif shape=='decreasing':values=list(range(n,0,-1))
    elif shape=='equal':values=[1000000000]*n
    elif shape=='zigzag':values=[0 if i%2 else 1000000000 for i in range(n)]
    else:values=[rng.randrange(case.get('alphabet',1000000001)) for _ in range(n)]
    queries=[]
    for i in range(m):
        if case.get('mode')=='whole':left=1;right=n
        elif i%17==0:left=right=rng.randint(1,n)
        else:left,right=sorted([rng.randint(1,n),rng.randint(1,n)])
        queries.append((left,right,i))
    # Independent offline oracle on the already known clear-text intervals.
    bit=[0]*(n+1);stack=[];answers=[0]*m
    def add(i,value):
        while i<=n:bit[i]+=value;i+=i&-i
    def prefix(i):
        value=0
        while i:value+=bit[i];i-=i&-i
        return value
    endpoint=0
    for left,right,index in sorted(queries,key=lambda q:q[1]):
        while endpoint<right:
            endpoint+=1
            while stack and values[stack[-1]-1]<=values[endpoint-1]:add(stack.pop(),-1)
            stack.append(endpoint);add(endpoint,1)
        answers[index]=prefix(right)-prefix(left-1)
    lines=[f'{n} {m}',' '.join(map(str,values))];last=0
    for (left,right,index),answer in zip(queries,answers):
        u=left-1+n*rng.randint(0,(2**31-left)//n);v=right-1+n*rng.randint(0,(2**31-right)//n)
        if index%2:u,v=v,u
        lines.append(f'{u^last} {v^last}');last=answer
    return '\n'.join(lines)+'\n',''.join(f'{answer}\n' for answer in answers)
def generate(case):return make_case(case)[0]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    requested = set(args.case)
    unknown = requested - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if requested and case['id'] not in requested:
            continue
        target = args.out_dir / (case['id'] + '.in')
        target.write_text(generate(case), encoding='utf-8', newline='\n')
        if args.std:
            with target.open('rb') as source, target.with_suffix('.out').open('wb') as output:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=output, check=True)
if __name__ == '__main__':
    main()
