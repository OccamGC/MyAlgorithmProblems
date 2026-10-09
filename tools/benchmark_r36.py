"""Generate, validate and measure R36 with five timings and separate peak memory."""
from pathlib import Path
import argparse,gc,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r36 import PROBLEMS,module,queue_oracle,direct_box,direct_monotone,falling,P
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R36'
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -Wall -Wextra','problems':{}};audit={}
    if args.only and (ROOT/'docs/benchmark-R36.json').exists():result=json.loads((ROOT/'docs/benchmark-R36.json').read_text());audit=json.loads((OUT/'formal-audit.json').read_text())
    for topic,slug in PROBLEMS:
        if args.only and args.only!=slug:continue
        d=ROOT/'topics'/topic/slug;gen=module(d/'tests/generate.py');plan=json.loads((d/'tests/plan.json').read_text());variants=[p.stem for p in d.glob('*.cpp')];programs={v:OUT/f'{slug}-{v}.exe' for v in variants};dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{str(p.relative_to(d)):sha256(p) for p in d.rglob('*') if p.suffix in ['.cpp','.hpp']},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(d/'tests/generate.py'),'plan_sha256':sha256(d/'tests/plan.json'),'cases':[]}
        assert sum(c['score_percent'] for c in plan['cases'])==100
        for case in plan['cases']:
            print(slug,case['id'],'generating',flush=True);text=gen.generate(case);assert text==gen.generate(case);gen.validate(text);expected=None;method='independent small enumeration, verified formula and factorial checkpoints'
            if slug=='bounded-conveyor':expected=queue_oracle(text);method='Python deque'
            elif slug=='white-cell-board':method='independent inclusion-exclusion calculation; exhaustive boards through n=4'
            elif slug in ['box-gcd-prefix-sum','monotone-gcd-sum']:
                n,m=map(int,text.split())
                if m==1:expected=[str((n*(n+1)*(n+2)//6 if slug=='box-gcd-prefix-sum' else n*(n+1)//2)%P)];method='closed m=1 identity'
                elif n<=2000001:expected=[str((direct_box if slug=='box-gcd-prefix-sum' else direct_monotone)(n,m))];method='direct phi sieve and ungrouped divisor sum'
                else:
                    expected=subprocess.check_output([str(OUT/f'{slug}-cutoff-medium.exe')],input=text.encode()).decode().split();method='separate B=1000000 build; small literal models verify the shared identities'
            else:
                value=falling(*map(int,text.split()))
                if value is not None:expected=[str(value)];method='direct product or Wilson complement'
            gc.collect();inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n');item={'id':case['id'],'input_sha256':sha256(inp),'programs':{},'verification_method':method};outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes().replace(b'\r\n',b'\n');assert peak<=(8 if slug in ['bounded-conveyor','white-cell-board'] else 128)*2**20,(slug,peak)
                if expected is not None:assert outputs[v].decode().split()==expected,(slug,case['id'],v)
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            assert all(x==outputs['std'] for x in outputs.values()),(slug,case['id'])
            for repeat in range(5):
                for v in variants if repeat%2==0 else variants[::-1]:
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes().replace(b'\r\n',b'\n')==outputs[v];item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=sha256(inp.with_suffix('.out'));entry['cases'].append(item);print(slug,case['id'],'passed',flush=True)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants};entry['limit_seconds']=max(.5,math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2)
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        samples=0
        for inp in sorted((d/'tests/samples').glob('*.in')):
            gen.validate(inp.read_text());expected=inp.with_suffix('.out').read_bytes()
            for p in programs.values():assert subprocess.check_output([str(p)],input=inp.read_bytes()).split()==expected.split()
            samples+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True);ids=[c['id'] for c in plan['cases'][:2]]
        command=[sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--std',str(programs['std'])]
        for cid in ids:command+=['--case',cid]
        subprocess.run(command,check=True)
        for cid in ids:
            for suffix in ['.in','.out']:assert (cli/(cid+suffix)).read_bytes()==(dest/(cid+suffix)).read_bytes()
        assert subprocess.run([sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True).returncode!=0
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':len(plan['cases']),'samples':samples,'all_variants_valid':True,'determinism_and_cli':True}
        (ROOT/'docs/benchmark-R36.json').write_text(json.dumps(result,indent=2)+'\n','utf-8',newline='\n');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8',newline='\n');print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
