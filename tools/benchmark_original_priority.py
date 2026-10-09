"""Compare restored original algorithms with the preserved alternatives (P1).

Compile std.cpp and alternative.cpp into build/bin/<slug>[-alternative].exe first.
Generate the existing formal plans into build/data/<slug>. This driver validates
those inputs, checks both outputs, and records five alternating timed repetitions.
No limits or data plans are changed by this script.
"""
import importlib
import json
import math
import platform
import statistics
import subprocess
import time
import sys
from pathlib import Path
import benchmark_reference as ref

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ['forest-ranger', 'festival-plan', 'grinder', 'vacuum-imploder',
         'psychic-control-tree', 'spice-routes', 'colony-trade', 'gran-forest', 'crystal-list']


def main():
    for name in ['validate_ra1', 'validate_ra2', *['validate_r' + str(i) for i in range(6, 13)]]:
        module = importlib.import_module(name)
        ref.VALIDATORS.update(module.VALIDATORS)
        ref.GROUP_SHARES.update(module.GROUP_SHARES)
    folder = ROOT / 'build/original-priority'
    folder.mkdir(exist_ok=True, parents=True)
    report = {'timestamp': time.strftime('%Y-%m-%d %H:%M:%S %z'),
              'platform': platform.platform(), 'python': platform.python_version(),
              'repeats': 5, 'multiplier': 2, 'resolution_seconds': 0.5,
              'timing': 'One warm run with peak working set; five alternating wall-clock runs; median per case.',
              'problems': {}}
    if '--resume' in sys.argv:
        report = json.loads((folder / 'benchmark-P1.json').read_text(encoding='utf-8'))
    for slug in SLUGS:
        problem = next((ROOT / 'topics').glob('*/' + slug))
        if slug in report['problems']:
            old = report['problems'][slug]
            assert all(old['sources_sha256'][v] == ref.sha256(problem / (v + '.cpp')) for v in ['std', 'alternative'])
            print('Using completed measurements:', slug, flush=True)
            continue
        plan = json.loads((problem / 'tests/plan.json').read_text(encoding='utf-8'))
        ref.validate_groups(slug, plan)
        binaries = {v: ROOT / 'build/bin' / (slug + ('' if v == 'std' else '-alternative') + '.exe')
                    for v in ['std', 'alternative']}
        rows = []
        entry = {'sample_counts': {v: ref.check_samples(problem, p) for v, p in binaries.items()},
                 'sources_sha256': {v: ref.sha256(problem / (v + '.cpp')) for v in binaries},
                 'binaries_sha256': {v: ref.sha256(p) for v, p in binaries.items()},
                 'generator_sha256': ref.sha256(problem / 'tests/generate.py'),
                 'plan_sha256': ref.sha256(problem / 'tests/plan.json'), 'cases': rows}
        for spec in plan['cases']:
            source = ROOT / 'build/data' / slug / (spec['id'] + '.in')
            dims = ref.VALIDATORS[slug](source)
            ref.validate_group_case(slug, spec, dims)
            outputs = {v: folder / (slug + '-' + v + '.out') for v in binaries}
            variants = {}
            for variant, binary in binaries.items():
                peak = ref.run_with_peak_memory(binary, source, outputs[variant])
                ref.check_output(slug, outputs[variant], dims)
                variants[variant] = {'peak_working_set_bytes': peak,
                                     'output_sha256': ref.sha256(outputs[variant]), 'times_seconds': []}
            if slug == 'vacuum-imploder':
                subprocess.run([str(ROOT / 'build/bin/vacuum-imploder-checker.exe'), str(source),
                                str(outputs['std']), str(outputs['alternative'])], check=True,
                               stdout=subprocess.DEVNULL)
            else:
                assert variants['std']['output_sha256'] == variants['alternative']['output_sha256'], (slug, spec['id'])
            for repeat in range(5):
                order = ['std', 'alternative'] if repeat % 2 == 0 else ['alternative', 'std']
                for variant in order:
                    variants[variant]['times_seconds'].append(ref.run(binaries[variant], source, outputs[variant]))
            for value in variants.values():
                value['median_seconds'] = statistics.median(value['times_seconds'])
            rows.append({'id': spec['id'], 'group': spec['group'], 'score_percent': spec['score_percent'],
                         'dimensions': dims, 'input_bytes': source.stat().st_size,
                         'input_sha256': ref.sha256(source), 'variants': variants})
            print(slug, spec['id'], {v: round(r['median_seconds'], 6) for v,r in variants.items()}, flush=True)
        for variant in binaries:
            med = max(r['variants'][variant]['median_seconds'] for r in rows)
            entry[variant] = {'standard_time_seconds': med, 'indicative_limit_seconds': math.ceil(med * 4) / 2,
                              'peak_working_set_bytes': max(r['variants'][variant]['peak_working_set_bytes'] for r in rows)}
        report['problems'][slug] = entry
        (folder / 'benchmark-P1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('SUMMARY', slug, entry['std'], entry['alternative'], flush=True)


if __name__ == '__main__':
    main()
