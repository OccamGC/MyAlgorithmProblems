"""Check the R42 C++ programs against exact grids and generic matrix powers."""
from pathlib import Path
from fractions import Fraction
import argparse
import importlib.util
import json
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/R42'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin-dir', type=Path, default=OUT)
    args = parser.parse_args()
    rng = random.Random(421002)
    result = {'seed': 421002, 'problems': {}}
    for number in (4, 5):
        slug = f'town-editing-simoleons-{number}'
        directory = ROOT / 'topics/greedy' / slug
        gen = module(directory / 'tests/generate.py', f'recipe{number}')
        programs = [args.bin_dir / f'{slug}-{p.stem}.exe' for p in directory.glob('*.cpp')]
        counts = {'exact_grid': 0, 'generic_matrix_large_counts': 0, 'invalid_inputs_per_mode': 0}

        def check(rows, expected):
            text = gen.as_text(rows)
            gen.validate(text)
            for program in programs:
                output = subprocess.check_output([str(program.resolve())], input=text.encode(), timeout=10).decode()
                if not gen.matches(output, str(expected)):
                    raise ValueError((program, rows, expected, output))

        for _ in range(350 if number == 4 else 400):
            k = rng.randint(1, 12 if number == 4 else 8)
            rows = [(k, rng.randrange(51))]
            if number == 4:
                rows += [(1, rng.randrange(51)) for _ in range(rng.randrange(21))] + [(0, 0)]
            else:
                levels = rng.sample([Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(3, 2), Fraction(7, 3), Fraction(9)], 3)
                for _ in range(rng.randrange(8)):
                    value = rng.choice(levels); scale = rng.randint(1, 2)
                    rows.append((value.denominator * scale, value.numerator * scale))
                rows += [(0, 0)] * max(0, k + len(gen.groups(rows)) + 1 - len(rows))
            answer = gen.exact(rows)
            if gen.matrix(rows) != answer:
                raise ValueError('independent grid / matrix disagreement')
            check(rows, answer)
            counts['exact_grid'] += 1

        for _ in range(100 if number == 4 else 30):
            k = rng.randint(100000, 1000000) if number == 4 else rng.randint(1, 20)
            rows = [(k, rng.randrange(1000000001))]
            if number == 4:
                rows += [(1, rng.randrange(1000000001)) for _ in range(rng.randrange(13))] + [(0, 0)]
            else:
                for value in (997, 998, 999):
                    for _ in range(rng.randint(1, 8)):
                        population = rng.randint(100000, 1000000)
                        rows.append((population, population * value))
                rows += [(0, 0)] * max(0, k + len(gen.groups(rows)) + 1 - len(rows))
            check(rows, gen.matrix(rows))
            counts['generic_matrix_large_counts'] += 1

        invalid = ['1\n1 0\n', '1000001\n', '2\n0 0\n0 0\n',
                   '2\n1 -1\n0 0\n', '2\n1 1000000001\n0 0\n',
                   '2\n1 0\n0 1\n', '2\n1 0\n', '2\n1 0\n0 0\nextra\n',
                   '2\n1 0\n-1 0\n', '2\n1 0 1\n0 0\n']
        invalid += (['2\n1 0\n1 1\n', '3\n1 0\n2 1\n0 0\n', '2\n1000001 0\n0 0\n'] if number == 4 else
                    ['2\n21 0\n0 0\n', '3\n1 0\n1000001 1\n0 0\n',
                     '6\n1 0\n1 1\n1 2\n1 3\n1 4\n0 0\n', '3\n2 0\n1 1\n0 0\n'])
        validation = 'import sys; sys.path.insert(0,sys.argv[1]); import generate; generate.validate(sys.stdin.read())'
        valid = [gen.as_text([(1, 0), (0, 0)])]
        if number == 5:
            valid += [gen.as_text([(1, 0), (3, 1), (6, 2)]),
                      gen.as_text([(1, 100), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)])]
        for optimized in (False, True):
            command = [sys.executable] + (['-O'] if optimized else []) + ['-c', validation, str(directory/'tests')]
            for text in invalid:
                process = subprocess.run(command, input=text.encode(), capture_output=True)
                if process.returncode == 0:
                    raise ValueError(('accepted invalid input', number, optimized, text))
            for text in valid:
                subprocess.run(command, input=text.encode(), check=True, capture_output=True)
        counts['invalid_inputs_per_mode'] = len(invalid)
        counts['validator_modes'] = ['normal', '-O']
        for text in ('-1', str(gen.MOD), '1 1', 'nan', '', '2'):
            if gen.matches(text, '1'):
                raise ValueError(('accepted bad output', text))
        result['problems'][slug] = counts
        print(slug, counts, flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'small-checks.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
