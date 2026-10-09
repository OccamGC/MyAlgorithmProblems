"""Deterministic test recipes; Python standard library only."""
import argparse,bisect,collections,json,random,subprocess
from pathlib import Path


def make_case(case):
    rng=random.Random(case['seed']);n=case['n'];m=case['m'];q=case['q'];mode=case['mode']
    rb=min(n,8);cb=min(m,8);rows=[i*n//rb for i in range(rb+1)];cols=[j*m//cb for j in range(cb+1)]
    grid=[[rng.randint(-20000,20000) for _ in range(cb)] for _ in range(rb)]
    if mode=='negative':grid=[[-20000]*cb for _ in range(rb)]
    if mode=='overflow':grid=[[20000]*cb for _ in range(rb)]
    body=[]
    for i in range(rb):
        row=' '.join(' '.join([str(grid[i][j])]*(cols[j+1]-cols[j])) for j in range(cb))+'\n'
        body.append(row*(rows[i+1]-rows[i]))
    lines=[];answers=[]
    for t in range(q):
        update=t<q-1 if mode=='overflow' else (t*40//q)%2==0
        if mode=='queries':update=False
        if update:
            a,b=sorted([rng.randrange(rb),rng.randrange(rb)]);c,d=sorted([rng.randrange(cb),rng.randrange(cb)])
            if mode in ['negative','overflow']:a=c=0;b=rb-1;d=cb-1
            value=-20000 if mode=='negative' else 20000 if mode=='overflow' else rng.randint(-20000,20000)
            lines.append(f'1 {rows[a]+1} {cols[c]+1} {rows[b+1]} {cols[d+1]} {value}')
            for i in range(a,b+1):
                for j in range(c,d+1):grid[i][j]+=value
        else:
            x1,x2=sorted([rng.randrange(n),rng.randrange(n)]);y1,y2=sorted([rng.randrange(m),rng.randrange(m)])
            if mode=='overflow':x1=y1=0;x2=n-1;y2=m-1
            lines.append(f'2 {x1+1} {y1+1} {x2+1} {y2+1}')
            a=bisect.bisect_right(rows,x1)-1;b=bisect.bisect_right(rows,x2)-1;c=bisect.bisect_right(cols,y1)-1;d=bisect.bisect_right(cols,y2)-1
            answers.append(max(grid[i][j] for i in range(a,b+1) for j in range(c,d+1)))
    return f'{n} {m} {q}\n'+''.join(body)+'\n'.join(lines)+'\n',''.join(str(v)+'\n' for v in answers)
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
