"""Count selected operations in P1 algorithms without editing delivered C++.

Requires the existing formal inputs in build/data. Instrumented sources, binaries,
and output go to build/priority-work. Counts describe executed work, not CPU time.
Example: python tools/profile_priority_work.py --cxx <g++ path>
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['Components', 'ComponentVertices', 'SmallComponents', 'SmallVertices',
          'Queries', 'QueryLoops', 'QueryFragments', 'EmptyQueries', 'MaxDepth',
          'TreeSlots', 'VisitBytes', 'GainCount', 'GainSum', 'GainOnes', 'GainDistinct',
          'MaxGain', 'SortComparisons']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def instrument(text, slug, variant):
    declaration = '#include <iostream>\n#include <algorithm>\n'
    declaration += ''.join('long long P1' + key + ' = 0;\n' for key in FIELDS)
    declaration += 'struct FP1Report { ~FP1Report() { std::cerr << "{";\n'
    for index, key in enumerate(FIELDS):
        prefix = ',' if index else ''
        declaration += f'std::cerr << "{prefix}\\\"{key}\\\":" << P1{key};\n'
    declaration += 'std::cerr << "}\\n"; } } P1Report;\n'
    text = declaration + text

    def replace(old, new, count=1):
        nonlocal text
        assert text.count(old) == count, (slug, variant, old, text.count(old))
        text = text.replace(old, new)

    if slug == 'forest-ranger':
        replace('std::sort(Gains.begin(), Gains.end(), std::greater<int>());',
                'std::sort(Gains.begin(), Gains.end(), [](int a, int b) { ++P1SortComparisons; return a > b; });\n'
                '\tP1GainCount = Gains.size();\n'
                '\tfor (std::size_t i = 0; i < Gains.size(); ++i) {\n'
                '\t\tP1GainSum += Gains[i]; P1GainOnes += Gains[i] == 1;\n'
                '\t\tP1GainDistinct += i == 0 || Gains[i] != Gains[i-1];\n'
                '\t\tP1MaxGain = std::max(P1MaxGain, static_cast<long long>(Gains[i]));\n\t}')
    else:
        needle = 'int Total = static_cast<int>(Order.size());'
        replace(needle, needle + '\n\t\t++P1Components; P1ComponentVertices += Total; P1VisitBytes = sizeof(FVisit);')
        if variant == 'std':
            indent = '\t\t\t' if slug == 'grinder' else '\t\t'
            replace('if (Total <= 8)\n' + indent + '{',
                    'if (Total <= 8)\n' + indent + '{\n' + indent + '\t++P1SmallComponents; P1SmallVertices += Total;')
        else:
            replace('std::vector<FBestTwo> Tree(2 * Base);',
                    'P1Queries += Visits.size(); P1MaxDepth = std::max(P1MaxDepth, static_cast<long long>(MaxDepth));\n'
                    '\t\tP1TreeSlots += 2 * Base;\n\t\tstd::vector<FBestTwo> Tree(2 * Base);')
            replace('while (Left < Right)\n\t\t\t{',
                    'P1EmptyQueries += Left >= Right;\n\t\t\twhile (Left < Right)\n\t\t\t{\n\t\t\t\t++P1QueryLoops;')
            for expr in ['Tree[Left++]', 'Tree[--Right]']:
                replace(f'Best.Merge({expr});', f'++P1QueryFragments; Best.Merge({expr});')
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cxx', required=True, type=Path)
    args = parser.parse_args()
    folder = ROOT / 'build/priority-work'
    folder.mkdir(parents=True, exist_ok=True)
    bench = json.loads((ROOT / 'docs/benchmark-P1.json').read_text(encoding='utf-8'))
    report = {'purpose': 'Executed operation counts; instrumented timings are not used.',
              'compiler': subprocess.check_output([str(args.cxx), '--version']).decode().splitlines()[0],
              'flags': ['-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Wpedantic'],
              'instrumentation_sha256': sha(Path(__file__)), 'problems': {}}
    for slug in ['forest-ranger', 'festival-plan', 'grinder']:
        problem = next((ROOT / 'topics').glob('*/' + slug))
        variants = ['alternative'] if slug == 'forest-ranger' else ['std', 'alternative']
        result = {'sources_sha256': {}, 'cases': []}
        binaries = {}
        for variant in variants:
            source = problem / (variant + '.cpp')
            result['sources_sha256'][variant] = sha(source)
            target = folder / (slug + '-' + variant)
            copy = target.with_suffix('.cpp')
            binary = target.with_suffix('.exe')
            copy.write_text(instrument(source.read_text(encoding='utf-8'), slug, variant), encoding='utf-8', newline='\n')
            compiled = subprocess.run([str(args.cxx), *report['flags'], str(copy), '-o', str(binary)], capture_output=True, check=True)
            assert not compiled.stderr, compiled.stderr.decode(errors='replace')
            binaries[variant] = binary
        for case in bench['problems'][slug]['cases']:
            if case['dimensions'].get('n', 0) < 100000:
                continue
            path = ROOT / 'build/data' / slug / (case['id'] + '.in')
            assert sha(path) == case['input_sha256']
            row = {'id': case['id'], 'n': case['dimensions']['n'], 'input_sha256': sha(path), 'variants': {}}
            for variant, binary in binaries.items():
                output = folder / (slug + '-' + variant + '.out')
                with path.open('rb') as src, output.open('wb') as dst:
                    run = subprocess.run([str(binary)], stdin=src, stdout=dst, stderr=subprocess.PIPE, check=True, timeout=120)
                assert sha(output) == case['variants'][variant]['output_sha256'], (slug, case['id'], variant)
                row['variants'][variant] = json.loads(run.stderr)
            result['cases'].append(row)
            print(slug, row['id'], row['variants'], flush=True)
        report['problems'][slug] = result
        (folder / 'counts.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
