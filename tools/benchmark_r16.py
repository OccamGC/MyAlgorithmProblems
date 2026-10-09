"""Generate, independently audit and benchmark the four R16 packages."""
from pathlib import Path
import hashlib,importlib.util,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r16 import PROBLEMS,paper_oracle,hanoi_bfs
from validate_r16 import validate
ROOT=Path(__file__).resolve().parents[1]

def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    report=dict(date='2026-09-30',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-Wpedantic'],repeat=5,multiplier=2,resolution_seconds=0.5,timing_scope='Startup and I/O included; generation and validation excluded.',memory_scope='Separately measured peak working set includes runtime overhead.',problems={})
    selected=set(sys.argv[1:])
    if selected:
        report=json.loads((ROOT/'docs/benchmark-R16.json').read_text(encoding='utf-8'))
    audit=json.loads((ROOT/'build/R16-audit.json').read_text(encoding='utf-8')) if (ROOT/'build/R16-audit.json').exists() else {}
    for topic,slug in PROBLEMS:
        if selected and slug not in selected:continue
        directory=ROOT/'topics'/topic/slug
        data=ROOT/'build/data'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(data)],check=True)
        spec=importlib.util.spec_from_file_location(slug,directory/'tests/generate.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((directory/'tests/plan.json').read_text(encoding='utf-8'))
        variants=['std','alternative']
        programs=[ROOT/'build/bin'/f'{slug}-{v}.exe' for v in variants]
        outputs=[ROOT/'build'/f'R16-{slug}-{v}.out' for v in variants]
        item=dict(sources={v+'.cpp':sha256(directory/(v+'.cpp')) for v in variants},binaries={v:sha256(p) for v,p in zip(variants,programs)},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        for recipe in plan['cases']:
            path=data/(recipe['id']+'.in')
            dim=validate(slug,path)
            digest=hashlib.sha256()
            for line in module.generate(recipe):digest.update(line.encode('ascii'))
            assert digest.hexdigest()==sha256(path)
            peaks=[run_with_peak_memory(p,path,o) for p,o in zip(programs,outputs)]
            canonical=outputs[0].read_bytes().replace(b'\r\n',b'\n')
            assert outputs[1].read_bytes().replace(b'\r\n',b'\n')==canonical
            if slug=='paper-tiger-sequence':
                assert canonical.decode()==paper_oracle(dim['initial'],dim['positions'],dim['queries'])
            elif slug=='block-tower':
                n=dim['n'];names=dim['names'][:3];blocks=dim['names'][3:]
                expected=''.join(f'Move {blocks[n-1-d]} from {names[a]} to {names[b]}.\n' for d,a,b in hanoi_bfs(n))
                assert canonical.decode()==expected
            elif slug=='circuit-board-test':
                expected=''.join('T\n' if x>0 and x**3<3000 and x*x>=10 and (x*x>2000 or x*x<700) else 'F\n' for x in dim['values'])
                assert canonical.decode()==expected
            else:
                value=canonical.decode().strip(); mode=recipe['mode']
                if mode=='disconnected' or dim['m']==0 and dim['n']>1: assert value=='bad idea'
                else:
                    number=int(value);assert abs(number)<=2*10**15
                    if mode in ['zero','all-negative','negative-loops']:assert number==dim['negative_sum']
                    if mode=='parallel':
                        with path.open() as stream:
                            next(stream);assert number==min(int(line.split()[2]) for line in stream)
            times=[[],[]]
            for repetition in range(5):
                for i in ([0,1] if repetition%2==0 else [1,0]):times[i].append(run(programs[i],path,outputs[i]))
            item['cases'].append(dict(id=recipe['id'],input_sha256=sha256(path),output_sha256=sha256(outputs[0]),programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)}))
            print('Measured',slug,recipe['id'],flush=True)
        item['summary']={v:dict(slowest_median_seconds=max(c['programs'][v]['median_seconds'] for c in item['cases']),peak_working_set_bytes=max(c['programs'][v]['peak_working_set_bytes'] for c in item['cases'])) for v in variants}
        item['limit_seconds']=math.ceil(2*item['summary']['std']['slowest_median_seconds']/0.5)*0.5
        item['within_limit']={v:result['slowest_median_seconds']<=item['limit_seconds'] for v,result in item['summary'].items()}
        report['problems'][slug]=item
        (ROOT/'docs/benchmark-R16.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        samples=[]
        for path in sorted((directory/'tests/samples').glob('*.in')):
            validate(slug,path);expected=path.with_suffix('.out').read_bytes()
            for p in programs:
                actual=subprocess.check_output([str(p)],input=path.read_bytes()).replace(b'\r\n',b'\n')
                assert actual==expected
            samples.append(path.stem)
        cli=ROOT/'build/cli-r16'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','02','--std',str(programs[0])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['02.in','02.out']
        assert sha256(cli/'02.in')==sha256(data/'02.in')
        actual=subprocess.check_output([str(programs[0])],input=(cli/'02.in').read_bytes()).replace(b'\r\n',b'\n')
        assert (cli/'02.out').read_bytes()==actual
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True)
        assert bad.returncode!=0 and b'unknown case' in bad.stderr
        audit[slug]=dict(validated_cases=10,reproduced_cases=10,samples=samples,cli_checks=2)
        (ROOT/'build/R16-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
        print(slug,item['summary'],'limit',item['limit_seconds'],flush=True)

if __name__=='__main__':main()
