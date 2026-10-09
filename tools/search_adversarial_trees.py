"""Reproducible structural stress search for three tree algorithm pairs.

This is an experiment: it does not edit statements, solutions or formal plans.
Screen timings select candidates only; repeated confirmation is a separate stage.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics
import subprocess
import time

import benchmark_reference as bench

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/adversarial-trees'
LIMITS = {'forest-ranger': 1000000, 'festival-plan': 500000, 'grinder': 300000}
FLAGS = ['-std=c++17', '-O2', '-DNDEBUG', '-Wall', '-Wextra', '-Wpedantic']


def pivot_guard_gains(n):
    """Make libstdc++'s median-of-three partitions repeatedly unbalanced.

    Most gains are one. A sparse set of decreasing large gains occupies the
    sampled positions. Simulate the partition swaps with sparse maps; all
    unassigned positions are below every selected pivot. The initial maximum
    is mandatory because the tree program emits its root-chain gain first.
    """
    # This upper bound also works when the extra gain mass crosses a power of
    # two. Iterating to a fixed point can oscillate at those boundaries.
    depth=2*((n-1).bit_length()-1)
    count=n-1-(2*depth*depth+3*depth+4)
    if count<=4*depth:
        raise ValueError('The pivot-guard construction needs a larger n.')
    identities={};values={};assigned={}
    def assign(pos,value):
        assert values.get(pos,0)==0
        values[pos]=value;assigned[identities.get(pos,pos)]=value
    def swap(a,b):
        identities[a],identities[b]=identities.get(b,b),identities.get(a,a)
        values[a],values[b]=values.get(b,0),values.get(a,0)
    assign(0,2*depth+5)
    first=0
    for step in range(depth):
        mid=first+(count-first)//2
        assign(first+1,2*(depth-step)+1)
        assign(mid,2*(depth-step))
        # The median of positions first+1, mid and last-1 is mid.
        assert values[first+1]>values[mid]>values.get(count-1,0)
        swap(first,mid)
        pivot=values[first];left=first+1;right=count
        while True:
            while values.get(left,0)>pivot:left+=1
            right-=1
            if pivot>values.get(right,0):
                right=max(pos for pos,value in values.items() if pos<=right and value>=pivot)
            if left>=right:break
            swap(left,right);left+=1
        assert left-first<=3
        first=left
    gains=array('i',[1])*count
    for i,value in assigned.items():gains[i]=value
    assert sum(gains)==n-1 and gains[0]==max(gains)
    return gains


def tree(case):
    n, kind = case['n'], case['shape']
    rng = random.Random(case.get('seed', 2026093001))
    parents = array('i', [-1])
    param = case.get('param', 0)
    if kind == 'chain':
        parents.extend(range(n - 1))
    elif kind == 'star':
        parents.extend([0] * (n - 1))
    elif kind == 'random':
        parents.extend(rng.randrange(v) for v in range(1, n))
    elif kind == 'comb':
        # Backbone with equally long teeth, including its final vertex.
        spine = max(2, n // (param + 1))
        parents.extend(range(spine - 1))
        for v in range(spine, n):
            parents.append((v - spine) // param if (v-spine) % param == 0 else v-1)
    elif kind == 'spider':
        # Unequal arms: the length variation avoids repeated power-of-two ranges.
        left = n-1
        for arm in range(param):
            length = left // (param-arm)
            if arm < param-1:
                length += rng.randrange(-max(1,length//3), max(1,length//3)+1)
                length = max(1, min(left-(param-arm-1), length))
            last = 0
            for _ in range(length):
                parents.append(last); last = len(parents)-1
            left -= length
        assert left == 0
    elif kind == 'subdivided-binary':
        # Every skeleton edge is a path with param edges.
        endpoints = array('i', [0])
        vertex = 1
        while len(parents) < n:
            last = endpoints[(vertex-1)//2]
            for _ in range(min(param,n-len(parents))):
                parents.append(last);last=len(parents)-1
            endpoints.append(last);vertex+=1
    elif kind == 'double-broom':
        spine = max(2,n//param)
        parents.extend(range(spine-1))
        parents.extend(0 if v%2 else spine-1 for v in range(spine,n))
    elif kind == 'recursive-comb':
        # Each component has a long central path and two recursive end pieces.
        todo=[(0,n-1)]
        while todo:
            root,count=todo.pop()
            if count == 0:continue
            length=max(1,count//param)
            last=root
            for _ in range(length):
                parents.append(last);last=len(parents)-1
            remainder=count-length
            todo.extend([(root,remainder//2),(last,remainder-remainder//2)])
    elif kind.startswith('gains-'):
        # A spider realizes any positive gain multiset with sum n-1.
        gains=[];left=n-1
        if kind=='gains-pivot-guards':
            gains=pivot_guard_gains(n);left=0
        elif kind=='gains-uniform':
            while left:
                g=min(left,rng.randrange(1,param+1));gains.append(g);left-=g
        elif kind=='gains-geometric':
            while left:
                g=1
                while g<param and rng.randrange(2):g+=1
                g=min(left,g);gains.append(g);left-=g
        elif kind=='gains-distinct':
            while left:
                g=min(left,len(gains)+1);gains.append(g);left-=g
        else:
            raise ValueError(kind)
        order=case.get('order','shuffle')
        if kind=='gains-pivot-guards':order='fixed'
        if order=='ascending':gains.sort()
        elif order=='descending':gains.sort(reverse=True)
        elif order=='organ':
            gains.sort();gains=gains[::2]+gains[1::2][::-1]
        elif order=='shuffle':rng.shuffle(gains)
        for g in gains:
            last=0
            for _ in range(g):parents.append(last);last=len(parents)-1
    else:
        raise ValueError(kind)
    assert len(parents)==n,(case,len(parents))
    assert all(0<=parents[v]<v for v in range(1,n))
    return parents,rng


def generate(case,path):
    parents,rng=tree(case);n=case['n'];slug=case['slug']
    labels=None
    if case.get('relabel'):
        labels=list(range(1,n));rng.shuffle(labels);labels.insert(0,0)
    def label(v):return v+1 if labels is None else labels[v]+1
    if slug!='forest-ranger':
        max_length=n if slug=='festival-plan' else n-1
        mode=case.get('window','full')
        if mode=='full':lo,hi=(1 if slug=='festival-plan' else 0),max_length
        elif mode=='half':lo,hi=1,max_length//2-3
        elif mode=='third':lo,hi=1,max_length//3-5
        elif mode=='dyadic':lo,hi=1,2**(max_length.bit_length()-2)-2
        elif mode=='middle':lo,hi=max_length//7,max_length*4//7
        else:raise ValueError(mode)
        assert 0<=lo<=hi<=max_length
        case['L'],case['R']=lo,hi
    with path.open('w',encoding='ascii',newline='\n') as out:
        out.write(f'{n}\n' if slug=='forest-ranger' else f'{n} {lo} {hi}\n')
        if slug!='forest-ranger':
            pattern=case.get('weights','random')
            weights=array('i',[0])*n
            for v in range(n):
                if pattern=='positive':w=1
                elif pattern=='alternating':w=1000 if v%2 else -1000
                elif pattern=='zero':w=0
                else:w=rng.randrange(-1000,1001)
                weights[v if labels is None else labels[v]]=w
            out.write(' '.join(map(str,weights))+'\n')
        for v in range(1,n):out.write(f'{label(parents[v])} {label(v)}\n')
    case['input_sha256']=bench.sha256(path)
    case['input_bytes']=path.stat().st_size


def candidates():
    result=[]
    for slug in ['festival-plan','grinder']:
        n=LIMITS[slug]
        shapes=[('chain',0),('comb',1),('comb',7),('comb',63),('comb',1023),
                ('spider',3),('spider',7),('spider',31),
                ('subdivided-binary',16),('subdivided-binary',256),('subdivided-binary',4096),
                ('double-broom',2),('double-broom',8),('recursive-comb',2),('recursive-comb',4)]
        for shape,param in shapes:
            result.append(dict(slug=slug,n=n,shape=shape,param=param,window='full',weights='random'))
        for window in ['half','third','dyadic','middle']:
            result.append(dict(slug=slug,n=n,shape='chain',window=window,weights='random'))
        for weight in ['zero','positive','alternating']:
            result.append(dict(slug=slug,n=n,shape='chain',window='full',weights=weight))
        for offset in [-3,-1,1]:
            result.append(dict(slug=slug,n=2**(n.bit_length()-1)+offset,shape='chain',window='full',weights='random'))
        for shape,param in [('chain',0),('comb',7),('subdivided-binary',256)]:
            result.append(dict(slug=slug,n=n,shape=shape,param=param,window='half',weights='random',relabel=True))
    slug='forest-ranger';n=LIMITS[slug]
    for shape,param in [('star',0),('gains-uniform',2),('gains-uniform',4),('gains-uniform',16),('gains-uniform',64),('gains-geometric',32),('gains-distinct',0)]:
        for order in (['shuffle'] if shape=='star' else ['shuffle','organ','ascending','descending']):
            result.append(dict(slug=slug,n=n,shape=shape,param=param,order=order))
    for i,c in enumerate(result):
        c['id']=f'screen-{i:02d}';c['seed']=2026093001
    return result


def programs():
    previous=json.loads((ROOT/'docs/benchmark-P1.json').read_text(encoding='utf-8'))
    progs={};provenance={}
    for slug in LIMITS:
        provenance[slug]={};progs[slug]={}
        for variant in ['std','alternative']:
            src=ROOT/'topics/trees'/slug/(variant+'.cpp')
            exe=ROOT/'build/bin'/(slug+('' if variant=='std' else '-alternative')+'.exe')
            assert bench.sha256(src)==previous['problems'][slug]['sources_sha256'][variant]
            assert bench.sha256(exe)==previous['problems'][slug]['binaries_sha256'][variant]
            progs[slug][variant]=exe
            provenance[slug][variant]={'source_sha256':bench.sha256(src),'binary_sha256':bench.sha256(exe)}
    return progs,provenance


def measure(case,path,progs,repeats,peak):
    variants={v:{'times_seconds':[]} for v in progs}
    output={v:OUT/(v+'.out') for v in progs}
    if peak:
        for v,exe in progs.items():
            variants[v]['peak_working_set_bytes']=bench.run_with_peak_memory(exe,path,output[v])
    for i in range(repeats):
        order=['std','alternative'] if (i+case.get('order_index',0))%2==0 else ['alternative','std']
        for v in order:variants[v]['times_seconds'].append(bench.run(progs[v],path,output[v]))
    for v in progs:
        variants[v]['output_sha256']=bench.sha256(output[v])
        variants[v]['median_seconds']=statistics.median(variants[v]['times_seconds'])
    assert variants['std']['output_sha256']==variants['alternative']['output_sha256'],case
    case['variants']=variants
    a=variants['std']['median_seconds'];b=variants['alternative']['median_seconds']
    case['ratio']=b/a
    print(case['id'],case['slug'],case['shape'],case.get('param',0),case['n'],case.get('window'),case.get('weights'),case.get('order'),f'{a:.6f} {b:.6f} ratio {b/a:.3f}',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['screen','confirm'],required=True)
    parser.add_argument('--cases',type=Path)
    parser.add_argument('--repeats',type=int,default=None)
    parser.add_argument('--output-name',default=None)
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True,parents=True)
    progs,provenance=programs()
    cases=candidates() if args.stage=='screen' else json.loads(args.cases.read_text(encoding='utf-8'))
    repeats=args.repeats or (1 if args.stage=='screen' else 7)
    report={'stage':args.stage,'repeats':repeats,'platform':platform.platform(),'python':platform.python_version(),
            'generator_sha256':bench.sha256(Path(__file__)),'programs':provenance,'flags':FLAGS,
            'formal_limits':LIMITS,'timing':'Sequential wall-clock processes, alternating variant order; output hashes checked.',
            'cases':[]}
    dest=OUT/((args.output_name or args.stage)+'.json')
    for i,case in enumerate(cases):
        case['order_index']=i
        path=OUT/'candidate.in'
        generate(case,path)
        measure(case,path,progs[case['slug']],repeats,args.stage=='confirm')
        report['cases'].append(case)
        dest.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Report:',dest,flush=True)


if __name__=='__main__':main()
