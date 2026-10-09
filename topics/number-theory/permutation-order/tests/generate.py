"""Generate reproducible formal inputs using the Python standard library."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])

    n=case['n'];mode=case['mode'];a=list(range(1,n+1))
    if mode=='random':rng.shuffle(a)
    else:
        lengths=case.get('lengths',[])
        if mode=='cycle':lengths=[n]
        elif mode=='pairs':lengths=[2]*(n//2)
        elif mode=='increasing':
            lengths=[];total=0;length=1
            while total+length<=n:lengths.append(length);total+=length;length+=1
        elif mode=='prime-powers':
            lengths=[2**i for i in range(1,19)]+[3**i for i in range(1,12)]
        start=0
        for length in lengths:
            if start+length>n:break
            for j in range(length):a[start+j]=start+(j+1)%length+1
            start+=length
    return str(n)+'\n'+' '.join(map(str,a))+'\n'

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
