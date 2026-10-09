"""Generate reproducible inputs from plan.json; optionally run a compiled reference."""
import argparse
import json
import subprocess
from pathlib import Path

class Random:
    def __init__(self, seed): self.state = seed
    def next(self):
        mask = (1 << 64) - 1
        self.state = (self.state + 0x9e3779b97f4a7c15) & mask
        value = self.state
        value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & mask
        value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & mask
        return value ^ (value >> 31)
    def below(self, n): return self.next() % n
    def shuffle(self, values):
        for i in range(len(values)-1, 0, -1):
            j = self.below(i+1)
            values[i], values[j] = values[j], values[i]


def generate(s, rng):
    n=s['n'];m=s['m'];kind=s['kind']
    lines=[f'{n} {m}']
    for v in range(2,n+1):
        p = v-1 if kind in ('chain','relink','negative') else 1 if kind=='star' else v//2 if kind=='balanced' else 1+rng.below(v-1)
        w = -10000 if kind=='negative' else rng.below(20001)-10000
        lines.append(f'{p} {v} {w}')
    budget=200000
    for i in range(m):
        a=1+rng.below(n);b=1+rng.below(n);w=rng.below(20001)-10000
        if kind=='wide' and i==0:
            lines.append('4 '+str(n)+' '+' '.join(map(str,range(1,n+1))))
            budget-=n
        elif kind=='relink':
            phase=i%4
            lines.append(f'1 {n} {1 if i//4%2==0 else n-1} {w}' if phase==0 else f'3 {n} {1 if i//4%2==0 else n-1} {w}' if phase==1 else f'4 1 {n}' if phase==2 else f'4 2 {n} {n-1}')
        elif i%4==0 and budget>=2:
            if a==b:b=b%n+1
            lines.append(f'4 2 {a} {b}');budget-=2
        elif i%4==1:
            lines.append(f'2 {a}')
        elif i%4==2:
            lines.append(f'1 {a} {b} {w}')
        else:
            lines.append(f'3 {a} {b} {w}')
    return '\n'.join(lines)+'\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case')
    args = parser.parse_args()
    problem = Path(__file__).resolve().parents[1]
    output = args.out_dir.resolve()
    if output == problem or problem in output.parents:
        parser.error('Place generated data outside the problem directory.')
    specs = json.loads(args.plan.read_text(encoding='utf-8'))['cases']
    if args.case and args.case not in {s['id'] for s in specs}: parser.error('Unknown case id')
    output.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        if args.case and spec['id'] != args.case: continue
        if spec['kind'] == 'sample':
            data = (problem/'tests/samples'/(spec['sample']+'.in')).read_text(encoding='ascii')
        else: data = generate(spec, Random(spec['seed']))
        path = output/(spec['id']+'.in')
        path.write_text(data, encoding='ascii', newline='\n')
        if args.std:
            with path.open('rb') as source, path.with_suffix('.out').open('wb') as sink:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=sink, check=True)
        print(spec['id'], flush=True)

if __name__ == '__main__': main()
