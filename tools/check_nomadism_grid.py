"""Exhaust all nonempty subsets of a 4-by-4 grid against dense Prim."""

import hashlib
import itertools
import json
import random
import subprocess

from check_r8 import ROOT, SLUGS, encode, executable


def main():
    points = list(itertools.product(range(-1,3),repeat=2))
    rng = random.Random(2026092809)
    inputs = []
    for mask in range(1,1<<len(points)):
        selected = [p for i,p in enumerate(points) if (mask>>i)&1]
        rng.shuffle(selected)
        inputs.append(encode(selected))
    data = b''.join(inputs)
    report = {'cases_per_problem':len(inputs),'input_sha256':hashlib.sha256(data).hexdigest()}
    for slug in SLUGS:
        fast = subprocess.run([str(executable(slug,'-mst'))],input=data,
                              capture_output=True,check=True,timeout=60)
        dense = subprocess.run([str(executable(slug,'-brute'))],input=data,
                               capture_output=True,check=True,timeout=60)
        actual = [int(line.split()[0]) for line in fast.stdout.splitlines()]
        expected = list(map(int,dense.stdout.split()))
        assert len(actual)==len(expected)==len(inputs)
        for i,(a,b) in enumerate(zip(actual,expected)):
            assert a==b,(slug,i,inputs[i],a,b)
        report[slug] = len(actual)
        print(f'{slug}: {len(actual)} exhaustive grid subsets passed',flush=True)
    (ROOT/'build/R8-grid-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
