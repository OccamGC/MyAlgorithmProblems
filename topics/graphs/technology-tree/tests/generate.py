"""Generate deterministic inputs using Python 3; optionally run a compiled reference."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec, output):
    rng = random.Random(spec['seed'])
    n, m, mode = spec['n'], spec['m'], spec['mode']
    if mode == 'complete': times = [-1] * n
    elif mode == 'chain': times = [1000000000] * n
    elif mode == 'zero-cycle': times = [0] * n
    elif mode == 'broken-cycle': times = [-1] + [1] * (n - 1)
    elif mode == 'mixed': times = [-1 if i % 5 == 0 else rng.randrange(1000000001) for i in range(n)]
    else: times = [rng.randrange(1000000001) for _ in range(n)]
    print(n, m, file=output)
    print(*times, file=output)
    for i in range(m):
        if mode in ('cycle', 'zero-cycle', 'broken-cycle'): u, v = i % n + 1, (i + 1) % n + 1
        elif mode == 'complete': u, v = rng.randrange(1, n + 1), rng.randrange(1, n + 1)
        elif mode == 'parallel': u, v = n, i % (n - 1) + 1
        elif i < n - 1: u, v = i + 2, i + 1
        else:
            u = rng.randrange(2, n + 1)
            v = rng.randrange(1, u)
        print(u, v, file=output)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', dest='cases')
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    known = {case['id'] for case in plan['cases']}
    if args.cases and set(args.cases) - known:
        parser.error('unknown case: ' + ', '.join(sorted(set(args.cases) - known)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in plan['cases']:
        if args.cases and spec['id'] not in args.cases:
            continue
        path = args.out_dir / (spec['id'] + '.in')
        with path.open('w', encoding='ascii', newline='\n') as output:
            generate(spec, output)
        if args.std:
            with path.open('rb') as source:
                result = subprocess.run([str(args.std.resolve())], stdin=source, capture_output=True, check=True)
            path.with_suffix('.out').write_bytes(result.stdout.replace(b'\r\n', b'\n'))

if __name__ == '__main__':
    main()
