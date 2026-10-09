"""Compare R14 reference and supplementary programs on the same formal inputs."""
import json
import platform
import statistics
import subprocess
import time

from benchmark_reference import run, run_with_peak_memory, sha256
from check_r14_supplements import ROOT, METHODS, program


def main():
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S %z'),
        'platform': platform.platform(), 'python': platform.python_version(),
        'compiler': 'GCC 16.2.0',
        'compiler_flags': ['-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Wpedantic'],
        'repeats': 5,
        'timing': 'Alternating wall-clock runs, order reversed each round; per-input medians.',
        'memory': 'Separate untimed peak working-set run, including process/runtime overhead.',
        'problems': {},
    }
    compiler = ROOT.parent / 'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    slug = 'grox-sequence-5a'
    source = ROOT / 'topics/combinatorics' / slug / 'alternative-decimal.cpp'
    result = subprocess.run([str(compiler), *report['compiler_flags'], str(source), '-o', str(program(slug))],
                            capture_output=True, text=True, check=True)
    assert not result.stderr, result.stderr
    limits = {'grox-sequence-4': 1.0, 'grox-sequence-5a': 0.5, 'grox-sequence-5b': 0.5,
              'grox-sequence-6': 0.5, 'grox-sequence-7': 1.0, 'gnome-sort': 0.5}
    output_dir = ROOT / 'build/supplement-benchmark'
    output_dir.mkdir(exist_ok=True)
    for slug, (topic, method) in METHODS.items():
        directory = ROOT / 'topics' / topic / slug
        programs = {'standard': ROOT / 'build/bin' / f'{slug}.exe', method: program(slug)}
        sources = {'standard': directory / 'std.cpp', method: directory / f'alternative-{method}.cpp'}
        entry = {
            'indicative_limit_seconds': limits[slug],
            'source_sha256': {name: sha256(path) for name, path in sources.items()},
            'header_sha256': {p.name: sha256(p) for p in sorted(directory.glob('*.hpp'))},
            'program_sha256': {name: sha256(path) for name, path in programs.items()},
            'cases': [],
        }
        for case in sorted((ROOT / 'build/data' / slug).glob('*.in')):
            sinks = {name: output_dir / f'{slug}-{name}.out' for name in programs}
            peak = {name: run_with_peak_memory(exe, case, sinks[name]) for name, exe in programs.items()}
            assert sinks['standard'].read_bytes().split() == sinks[method].read_bytes().split(), (slug, case)
            times = {name: [] for name in programs}
            for repeat in range(5):
                order = list(programs) if repeat % 2 == 0 else list(reversed(programs))
                for name in order:
                    times[name].append(run(programs[name], case, sinks[name]))
            assert sinks['standard'].read_bytes().split() == sinks[method].read_bytes().split(), (slug, case)
            entry['cases'].append({
                'id': case.stem, 'input_sha256': sha256(case),
                'output_sha256': {name: sha256(path) for name, path in sinks.items()},
                'times_seconds': times,
                'medians_seconds': {name: statistics.median(values) for name, values in times.items()},
                'peak_working_set_bytes': peak,
            })
            print(slug, case.stem, entry['cases'][-1]['medians_seconds'], flush=True)
        entry['max_median_seconds'] = {
            name: max(c['medians_seconds'][name] for c in entry['cases']) for name in programs}
        entry['peak_working_set_bytes'] = {
            name: max(c['peak_working_set_bytes'][name] for c in entry['cases']) for name in programs}
        entry['over_limit_cases'] = {
            name: [c['id'] for c in entry['cases'] if c['medians_seconds'][name] > limits[slug]]
            for name in programs}
        report['problems'][slug] = entry
        print('Completed:', slug, entry['max_median_seconds'], flush=True)
    target = ROOT / 'docs/benchmark-R14-supplements.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Saved:', target, flush=True)


if __name__ == '__main__':
    main()
