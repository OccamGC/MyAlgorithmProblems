"""Reproduce R35 data; independent checks, five timings and separate peak memory."""
from pathlib import Path
import argparse,functools,gc,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r35 import PROBLEMS,module,validate,substring_oracle,rational_answer,CHECKER
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R35'

def survey_expected(parsed):
    n,edges=parsed;total=sum(w for u,v,w in edges)
    if len(edges)==n-1:return 2*total,'each tree edge twice'
    adj=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):adj[u].append((v,w,i));adj[v].append((u,w,i))
    odd=[u for u in range(n) if len(adj[u])%2]
    if not odd:return total,'Euler circuit'
    if all(len(adj[u])==1 for u in odd):return total+sum(adj[u][0][1] for u in odd),'Euler core and mandatory doubled bridges'
    if not total:return 0,'zero weights'
    branch=[u for u in range(n) if len(adj[u])!=2];assert len(branch)<=20
    index={u:i for i,u in enumerate(branch)};k=len(branch);matrix=[[10**30]*k for _ in branch]
    for s in branch:
        a=index[s];matrix[a][a]=0
        for v,w,e in adj[s]:
            cost=w
            while v not in index:
                nxt=next(x for x in adj[v] if x[2]!=e);v,w,e=nxt;cost+=w
            b=index[v];matrix[a][b]=min(matrix[a][b],cost)
    for z in range(k):
        for a in range(k):
            for b in range(k):matrix[a][b]=min(matrix[a][b],matrix[a][z]+matrix[z][b])
    ids=[index[u] for u in odd]
    @functools.cache
    def match(mask):
        if not mask:return 0
        first=mask&-mask;a=first.bit_length()-1;rest=mask^first;best=10**30
        bits=rest
        while bits:
            bit=bits&-bits;b=bit.bit_length()-1;bits^=bit;best=min(best,matrix[ids[a]][ids[b]]+match(rest^bit))
        return best
    return total+match((1<<len(ids))-1),'degree-two chain contraction, Floyd distances and memoized pairing'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -Wall -Wextra','problems':{}};audit={}
    if args.only and (ROOT/'docs/benchmark-R35.json').exists():result=json.loads((ROOT/'docs/benchmark-R35.json').read_text());audit=json.loads((OUT/'formal-audit.json').read_text())
    for topic,slug in PROBLEMS:
        if args.only and slug!=args.only:continue
        d=ROOT/'topics'/topic/slug;gen=module(d/'tests/generate.py');plan=json.loads((d/'tests/plan.json').read_text());variants=[p.stem for p in d.glob('*.cpp')];programs={v:OUT/f'{slug}-{v}.exe' for v in variants};dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{p.name:sha256(p) for p in d.iterdir() if p.suffix in ['.cpp','.hpp']},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(d/'tests/generate.py'),'plan_sha256':sha256(d/'tests/plan.json'),'cases':[]}
        if slug=='lower-weight-imperfect-non-matching':entry['checker_sha256']=sha256(d/'checker.py')
        for case in plan['cases']:
            print(slug,case['id'],'generating',flush=True);expected=None;kind='SA and SAM plus independent small substring enumeration'
            if slug in ['batched-rectangle-maximum','path-neighborhood-updates']:
                text,expected=gen.make_case(case);assert (text,expected)==gen.make_case(case);kind='compressed uniform bands' if slug=='batched-rectangle-maximum' else 'literal or sparse values, LCA distance membership and set cardinalities'
            else:text=gen.generate(case);assert text==gen.generate(case)
            parsed=validate(slug,text,case['group'])
            if slug=='lower-weight-imperfect-non-matching':kind='independent Prim baseline and complete route checker'
            elif slug=='closed-edge-survey':value,kind=survey_expected(parsed);expected=f'1\n{value}\n'
            elif slug=='unique-substring-hits':
                s,targets=parsed;n=len(s);mode=case['mode'];counts=None
                if mode=='same':counts=(n,1)
                elif mode=='alternating':counts=(2*n-1,4)
                elif mode=='singular':counts=(1000096051,1000000007)
                elif n<=500:expected='\n'.join(substring_oracle(text));kind='explicit substring occurrence Counter'
                if counts:expected='\n'.join(str(rational_answer(t,*counts)) for t in targets);kind='closed substring counts and exact rational reduction'
            del parsed;gc.collect()
            inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n');item={'id':case['id'],'input_sha256':sha256(inp),'programs':{},'verification_method':kind,'expected_output_available':expected is not None or slug=='lower-weight-imperfect-non-matching'};outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes();assert peak<=(512 if slug in ['batched-rectangle-maximum','path-neighborhood-updates'] else 256 if slug=='closed-edge-survey' else 128)*2**20
                if expected is not None:assert outputs[v].split()==expected.encode().split(),(slug,case['id'],v,'expected')
                if slug=='lower-weight-imperfect-non-matching':assert CHECKER.check(text,outputs[v].decode())['score']==100
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            assert all(x==outputs['std'] for x in outputs.values()),(slug,case['id'])
            for repeat in range(5):
                for v in variants if repeat%2==0 else variants[::-1]:
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes()==outputs[v];item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=sha256(inp.with_suffix('.out'));entry['cases'].append(item);print(slug,case['id'],'passed',flush=True)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants};entry['limit_seconds']=max(.5,math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2)
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        samples=0
        for inp in sorted((d/'tests/samples').glob('*.in')):
            text=inp.read_text();expected=inp.with_suffix('.out').read_bytes();validate(slug,text)
            for p in programs.values():
                answer=subprocess.run([str(p)],input=inp.read_bytes(),capture_output=True,check=True).stdout
                if slug=='lower-weight-imperfect-non-matching':assert CHECKER.check(text,answer.decode())['score']==100
                else:assert answer.split()==expected.split()
            samples+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True)
        subprocess.run([sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--case','01','--case','02','--std',str(programs['std'])],check=True)
        for name in ['01.in','01.out','02.in','02.out']:assert (cli/name).read_bytes()==(dest/name).read_bytes(),(slug,name)
        assert subprocess.run([sys.executable,str(d/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True).returncode!=0
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':len(plan['cases']),'reproduced_inputs':len(plan['cases']),'samples':samples,'generator_cli_checks':4,'all_variants_valid':True,'expected_outputs':sum(c['expected_output_available'] for c in entry['cases'])}
        (ROOT/'docs/benchmark-R35.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
