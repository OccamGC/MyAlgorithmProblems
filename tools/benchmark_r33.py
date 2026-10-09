"""Validate, reproduce, cross-check and measure R33 programs (five runs per input)."""
from pathlib import Path
import argparse,hashlib,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r33 import PROBLEMS,load_generator,validate,permutation_oracle,leaf_oracle,direct_sum,CHECKER,P,Q
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build/R33'

def leaf_formula(n,m,anonymous):
    if n<=2:return str(int(n==m))
    if not 2<=m<n:return '0'
    if n<=1000:answer=leaf_oracle(n,m)
    elif m==n-1:answer=n*math.factorial(n-1)%Q
    elif m==2:answer=(math.factorial(n)%Q)*(math.factorial(n-1)%Q)%Q*pow(2,Q-2,Q)%Q
    else:
        fact=[1]*(n+1)
        for i in range(1,n+1):fact[i]=fact[i-1]*i%Q
        inv=[1]*(n+1);inv[n]=pow(fact[n],Q-2,Q)
        for i in range(n,0,-1):inv[i-1]=inv[i]*i%Q
        t=n-m;onto=sum((-1 if j&1 else 1)*fact[t]*inv[j]%Q*inv[t-j]%Q*pow(t-j,n-2,Q) for j in range(t+1))%Q
        answer=fact[n]*inv[m]%Q*inv[t]%Q*onto%Q*fact[n-1]%Q
    if anonymous:answer=answer*pow(math.factorial(m),Q-2,Q)%Q
    return str(answer)

def lagrange_weights(x,count):
    if 0<=x<count:return [int(i==x) for i in range(count)]
    fact=[1]*count
    for i in range(1,count):fact[i]=fact[i-1]*i%P
    inv=[1]*count;inv[-1]=pow(fact[-1],P-2,P)
    for i in range(count-1,0,-1):inv[i-1]=inv[i]*i%P
    prefix=[1]*(count+1);suffix=[1]*(count+1)
    for i in range(count):prefix[i+1]=prefix[i]*(x-i)%P
    for i in range(count-1,-1,-1):suffix[i]=suffix[i+1]*(x-i)%P
    return [prefix[i]*suffix[i+1]%P*inv[i]%P*inv[count-1-i]%P*(-1 if (count-1-i)&1 else 1)%P for i in range(count)]

