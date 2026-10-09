"""Reproduce and validate R34 data, then measure five runs per formal input."""
from pathlib import Path
import argparse,collections,hashlib,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r34 import PROBLEMS,module,validate,stack_oracle,noise_oracle,charger_heap,JUDGE
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R34'
def noise_expected(text):
    edges,bounds,weights=validate('tolerance-paths',text);n=len(bounds)
    if n<=8:return noise_oracle(text),'enumeration of all path-weight assignments'
    if all(l==-10**9 and r==10**9 for l,r in bounds):
        parent=list(range(n))
        def find(x):
            while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
            return x
        for (u,v),w in zip(edges,weights):
            if w:parent[find(u)]=find(v)
        sizes=collections.Counter(find(i) for i in range(n));return [sizes[find(i)] for i in range(n)],'unrestricted component sizes'
    if all(l==r==0 for l,r in bounds):
        reached=[1<<i for i in range(n)]
        for value in set(v for w in weights for v in w):
            parent=list(range(n))
            def find(x):
                while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
                return x
            for (u,v),w in zip(edges,weights):
                if value in w:parent[find(u)]=find(v)
            masks=collections.defaultdict(int)
            for i in range(n):masks[find(i)]|=1<<i
            for i in range(n):reached[i]|=masks[find(i)]
        return [x.bit_count() for x in reached],'union of equal-weight connected components'
    if all(u==0 for u,v in edges) and all(l==r==1 for l,r in bounds):
        at_weight=collections.defaultdict(int)
        for (_,v),weights_here in zip(edges,weights):
            for w in weights_here:at_weight[w]|=1<<v
        answers=[n]
        for (_,v),weights_here in zip(edges,weights):
            mask=(1<<v)|1
            for w in weights_here:mask|=at_weight[w+1]
            answers.append(mask.bit_count())
        return answers,'two-edge star paths grouped by edge weight'
    # Medium cases: explicit cross product of feasible predecessor and next weights.
    adjacent=[[] for _ in range(n)]
    for e,(u,v) in enumerate(edges):adjacent[u].append((v,e));adjacent[v].append((u,e))
    answer=[]
    for start in range(n):
        queue=[(start,-1,None)]
        for u,parent,previous in queue:
            for v,e in adjacent[u]:
                if v==parent:continue
                possible=set(weights[e]) if previous is None else {w for w in weights[e] if any(bounds[u][0]<=w-p<=bounds[u][1] for p in previous)}
                if possible:queue.append((v,u,possible))
        answer.append(len(queue))
    return answer,'set cross products without ordered searches'
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -Wall -Wextra','problems':{}};audit={}
    if args.only and (ROOT/'docs/benchmark-R34.json').exists():
        result=json.loads((ROOT/'docs/benchmark-R34.json').read_text('utf-8'));audit=json.loads((OUT/'formal-audit.json').read_text('utf-8'))
    for topic,slug in PROBLEMS:
        if args.only and slug!=args.only:continue
        directory=ROOT/'topics'/topic/slug;gen=module(directory/'tests/generate.py');plan=json.loads((directory/'tests/plan.json').read_text('utf-8'));interactive=slug=='substring-permutation'
        variants=['std'] if interactive else [p.stem for p in directory.glob('*.cpp')];programs={v:OUT/f'{slug}-{v}.exe' for v in variants}
        dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{p.name:sha256(p) for p in directory.iterdir() if p.suffix in ['.cpp','.hpp']},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(directory/'tests/generate.py'),'plan_sha256':sha256(directory/'tests/plan.json'),'cases':[]}
        if interactive:entry.update(judge_sha256=sha256(directory/'judge.py'),timing_note='Actual interactive solver via pipes, including Python judge wall time; memory measures only solver. simulate.cpp is a testing harness, not a submission.')
        for case in plan['cases']:
            expected=None;kind='two complete algorithms and independent small models'
            if slug=='you-wrote-this-problem':text,expected=gen.make_case(case);assert (text,expected)==gen.make_case(case);kind='Python block Counters; no pair matrix or position tree'
            else:text=gen.generate(case);assert text==gen.generate(case)
            parsed=validate(slug,text,case['group'],answers=expected.split() if expected is not None else None)
            if slug=='shared-charger':
                n,m,a,b=parsed;mode=case['mode']
                if mode in ['zero','covered']:answer=0
                elif mode in ['impossible','overflow','late-conflict']:answer=-1
                elif mode=='staggered':answer=m*case['bmax']
                elif mode=='single':answer=case['bmax']
                else:answer=charger_heap(a,b,m)
                expected=str(answer);kind='closed boundary formula' if mode!='random' else 'Python priority-queue earliest-deadline scheduling'
            elif slug=='tolerance-paths':values,kind=noise_expected(text);expected=' '.join(map(str,values))
            elif slug=='dynamic-decreasing-stack':
                if case['group']<3:expected=' '.join(map(str,stack_oracle(text)));kind='literal stack simulation'
                elif case['shape'] in ['equal','decreasing']:
                    _,ops=parsed;expected=' '.join(str(1 if case['shape']=='equal' else y-x+1) for t,x,y in ops if t==2);kind='constant or strictly decreasing invariant'
                elif case.get('mode')=='updates':expected='';kind='no queries'
            elif interactive:expected=' '.join(map(str,parsed))+'\n';kind='actual hidden-permutation judge'
            inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n');item={'id':case['id'],'input_sha256':sha256(inp),'programs':{},'verification_method':kind,'expected_output_available':expected is not None};outputs={}
            if interactive:
                measured=[JUDGE.run(programs['std'],parsed) for _ in range(5)]
                peak=JUDGE.run(programs['std'],parsed)['peak_working_set_bytes'];seconds=[x['seconds'] for x in measured]
                item['programs']['std']={'seconds':seconds,'median_seconds':statistics.median(seconds),'peak_working_set_bytes':peak}
                item['queries']=measured[0]['queries'];assert all(x['queries']==item['queries'] for x in measured)
                outputs['std']=expected.encode();(dest/(case['id']+'.trace.json')).write_text(json.dumps(measured[0],indent=2)+'\n','utf-8')
            else:
                for v,p in programs.items():
                    target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes();assert peak<=(256 if slug=='dynamic-decreasing-stack' else 128)*2**20
                    if expected is not None:assert outputs[v].split()==expected.encode().split(),(slug,case['id'],v,'expected')
                    item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
                assert all(x==outputs['std'] for x in outputs.values()),(slug,case['id'])
                for repeat in range(5):
                    for v in variants if repeat%2==0 else variants[::-1]:
                        target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes()==outputs[v];item['programs'][v]['seconds'].append(elapsed)
                for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=sha256(inp.with_suffix('.out'));entry['cases'].append(item)
            print(slug,case['id'],'passed',flush=True)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants}
        entry['limit_seconds']=math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        samples=0
        for inp in sorted((directory/'tests/samples').glob('*.in')):
            text=inp.read_text('utf-8');expected=inp.with_suffix('.out').read_bytes();validate(slug,text,5 if slug=='shared-charger' else 3,expected.split() if slug=='you-wrote-this-problem' else None)
            if interactive:assert JUDGE.run(programs['std'],JUDGE.read_hidden(text))['answer']==list(map(int,expected.split()))
            else:
                for p in programs.values():assert subprocess.run([str(p)],input=inp.read_bytes(),capture_output=True,check=True).stdout.split()==expected.split(),(slug,inp.name)
            samples+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True)
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','01','--case','02','--std',str(programs['std'])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['01.in','01.out','02.in','02.out']
        for name in ['01.in','01.out','02.in','02.out']:assert (cli/name).read_bytes()==(dest/name).read_bytes(),(slug,name)
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True);assert bad.returncode!=0
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':len(plan['cases']),'reproduced_inputs':len(plan['cases']),'samples':samples,'generator_cli_checks':4,'all_variants_valid':True,'expected_outputs':sum(c['expected_output_available'] for c in entry['cases'])}
        (ROOT/'docs/benchmark-R34.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8')
        print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
