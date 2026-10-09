"""Generate deterministic inputs; optionally run a locally compiled reference."""
import argparse
import json
import subprocess
from pathlib import Path

MASK = (1 << 64) - 1

class SplitMix64:
    def __init__(self, seed):
        self.state = seed & MASK

    def next(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK
        value = self.state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK
        return value ^ (value >> 31)

    def between(self, low, high):
        return low + self.next() % (high - low + 1)

    def shuffle(self, values):
        for i in range(len(values)-1, 0, -1):
            j = self.between(0, i)
            values[i], values[j] = values[j], values[i]

def make_case(spec, output):
    if spec['kind'] == 'sample':
        output.write((Path(__file__).parent/'samples'/(spec['sample']+'.in')).read_text(encoding='utf-8'))
        return
    rng = SplitMix64(spec['seed'])
    make_generated(spec, output, rng)

def make_generated(spec, output, rng):
    q,n,kind = spec['q'],spec['n'],spec['kind']
    output.write(f'{q}\n')
    for i in range(q):
        half = n//2
        if kind in ('all-change','same','impossible','center'):
            text = '0'*n
        else:
            text = ''.join(str(rng.between(0,3)) for _ in range(n))
        m = rng.between(0,n)
        if kind == 'all-change':
            m=n
        elif kind == 'same':
            m=0
        elif kind == 'center':
            m=1
        elif kind == 'impossible':
            text='0'*(half+1)+'1'*half
            m=max(0,half-1)
        elif kind == 'minimum':
            m=sum(text[j]!=text[j+half+1] for j in range(half))
        output.write(f'{n} {m} {text}\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    parser.add_argument('--std', type=Path)
    parser.add_argument('--case')
    args = parser.parse_args()
    problem = Path(__file__).resolve().parents[1]
    destination = args.out_dir.resolve()
    if destination == problem or destination.is_relative_to(problem):
        parser.error('write generated data outside the problem directory')
    plan = json.loads((Path(__file__).parent/'plan.json').read_text(encoding='utf-8'))
    cases = [case for case in plan['cases'] if args.case is None or case['id'] == args.case]
    if not cases:
        parser.error('unknown case id')
    destination.mkdir(parents=True, exist_ok=True)
    for case in cases:
        path = destination/(case['id']+'.in')
        with path.open('w', encoding='utf-8', newline='\n') as output:
            make_case(case, output)
        if args.std is not None:
            with path.open('rb') as source, path.with_suffix('.out').open('wb') as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(path)

if __name__ == '__main__':
    main()
