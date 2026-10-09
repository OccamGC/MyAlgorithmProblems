"""Generate, independently audit and measure the three retained R20 packages."""
from pathlib import Path
import importlib.util
import json
import math
import platform
import statistics
import subprocess
import sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r20 import PROBLEMS,VARIANTS,ORACLES,validate as validate_text

def validate(slug,path,group=None):
    return validate_text(slug,path.read_text(encoding="ascii"),group)
ROOT=Path(__file__).resolve().parents[1]

def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    report=dict(date='2026-10-01',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-Wpedantic'],repeat=5,multiplier=2,resolution_seconds=0.5,timing_scope='Startup and I/O included; generation and validation excluded.',memory_scope='Separately measured peak working set includes runtime overhead.',problems={})
    selected=set(sys.argv[1:])
    if selected:
        assert selected<={slug for _,slug in PROBLEMS}
        report=json.loads((ROOT/'docs/benchmark-R20.json').read_text(encoding='utf-8'))
    audit_path=ROOT/'build/R20/audit.json'
    audit=json.loads(audit_path.read_text(encoding='utf-8')) if audit_path.exists() else {}
    for topic,slug in PROBLEMS:
        if selected and slug not in selected:
            continue
        directory=ROOT/'topics'/topic/slug;data=ROOT/'build/data'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(data)],check=True)
        spec=importlib.util.spec_from_file_location(slug,directory/'tests/generate.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((directory/'tests/plan.json').read_text(encoding='utf-8'))
        variants=VARIANTS[slug]
        programs=[ROOT/'build/bin'/f'{slug}-{v}.exe' for v in variants]
        outputs=[ROOT/'build/R20'/f'{slug}-{v}.out' for v in variants]
        item=dict(sources={v+'.cpp':sha256(directory/(v+'.cpp')) for v in variants},binaries={v:sha256(p) for v,p in zip(variants,programs)},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        for recipe in plan['cases']:
            path=data/(recipe['id']+'.in')
            dimensions=validate(slug,path,recipe['group'])
            assert module.generate(recipe).encode('ascii')==path.read_bytes()
            expected=ORACLES[slug](path.read_text(encoding='ascii')).encode('ascii')
            peaks=[run_with_peak_memory(p,path,o) for p,o in zip(programs,outputs)]
            for output in outputs:
                assert output.read_bytes().replace(b'\r\n',b'\n')==expected,(slug,recipe['id'],output)
            times=[[] for _ in variants]
            for repetition in range(5):
                order=list(range(len(variants)))
                if repetition%2:
                    order.reverse()
                for i in order:
                    times[i].append(run(programs[i],path,outputs[i]))
            item['cases'].append(dict(id=recipe['id'],dimensions=dimensions,input_sha256=sha256(path),output_sha256=sha256(outputs[0]),programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)}))
            print('Measured',slug,recipe['id'],flush=True)
        item['summary']={v:dict(slowest_median_seconds=max(c['programs'][v]['median_seconds'] for c in item['cases']),peak_working_set_bytes=max(c['programs'][v]['peak_working_set_bytes'] for c in item['cases'])) for v in variants}
        item['limit_seconds']=math.ceil(2*item['summary']['std']['slowest_median_seconds']/0.5)*0.5
        item['within_limit']={v:result['slowest_median_seconds']<=item['limit_seconds'] for v,result in item['summary'].items()}
        report['problems'][slug]=item
        (ROOT/'docs/benchmark-R20.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        samples=[]
        for path in sorted((directory/'tests/samples').glob('*.in')):
            validate(slug,path);expected=path.with_suffix('.out').read_bytes()
            assert expected==ORACLES[slug](path.read_text(encoding='ascii')).encode('ascii')
            for program in programs:
                assert subprocess.check_output([str(program)],input=path.read_bytes()).replace(b'\r\n',b'\n')==expected
            samples.append(path.stem)
        cli=ROOT/'build/R20/cli'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','02','--std',str(programs[0])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['02.in','02.out']
        assert sha256(cli/'02.in')==sha256(data/'02.in')
        assert (cli/'02.out').read_text(encoding='ascii')==ORACLES[slug]((cli/'02.in').read_text(encoding='ascii'))
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True)
        assert bad.returncode!=0 and b'unknown case' in bad.stderr
        audit[slug]=dict(validated_cases=10,reproduced_cases=10,independent_formal_oracle_checks=10,samples=samples,cli_checks=2)
        audit_path.write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
        print(slug,item['summary'],'limit',item['limit_seconds'],flush=True)

if __name__=='__main__':
    main()
