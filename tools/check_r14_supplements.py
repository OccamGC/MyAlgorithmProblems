"""Compile and independently verify the supplementary solutions for batch R14."""
from pathlib import Path
import json
import math
import random
import subprocess

import check_r14 as base
from check_r14_formulas import determinant, matrix_recurrence

ROOT = Path(__file__).resolve().parents[1]
METHODS = {
    'grox-sequence-4': ('combinatorics', 'residue'),
    'grox-sequence-5a': ('combinatorics', 'decimal'),
    'grox-sequence-5b': ('combinatorics', 'fps'),
    'grox-sequence-6': ('linear-algebra', 'newton'),
    'grox-sequence-7': ('linear-algebra', 'product-tree'),
    'gnome-sort': ('sorting', 'fenwick'),
}


def program(slug):
    return ROOT / 'build/bin' / f'{slug}-alternative-{METHODS[slug][1]}.exe'


def run(slug, text):
    return list(map(int, subprocess.check_output(
        [str(program(slug))], input=text.encode(), timeout=90).split()))


def compile_sources():
    compiler = ROOT.parent / 'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    flags = ['-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Wpedantic']
    for slug, (topic, method) in METHODS.items():
        source = ROOT / 'topics' / topic / slug / f'alternative-{method}.cpp'
        result = subprocess.run([str(compiler), *flags, str(source), '-o', str(program(slug))],
                                capture_output=True, text=True, check=True)
        assert not result.stderr, (slug, result.stderr)
        print(f'Compiled without warnings: {slug}/{method}', flush=True)
    source = ROOT / 'topics/combinatorics/grox-sequence-5b/std.cpp'
    result = subprocess.run([str(compiler), *flags, str(source), '-o',
                             str(ROOT / 'build/bin/grox-sequence-5b.exe')],
                            capture_output=True, text=True, check=True)
    assert not result.stderr, result.stderr


def main():
    compile_sources()
    original_run = base.run
    counts = {slug: 0 for slug in METHODS}

    def compared_run(slug, text, suffix=''):
        expected = original_run(slug, text, suffix)
        if not suffix:
            actual = run(slug, text)
            assert actual == expected, (slug, text, actual, expected)
            counts[slug] += 1
            if sum(counts.values()) % 200 == 0:
                print('Independent model cases:', sum(counts.values()), flush=True)
        return expected

    # The base suite separately checks each returned result against its independent oracle.
    base.run = compared_run
    base.main()
    base.run = original_run
    rng = random.Random(2026093022)
    extra = {}
    count = 0
    for beta in [0, 1, -1, 2, -1000000000, 1000000000]:
        for k in range(6):
            alpha = rng.randrange(-10**9, 10**9 + 1)
            coeff = [rng.randrange(-10**9, 10**9 + 1) for _ in range(k + 1)]
            indices = [0, 1, 200, 999999937, 1000000000]
            text = f'{len(indices)} {beta} {k}\n' + ' '.join(map(str, [alpha, *coeff])) + '\n'
            text += ''.join(f'0 {n}\n' for n in indices)
            assert run('grox-sequence-6', text) == [matrix_recurrence(beta, alpha, coeff, n) for n in indices]
            count += 1
    extra['large_index_matrix_models'] = count
    count = 0
    for k in range(3):
        n = 1 << k
        for _ in range(12):
            a = [[rng.randrange(1000) for _ in range(n)] for _ in range(n)]
            text = f'{k}\n' + '\n'.join(' '.join(map(str, row)) for row in a) + '\n'
            assert run('grox-sequence-7', text) == determinant(a)
            count += 1
    extra['direct_determinants'] = count
    count = 0
    for n in [0, 1, 2, 7, 40]:
        for k in [511, 512, 513, 4095, 4096, 65535, 65536, 100000]:
            text = f'{n} {k}\n'
            expected = base.oracle('grox-sequence-5b', text)
            assert run('grox-sequence-5b', text) == expected
            assert original_run('grox-sequence-5b', text) == expected
            count += 1
    extra['high_degree_direct_binomial_sums'] = count
    formal = {}
    for slug, (topic, _) in METHODS.items():
        problem = ROOT / 'topics' / topic / slug
        samples = sorted((problem / 'tests/samples').glob('*.in'))
        for sample in samples:
            assert run(slug, sample.read_text()) == list(map(int, sample.with_suffix('.out').read_text().split()))
        cases = sorted((ROOT / 'build/data' / slug).glob('*.in'))
        for case in cases:
            text = case.read_text()
            assert run(slug, text) == original_run(slug, text)
        formal[slug] = {'samples': len(samples), 'formal_inputs': len(cases)}
        print('Formal inputs verified:', slug, len(cases), flush=True)
    report = {'base_seed': 2026093014, 'extra_seed': 2026093022, 'independent_cases': counts,
              'independent_total': sum(counts.values()), 'extra': extra, 'formal': formal}
    (ROOT / 'build/R14-supplement-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
