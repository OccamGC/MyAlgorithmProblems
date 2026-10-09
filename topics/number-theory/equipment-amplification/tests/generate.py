"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    q, mode = spec['q'], spec['mode']
    if mode == 'small':
        values = [rng.randrange(200000) for _ in range(q)]
    elif mode == 'maximum':
        values = [10**30-1]*q
    elif mode == 'binary':
        values = [int(''.join(rng.choice('01') for _ in range(30))) for _ in range(q)]
    elif mode == 'boundary':
        masks = [min((1<<30)-1, max(0, rng.randrange(6711)*160000+rng.choice([-1,0,1]))) for _ in range(q)]
        values = [int(bin(mask)[2:]) for mask in masks]
    elif mode == 'powers':
        values = [max(0,10**(i%30)+rng.choice([-1,0,1])) for i in range(q)]
    else:
        values = [rng.randrange(10**30) for _ in range(q)]
    return str(q)+'\n'+'\n'.join(map(str,values))+'\n'


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
        if args.cases and spec['id'] not in args.cases:
            continue
        text = generate(spec)
        file = args.out_dir/(spec['id']+'.in')
        file.write_text(text, encoding='ascii', newline='\n')
        if args.std:
            output = subprocess.check_output([str(args.std.resolve())],input=text.encode('ascii'))
            file.with_suffix('.out').write_bytes(output.replace(b'\r\n',b'\n'))


if __name__ == '__main__':
    main()
