"""Measure R30 programs after validation and full-output cross-checks."""
from pathlib import Path
import json,math,platform,statistics,subprocess,sys,hashlib
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r30 import PROBLEMS,load_generator,validate,unlock_oracle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/R30'

def main():
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -DNDEBUG -Wall -Wextra -Wpedantic','problems':{}}
    audit={}
    for topic,slug in PROBLEMS:
        directory=ROOT/'topics'/topic/slug;gen=load_generator(topic,slug);plan=json.loads((directory/'tests/plan.json').read_text('utf-8'))
        variants=[p.stem for p in sorted(directory.glob('*.cpp'))]
        programs={v:OUT/f'{slug}-{v}.exe' for v in variants}
        dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{p.name:sha256(p) for p in sorted(directory.glob('*.cpp'))},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(directory/'tests/generate.py'),'plan_sha256':sha256(directory/'tests/plan.json'),'cases':[]}
        for case in plan['cases']:
            text=gen.generate(case);validate(slug,text,case['group']);assert text==gen.generate(case)
            inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n')
            item={'id':case['id'],'input_sha256':sha256(inp),'programs':{}}
            expected=None
            if slug=='monotone-sequence-count':
                n,m=map(int,text.split());expected=str(math.comb(n+m-1,n)%998244353).encode()+b'\n'
            if slug=='nested-linear-sum':
                n,m,k,c=map(int,text.split())
                # Large factorials are avoided; boundary identities are independent.
                if m==0:expected=b'0\n'
                elif m==1:expected=f'{(k+c)%998244353}\n'.encode()
                elif n==1:expected=f'{(k*m*(m+1)//2+c*m)%998244353}\n'.encode()
                elif m==998244353:expected=b'0\n'
                elif m==998244354:expected=f'{(k+c)%998244353}\n'.encode()
                elif n<=100 and m<=2000:expected=f'{(k*math.comb(n+m,n+1)+c*math.comb(n+m-1,n))%998244353}\n'.encode()
            if slug=='monotone-unlocks':
                N,M=map(int,text.splitlines()[0].split())
                if case['mode'] in ['literal','random']:expected=unlock_oracle(text).encode()
                else:expected=('0\n' if case['mode']=='cycle' else '1\n').encode()*M
            outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes()
                assert peak<=128*2**20
                if expected is not None:assert outputs[v].split()==expected.split(),(slug,case['id'],v,'independent output')
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            assert all(value==outputs['std'] for value in outputs.values()),(slug,case['id'])
            item['output_sha256']=hashlib.sha256(outputs['std']).hexdigest();inp.with_suffix('.out').write_bytes(outputs['std'])
            for repeat in range(5):
                for v in (variants if repeat%2==0 else variants[::-1]):
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target)
                    assert target.read_bytes()==outputs[v]
                    item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            item['independent_expected_output']=expected is not None
            entry['cases'].append(item)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants}
        entry['limit_seconds']=math.ceil(entry['summary']['std']['slowest_median_seconds']*2/0.5)*0.5
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
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','unknown'],capture_output=True)
        assert bad.returncode!=0 and b'unknown case' in bad.stderr
        result['problems'][slug]=entry
        audit[slug]={'formal_inputs':10,'reproduced_inputs':10,'samples':sample_count,'generator_cli_checks':4,'all_variants_equal':True,'independent_full_outputs':sum(c['independent_expected_output'] for c in entry['cases'])}
        (ROOT/'docs/benchmark-R30.json').write_text(json.dumps(result,indent=2)+'\n','utf-8')
        (OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8')
        print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
