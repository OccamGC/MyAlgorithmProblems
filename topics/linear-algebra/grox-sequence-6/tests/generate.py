"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    Q,b,k,mode=spec['Q'],spec['beta'],spec['k'],spec['mode']
    def state():
        if mode=='zero':return [0]*(k+2)
        if mode=='maximum':return [(-1 if i%2 else 1)*1000000000 for i in range(k+2)]
        return [rng.randrange(-1000000000,1000000001) for _ in range(k+2)]
    rows=[f'{Q} {b} {k}',' '.join(map(str,state()))]
    for i in range(Q):
        if mode=='updates' and i%2==0:rows.append('1 '+' '.join(map(str,state())))
        else:
            n=(0 if i==0 else 1000000000 if i==1 else rng.randrange(1000000001))
            rows.append(f'0 {n}')
    return '\n'.join(rows)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', dest='cases')
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    known = {case['id'] for case in plan['cases']}
    if args.cases and set(args.cases)-known:
        parser.error('unknown case: '+', '.join(sorted(set(args.cases)-known)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in plan['cases']:
        if args.cases and spec['id'] not in args.cases:continue
        text = generate(spec)
        path = args.out_dir / (spec['id']+'.in')
        path.write_text(text,encoding='ascii',newline='\n')
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())],stdin=source,capture_output=True,check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n',b'\n'))


if __name__=='__main__':main()
