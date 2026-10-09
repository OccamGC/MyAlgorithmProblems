"""Generate deterministic inputs using Python 3; optionally run a compiled reference."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec, output):
    rng = random.Random(spec['seed'])
    n, mode = spec['n'], spec['mode']
    if mode == 'ascending': values = [i - n // 2 for i in range(n)]
    elif mode == 'descending': values = [n // 2 - i for i in range(n)]
    elif mode == 'negative': values = [-1000000000] * n
    elif mode == 'positive': values = [1000000000] * n
    elif mode == 'alternating': values = [1000000000 if i % 2 else -1000000000 for i in range(n)]
    elif mode == 'duplicates': values = [rng.choice([-7, 0, 7]) for _ in range(n)]
    elif mode == 'zero': values = [0] * n
    else: values = [rng.randrange(-1000000000, 1000000001) for _ in range(n)]
    print(n, file=output)
    print(*values, file=output)

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
