"""Validate tree stress inputs and calibrate the added formal chain cases.

Read recipes and measured hashes from docs/benchmark-tree-stress.json, rebuild
the instrumented trail program, and regenerate its inputs and operation counts.
The six measured reference binaries must already exist under build/bin.
Use --verify-only to check reproduction without repeating timed calibration.
All generated files stay under build; published records are never rewritten.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import platform
import subprocess
import time

import benchmark_reference as bench
import search_adversarial_trees as stress
import profile_priority_work as profile
import validate_r11 as contracts

ROOT = stress.ROOT
OUT = stress.OUT


def count_gains(case, path, source, binary):
    output = OUT/('counted-' + str(case['n']) + '.out')
    with path.open('rb') as input_stream, output.open('wb') as sink:
        run = subprocess.run([str(binary)], stdin=input_stream, stdout=sink,
                             stderr=subprocess.PIPE, check=True, timeout=120)
    output_hash = bench.sha256(output)
    assert output_hash == case['variants']['std']['output_sha256']
    return {'n': case['n'], 'input_sha256': case['input_sha256'],
            'output_sha256': output_hash, 'instrumented_source_sha256': bench.sha256(source),
            'counts': json.loads(run.stderr)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cxx', default='g++', help='Compiler from the measured environment')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    bench.GROUP_SHARES.update(contracts.GROUP_SHARES)
    progs, provenance = stress.programs()
    previous = json.loads((ROOT/'docs/benchmark-P1.json').read_text(encoding='utf-8'))
    recorded = json.loads((ROOT/'docs/benchmark-tree-stress.json').read_text(encoding='utf-8'))
    confirmed, pivot = recorded['confirm'], recorded['pivot']
    source = OUT/'trail-counted.cpp'
    source.write_text(profile.instrument(
        (ROOT/'topics/trees/forest-ranger/alternative.cpp').read_text(encoding='utf-8'),
        'forest-ranger', 'alternative'), encoding='utf-8', newline='\n')
    binary = source.with_suffix('.exe')
    subprocess.run([args.cxx, *stress.FLAGS, str(source), '-o', str(binary)], check=True)
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S %z'),
        'platform': platform.platform(), 'python': platform.python_version(),
        'programs': provenance, 'flags': stress.FLAGS,
        'generator_sha256': bench.sha256(Path(stress.__file__)),
        'calibration_script_sha256': bench.sha256(Path(__file__)),
        'repeats': 7, 'multiplier': 2, 'resolution_seconds': 0.5,
        'baseline_record': 'benchmark-P1.json',
        'baseline_sha256': bench.sha256(ROOT/'docs/benchmark-P1.json'),
        'formal_input_validation': [], 'operation_counts': [],
        'cases': [], 'summary': {}}
    path = OUT/'validated.in'
    for original in confirmed['cases'] + pivot['cases'][:1]:
        case = dict(original)
        stress.generate(case, path)
        assert case['input_sha256'] == original['input_sha256'], case['id']
        validator = bench.validate_trail if case['slug']=='forest-ranger' else contracts.VALIDATORS[case['slug']]
        dims = validator(path)
        report['formal_input_validation'].append({
            'id': case['id'], 'slug': case['slug'], 'input_sha256': case['input_sha256'],
            'dimensions': dims, 'matches_measured_input': True})
        if case['shape']=='gains-pivot-guards':
            report['operation_counts'].append(count_gains(case, path, source, binary))
        print('Validated:', case['slug'], case['id'], flush=True)
    large = dict(pivot['cases'][-1])
    stress.generate(large, path)
    assert large['input_sha256'] == pivot['cases'][-1]['input_sha256']
    report['operation_counts'].append(count_gains(large, path, source, binary))
    for actual in report['operation_counts']:
        expected = next(c for c in recorded['calibration']['operation_counts'] if c['n']==actual['n'])
        assert actual == expected, actual['n']
    if args.verify_only:
        report['mode'] = 'Input and operation-count verification; no timed runs.'
        destination = OUT/'reproduction-check.json'
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        print('Verified input hashes, output hashes and operation counts:', destination, flush=True)
        return
    for slug in ['festival-plan', 'grinder']:
        problem = ROOT/'topics/trees'/slug
        plan = json.loads((problem/'tests/plan.json').read_text(encoding='utf-8'))
        bench.validate_groups(slug, plan)
        spec = next(c for c in plan['cases'] if c['id']=='maximum-relabelled-chain')
        module_spec = importlib.util.spec_from_file_location('formal_generator', problem/'tests/generate.py')
        generator = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(generator)
        data = generator.generate(spec, generator.Random(spec['seed']))
        formal_dir = ROOT/'build/data'/slug
        formal_dir.mkdir(parents=True, exist_ok=True)
        path = formal_dir/(spec['id']+'.in')
        path.write_text(data, encoding='ascii', newline='\n')
        dims = contracts.VALIDATORS[slug](path)
        contracts.validate_group(slug, spec, dims)
        case = dict(spec, slug=slug, shape=spec['kind'],
                    input_sha256=bench.sha256(path), input_bytes=path.stat().st_size,
                    dimensions=dims, generator_sha256=bench.sha256(problem/'tests/generate.py'),
                    plan_sha256=bench.sha256(problem/'tests/plan.json'))
        stress.measure(case, path, progs[slug], 7, True)
        for variant in progs[slug]:
            contracts.check_output(slug, OUT/(variant+'.out'), dims)
        # Make the standard output available with the formal input.
        path.with_suffix('.out').write_bytes((OUT/'std.out').read_bytes())
        report['cases'].append(case)
        rows = previous['problems'][slug]['cases'] + [
            c for c in confirmed['cases'] if c['slug']==slug] + [case]
        report['summary'][slug] = {}
        for variant in progs[slug]:
            med = max(c['variants'][variant]['median_seconds'] for c in rows)
            peak = max(c['variants'][variant]['peak_working_set_bytes'] for c in rows)
            report['summary'][slug][variant] = {
                'max_median_seconds': med, 'peak_working_set_bytes': peak,
                'indicative_limit_seconds': math.ceil(med*4)/2}
    (OUT/'calibration.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Report:', OUT/'calibration.json', flush=True)


if __name__=='__main__':
    main()
