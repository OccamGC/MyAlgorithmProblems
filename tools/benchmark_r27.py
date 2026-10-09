"""Reproduce, validate and measure all five R27 packages, resuming completed cases."""
from pathlib import Path
import importlib.util,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r27 import PROBLEMS,VARIANTS,ORACLES,check_output,validate
ROOT=Path(__file__).resolve().parents[1]

def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    report_path=ROOT/'docs/benchmark-R27.json'
    report=json.loads(report_path.read_text('utf-8')) if report_path.exists() else dict(date='2026-10-01',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-DNDEBUG','-Wall','-Wextra','-Wpedantic'],repeat=5,multiplier=2,resolution_seconds=0.5,timing_scope='Startup and I/O included; generation and validation excluded.',memory_scope='Separately measured peak working set includes runtime overhead.',problems={})
    audit_path=ROOT/'build/R27/audit.json';audit=json.loads(audit_path.read_text('utf-8')) if audit_path.exists() else {}
    for topic,slug in PROBLEMS:
        if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
        directory=ROOT/'topics'/topic/slug;data=ROOT/'build/data'/slug;data.mkdir(parents=True,exist_ok=True)
        spec=importlib.util.spec_from_file_location(slug,directory/'tests/generate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((directory/'tests/plan.json').read_text('utf-8'));variants=VARIANTS[slug]
        programs=[ROOT/'build/bin'/f'{slug}-{v}.exe' for v in variants];outputs=[ROOT/'build/R27'/f'{slug}-{v}.out' for v in variants]
        item=dict(sources={v+'.cpp':sha256(directory/(v+'.cpp')) for v in variants},binaries={v:sha256(p) for v,p in zip(variants,programs)},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        prior=report['problems'].get(slug,{})
        if all(prior.get(k)==item[k] for k in ['sources','binaries','generator_sha256','plan_sha256']):item['cases']=prior['cases']
        report['problems'][slug]=item
        for recipe in plan['cases']:
            path=data/(recipe['id']+'.in')
            done=next((c for c in item['cases'] if c['id']==recipe['id']),None)
            if done and path.exists() and path.with_suffix('.out').exists() and sha256(path)==done['input_sha256'] and sha256(path.with_suffix('.out'))==done['output_sha256']:
                print('Already audited',slug,recipe['id'],flush=True);continue
            text=module.generate(recipe);path.write_text(text,encoding='ascii',newline='\n');dimensions=validate(slug,text,recipe['group']);del text
            assert module.generate(recipe).encode('ascii')==path.read_bytes()
            peaks=[run_with_peak_memory(p,path,o) for p,o in zip(programs,outputs)]
            for output in outputs[1:]:assert output.read_bytes()==outputs[0].read_bytes(),(slug,recipe['id'])
            expected=ROOT/'build/R27/independent.out'
            verifier={'digit-merge-extremes':'digits','queue-with-stacks':'queue','exact-search-tree':'bst','rotating-bytes':'byte'}.get(slug)
            if verifier:
                with path.open('rb') as inp,expected.open('wb') as out:subprocess.run([str(ROOT/'build/R27'/f'verify-{verifier}.exe')],stdin=inp,stdout=out,check=True)
                assert outputs[0].read_bytes()==expected.read_bytes(),(slug,recipe['id'],'independent verifier')
            scope={
                'digit-merge-extremes':'All positions enumerated with first/last feasible partner queries and exact piecewise digit-string comparisons; independent of greedy branch selection.',
                'queue-with-stacks':'Explicit stack contents and actual transfers establish the reported cost is attainable; small time-aware Dijkstra and the exchange proof establish optimality.',
                'exact-search-tree':'Direct BST search with explicit child links and successor deletion, without an ordered index; every printed traversal compared including empty lines.',
                'lexicographic-heap-labels':'Component-interval algorithm versus independent static persistent ancestor-set sorting. Small cases additionally enumerate every valid topological order.',
                'rotating-bytes':'Dijkstra distances, forward lexicographic frontier filtering, and matching-string reachability with greedy reverse-ID reconstruction; all three objectives.'
            }[slug]
            if recipe['id'] in ['01','02']:
                text=path.read_text('ascii');check_output(slug,text,outputs[0].read_text('ascii'))
            times=[[] for _ in variants]
            for repetition in range(5):
                order=list(range(len(variants)))
                if repetition%2:order.reverse()
                for i in order:times[i].append(run(programs[i],path,outputs[i]))
            path.with_suffix('.out').write_bytes(outputs[0].read_bytes())
            record=dict(id=recipe['id'],verification_scope=scope,dimensions=dimensions,input_sha256=sha256(path),output_sha256=sha256(outputs[0]),programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)})
            item['cases']=[c for c in item['cases'] if c['id']!=recipe['id']]+[record]
            report_path.write_text(json.dumps(report,indent=2)+'\n','utf-8');print('Measured',slug,recipe['id'],{v:round(statistics.median(times[i]),4) for i,v in enumerate(variants)},flush=True)
        item['summary']={v:dict(slowest_median_seconds=max(c['programs'][v]['median_seconds'] for c in item['cases']),peak_working_set_bytes=max(c['programs'][v]['peak_working_set_bytes'] for c in item['cases'])) for v in variants}
        slowest=max(s['slowest_median_seconds'] for s in item['summary'].values());standard=item['summary']['std']['slowest_median_seconds']
        multiplier=2
        while math.ceil(multiplier*standard/0.5)*0.5<2*slowest:multiplier+=1
        item['multiplier']=multiplier;item['multiplier_reason']='Default multiplier.' if multiplier==2 else 'The static ancestor-set sorting alternative needs at least twofold measured headroom on the full original range.'
        item['limit_seconds']=math.ceil(multiplier*standard/0.5)*0.5;item['within_limit']={v:r['slowest_median_seconds']<=item['limit_seconds'] for v,r in item['summary'].items()}
        report_path.write_text(json.dumps(report,indent=2)+'\n','utf-8')
        samples=[]
        for path in sorted((directory/'tests/samples').glob('*.in')):
            text=path.read_text('ascii');validate(slug,text);expected=path.with_suffix('.out').read_text('ascii');check_output(slug,text,expected)
            for program in programs:check_output(slug,text,subprocess.check_output([str(program)],input=text.encode()).decode(),expected)
            samples.append(path.stem)
        cli=ROOT/'build/R27/cli'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--plan',str(directory/'tests/plan.json'),'--out-dir',str(cli),'--case','02','--std',str(programs[0])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['02.in','02.out'];assert sha256(cli/'02.in')==sha256(data/'02.in');assert sha256(cli/'02.out')==sha256(data/'02.out')
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True);assert bad.returncode!=0 and b'unknown case' in bad.stderr
        audit[slug]=dict(validated_cases=10,reproduced_cases=10,full_output_verifier_checks=10,verification_scope=[c['verification_scope'] for c in item['cases']],samples=samples,cli_checks=3)
        audit_path.write_text(json.dumps(audit,indent=2)+'\n','utf-8');print(slug,item['summary'],'multiplier',multiplier,'limit',item['limit_seconds'],flush=True)
if __name__=='__main__':main()
