"""Validate, cross-check, and measure the R32 reference implementations."""
from pathlib import Path
import argparse,hashlib,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r32 import PROBLEMS,MEMORY_MB,load_generator,validate,tree_oracle,calculator_oracle,refuel_oracle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R32'

def tree_expected(case,text):
    N,edges,queries=validate('giant-christmas-tree',text)
    if N<=30:return '\n'.join(tree_oracle(N,edges,queries))
    if case['state']=='off':return '\n'.join(['0']*len(queries))
    if case['shape']=='chain' and case['mode']=='late-cut':return '\n'.join([str(N-1)]*(len(queries)-1)+['0'])
    if case['shape']=='star':
        active={v for u,v,s in edges if s};answers=[]
        for u,v in queries:
            if u!=v:active.discard(u);active.discard(v)
            answers.append(str(min(2,len(active))))
        return '\n'.join(answers)
    if case['mode']=='points':
        graph=[[] for _ in range(N)]
        for u,v,s in edges:
            if s:graph[u].append(v);graph[v].append(u)
        def far(start):
            queue=[(start,-1,0)]
            for u,p,d in queue:
                for v in graph[u]:
                    if v!=p:queue.append((v,u,d+1))
            return max(queue,key=lambda t:t[2])
        diameter=far(far(0)[0])[2]
        return '\n'.join([str(diameter)]*len(queries))
    if case['shape']=='chain':
        state=[s for u,v,s in edges];answers=[]
        for u,v in queries:
            a,b=sorted([u,v]);state[a:b]=[0]*(b-a);best=run=0
            for s in state:run=run+1 if s else 0;best=max(best,run)
            answers.append(str(best))
        return '\n'.join(answers)
    return None


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -DNDEBUG -Wall -Wextra -Wpedantic','problems':{}}
    audit={}
    if args.only:
        result=json.loads((ROOT/'docs/benchmark-R32.json').read_text('utf-8'))
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
            if slug=='apostle-luke-password' and case['group']<3:
                n,g,k,b=map(int,text.split());total=0;answers=[]
                for j in range(g,g+n):
                    p=k*j+b;total+=p==1 or p>=2 and all(p%d for d in range(2,math.isqrt(p)+1));answers.append(str(total))
                expected='\n'.join(answers)
            if slug=='giant-christmas-tree':expected=tree_expected(case,text)
            if slug=='old-y-segment-tree':expected=gen.make_case(case)[1]
            if slug=='short-circuit-calculator':
                if 'expression' in case:expected=' '.join(calculator_oracle(text))
                elif case['mode']=='deep' or case['mode']=='middle':expected='7'
                elif case['mode']=='unary':expected=str(-8 if (len(text.strip())-1)%2 else 7)
                elif case['mode']=='conditional':expected=str(0 if text.count('?')%2 else 1)
                elif case['mode']=='spaces':expected='30'
                else:expected='0'
            if slug=='limited-refueling':
                L,R,stations=validate(slug,text)
                if L<=200:expected=' '.join(refuel_oracle(text))
                elif case['mode']=='unit':expected=f'{sum(c for x,c,r in stations)} {L}'
                elif case['mode']=='descending':expected=f'{sum(c for x,c,r in stations)} 1'
                elif case['mode']=='ascending':expected=f'{min(stations)[1]*L} 1'
                elif case['mode']=='free':expected='0 1'
            outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes()
                assert peak<=MEMORY_MB[slug]*2**20,(slug,v,peak)
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
        entry['multiplier']=max(2,math.ceil(2*entry['summary']['alternative']['slowest_median_seconds']/entry['summary']['std']['slowest_median_seconds'])) if slug in ['giant-christmas-tree','limited-refueling'] else 2
        entry['limit_seconds']=math.ceil(entry['summary']['std']['slowest_median_seconds']*entry['multiplier']*2)/2
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
        (ROOT/'docs/benchmark-R32.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8')
        print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
