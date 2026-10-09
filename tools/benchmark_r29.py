"""Full-range timing, input checks and mathematical certificates for R29."""
from pathlib import Path
import collections,importlib.util,json,math,platform,statistics,subprocess,sys
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r29 import validate,oracle
ROOT=Path(__file__).resolve().parents[1]
SELECTION = [
    {'topic': 'data-structures', 'slug': 'selective-suffix-sort'},
    {'topic': 'graphs', 'slug': 'common-tree-subset'},
    {'topic': 'combinatorics', 'slug': 'binary-power-partitions'},
    {'topic': 'optimization', 'slug': 'battle-upgrades'},
    {'topic': 'strings', 'slug': 'dynamic-path-independence'},
]
VARIANTS={r['slug']:['std'] for r in SELECTION}
VARIANTS['battle-upgrades'].append('alternative-heap')
VARIANTS['dynamic-path-independence'].append('alternative-offline')

def common_certificate(data,inp_path,expected,tag):
    n,weights,trees=data
    cert=ROOT/'build/R29'/f'common-{tag}.certificate.txt';output=cert.with_suffix('.out')
    with inp_path.open('rb') as src,cert.open('wb') as err,output.open('wb') as dst:
        subprocess.run([str(ROOT/'build/R29/common-certificate.exe')],stdin=src,stdout=dst,stderr=err,check=True)
    assert output.read_bytes()==expected
    graph=[]
    for edges in trees:
        adj=[[] for _ in range(n)]
        for u,v in edges:adj[u].append(v);adj[v].append(u)
        graph.append(adj)
    removed=set();best=0;flows=0
    with cert.open('r',encoding='ascii') as source:
        while True:
            line=source.readline()
            if not line:break
            head=line.split();assert head[0]=='C' and len(head)==4
            center=int(head[1])-1;size=int(head[2]);positive=int(head[3])
            assert 0<=center<n and center not in removed
            component={center};queue=[center]
            for u in queue:
                for v in graph[0][u]:
                    if v not in removed and v not in component:component.add(v);queue.append(v)
            parents=[];descendants=collections.defaultdict(list)
            for adj in graph:
                par={center:-1};queue=[center]
                for u in queue:
                    for v in adj[u]:
                        if v in component and v not in par:par[v]=u;queue.append(v);descendants[u].append(v)
                parents.append(par)
            bad={u for u in component if any(u not in par for par in parents)};queue=list(bad)
            for u in queue:
                for v in descendants[u]:
                    if v not in bad:bad.add(v);queue.append(v)
            allowed=component-bad
            vertex=source.readline().split();assert vertex[0]=='V'
            ids=[int(v)-1 for v in vertex[1:]];assert len(ids)==size and len(set(ids))==size and set(ids)==allowed
            assert positive==sum(max(weights[u],0) for u in allowed)
            row=source.readline().split()
            if row==['S']:
                assert positive<=best
            else:
                assert row[0]=='F' and len(row)==6
                count,src,sink,value,edge_count=map(int,row[1:])
                assert (count,src,sink)==(size+2,size,size+1) and 0<=value<=positive
                index={u:i for i,u in enumerate(ids)};wanted=collections.Counter()
                for u in ids:
                    if weights[u]>0:wanted[(src,index[u],weights[u])]+=1
                    if weights[u]<0:wanted[(index[u],sink,-weights[u])]+=1
                    for par in parents:
                        if par[u]!=-1:wanted[(index[u],index[par[u]],positive+1)]+=1
                actual=collections.Counter();balance=[0]*count;residual=[[] for _ in range(count)];edges=[]
                for _ in range(edge_count):
                    u,v,capacity,flow=map(int,source.readline().split())
                    assert 0<=u<count and 0<=v<count and 0<=flow<=capacity
                    actual[(u,v,capacity)]+=1;balance[u]-=flow;balance[v]+=flow;edges.append((u,v,capacity))
                    if capacity>flow:residual[u].append(v)
                    if flow>0:residual[v].append(u)
                assert actual==wanted
                assert balance[src]==-value and balance[sink]==value
                assert all(balance[u]==0 for u in range(size))
                reached={src};queue=[src]
                for u in queue:
                    for v in residual[u]:
                        if v not in reached:reached.add(v);queue.append(v)
                assert sink not in reached
                assert sum(cap for u,v,cap in edges if u in reached and v not in reached)==value
                best=max(best,positive-value);flows+=1
            removed.add(center)
    assert len(removed)==n and [best]==list(map(int,expected.split()))
    return dict(certificate_sha256=sha256(cert),centers=n,flow_certificates=flows)

