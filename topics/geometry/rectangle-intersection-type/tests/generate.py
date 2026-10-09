"""Reproduce inputs from plan.json; optionally run a compiled reference program."""
from pathlib import Path
import argparse
import json
import random
import subprocess



def generate(case):
    rng=random.Random(case['seed'])
    patterns=[(0,0,4,4,2,2,6,6),(0,0,2,2,2,0,4,2),(0,0,2,2,2,2,4,4),
              (0,0,1,1,2,2,3,3),(0,0,4,4,2,1,2,3),(0,0,4,4,2,2,2,2),
              (0,0,4,0,2,-2,2,2),(0,0,4,0,2,0,5,0),(-1,-1,-5,-5,-2,-1,-2,-2),(-10,-10,10,10,-10,-10,10,10),(-10,-10,0,10,0,-10,10,10)]
    if "types" in case:
        patterns=[row for row in patterns if all(int(row[i]!=row[i+2])+int(row[i+1]!=row[i+3]) in case["types"] for i in [0,4])]
    rows=[]
    for i in range(case['T']):
        if case['mode']=='boundary':
            row=list(patterns[i%len(patterns)])
            scale=1 if i%2 else 100000000
            row=[x*scale for x in row]
        else:
            kinds=case.get('types',[0,1,2])
            row=[]
            for _ in range(2):
                dimension=rng.choice(kinds)
                x=rng.randint(-10**9,10**9-1000);y=rng.randint(-10**9,10**9-1000)
                dx=rng.randint(1,1000);dy=rng.randint(1,1000)
                if dimension==0:dx=dy=0
                elif dimension==1:
                    if rng.randrange(2):dx=0
                    else:dy=0
                row.extend([x,y,x+dx,y+dy])
            if i%3==0:
                # Move the second shape near the first without exceeding bounds.
                dx=row[6]-row[4];dy=row[7]-row[5]
                row[4]=row[0];row[5]=row[1]
                row[6]=row[4]+dx;row[7]=row[5]+dy
        # Flip endpoint order without changing the shape.
        for start in [0,4]:
            if rng.randrange(2):row[start],row[start+2]=row[start+2],row[start]
            if rng.randrange(2):row[start+1],row[start+3]=row[start+3],row[start+1]
        rows.append(' '.join(map(str,row)))
    return str(case['T'])+'\n'+''.join(row+'\n' for row in rows)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    selected = set(args.case or [case['id'] for case in plan['cases']])
    unknown = selected - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if case['id'] not in selected:
            continue
        path = args.out_dir / (case['id'] + '.in')
        path.write_text(generate(case), encoding='ascii', newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())], stdin=source,
                                        stdout=subprocess.PIPE, check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n', b'\n'))

if __name__ == '__main__':
    main()
