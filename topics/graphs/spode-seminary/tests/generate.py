"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    n,m,q,mode = spec['n'],spec['m'],spec['q'],spec['mode']
    satisfaction = [rng.randrange(m+1) for _ in range(n)]
    capacity = [rng.randrange(3) for _ in range(m)]
    if mode == 'none': capacity = [0]*m
    if mode in ('ordered','ties','chain'): capacity = [1]*m
    if mode == 'ample': capacity = [1000]*m
    rows = [f'{n} {m} {q}',' '.join(map(str,satisfaction)),' '.join(map(str,capacity))]
    for i in range(n):
        if mode == 'ordered': row = list(range(1,m+1))
        elif mode == 'ties': row = [j//3+1 for j in range(m)]
        elif mode == 'chain':
            row = [-1]*m
            row[i%m] = 1; row[(i+1)%m] = 1
        else:
            tiers = [j//3+1 for j in range(3*m)]; rng.shuffle(tiers)
            row = [tiers[j] if rng.randrange(4) else -1 for j in range(m)]
        rows.append(' '.join(map(str,row)))
    for k in range(q):
        rank = list(range(1,n+1))
        if k%3 == 1: rank.reverse()
        elif k%3 == 2: rng.shuffle(rank)
        rows.append(' '.join(map(str,rank)))
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
