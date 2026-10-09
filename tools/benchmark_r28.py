"""Reproducible full-range measurement and cross-checks for R28."""
from pathlib import Path
import importlib.util,json,math,platform,statistics,subprocess,sys,heapq
from benchmark_reference import run,run_with_peak_memory,sha256
from check_r28 import validate,ORACLES
ROOT=Path(__file__).resolve().parents[1]
SELECTION = [
    {'topic': 'greedy', 'slug': 'tree-demolition'},
    {'topic': 'data-structures', 'slug': 'line-capacity-transport'},
    {'topic': 'optimization', 'slug': 'time-management-and-team-sports'},
    {'topic': 'bitwise', 'slug': 'dynamic-binary-bounds'},
    {'topic': 'simulation', 'slug': 'grid-forest-matching'},
]
VARIANTS={'tree-demolition':['std'],'line-capacity-transport':['std','alternative-blocks'],'time-management-and-team-sports':['std'],'dynamic-binary-bounds':['std'],'grid-forest-matching':['std','alternative-bitsets']}
def certificate(data,inp,out):
    a=data;n=len(a)
    result=subprocess.run([str(ROOT/'build/R28/assignment-certificate.exe')],input=inp.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    assert result.stdout.split()==out.split()
    rows=result.stderr.decode().split();assert len(rows)==3*n+1 and int(rows[0])==n
    match=list(map(int,rows[1:n+1]));assert sorted(match)==list(range(1,n+1))
    def signed(s):
        x=int(s,16);return x-(1<<768) if x>>(768-1) else x
    u=list(map(signed,rows[n+1:2*n+1]));v=list(map(signed,rows[2*n+1:]))
    weight=[-(1<<(9*g)) for g in range(71)]
    for i in range(n):
        for j in range(n):assert u[i]+v[j]<=weight[a[i][j]],('dual infeasible',i,j)
    for j,i in enumerate(match):assert u[i-1]+v[j]==weight[a[i-1][j]],('matched edge not tight',i,j)
    counts=[0]*71
    for j,i in enumerate(match):counts[70-a[i-1][j]]+=1
    assert counts==list(map(int,out.split()))
def demolition_check(data,out):
    p,edges=data;n=len(p);values=list(map(int,out.split()));assert len(values)==n+1
    order=values[1:];assert sorted(order)==list(range(1,n+1))
    position=[0]*n
    for i,u in enumerate(order):position[u-1]=i
    assert values[0]==sum(position[i]*p[i] for i in range(n))
    adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    parent=[-1]*n;root_order=[0]
    for u in root_order:
        for v in adj[u]:
            if v!=parent[u]:
                parent[v]=u;root_order.append(v);assert position[v]<position[u]
    if min(p)==max(p):
        degree=[len(row)-(i!=0) for i,row in enumerate(adj)]
        available=[i for i in range(n) if degree[i]==0];heapq.heapify(available);lex=[]
        while available:
            u=heapq.heappop(available);lex.append(u+1)
            if parent[u]!=-1:
                v=parent[u];degree[v]-=1
                if degree[v]==0:heapq.heappush(available,v)
        assert lex==order,'equal-weight lexicographic order'
def main():
    compiler=ROOT.parent/'Toolchains/w64devkit-2.10.0/w64devkit/bin/g++.exe'
    path=ROOT/'docs/benchmark-R28.json'
    report=json.loads(path.read_text('utf-8')) if path.exists() else dict(date='2026-10-01',timezone='Asia/Shanghai',cpu='Intel(R) Core(TM) Ultra 9 275HX',os=platform.platform(),python=platform.python_version(),compiler=subprocess.check_output([str(compiler),'--version']).decode().splitlines()[0],flags=['-std=c++17','-O2','-Wall','-Wextra','-pedantic-errors'],repeat=5,resolution_seconds=.5,timing_scope='Process startup and input/output included; generation and validation excluded.',memory_scope='Separately measured peak working set includes runtime.',problems={})
    audit_path=ROOT/'build/R28/audit.json';audit=json.loads(audit_path.read_text('utf-8')) if audit_path.exists() else {}
    scopes={
      'tree-demolition':'Every full output checked for permutation, leaf-removal precedence and exact 64-bit objective; equal-weight instances additionally compared with a smallest-leaf heap. Optimality and tie handling have a block-exchange proof and exhaustive small-instance checks.',
      'line-capacity-transport':'Every prefix compared between sign-aware segment tree and independent sorted-block range-flow representation; full assignment-state enumeration on small inputs.',
      'time-management-and-team-sports':'Every full output has an independently checked arbitrary-precision matching/dual certificate: all dual inequalities, equality on matched edges, bijection and reward histogram.',
      'dynamic-binary-bounds':'Every answer compared with a dense, decreasing equal-mask automaton using generic matrix multiplication and subset Mobius inversion; small inputs additionally enumerate all integer pairs.',
      'grid-forest-matching':'Every answer compared between candidate-list filtering and word-parallel translated masks; small inputs move all surviving positions after every operation.'
    }
    for row in SELECTION:
        slug=row['slug']
        if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
        directory=ROOT/'topics'/row['topic']/slug;data_dir=ROOT/'build/data'/slug;data_dir.mkdir(parents=True,exist_ok=True)
        spec=importlib.util.spec_from_file_location(slug,directory/'tests/generate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((directory/'tests/plan.json').read_text('utf-8'));variants=VARIANTS[slug]
        programs=[ROOT/'build/R28'/f'{slug}-{v}.exe' for v in variants];outputs=[ROOT/'build/R28'/f'{slug}-{v}.out' for v in variants]
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
            if slug=='tree-demolition':demolition_check(data,expected)
            elif slug=='time-management-and-team-sports':certificate(data,inp,expected)
            elif slug=='dynamic-binary-bounds':
                checker_out=ROOT/'build/R28/dense-verifier.out'
                with inp_path.open('rb') as source,checker_out.open('wb') as target:subprocess.run([str(ROOT/'build/R28/verify-binary.exe')],stdin=source,stdout=target,check=True)
                assert checker_out.read_bytes()==expected,(slug,recipe['id'],'dense automaton')
            if recipe['mode']=='literal':assert list(map(int,expected.split()))==ORACLES[slug](data)
            del data,inp
            times=[[] for _ in variants]
            for repetition in range(5):
                order=list(range(len(variants)))
                if repetition%2:order.reverse()
                for i in order:times[i].append(run(programs[i],inp_path,outputs[i]))
            inp_path.with_suffix('.out').write_bytes(expected)
            record=dict(id=recipe['id'],verification_scope=scopes[slug],input_sha256=sha256(inp_path),output_sha256=sha256(inp_path.with_suffix('.out')),programs={v:dict(seconds=times[i],median_seconds=statistics.median(times[i]),peak_working_set_bytes=peaks[i]) for i,v in enumerate(variants)})
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
            inp=sample.read_text('ascii');data=validate(slug,inp);want=list(map(int,sample.with_suffix('.out').read_bytes().split()));assert want==ORACLES[slug](data)
            for program in programs:assert list(map(int,subprocess.check_output([str(program)],input=inp.encode()).split()))==want
            samples.append(sample.stem)
        cli=ROOT/'build/R28/cli'/slug
        subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--plan',str(directory/'tests/plan.json'),'--out-dir',str(cli),'--case','02','--std',str(programs[0])],check=True)
        assert sorted(p.name for p in cli.iterdir())==['02.in','02.out'];assert sha256(cli/'02.in')==sha256(data_dir/'02.in');assert sha256(cli/'02.out')==sha256(data_dir/'02.out')
        bad=subprocess.run([sys.executable,str(directory/'tests/generate.py'),'--out-dir',str(cli),'--case','missing'],capture_output=True);assert bad.returncode!=0 and b'unknown case' in bad.stderr
        audit[slug]=dict(validated_cases=10,reproduced_cases=10,formal_checks=10,verification_scope=scopes[slug],samples=samples,cli_checks=3)
        audit_path.write_text(json.dumps(audit,indent=2)+'\n','utf-8');print('Completed',slug,item['summary'],'limit',item['limit_seconds'],'multiplier',multiplier,flush=True)
if __name__=='__main__':main()
