"""Generate deterministic inputs; optionally run a compiled C++17 reference program."""
import argparse
import json
from pathlib import Path
import random
import subprocess


def generate(spec):
    rng = random.Random(spec['seed'])

    n, upper = spec['n'], spec['upper']
    mode = spec['mode']
    if mode == 'equal':
        a = [upper]*n
    elif mode == 'alternating':
        a = [1 if i%2 else upper for i in range(n)]
    elif mode == 'ramp':
        a = [1+i%(upper) for i in range(n)]
    elif mode == 'spaced':
        a = [1+(i*499) % upper for i in range(n)]
    elif mode == 'permutation':
        a = list(range(1,upper+1)); rng.shuffle(a); a = a[:n]
        if upper in a:
            at = a.index(upper)
            a[at], a[-1] = a[-1], a[at]
    else:
        a = [rng.randint(1,upper) for _ in range(n)]
    a[-1] = upper
    return str(n)+'\n'+' '.join(map(str,a))+'\n'


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
