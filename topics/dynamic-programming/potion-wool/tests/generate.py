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
    a,b,p,k,t=s['a'],s['b'],s['p'],s['k'],s['t']
    if s['kind']=='negative':effects=[-100]*k
    elif s['kind']=='positive':effects=[100]*k
    else:effects=[rng.below(201)-100 for _ in range(k)]
    counts=[[rng.below(11) for _ in range(k)] for _ in range(p)]
    for row in counts:
        if not any(row):row[0]=1
    cells=[str(i) for i in range(p)]+['S']+['C']*s['chests']
    cells+=['E']*(a*b-len(cells));rng.shuffle(cells)
    if s['kind']=='maze':
        # Keep one connected snake corridor; place all objects on it.
        path=[x*b+y for x in range(a) for y in range(b) if x%2==0 or y==(b-1 if x%4==1 else 0)]
        objects=[str(i) for i in range(p)]+['S']+['C']*s['chests']
        rng.shuffle(path);cells=['B']*(a*b)
        for pos in path:cells[pos]='E'
        for pos,value in zip(path,objects):cells[pos]=value
    return f'{a} {b} {p} {k} {t}\n'+' '.join(map(str,effects))+'\n'+'\n'.join(' '.join(map(str,row)) for row in counts)+'\n'+'\n'.join(' '.join(cells[i*b:(i+1)*b]) for i in range(a))+'\n'

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
