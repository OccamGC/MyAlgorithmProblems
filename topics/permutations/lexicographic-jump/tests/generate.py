"""Deterministic test recipes; Python standard library only."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(case):
    rng=random.Random(case['seed']);lines=[str(len(case['items']))]
    for item in case['items']:
        for repeat in range(item.get('repeat',1)):
            n=item['n'];k=item['k'];shape=item['shape'];values=list(range(1,n+1))
            if shape=='descending':values.reverse()
            elif shape=='random':rng.shuffle(values)
            elif shape=='suffix':
                start=max(1,n//10);values[start:]=values[start:][::-1];part=values[:start];rng.shuffle(part);values[:start]=part
            lines.append(f'{n} {k}');lines.append(' '.join(map(str,values)))
    lines[0]=str(sum(x.get('repeat',1) for x in case['items']))
    return '\n'.join(lines)+'\n'


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
