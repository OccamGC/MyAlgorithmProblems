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
        text = (Path(__file__).parent / 'samples' / (spec['sample']+'.in')).read_text(encoding='ascii')
        lines = text.splitlines()
        header = lines[0].split()
        header[3] = str(spec['mod'])
        lines[0] = ' '.join(header)
        output.write('\n'.join(lines)+'\n')
        return
    N,M,K,mod = (spec[key] for key in ('N','M','K','mod'))
    times = list(range(K))
    for i in range(K-1, 0, -1):
        j = rng.between(0,i)
        times[i],times[j] = times[j],times[i]
    if spec['group'] != 1:
        times = [10**18-K+value+1 for value in times]
    output.write(f'{N} {M} {K} {mod}\n')
    for i in range(K):
        if kind == 'clique':
            x,y,age = 1,2**i,i
        elif kind == 'overlap':
            x,y,age = 1,1,times[i]
        elif kind == 'line':
            x,y,age = 1,1+(M-1)*i//max(K-1,1),times[i]
        else:
            x,y,age = rng.between(1,N),rng.between(1,M),times[i]
        if kind == 'star' or kind == 'overlap':
            thresholds = [K]*K
        elif spec.get('all_thresholds') or kind == 'clique':
            thresholds = list(range(1,K+1))
        else:
            thresholds = [rng.between(1,K) for _ in range(rng.between(0,K-1))] + [K]
        output.write(f'{x} {y} {age} {len(thresholds)} ' + ' '.join(map(str,thresholds)) + '\n')

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
