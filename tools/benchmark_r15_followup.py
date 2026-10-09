"""Five-round comparison of each implementation on all follow-up inputs."""
from pathlib import Path
import json
import math
import platform
import statistics
import subprocess
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r15_followup import PROBLEMS
from validate_r15_followup import validate,check_output,MOD

ROOT=Path(__file__).resolve().parents[1]

def main():
    cxx=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    report=dict(date='2026-09-30',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(cxx),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-Wpedantic'],repeat=5,multiplier=2,resolution_seconds=0.5,timing_scope='Startup, input and output included; generation and validation excluded.',memory_scope='Peak working set includes runtime overhead.',problems={})
    expectations={}
    for topic,slug,alts in PROBLEMS:
        directory=ROOT/'topics'/topic/slug
        variants=['std',*['alternative-'+a for a in alts]]
        programs=[ROOT/'build/bin'/f'{slug}-{v}.exe' for v in variants]
        outputs=[ROOT/'build'/f'{slug}-{v}.out' for v in variants]
        item=dict(sources={v+'.cpp':sha256(directory/(v+'.cpp')) for v in variants},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        plan=json.loads((directory/'tests/plan.json').read_text(encoding='utf-8'))
        for spec in plan['cases']:
            path=ROOT/'build/data'/slug/(spec['id']+'.in')
            dim=validate(slug,path)
            peaks=[run_with_peak_memory(p,path,o) for p,o in zip(programs,outputs)]
            canonical=outputs[0].read_bytes()
            for output in outputs:
                assert output.read_bytes()==canonical
            values=check_output(slug,canonical,dim)
            if slug=='shuffle-expectation':expectations[spec['id']]=values
            if slug=='shuffle-distribution':
                assert sha256(path)==sha256(ROOT/'build/data/shuffle-expectation'/(spec['id']+'.in'))
                assert [sum((j+1)*v for j,v in enumerate(row))%MOD for row in values]==expectations[spec['id']]
            if slug=='power-call-count':
                mode,total=spec['mode'],spec['total']
                expected={'empty':[],'single-zero':[0],'zero':[0],'ones':[2*total-1],'power':[total],'leading-zero':[1],'alternating':[total+(total+1)//2-1]}.get(mode)
                if mode=='many':expected=[i%2 for i in range(total)]
                if expected is not None:assert values==expected,(mode,values[:5])
                if mode=='random':
                    original=subprocess.check_output([str(ROOT/'build/bin/power-call-count-original.exe')],input=path.read_bytes())
                    assert original==canonical
            times=[[] for _ in variants]
            for repeat in range(5):
                order=range(len(variants)) if repeat%2==0 else reversed(range(len(variants)))
                for i in order:times[i].append(run(programs[i],path,outputs[i]))
            item['cases'].append(dict(id=spec['id'],input_sha256=sha256(path),output_sha256=sha256(outputs[0]),programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)}))
        item['summary']={v:dict(slowest_median_seconds=max(c['programs'][v]['median_seconds'] for c in item['cases']),peak_working_set_bytes=max(c['programs'][v]['peak_working_set_bytes'] for c in item['cases'])) for v in variants}
        item['limit_seconds']=math.ceil(2*item['summary']['std']['slowest_median_seconds']/0.5)*0.5
        item['within_limit']={v:result['slowest_median_seconds']<=item['limit_seconds'] for v,result in item['summary'].items()}
        report['problems'][slug]=item
        (ROOT/'docs/benchmark-R15-followup.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(slug,json.dumps(item['summary']),flush=True)

if __name__=='__main__':
    main()
