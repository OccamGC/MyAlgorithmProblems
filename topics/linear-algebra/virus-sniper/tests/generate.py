"""Generate deterministic test inputs; optionally run a locally compiled reference."""
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


def make_case(spec, output):
    rng = SplitMix64(spec['seed'])
    kind = spec['kind']
    if kind == 'sample':
        output.write((Path(__file__).parent / 'samples' / (spec['sample'] + '.in')).read_text(encoding='ascii'))
        return
    A, B, N, M, Q = (spec[k] for k in ('A','B','N','M','Q'))
    times = list(map(str, spec.get('times', [])))
    if spec.get('huge'):
        times = ['0', str(10**18), '9'*1000, '1'+'0'*1000,
                 ''.join(str(rng.between(1,9) if i==0 else rng.between(0,9)) for i in range(1000))]
    output.write(f'{A} {B} {N} {M} {Q} {len(times)}\n')
    for _ in range(Q):
        if spec.get('full_updates'):
            x1,y1,x2,y2,value = 1,1,A,B,1000000000
        else:
            x1,x2 = sorted((rng.between(1,A),rng.between(1,A)))
            y1,y2 = sorted((rng.between(1,B),rng.between(1,B)))
            value = rng.between(0,1000000000)
        output.write(f'{x1} {y1} {x2} {y2} {value}\n')
    for i in range(N*M):
        pairs = []
        for direction in range(5):
            if kind == 'identity':
                a,b = 0,1
            elif kind == 'zero-scalar':
                a,b = (9,1000000000) if direction==0 else (1,1)
            elif kind == 'one-way':
                a,b = int(direction==4),1
            else:
                b = rng.between(1,1000000000)
                a = rng.between(0,b)
            pairs += [a,b]
        output.write(' '.join(map(str,pairs)) + '\n')
    output.write('\n'.join(times) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--std", type=Path)
    parser.add_argument("--case")
    args = parser.parse_args()
    plan = json.loads((Path(__file__).parent / "plan.json").read_text(encoding="utf-8"))
    cases = [spec for spec in plan["cases"] if args.case is None or spec["id"] == args.case]
    if not cases:
        parser.error("unknown case id")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for spec in cases:
        input_path = args.out_dir / (spec["id"] + ".in")
        with input_path.open("w", encoding="utf-8", newline="\n") as output:
            make_case(spec, output)
        if args.std is not None:
            with input_path.open("rb") as source, input_path.with_suffix(".out").open("wb") as answer:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=answer, check=True)
        print(input_path)

if __name__ == "__main__":
    main()
