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
    n=s['n']; m=s['m']; kind=s['kind']
    potential=[rng.below(200000001)-100000000 for _ in range(n)]
    edges=[]
    for index in range(m):
        u=rng.below(n);v=rng.below(n-1)
        if v>=u:v+=1
        if kind=='dag' and u>v:u,v=v,u
        w=rng.below(1001)+potential[v]-potential[u]
        if kind=='ties':w=0
        edges.append((u+1,v+1,w))
    if kind=='negative-cycle':edges[:2]=[(n-1,n,-1000000000),(n,n-1,999999999)]
    rows=[]
    for i in range(n):
        k=0 if kind=='no-targets' else 10
        quantity=0 if kind=='no-travelers' else rng.below(1000000001)
        capacity=rng.below(1000000001)
        visits=0 if kind=='zero-cost' else rng.below(31)
        price=rng.below(31)
        rows.append((k,quantity,visits,capacity,price))
    return f'{n} {m}\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)+''.join(' '.join(map(str,row))+'\n' for row in rows)

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
