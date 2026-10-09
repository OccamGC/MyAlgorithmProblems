"""Input, sample and construction validation for the nomadism pair."""

import os
from pathlib import Path
import subprocess

from check_r8 import dense_mst, tour_cost

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (('geometry', 'nomadism-day'), ('geometry', 'nomadism-night'))
GROUP_SHARES = {slug:(100,) for _,slug in PROBLEMS}


def validate(path):
    with path.open('r',encoding='ascii') as stream:
        first = stream.readline().split()
        assert len(first) == 1
        n = int(first[0])
        assert 1 <= n <= 400000
        for _ in range(n):
            values = list(map(int,stream.readline().split()))
            assert len(values) == 2 and all(-10000 <= x <= 10000 for x in values)
        assert not stream.read().strip()
    return {'n':n}


VALIDATORS = {slug:validate for _,slug in PROBLEMS}


def read_points(path):
    values = list(map(int,path.read_bytes().split()))
    assert len(values) == 2*values[0]+1
    return list(zip(values[1::2],values[2::2]))


def validate_group(slug,spec,dimensions):
    assert spec['group'] == 1
    if 'n' in spec:
        assert dimensions['n'] == spec['n']


def binary(slug,suffix):
    return ROOT/'build/bin'/(slug+suffix+('.exe' if os.name=='nt' else ''))


def check_sample(path,slug,actual,expected):
    points = read_points(path)
    weight = dense_mst(points,slug)
    assert tour_cost(points,actual,slug) <= 2*weight
    assert 1000*tour_cost(points,expected,slug) <= 2001*weight+1


def check_output(slug,path,dimensions):
    source = path.with_suffix('.in')
    points = read_points(source)
    cost = tour_cost(points,path.read_bytes().split(),slug)
    with source.open('rb') as stream:
        result = subprocess.run([str(binary(slug,'-mst'))],stdin=stream,
                                capture_output=True,check=True,timeout=60)
    weight = int(result.stdout.split()[0])
    assert cost <= 2*weight,(slug,path,cost,weight)
    known = {'all-coincident':0,'maximum-grid':9607960,'narrow-strip':399999,
             'horizontal-line':20000,'vertical-line':20000,'diagonal-line':40000,
             'anti-diagonal':40000,'square-boundary':79999,'two-columns':60000,
             'many-equal-x':418980}
    if path.stem in known:
        assert weight == known[path.stem],(slug,path,weight,known[path.stem])
    elif path.stem == 'cocircular':
        assert weight == dense_mst(list(set(points)),slug)
    elif dimensions['n'] <= 3000:
        with source.open('rb') as stream:
            result = subprocess.run([str(binary(slug,'-brute'))],stdin=stream,
                                    capture_output=True,check=True,timeout=60)
        assert weight == int(result.stdout),(slug,path,'dense oracle')
    result = subprocess.run([str(binary(slug,'-checker')),str(source),str(path),str(path)],
                            capture_output=True,timeout=60)
    assert result.returncode == 0,(slug,path,result.stderr)
