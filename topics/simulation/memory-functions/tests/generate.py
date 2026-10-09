"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case['seed']);sizes=case['sizes'];S=sum(sizes);k=case['k'];mode=case['mode']
    values=[rng.randrange(2) for _ in range(S)] if mode=='random' else [1]*(S-1)+[0]
    if mode=='copy':values[S//2-1]=0
    lines=[str(len(sizes)), ' '.join(map(str,sizes))];pos=0
    for size in sizes:lines.append(' '.join(map(str,values[pos:pos+size])));pos+=size
    lines.append(str(k))
    for i in range(k):
        if mode=='length':op=[2,0,0]
        elif mode=='copy':op=[1,0,0,len(sizes)-1,0] if i%2 else [0,0,0,1,max(0,S//2-1)]
        elif mode=='fill':op=[0,0,0,i%2,S] if i%3 else [2,0,0]
        else:
            kind=rng.randrange(3);a=rng.randrange(len(sizes));offset=rng.choice([rng.randrange(-S,S+1),-10**9,10**9,0]);op=[kind,a,offset]
            if kind==0:op += [rng.randrange(2),rng.choice([0,1,S,10**9,rng.randrange(S+1)])]
            if kind==1:op += [rng.randrange(len(sizes)),rng.choice([0,-S,S,10**9,rng.randrange(-S,S+1)])]
        lines.append(' '.join(map(str,op)))
    return '\n'.join(lines)+'\n'

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
