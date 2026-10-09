"""Deterministic tree recipes with a separate sparse-value oracle."""
import argparse,json,random,subprocess
from pathlib import Path

def make_case(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];shape=case['shape'];mode=case['mode']
    parent=[0]+[v-1 if shape=='chain' else 0 if shape=='star' else (v-1)//2 if shape=='binary' else rng.randrange(v) for v in range(1,n)]
    adj=[[] for _ in range(n)];depth=[0]*n;degree=[0]*n;size=[1]*n
    for v in range(1,n):
        u=parent[v];adj[u].append(v);adj[v].append(u);depth[v]=depth[u]+1;degree[u]+=1;degree[v]+=1
    prefix=[degree[0]]+[0]*(n-1)
    for v in range(1,n):prefix[v]=prefix[parent[v]]+degree[v]
    for v in range(n-1,0,-1):size[parent[v]]+=size[v]
    up=[parent]
    for _ in range(n.bit_length()):up.append([up[-1][up[-1][v]] for v in range(n)])
    def lca(a,b):
        if depth[a]<depth[b]:a,b=b,a
        diff=depth[a]-depth[b]
        for j in range(diff.bit_length()):
            if diff>>j&1:a=up[j][a]
        if a==b:return a
        for level in up[::-1]:
            if level[a]!=level[b]:a,b=level[a],level[b]
        return parent[a]
    def dist(a,b):return depth[a]+depth[b]-2*depth[lca(a,b)]
    low=[u for u in range(n) if degree[u]<=3];base=0;delta={};values=[0]*n;answers=[];ops=[]
    for i in range(m):
        t=i%12+1;region=(t-1)%3;action=(t-1)//3;a=rng.randrange(n);b=rng.randrange(n);v=rng.randint(-10**8,10**8)
        if mode=='accumulate':t=3 if i<m-1 else 12;region=2;action=0 if i<m-1 else 3;a=0;v=10**8
        elif mode=='zero':v=0
        elif mode=='sparse' and action<2:
            if region==2:a=0
            else:a=rng.choice(low);b=a
        if region==2:
            count=size[a]
            def inside(x):return lca(a,x)==a
        else:
            c=lca(a,b);length=depth[a]+depth[b]-2*depth[c]
            count=length+1 if region==0 else prefix[a]+prefix[b]-2*prefix[c]+degree[c]-2*length
            def inside(x):return dist(a,x)+dist(x,b)-length==(0 if region==0 else 2)
        op=[t,a+1]+([] if region==2 else [b+1])+([v] if action<2 else []);ops.append(' '.join(map(str,op)))
        if mode=='literal':
            vertices=[u for u in range(n) if inside(u)]
            if action<2:
                for u in vertices:values[u]=values[u]+v if action==0 else v
            else:answers.append(str(sum(values[u] for u in vertices)) if action==3 else str(max(values[u] for u in vertices)) if vertices else 'EMPTY')
        elif action<2:
            if mode=='zero':continue
            if region==2:
                if action==0:base+=v
                else:base=v;delta.clear()
            else:
                vertices=[a] if region==0 else adj[a]
                for u in vertices:delta[u]=delta.get(u,0)+v if action==0 else v-base
        else:
            changes=[v for u,v in delta.items() if inside(u)]
            if action==3:answers.append(str(base*count+sum(changes)))
            elif count==0:answers.append('EMPTY')
            else:answers.append(str(base+max(changes+([0] if len(changes)<count else []))))
    text=f'{n} {m}\n'+''.join(f'{parent[v]+1} {v+1}\n' for v in range(1,n))+'\n'.join(ops)+'\n'
    return text,'\n'.join(answers)+'\n'

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
