"""Deterministic test recipes; Python 3 standard library only."""
import argparse, json, random, subprocess
from pathlib import Path

def generate(case):
    n = case['n']
    rng = random.Random(case['seed'])
    children = [[0, 0] for _ in range(n + 1)]
    mode = case['mode']
    if mode in ['down', 'right', 'zigzag']:
        for i in range(1, n):
            side = 0 if mode == 'down' else 1 if mode == 'right' else i % 2
            children[i][side] = i + 1
    elif mode == 'balanced':
        for i in range(2, n + 1):
            children[i // 2][i % 2] = i
    else:
        slots = [(1, 0), (1, 1)]
        for i in range(2, n + 1):
            pos = rng.randrange(len(slots))
            parent, side = slots[pos]
            slots[pos] = slots[-1]
            slots.pop()
            children[parent][side] = i
            slots.extend([(i, 0), (i, 1)])
    labels = list(range(1, n + 1))
    rng.shuffle(labels)
    labels = [0] + labels
    output = [[0, 0] for _ in range(n + 1)]
    for i in range(1, n + 1):
        output[labels[i]] = [labels[x] for x in children[i]]
    return str(n) + '\n' + '\n'.join(f'{a} {b}' for a, b in output[1:]) + '\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    requested = set(args.case)
    unknown = requested - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if requested and case['id'] not in requested:
            continue
        target = args.out_dir / (case['id'] + '.in')
        target.write_text(generate(case), encoding='utf-8', newline='\n')
        if args.std:
            with target.open('rb') as source, target.with_suffix('.out').open('wb') as output:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=output, check=True)
if __name__ == '__main__':
    main()
