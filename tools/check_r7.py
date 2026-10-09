"""Independent small-instance checks for the eight R7 problems."""
import itertools
import json
import math
import os
import random
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = {
    'century-bomber': 'optimization', 'psychic-control-tree': 'trees',
    'gene-mutation': 'dynamic-programming', 'rhino-tank': 'combinatorics',
    'redstone-clock': 'number-theory', 'torch-light': 'data-structures',
    'redstone-computer': 'graphs', 'wheat-field': 'geometry',
}
MOD = 1000000007

def run(slug, data):
    program = ROOT / 'build/bin' / (slug + ('.exe' if os.name == 'nt' else ''))
    result = subprocess.run([str(program)], input=data.encode(), capture_output=True, check=True, timeout=30)
    return result.stdout.decode().split()

def century_oracle(a, positions, queries, m):
    answer = [0] * m
    for l, r in queries:
        for p in positions:
            for j in range(r-l+1):
                if p+j < m:
                    answer[p+j] += a[l+j]
    return answer

def tree_oracle(values, control, edges):
    n = len(values)
    graph = [[] for _ in values]
    for u,v in edges:
        graph[u].append(v); graph[v].append(u)
    parent = [-1] * n
    order = [0]
    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u; order.append(v)
    subtree = [{u} for u in range(n)]
    for u in reversed(order[1:]):
        subtree[parent[u]].update(subtree[u])
    result = []
    for nodes in subtree:
        targets = {control[u] for u in nodes}
        start = next(iter(targets))
        previous = [-1] * n
        previous[start] = start
        queue = [start]
        for u in queue:
            for v in graph[u]:
                if previous[v] == -1:
                    previous[v] = u; queue.append(v)
        used = {start}
        for v in targets:
            while v != start:
                used.add(v); v = previous[v]
        result.append(sum(values[v] for v in used-targets))
    return result

def digits(value, base):
    result = []
    while value:
        result.append(value % base); value //= base
    return result[::-1] or [0]

def evaluated(digit_list, base):
    result = 0
    for digit in digit_list:
        result = result * base + digit
    return result

def gene_oracle(n, m, a, b):
    target = evaluated(a,m)
    return sum(evaluated(digits(x,n),m) > target for x in range(evaluated(b,n)+1)) % MOD

def rhino_oracle(n, m, weights):
    numerator = 0
    denominator = math.prod(map(sum,weights))
    for colors in itertools.product(range(m), repeat=n*n):
        if any(len(set(colors[i*n:(i+1)*n])) == 1 for i in range(n)):
            continue
        if any(len({colors[i*n+j] for i in range(n)}) == 1 for j in range(n)):
            continue
        numerator += math.prod(weights[i][c] for i,c in enumerate(colors))
    return numerator % MOD * pow(denominator % MOD, MOD-2, MOD) % MOD

def clock_oracle(n, a):
    answer = [0,0]
    for i in range(1,n+1):
        for parity in range(2):
            # Search multiples of a, independently of Euclid's algorithm.
            multiple = a
            while multiple % i:
                multiple += a
            answer[parity] ^= multiple
            a = ((a+10007) if parity == 0 else (a*a+1)) % 10000000 + 1
    return answer

def torch_oracle(n,m,lights,thresholds):
    result = 0
    for x in range(n):
        for y in range(m):
            total = sum(light for i in range(n) for j in range(m)
                        for light,radius in [lights[i*m+j]] if abs(x-i)+abs(y-j)<radius)
            result += total <= thresholds[x*m+y]
    return result

def bit_operation(a,op,b):
    return a^b if op == '^' else a&b if op == '&' else a|b

def computer_possible(n,k,constraints):
    for bit in range(k):
        if not any(all(bit_operation((mask>>a)&1, op, (mask>>b)&1) == int(c[bit])
                       for a,op,b,c in constraints) for mask in range(1<<n)):
            return False
    return True

def valid_computer_output(n,k,constraints,tokens,possible):
    if tokens == ['No']:
        return not possible
    if not possible or len(tokens) != n:
        return False
    if any(len(x) != k or set(x)-set('01') for x in tokens):
        return False
    return all(bit_operation(int(tokens[a],2),op,int(tokens[b],2)) == int(c,2)
               for a,op,b,c in constraints)

def wheat_oracle(n,m,buildings):
    result = 0
    for side in range(1,min(n,m)+1):
        for x in range(n-side+1):
            for y in range(m-side+1):
                if not any(x<=a<x+side and y<=b<y+side for a,b in buildings):
                    result = side
    return result

