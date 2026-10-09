"""Deterministic test recipes; Python standard library only."""
import argparse,collections,json,random,subprocess
from pathlib import Path


def make_case(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];mode=case['mode'];alphabet=case['alphabet'];mask=(1<<64)-1
    a=[i-50000 for i in range(n)] if mode=='unique' else [rng.randrange(-alphabet,alphabet+1) for _ in range(n)]
    if mode=='constant':a=[-10**9]*n
    lines=[f'{n} {m}',' '.join(map(str,a))];last=0;answers=[];size=400
    blocks=[collections.Counter(a[i:i+size]) for i in range(0,n,size)]
    def interval(l,r):
        counter=collections.Counter();i=l
        while i<=r:
            if i%size==0 and i+size-1<=r:counter.update(blocks[i//size]);i+=size
            else:counter[a[i]]+=1;i+=1
        return counter
    for i in range(m):
        if mode=='updates' or i%3==1:
            x=rng.randrange(n);v=rng.choice([-10**9,10**9,rng.randrange(-alphabet,alphabet+1)])
            if mode=='constant':v=-10**9
            op=[1,x+1,v];blocks[x//size][a[x]]-=1
            if blocks[x//size][a[x]]==0:del blocks[x//size][a[x]]
            blocks[x//size][v]+=1;a[x]=v
        else:
            l,r=sorted([rng.randrange(n),rng.randrange(n)]);x,y=sorted([rng.randrange(n),rng.randrange(n)])
            if mode=='unique':r=min(r,l+700);y=min(y,x+700)
            if i%101==0:l=x=0;r=y=n-1
            op=[2,l+1,r+1,x+1,y+1]
        lines.append(' '.join(str((v&mask)^last) for v in op))
        if op[0]==2:
            c=interval(l,r);d=interval(x,y);last=sum(v*d[k] for k,v in c.items());answers.append(last)
    return '\n'.join(lines)+'\n',''.join(str(v)+'\n' for v in answers)
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
