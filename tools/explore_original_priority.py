"""P1 scale exploration, separate from the formal input plans.

These inputs intentionally exceed current statement limits; they are experiments,
not scored inputs. No statement or generator limit is changed by this script.
"""
import argparse
import importlib.util
import json
import statistics
from pathlib import Path
import benchmark_reference as ref

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate-only', action='store_true')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('tree_generator', ROOT / 'topics/trees/festival-plan/tests/generate.py')
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    cases = []
    for slug, n in [('forest-ranger', 4000000), ('festival-plan', 2000000), ('grinder', 1000000)]:
        for shape in ['random', 'comb', 'spider', 'chain-window']:
            cases.append({'slug': slug, 'n': n, 'kind': shape, 'seed': 2026093013,
                          'L': max(1, n * 21 // 100) if shape == 'chain-window' else 1,
                          'R': n * 67 // 100 if shape == 'chain-window' else n - 1})
    folder = ROOT / 'build/original-priority/scale'
    folder.mkdir(parents=True, exist_ok=True)
    report = {'purpose': 'Exploratory only; sizes exceed formal statement limits.', 'repeats': 5,
              'generator_sha256': ref.sha256(Path(__file__)), 'cases': []}
    # Generate everything before timing to avoid competing with benchmark processes.
    for case in cases:
        path = folder / (case['slug'] + '-' + case['kind'] + '.in')
        rng = gen.Random(case['seed'])
        n = case['n']
        with path.open('w', encoding='ascii', newline='\n') as out:
            if case['slug'] == 'forest-ranger':
                out.write(f'{n}\n')
            else:
                out.write(f"{n} {case['L']} {case['R']}\n")
                out.write(' '.join(str(rng.below(2001)-1000) for _ in range(n)) + '\n')
            for v in range(2, n+1):
                if case['kind'] == 'random':
                    parent = rng.below(v-1) + 1
                elif case['kind'] == 'comb':
                    parent = v-1 if v <= n//2 else v-n//2
                elif case['kind'] == 'spider':
                    parent = 1 if (v-2) % 8191 == 0 else v-1
                else:
                    parent = v-1
                out.write(f'{parent} {v}\n')
        case['input_bytes'] = path.stat().st_size
        case['input_sha256'] = ref.sha256(path)
        print('generated', path.name, flush=True)
    if args.generate_only:
        return
    for case in cases:
        slug = case['slug']
        source = folder / (slug + '-' + case['kind'] + '.in')
        variants = {}
        for variant in ['std', 'alternative']:
            binary = ROOT / 'build/bin' / (slug + ('' if variant == 'std' else '-alternative') + '.exe')
            output = folder / (variant + '.out')
            peak = ref.run_with_peak_memory(binary, source, output)
            variants[variant] = {'peak_working_set_bytes': peak, 'output_sha256': ref.sha256(output),
                                 'times_seconds': []}
        assert variants['std']['output_sha256'] == variants['alternative']['output_sha256'], case
        for repeat in range(5):
            for variant in (['std', 'alternative'] if repeat % 2 == 0 else ['alternative', 'std']):
                binary = ROOT / 'build/bin' / (slug + ('' if variant == 'std' else '-alternative') + '.exe')
                variants[variant]['times_seconds'].append(ref.run(binary, source, folder / (variant + '.out')))
        for v in variants.values():
            v['median_seconds'] = statistics.median(v['times_seconds'])
        case['variants'] = variants
        report['cases'].append(case)
        (ROOT / 'build/original-priority/scale-P1.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(slug, case['kind'], {k: (v['median_seconds'], v['peak_working_set_bytes']) for k,v in variants.items()}, flush=True)


if __name__ == '__main__':
    main()