def independent_sum(text):
    n,a,b,ops=validate('dynamic-polynomial-geometric-sum',text);k=len(b)-1
    if n<=1000 and all(op[0]!=1 or op[1]<=1000 for op in ops):return '\n'.join(direct_sum(text)),'direct summation'
    if a==0:return '\n'.join(['0']*(len(ops)+1)),'zero base'
    if a==1:
        # For a=1, the answer is a polynomial in n of degree at most k+1.
        table=[[0]*(k+1) for _ in range(k+2)]
        for x in range(1,k+2):
            power=1
            for j in range(k+1):table[x][j]=(table[x-1][j]+power)%P;power=power*x%P
        values=[sum(c*v for c,v in zip(b,row))%P for row in table];answer=[]
        def evaluate():return str(sum(w*v for w,v in zip(lagrange_weights(n,k+2),values))%P)
        answer.append(evaluate())
        for op in ops:
            if op[0]==1:n=op[1]
            else:
                j,value=op[1:];delta=value-b[j];b[j]=value
                values=[(v+delta*row[j])%P for v,row in zip(values,table)]
            answer.append(evaluate())
        return '\n'.join(answer),'finite polynomial interpolation'
    if a==P-1 and all(op[0]==2 for op in ops):
        # Pair consecutive odd/even terms; each moment is a polynomial in pair count.
        count=k+2;weights=lagrange_weights(n//2,count);table=[[0]*(k+1) for _ in range(count)]
        for x in range(1,count):
            even=odd=1
            for j in range(k+1):table[x][j]=(table[x-1][j]+even-odd)%P;even=even*(2*x)%P;odd=odd*(2*x-1)%P
        sums=[(sum(weights[x]*table[x][j] for x in range(count))-(pow(n,j,P) if n&1 else 0))%P for j in range(k+1)]
        current=sum(c*v for c,v in zip(b,sums))%P;answer=[str(current)]
        for _,j,value in ops:current=(current+(value-b[j])*sums[j])%P;b[j]=value;answer.append(str(current))
        return '\n'.join(answer),'paired alternating sums and interpolation'
    return None,'two complete algorithms and proof'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',choices=[s for _,s in PROBLEMS]);args=parser.parse_args()
    result={'repeat':5,'multiplier':2,'resolution_seconds':0.5,'platform':platform.platform(),'compiler':'GCC 16.2.0','flags':'-std=c++17 -O2 -DNDEBUG -Wall -Wextra -Wpedantic','problems':{}};audit={}
    if args.only:
        result=json.loads((ROOT/'docs/benchmark-R33.json').read_text('utf-8'));audit=json.loads((OUT/'formal-audit.json').read_text('utf-8'))
    for topic,slug in PROBLEMS:
        if args.only and slug!=args.only:continue
        directory=ROOT/'topics'/topic/slug;gen=load_generator(topic,slug);plan=json.loads((directory/'tests/plan.json').read_text('utf-8'))
        variants=[p.stem for p in sorted(directory.glob('*.cpp'))];programs={v:OUT/f'{slug}-{v}.exe' for v in variants};dest=ROOT/'build/data'/slug;dest.mkdir(parents=True,exist_ok=True)
        entry={'sources':{p.name:sha256(p) for p in directory.glob('*.cpp')},'binaries':{v:sha256(p) for v,p in programs.items()},'generator_sha256':sha256(directory/'tests/generate.py'),'plan_sha256':sha256(directory/'tests/plan.json'),'cases':[]}
        if slug=='mind-swap-restoration':entry['checker_sha256']=sha256(directory/'checker.py')
        for case in plan['cases']:
            text=gen.generate(case);parsed=validate(slug,text,case['group']);assert text==gen.generate(case)
            inp=dest/(case['id']+'.in');inp.write_text(text,'utf-8',newline='\n');item={'id':case['id'],'input_sha256':sha256(inp),'programs':{}};expected=None;kind='two complete algorithms and proof'
            if slug.endswith('leaf-orders'):
                expected=leaf_formula(*parsed,slug.startswith('anonymous'));kind='Stirling DP' if parsed[0]<=1000 else 'path/star/impossibility formula' if parsed[1] in [0,2,parsed[0]-1] else 'separate Python implementation of the proved inclusion-exclusion formula'
            elif slug=='lexicographic-jump':
                if case['group']<3:expected='\n'.join(' '.join(map(str,permutation_oracle(a,k))) for a,k in parsed);kind='Python exact rank and unrank'
                elif case['id'] in ['06','07']:
                    a,k=parsed[0];n=len(a);suffix=permutation_oracle(list(range(n-12,n+1)),k-(case['id']=='07'))
                    expected=' '.join(map(str,list(range(1,n-12))+suffix));kind='known ascending rank plus a bounded suffix'
            elif slug=='dynamic-polynomial-geometric-sum':expected,kind=independent_sum(text)
            else:kind='independent complete output checker'
            outputs={}
            for v,p in programs.items():
                target=OUT/f'{slug}-{v}.out';peak=run_with_peak_memory(p,inp,target);outputs[v]=target.read_bytes();assert peak<=128*2**20,(slug,v,peak)
                if expected is not None:assert outputs[v].split()==expected.encode().split(),(slug,case['id'],v,'expected output')
                if slug=='mind-swap-restoration':CHECKER.check(text,outputs[v].decode())
                item['programs'][v]={'seconds':[],'peak_working_set_bytes':peak}
            if slug!='mind-swap-restoration':assert all(x==outputs['std'] for x in outputs.values()),(slug,case['id'])
            inp.with_suffix('.out').write_bytes(outputs['std']);item['output_sha256']=hashlib.sha256(outputs['std']).hexdigest()
            for repeat in range(5):
                for v in variants if repeat%2==0 else variants[::-1]:
                    target=OUT/f'{slug}-{v}.out';elapsed=run(programs[v],inp,target);assert target.read_bytes()==outputs[v];item['programs'][v]['seconds'].append(elapsed)
            for stats in item['programs'].values():stats['median_seconds']=statistics.median(stats['seconds'])
            item.update(expected_output_available=expected is not None,verification_method=kind);entry['cases'].append(item)
        entry['summary']={v:{'slowest_median_seconds':max(c['programs'][v]['median_seconds'] for c in entry['cases']),'peak_working_set_bytes':max(c['programs'][v]['peak_working_set_bytes'] for c in entry['cases'])} for v in variants}
        entry['limit_seconds']=math.ceil(entry['summary']['std']['slowest_median_seconds']*4)/2
        for stats in entry['summary'].values():stats['passes_estimated_limit']=stats['slowest_median_seconds']<=entry['limit_seconds']
        sample_count=0
        for inp in sorted((directory/'tests/samples').glob('*.in')):
            text=inp.read_text('utf-8');validate(slug,text);expected=inp.with_suffix('.out').read_bytes()
            for v,p in programs.items():
                got=subprocess.run([str(p)],input=inp.read_bytes(),capture_output=True,check=True).stdout
                if slug=='mind-swap-restoration':CHECKER.check(text,got.decode())
                else:assert got.split()==expected.split(),(slug,inp.name,v)
            sample_count+=1
        cli=OUT/'cli'/slug;cli.mkdir(parents=True,exist_ok=True)
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--plan',str(directory/'tests/plan.json'),'--out-dir',str(cli),'--case','01','--case','02','--std',str(programs['std'])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['01.in','01.out','02.in','02.out']
        for name in ['01.in','01.out','02.in','02.out']:assert (cli/name).read_bytes()==(dest/name).read_bytes()
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','unknown'],capture_output=True);assert bad.returncode!=0 and b'unknown case' in bad.stderr
        result['problems'][slug]=entry;audit[slug]={'formal_inputs':10,'reproduced_inputs':10,'samples':sample_count,'generator_cli_checks':4,'all_variants_equal':None if slug=='mind-swap-restoration' else True,'all_variants_valid':True,'expected_outputs':sum(c['expected_output_available'] for c in entry['cases']),'checker_validations':10 if slug=='mind-swap-restoration' else 0}
        (ROOT/'docs/benchmark-R33.json').write_text(json.dumps(result,indent=2)+'\n','utf-8');(OUT/'formal-audit.json').write_text(json.dumps(audit,indent=2)+'\n','utf-8')
        print(slug,entry['summary'],'limit',entry['limit_seconds'],flush=True)
if __name__=='__main__':main()
