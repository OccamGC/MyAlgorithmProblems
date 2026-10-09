"""Compare R15 reference and alternative programs on every planned input."""
from pathlib import Path
import json
import math
import platform
import statistics
import subprocess
import time
from benchmark_reference import run, run_with_peak_memory, sha256
from check_r15 import PROBLEMS

ROOT=Path(__file__).resolve().parents[1]

def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    report=dict(date='2026-09-30',timezone='Asia/Shanghai',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-Wpedantic'],repeat=5,multiplier=2,resolution_seconds=0.5,problems={})
    for topic,slug in PROBLEMS:
        directory=ROOT/'topics'/topic/slug
        source_alt=next(directory.glob('alternative-*.cpp'))
        programs=[ROOT/'build/bin'/f'{slug}.exe',ROOT/'build/bin'/f'{slug}-alternative.exe']
        output_paths=[ROOT/'build'/f'R15-{slug}-std.out',ROOT/'build'/f'R15-{slug}-alt.out']
        item=dict(sources={p.name:sha256(p) for p in [directory/'std.cpp',source_alt]},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        plan=json.loads((directory/'tests/plan.json').read_text(encoding='utf-8'))
        for spec in plan['cases']:
            path=ROOT/'build/data'/slug/(spec['id']+'.in')
            peak=[run_with_peak_memory(program,path,output) for program,output in zip(programs,output_paths)]
            assert output_paths[0].read_bytes()==output_paths[1].read_bytes(),(slug,spec['id'])
            times=[[],[]]
            for round_index in range(5):
                for index in ([0,1] if round_index%2==0 else [1,0]):
                    times[index].append(run(programs[index],path,output_paths[index]))
            row=dict(id=spec['id'],input_sha256=sha256(path),output_sha256=sha256(output_paths[0]),programs={})
            for index,name in enumerate(['std','alternative']):
                row['programs'][name]=dict(seconds=times[index],median_seconds=statistics.median(times[index]),peak_working_set_bytes=peak[index])
            item['cases'].append(row)
        item['summary']={name:dict(slowest_median_seconds=max(row['programs'][name]['median_seconds'] for row in item['cases']),peak_working_set_bytes=max(row['programs'][name]['peak_working_set_bytes'] for row in item['cases'])) for name in ['std','alternative']}
        item['limit_seconds']=math.ceil(2*item['summary']['std']['slowest_median_seconds']/0.5)*0.5
        item['alternative_within_limit']=item['summary']['alternative']['slowest_median_seconds']<=item['limit_seconds']
        report['problems'][slug]=item
        (ROOT/'docs/benchmark-R15.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(slug,json.dumps(item['summary']), 'limit',item['limit_seconds'],flush=True)

if __name__=='__main__':
    main()
