"""Validate, cross-check, and measure the R31 reference implementations."""
from pathlib import Path
import argparse,hashlib,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r31 import PROBLEMS,load_generator,validate,memory_oracle,calculator_oracle,median_oracle,dna_formula,budget_oracle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R31'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -DNDEBUG -Wall -Wextra -Wpedantic','problems':{}}
    audit={}
    if args.only:
        result=json.loads((ROOT/'docs/benchmark-R31.json').read_text('utf-8'))
        audit=json.loads((OUT/'formal-audit.json').read_text('utf-8'))
    for topic,slug in PROBLEMS:
        if args.only and args.only!=slug:continue
        directory=ROOT/'topics'/topic/slug;gen=load_generator(topic,slug);plan=json.loads((directory/'tests/plan.json').read_text('utf-8'))
        variants=[p.stem for p in sorted(directory.glob('*.cpp'))];programs={v:OUT/f'{slug}-{v}.exe' for v in variants}
        dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{p.name:sha256(p) for p in sorted(directory.glob('*.cpp'))},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(directory/'tests/generate.py'),'plan_sha256':sha256(directory/'tests/plan.json'),'cases':[]}
        for case in plan['cases']:
            text=gen.generate(case);validate(slug,text,case['group']);assert text==gen.generate(case)
            inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n')
            item={'id':case['id'],'input_sha256':sha256(inp),'programs':{}};expected=None
            if slug=='memory-functions':expected=memory_oracle(text)
            if slug=='nearest-median':expected=median_oracle(text)
            if slug=='strand-length-range':expected=dna_formula(text)
            if slug=='small-integer-calculator':
                if 'expression' in case:expected=calculator_oracle(text)
                elif case['mode']=='deep':expected='6'
                elif case['mode']=='unary':expected=str(7+(len(text.strip())-1)//2)
                elif case['mode']=='sum':expected=str(9*((len(text.strip())+1)//2))
                elif case['mode']=='nested':expected=str((len(text.strip())-1)//4+2)
                else:expected='Runtime Error'
            if slug=='generated-budget-selection':
                n,A,B,C,D,L=case['values']
                if n<=100000:expected=budget_oracle(text)
                elif B==0:expected=str(n if C<=0 and n*C<=L else min(n,L//C) if C>0 and L>=0 else 0)
                elif [A,B,C,D]==[0,1,1,10**9]:expected=str((math.isqrt(1+8*L)-1)//2)
            outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes()
                assert peak<=128*2**20,(slug,v,peak)
                if expected is not None:assert outputs[v].split()==expected.encode().split(),(slug,case['id'],v,'independent output')
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            assert all(output==outputs['std'] for output in outputs.values()),(slug,case['id'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=hashlib.sha256(outputs['std']).hexdigest()
            for repeat in range(5):
                for v in (variants if repeat%2==0 else variants[::-1]):
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes()==outputs[v]
                    item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            item['independent_expected_output']=expected is not None;entry['cases'].append(item)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants}
        entry['limit_seconds']=math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        sample_count=0
        for inp in sorted((directory/'tests/samples').glob('*.in')):
            validate(slug,inp.read_text('utf-8'));expected=inp.with_suffix('.out').read_bytes()
            for v,p in programs.items():
                got=subprocess.run([str(p)],input=inp.read_bytes(),capture_output=True,check=True).stdout
                assert got.split()==expected.split(),(slug,inp.name,v)
            sample_count+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True)
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--plan',str(directory/'tests/plan.json'),'--out-dir',str(cli),'--case','01','--case','02','--std',str(programs['std'])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['01.in','01.out','02.in','02.out']
        for name in ['01.in','01.out','02.in','02.out']:assert (cli/name).read_bytes()==(dest/name).read_bytes()
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','unknown'],capture_output=True);assert bad.returncode!=0 and b'unknown case' in bad.stderr
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':10,'reproduced_inputs':10,'samples':sample_count,'generator_cli_checks':4,'all_variants_equal':True,'independent_full_outputs':sum(c['independent_expected_output'] for c in entry['cases'])}
        (ROOT/'docs/benchmark-R31.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8')
        print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
