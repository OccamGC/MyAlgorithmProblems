"""Generate deterministic inputs using Python 3; optionally run a compiled reference."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec, output):
    rng = random.Random(spec['seed'])
    k, total, m, mode = spec['k'], spec['total'], spec['m'], spec['mode']
    print(k, m, file=output)
    for i in range(k):
        size = total // k + (i < total % k)
        if mode == 'uneven': size = total - k + 1 if i == 0 else 1
        if mode == 'equal': values = [-1000000000] * size
        elif mode == 'extremes': values = [-1000000000] * (size // 2) + [1000000000] * (size - size // 2)
        elif mode == 'interleaved': values = [j * k + i - total // 2 for j in range(size)]
        elif mode == 'ranges': values = [i * 20000000 + j for j in range(size)]
        else: values = sorted(rng.randrange(-1000000000, 1000000001) for _ in range(size))
        if i % 2 or mode == 'descending': values.reverse()
        output.write(str(size) + ' ' + ' '.join(map(str, values)) + '\n')

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
