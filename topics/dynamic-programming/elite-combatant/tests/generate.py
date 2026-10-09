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
    initial_health, boris_attack, health_bonus = 1000000000, 100000, 1000000000
    if kind == 'small':
        types = [('Alpha', 20, 30, 2), ('Beta', 80, 10, 1)]
        initial_health, boris_attack, health_bonus = 100, 50, 100
    elif kind == 'healing':
        types = [('Medic', 100000, -100000, 50000)]
        boris_attack = 1
    elif kind == 'neutral':
        types = [('Factory', 100000, 0, 50000)]
        boris_attack = 1
    elif kind == 'absent':
        types = [('Unused', 100000, 100000, 0), ('无伤单位', 5, 0, 1)]
        initial_health, boris_attack, health_bonus = 1, 1, 0
    elif kind == 'fatal':
        types = [('EnemyA', 100000, 100000, 2), ('EnemyB', 100000, 100000, 2),
                 ('Healer', 1, -1, 1)]
        initial_health, boris_attack, health_bonus = 1, 1, 0
    elif kind == 'midturn':
        # Both boost and removal must still check survival before final healing.
        types = [('EnemyA', 3, 4, 2), ('EnemyB', 3, 4, 2), ('Healer', 1, -5, 1)]
        initial_health, boris_attack, health_bonus = 5, 1, 0
    elif kind == 'dense':
        types = [(f'Enemy{i}', rng.between(1, 100000), 1, 2000) for i in range(20)]
        types.append(('Healer', 100000, -100000, 10000))
        boris_attack = 1
    elif kind == 'types':
        types = [(f'Type{i}', rng.between(1, 100000),
                  rng.between(1, 20) if i < 20 else -rng.between(0, 100000), 10) for i in range(5000)]
    elif kind == 'wide':
        types = [(f'Enemy{i}', 100000, rng.between(1, 100000), 1250) for i in range(20)]
        types.append(('Healer', 100000, -100000, 25000))
        boris_attack = 1
    else:
        types = [(f'Enemy{i}', rng.between(1, 100000), rng.between(1, 1000), 1) for i in range(20)]
    output.write(f'{len(types)} {sum(t[3] for t in types)} {initial_health} {boris_attack} {health_bonus}\n')
    for name, health, power, count in types:
        output.write(f'{name} {health} {power}\n')
    # Reverse input order to exercise name lookup independently of declaration order.
    for name, health, power, count in reversed(types):
        for _ in range(count):
            output.write(name + '\n')

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
