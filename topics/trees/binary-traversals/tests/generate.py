"""Generate deterministic inputs using Python 3; optionally run a compiled reference."""
import argparse
import json
from pathlib import Path
import random
import subprocess

def generate(spec, output):
    rng = random.Random(spec['seed'])
    n, mode = spec['n'], spec['mode']
    left, right = [-1] * n, [-1] * n
    if mode in ('left', 'right', 'zigzag'):
        for i in range(n - 1):
            (left if mode == 'left' or mode == 'zigzag' and i % 2 == 0 else right)[i] = i + 1
    elif mode == 'random':
        slots = [(0, 0), (0, 1)]
        for i in range(1, n):
            at = rng.randrange(len(slots))
            parent, side = slots[at]
            slots[at] = slots[-1]
            slots.pop()
            (left if side == 0 else right)[parent] = i
            slots.extend([(i, 0), (i, 1)])
    else:
        for i in range(n):
            if 2 * i + 1 < n: left[i] = 2 * i + 1
            if 2 * i + 2 < n: right[i] = 2 * i + 2
    labels = list(range(1, n + 1))
    if spec.get('shuffle', False): rng.shuffle(labels)
    preorder, inorder = [], []
    stack = [(0, False)]
    while stack:
        u, emit = stack.pop()
        if emit:
            inorder.append(labels[u])
            continue
        preorder.append(labels[u])
        if right[u] != -1: stack.append((right[u], False))
        stack.append((u, True))
        if left[u] != -1: stack.append((left[u], False))
    print(n, file=output)
    print(*preorder, file=output)
    print(*inorder, file=output)

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
