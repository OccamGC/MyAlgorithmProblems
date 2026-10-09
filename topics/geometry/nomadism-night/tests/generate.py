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
    n = spec['n']
    kind = spec['kind']
    if kind == 'same':
        points = [(10000,-10000)] * n
    elif kind == 'grid':
        points = [(i%800*24-9588,i//800*40-9980) for i in range(n)]
    elif kind == 'narrow':
        points = [(i%20000-10000,i//20000-10) for i in range(n)]
    elif kind in ('horizontal','vertical','diagonal','antidiagonal'):
        values = [i%20001-10000 for i in range(n)]
        points = [(x,0) if kind=='horizontal' else (0,x) if kind=='vertical'
                  else (x,x) if kind=='diagonal' else (x,-x) for x in values]
    elif kind == 'circle':
        sites = [(x,y) for x in range(-65,66) for y in range(-65,66) if x*x+y*y==65*65]
        points = [sites[i%len(sites)] for i in range(n)]
    elif kind == 'clusters':
        centers = [(x,y) for x in range(-8000,8001,4000) for y in range(-8000,8001,4000)]
        points = [(centers[i%25][0]+rng.between(-400,400),
                   centers[i%25][1]+rng.between(-400,400)) for i in range(n)]
    elif kind == 'boundary':
        def boundary(i):
            t = i%80000
            side,offset = divmod(t,20000)
            return [(-10000+offset,-10000),(10000,-10000+offset),
                    (10000-offset,10000),(-10000,10000-offset)][side]
        points = [boundary(i) for i in range(n)]
    elif kind == 'columns':
        points = [((-10000 if i%2 else 10000),i//2%20001-10000) for i in range(n)]
    elif kind == 'zigzag':
        points = [(i//20-10000,(i%20)*1000-9500) for i in range(n)]
    else:
        points = [(rng.between(-10000,10000),rng.between(-10000,10000)) for _ in range(n)]
    rng.shuffle(points)
    output.write(str(n)+'\n')
    output.writelines(f'{x} {y}\n' for x,y in points)

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
