"""Deterministic test recipes; Python 3 standard library only."""
import argparse, json, random, subprocess
from pathlib import Path

def generate(case):
    mode = case['mode']
    if mode == 'literal':
        return case['input']
    if mode == 'deep':
        depth = case['depth']
        return '1 1\n' + '(' * depth + '1' + ')' * depth + '\n'
    if mode == 'wide':
        return '1 1\n' + '&&'.join(['1'] * case['terms']) + '\n'
    M = case['m']
    if mode == 'chain':
        return '1 ' + str(M) + '\n' + '\n'.join(str(i) for i in range(1, M + 1)) + '\n'
    if mode == 'cycle':
        return '0 ' + str(M) + '\n' + '\n'.join(str(i % M + 1) for i in range(1, M + 1)) + '\n'
    if mode == 'break':
        expressions = [str(i) for i in range(3, M + 2)] + ['1||2']
        return '1 ' + str(M) + '\n' + '\n'.join(expressions) + '\n'
    rng = random.Random(case['seed'])
    N = case.get('n', 3)
    lines = []
    for _ in range(M):
        a, b, c = [rng.randint(1, N + M) for _ in range(3)]
        lines.append(f'({a} && {b}) || {c}')
    return f'{N} {M}\n' + '\n'.join(lines) + '\n'

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
