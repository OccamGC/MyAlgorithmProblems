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


def generate(s,rng):
    n=s['n'];q=s['q'];kind=s['kind']
    components=[];edges=[]
    chunk=1000 if kind=='forest' else 1 if kind=='isolated' else n
    for begin in range(1,n+1,chunk):
        end=min(n+1,begin+chunk);components.append((begin,end))
        for v in range(begin+1,end):
            p=v-1 if kind in ('chain','negative','forest') else begin if kind=='star' else begin+(v-begin-1)//2 if kind=='balanced' else begin+rng.below(v-begin)
            edges.append((p,v))
    initial=[-10000 if kind=='negative' else rng.below(20001)-10000 for _ in range(n)]
    lines=[f'{n} {len(edges)} {q}',' '.join(map(str,initial))]+[f'{a} {b}' for a,b in edges]
    for i in range(q):
        begin,end=components[rng.below(len(components))]
        a=begin+rng.below(end-begin);b=begin+rng.below(end-begin)
        if kind in ('chain','negative') and i%6<4:a=1;b=n
        op=1+i%4
        c=-10000 if kind=='negative' and op<=2 else (-100000000 if kind=='negative' else rng.below(20001)-10000)
        lines.append(f'{op} {a} {b} {c}')
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