def check_checker():
    checker=ROOT/'build/bin'/('redstone-checker.exe' if os.name=='nt' else 'redstone-checker')
    cases=[('2 2 2\n1 | 2 11\n1 & 2 00\n','00\n11\n',candidate,code)
           for candidate,code in [('11\n00\n',0),('01\n10\n',0),('00\n00\n',1),
                                  ('00\n1\n',1),('00\n12\n',1),('00\n11\n0\n',1),('No\n',1),('',1)]]
    cases += [('1 1 1\n1 ^ 1 1\n','No\n',candidate,code)
              for candidate,code in [('No\n',0),('Exist\n',1),('No extra\n',1),('0\n',1)]]
    cases += [('0 0 150\n','',candidate,code) for candidate,code in [('',0),('0',1),('No',1)]]
    with tempfile.TemporaryDirectory(dir=ROOT/'build') as folder:
        directory=Path(folder)
        for source,answer,candidate,code in cases:
            paths=[directory/name for name in ('input','answer','candidate')]
            for path,content in zip(paths,(source,answer,candidate)):
                path.write_text(content,encoding='ascii')
            result=subprocess.run([str(checker),*map(str,paths)],check=False)
            assert result.returncode==code,(source,candidate,result.returncode)
    return len(cases)

def main():
    counts = {}
    rng = random.Random(2026092807)
    for slug in PROBLEMS:
        count = 0
        rounds = 100 if slug == 'rhino-tank' else 240
        for iteration in range(rounds):
            if slug == 'century-bomber':
                n,m = rng.randint(1,10),rng.randint(1,12)
                a = [rng.randrange(10) for _ in range(n)]
                positions = rng.sample(range(m),rng.randrange(m+1))
                queries = [sorted([rng.randrange(n),rng.randrange(n)]) for _ in range(rng.randrange(20))]
                data = f'{n} {m} {len(positions)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+' '.join(str(p+1) for p in positions)+'\n'+''.join(f'{l+1} {r+1}\n' for l,r in queries)
                expected = century_oracle(a,positions,queries,m)
            elif slug == 'psychic-control-tree':
                n = rng.randint(1,35)
                values = [rng.randint(1,5000) for _ in range(n)]
                control = list(range(n)); rng.shuffle(control)
                edges = [(rng.randrange(v),v) for v in range(1,n)]
                rng.shuffle(edges)
                data = f'{n}\n'+''.join(f'{a} {b+1}\n' for a,b in zip(values,control))+''.join(f'{a+1} {b+1}\n' for a,b in edges)
                expected = tree_oracle(values,control,edges)
            elif slug == 'gene-mutation':
                n,m = rng.randint(2,30),rng.randint(2,30)
                a = digits(rng.randrange(10000),n)
                b = digits(rng.randrange(5000),n)
                data = f'{n} {m} {len(a)} {len(b)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'
                expected = [gene_oracle(n,m,a,b)]
            elif slug == 'rhino-tank':
                n = rng.randint(1,3)
                m = rng.randint(1,3)
                weights = [[rng.randrange(5) for _ in range(m)] for _ in range(n*n)]
                for row in weights:
                    if not any(row): row[0]=1
                data = f'{n} {m}\n'+''.join(' '.join(map(str,row))+'\n' for row in weights)
                expected = [rhino_oracle(n,m,weights)]
            elif slug == 'redstone-clock':
                n,a = rng.randint(1,100),rng.randint(1,10000000)
                data = f'{n} {a}\n'
                expected = clock_oracle(n,a)
            elif slug == 'torch-light':
                n,m = rng.randint(1,10),rng.randint(1,10)
                lights = [(rng.randint(-100000000,100000000),rng.randint(0,n+m+2)) for _ in range(n*m)]
                thresholds = [rng.choice([-10**15,10**15,rng.randrange(-10**9,10**9)]) for _ in lights]
                data = f'{n} {m}\n'+''.join(f'{a} {b}\n' for a,b in lights)+' '.join(map(str,thresholds))+'\n'
                expected = [torch_oracle(n,m,lights,thresholds)]
            elif slug == 'redstone-computer':
                n,k = rng.randint(0,7),rng.randint(1,5)
                solution = [rng.randrange(1<<k) for _ in range(n)]
                constraints = []
                for _ in range(rng.randrange(25) if n else 0):
                    a,b = rng.randrange(n),rng.randrange(n)
                    op = rng.choice('^&|')
                    c = bit_operation(solution[a],op,solution[b]) if iteration % 2 else rng.randrange(1<<k)
                    constraints.append((a,op,b,format(c,f'0{k}b')))
                data = f'{n} {len(constraints)} {k}\n'+''.join(f'{a+1} {op} {b+1} {c}\n' for a,op,b,c in constraints)
                possible = computer_possible(n,k,constraints)
                assert valid_computer_output(n,k,constraints,run(slug,data),possible),data
                count += 1
                continue
            else:
                n,m = rng.randint(1,9),rng.randint(1,9)
                buildings = [(rng.randrange(n),rng.randrange(m)) for _ in range(rng.randrange(25))]
                data = f'{n} {m} {len(buildings)}\n'+''.join(f'{a+1} {b+1}\n' for a,b in buildings)
                expected = [wheat_oracle(n,m,buildings)]
            assert list(map(int,run(slug,data))) == expected,(slug,data,expected)
            count += 1
        counts[slug] = count
        print(f'{slug}: {count} independent comparisons passed',flush=True)
    counts['checker']=check_checker()
    print(f"checker: {counts['checker']} acceptance/rejection cases passed",flush=True)
    (ROOT/'build/R7-checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