def inversions(a):
    values={v:i+1 for i,v in enumerate(sorted(set(a)))};bit=[0]*(len(values)+1);answer=0
    for v in reversed(a):
        i=values[v]-1
        while i:answer+=bit[i];i-=i&-i
        i=values[v]
        while i<len(bit):bit[i]+=1;i+=i&-i
    return answer
def formal_check(slug,data,inp_path,expected,recipe):
    values=list(map(int,expected.split()))
    if slug=='common-tree-subset':return common_certificate(data,inp_path,expected,recipe['id'])
    if slug=='binary-power-partitions':
        got=subprocess.check_output([str(ROOT/'build/R29/partitions-original.exe')],input=inp_path.read_bytes(),timeout=15)
        assert list(map(int,got.split()))==values and len(values)==1 and 0<=values[0]<10**9
    elif slug=='battle-upgrades':
        initial,prices,enemies=data;assert len(values)==4
        cost,hp,am,atk=values;oh,od,oa=initial;ch,cd,vd,ca,va=prices
        assert hp>=oh and am>=od and atk>=oa and (am-od)%vd==0 and (atk-oa)%va==0
        assert all(atk>d for k,h,d,a in enemies)
        damage=sum(k*((h+atk-d-1)//(atk-d))*max(a-am,0) for k,h,d,a in enemies)
        assert hp==max(oh,damage+1) and cost==(hp-oh)*ch+(am-od)//vd*cd+(atk-oa)//va*ca
    elif slug=='selective-suffix-sort':
        a,queries=data;assert len(values)==len(queries)+1
        assert values[0]==inversions(a) and all(0<=b<=a for a,b in zip(values,values[1:]))
        if recipe.get('shape')=='repeat':
            positions=[0]+[i for i in range(1,len(a)) if a[i]<a[0]]
            b=a.copy()
            for i,v in zip(positions,sorted(a[i] for i in positions)):b[i]=v
            assert values[1:]==[inversions(b)]*len(queries)
        if recipe.get('shape') in ['equal','increasing']:assert set(values)=={0}
        if recipe.get('shape') in ['two','descending']:assert values[-1]==0
    else:
        assert len(values)==sum(op[0]==3 for op in data) and all(0<=v<=100001 for v in values)
    if recipe['mode']=='literal' and not (slug=='binary-power-partitions' and data>20000):
        assert values==oracle(slug,data)
    return {}

def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    path=ROOT/'docs/benchmark-R29.json';audit_path=ROOT/'build/R29/audit.json'
    report=json.loads(path.read_text('utf-8')) if path.exists() else dict(date='2026-10-01',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic-errors'],repeat=5,resolution_seconds=.5,timing_scope='Includes process startup and input/output; excludes generation and validation.',memory_scope='Separately measured peak working set includes runtime.',problems={})
    audit=json.loads(audit_path.read_text('utf-8')) if audit_path.exists() else {}
    scopes={
    'selective-suffix-sort':'All initial inversion totals independently counted; every output checked for length and monotonic bounds; structured repeat/ordered cases have exact answers. Optimal count evolution proved and compared to actual array sorting on 700 small inputs.',
    'common-tree-subset':'Every centroid/pruned closure graph reconstructed independently; every non-skipped flow checked for capacities, conservation, source value and equal-capacity residual minimum cut. Complete center coverage and global maximum checked.',
    'binary-power-partitions':'Every full result compared with the unaccelerated original splitting recurrence. Four hundred small inputs additionally checked by ordinary coin-change DP.',
    'battle-upgrades':'Array event lists and heap event scheduling agree on every full output; final combat survival and cost independently recomputed with Python integers. Optimality/tie rules have proofs and 600 exhaustive small inputs.',
    'dynamic-path-independence':'Online canonical blocks and offline doubling ranks agree on every full output; operation validity checked independently. Both programs compared with explicit path strings on 600 small inputs each.'}
    for row in SELECTION:
        slug=row['slug']
        if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
        directory=ROOT/'topics'/row['topic']/slug;data_dir=ROOT/'build/data'/slug;data_dir.mkdir(parents=True,exist_ok=True)
        spec=importlib.util.spec_from_file_location(slug,directory/'tests/generate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((directory/'tests/plan.json').read_text('utf-8'));variants=VARIANTS[slug]
        programs=[ROOT/'build/R29'/f'{slug}-{v}.exe' for v in variants];outputs=[ROOT/'build/R29'/f'{slug}-{v}.out' for v in variants]
        item=dict(sources={v+'.cpp':sha256(directory/(v+'.cpp')) for v in variants},binaries={v:sha256(p) for v,p in zip(variants,programs)},generator_sha256=sha256(directory/'tests/generate.py'),plan_sha256=sha256(directory/'tests/plan.json'),cases=[])
        old=report['problems'].get(slug,{})
        if all(old.get(k)==item[k] for k in ['sources','binaries','generator_sha256','plan_sha256']):item['cases']=old['cases']
        report['problems'][slug]=item
        for recipe in plan['cases']:
            inp_path=data_dir/(recipe['id']+'.in');done=next((c for c in item['cases'] if c['id']==recipe['id']),None)
            if done and inp_path.exists() and inp_path.with_suffix('.out').exists() and sha256(inp_path)==done['input_sha256'] and sha256(inp_path.with_suffix('.out'))==done['output_sha256']:
                print('Already measured',slug,recipe['id'],flush=True);continue
            inp=module.generate(recipe);inp_path.write_text(inp,'ascii',newline='\n');data=validate(slug,inp)
            assert module.generate(recipe)==inp
            peaks=[run_with_peak_memory(program,inp_path,out) for program,out in zip(programs,outputs)]
            expected=outputs[0].read_bytes()
            for out in outputs[1:]:assert out.read_bytes()==expected,(slug,recipe['id'])
            certificate=formal_check(slug,data,inp_path,expected,recipe)
            del data,inp
            times=[[] for _ in variants]
            for repetition in range(5):
                order=list(range(len(variants)))
                if repetition%2:order.reverse()
                for i in order:times[i].append(run(programs[i],inp_path,outputs[i]))
            inp_path.with_suffix('.out').write_bytes(expected)
            record=dict(id=recipe['id'],verification_scope=scopes[slug],input_sha256=sha256(inp_path),output_sha256=sha256(inp_path.with_suffix('.out')),certificate=certificate,programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)})
            assert all(p<=row['memory_mb']*1024*1024 for p in peaks),(slug,peaks)
            item['cases']=[c for c in item['cases'] if c['id']!=recipe['id']]+[record];path.write_text(json.dumps(report,indent=2)+'\n','utf-8')
            print('Measured',slug,recipe['id'],{v:round(statistics.median(times[i]),4) for i,v in enumerate(variants)},flush=True)
        item['summary']={v:dict(slowest_median_seconds=max(c['programs'][v]['median_seconds'] for c in item['cases']),peak_working_set_bytes=max(c['programs'][v]['peak_working_set_bytes'] for c in item['cases'])) for v in variants}
        standard=item['summary']['std']['slowest_median_seconds'];good=max(x['slowest_median_seconds'] for x in item['summary'].values());multiplier=2
        while math.ceil(multiplier*standard/.5)*.5<2*good:multiplier+=1
        item['multiplier']=multiplier;item['limit_seconds']=math.ceil(multiplier*standard/.5)*.5
        item['multiplier_reason']='Default twofold headroom.' if multiplier==2 else 'The documented correct alternative needs twofold measured headroom on the original full range.'
        path.write_text(json.dumps(report,indent=2)+'\n','utf-8')
        samples=[]
        for sample in sorted((directory/'tests/samples').glob('*.in')):
            inp=sample.read_text('ascii');data=validate(slug,inp);want=list(map(int,sample.with_suffix('.out').read_bytes().split()));assert want==oracle(slug,data)
            for program in programs:assert list(map(int,subprocess.check_output([str(program)],input=inp.encode()).split()))==want
            samples.append(sample.stem)
        cli=ROOT/'build/R29/cli'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--plan',str(directory/'tests/plan.json'),'--out-dir',str(cli),'--case','02','--std',str(programs[0])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['02.in','02.out'];assert sha256(cli/'02.in')==sha256(data_dir/'02.in');assert sha256(cli/'02.out')==sha256(data_dir/'02.out')
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True);assert bad.returncode!=0 and b'unknown case' in bad.stderr
        audit[slug]=dict(validated_cases=10,reproduced_cases=10,formal_checks=10,verification_scope=scopes[slug],samples=samples,cli_checks=3)
        audit_path.write_text(json.dumps(audit,indent=2)+'\n','utf-8');print('Completed',slug,item['summary'],'limit',item['limit_seconds'],'multiplier',multiplier,flush=True)
if __name__=='__main__':main()
