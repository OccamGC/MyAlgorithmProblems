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
    n=s['n']; low=s['L']; high=s['R']; shape=s['kind']
    mode=s.get('weights','random')
    values=[1000 if mode=='positive' else -1000 if mode=='negative' else (1000 if i%2 else -999) if mode=='alternating' else rng.below(2001)-1000 for i in range(n)]
    edges=[]
    for v in range(1,n):
        parent=v-1 if shape=='chain' else 0 if shape=='star' else (v-1)//2 if shape=='binary' else min(v-1,n//2) if shape=='broom' else rng.below(v)
        edges.append((parent+1,v+1))
    if s.get('relabel'):
        labels=list(range(2,n+1));rng.shuffle(labels);labels=[1]+labels
        edges=[(labels[u-1],labels[v-1]) for u,v in edges]
        shuffled=[0]*n
        for i,label in enumerate(labels): shuffled[label-1]=values[i]
        values=shuffled
    return f'{n} {low} {high}\n'+' '.join(map(str,values))+'\n'+''.join(f'{u} {v}\n' for u,v in edges)

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
