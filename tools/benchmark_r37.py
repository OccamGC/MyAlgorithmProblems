"""Reproduce R37 recipes and expected answers; five timings plus peak memory."""
from pathlib import Path
import argparse,gc,importlib.util,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r37 import PROBLEMS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R37'
def module(path):
    s=importlib.util.spec_from_file_location('recipe_r37',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args();result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -Wall -Wextra','problems':{}};audit={}
    if args.only and (ROOT/'docs/benchmark-R37.json').exists():result=json.loads((ROOT/'docs/benchmark-R37.json').read_text());audit=json.loads((OUT/'formal-audit.json').read_text())
    methods=['known depths or no obstacle; literal color refinement for random graphs','small Bellman-Ford or explicit reset patterns; separate Python bounded-distance validator','closed chain formulas, with one changing jump in group 1','literal small packings or proved forest shapes','Python list for small sequences; independent heaps or uniform-weight identities at scale']
    for index,(topic,slug) in enumerate(PROBLEMS):
        if args.only and args.only!=slug:continue
        d=ROOT/'topics'/topic/slug;gen=module(d/'tests/generate.py');plan=json.loads((d/'tests/plan.json').read_text());variants=[p.stem for p in d.glob('*.cpp')];programs={v:OUT/f'{slug}-{v}.exe' for v in variants};dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        assert sum(c['score_percent'] for c in plan['cases'])==100
        entry={'sources':{str(p.relative_to(d)):sha256(p) for p in d.rglob('*') if p.suffix in ['.cpp','.hpp']},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(d/'tests/generate.py'),'plan_sha256':sha256(d/'tests/plan.json'),'cases':[]}
        for c in plan['cases']:
            print(slug,c['id'],'generating',flush=True);text,expected=gen.make_case(c);assert (text,expected)==gen.make_case(c);validation=gen.validate(text,c['group'])
            if slug=='encrypted-reset-network':assert validation==expected.split()
            inp=dest/(c['id']+'.in');inp.write_text(text,'utf-8',newline='\n');item={'id':c['id'],'input_sha256':sha256(inp),'verification_method':methods[index],'programs':{}};outputs={};gc.collect()
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes().replace(b'\r\n',b'\n');assert outputs[v].split()==expected.encode().split(),(slug,c['id'],v)
                assert peak<=[128,512,128,2048,256][index]*2**20,(slug,c['id'],v,peak)
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            for repeat in range(5):
                for v in variants if repeat%2==0 else variants[::-1]:
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes().replace(b'\r\n',b'\n')==outputs[v];item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=sha256(inp.with_suffix('.out'));entry['cases'].append(item);print(slug,c['id'],'passed',flush=True)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants};entry['limit_seconds']=max(.5,math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2)
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        samples=0
        for inp in sorted((d/'tests/samples').glob('*.in')):
            gen.validate(inp.read_text());expected=inp.with_suffix('.out').read_bytes()
            for p in programs.values():assert subprocess.check_output([str(p)],input=inp.read_bytes()).split()==expected.split()
            samples+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True);ids=[c['id'] for c in plan['cases'][:2]];command=[sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--std',str(programs['std'])]
        for cid in ids:command+=['--case',cid]
        subprocess.run(command,check=True)
        for cid in ids:
            for suffix in ['.in','.out']:assert (cli/(cid+suffix)).read_bytes()==(dest/(cid+suffix)).read_bytes()
        assert subprocess.run([sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True).returncode!=0
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':len(plan['cases']),'samples':samples,'all_program_outputs_valid':True,'determinism_and_cli':True}
        (ROOT/'docs/benchmark-R37.json').write_text(json.dumps(result,indent=2)+'\n','utf-8',newline='\n');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8',newline='\n');print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
