"""Reproduce input recipes using Python standard-library tools."""
import argparse
import json
import random
import subprocess
from pathlib import Path

def generate(case):
    rng=random.Random(case["seed"])
    values=case.get('values')
    if values is None:
        values=[]
        for i in range(case['T']):
            length=rng.randint(1,18)
            value=''.join(str(rng.randrange(10)) for _ in range(length))
            if case['mode']=='palindromes':
                half=''.join(str(rng.randrange(10)) for _ in range((length+1)//2))
                half=str(rng.randint(1,9))+half[1:]
                value=half+half[:length//2][::-1]
            elif case['mode']=='zeros':value='0'*length
            elif case['mode']=='padded':value=('0'*rng.randint(0,17)+str(rng.randint(0,999)))[:18]
            values.append(value)
    return str(len(values))+'\n'+'\n'.join(values)+'\n'

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
