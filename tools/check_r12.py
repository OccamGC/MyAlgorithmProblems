"""Independent direct models for R12; binaries must already exist in build/bin."""
import collections
import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (
    ('number-theory', 'factorial-recovery'),
    ('trees', 'dynamic-directory'),
    ('data-structures', 'gran-forest'),
    ('data-structures', 'crystal-list'),
    ('data-structures', 'contract-summoning'),
    ('data-structures', 'canister-sequence'),
)
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def path(graph, start, finish):
    parent = {start: None}
    queue = [start]
    for v in queue:
        if v == finish:
            break
        for u in graph[v]:
            if u not in parent:
                parent[u] = v
                queue.append(u)
    answer = []
    while finish is not None:
        answer.append(finish)
        finish = parent[finish]
    return answer[::-1]


def oracle(slug, data):
    values = iter(map(int, data.split()))
    answer = []
    if slug == 'factorial-recovery':
        return [str(math.factorial(next(values)))]
    n = next(values)
    if slug == 'dynamic-directory':
        m = next(values)
        graph = [dict() for _ in range(n+1)]
        for _ in range(n-1):
            a, b, w = (next(values) for _ in range(3))
            graph[a][b] = graph[b][a] = w
        root = 1
        for _ in range(m):
            op = next(values)
            if op == 2:
                root = next(values)
            elif op == 4:
                k = next(values)
                nodes = [next(values) for _ in range(k)]
                common = path(graph, root, nodes[0])
                for a in nodes[1:]:
                    other = path(graph, root, a)
                    length = 0
                    while length < min(len(common), len(other)) and common[length] == other[length]:
                        length += 1
                    common = common[:length]
                answer.append(sum(graph[a][b] for a, b in zip(common, common[1:])))
            else:
                a, b, w = (next(values) for _ in range(3))
                if op == 3:
                    if b in graph[a]:
                        graph[a][b] = graph[b][a] = w
                else:
                    if a not in path(graph, root, b):
                        parent = path(graph, root, a)[-2]
                        del graph[parent][a]
                        del graph[a][parent]
                        graph[a][b] = graph[b][a] = w
    elif slug == 'gran-forest':
        m, q = next(values), next(values)
        weight = [0] + [next(values) for _ in range(n)]
        graph = [[] for _ in range(n+1)]
        for _ in range(m):
            a, b = next(values), next(values)
            graph[a].append(b)
            graph[b].append(a)
        for _ in range(q):
            op, a, b, c = (next(values) for _ in range(4))
            nodes = path(graph, a, b)
            if op <= 2:
                for v in nodes:
                    weight[v] = weight[v] + c if op == 1 else c
            else:
                selected = [weight[v] for v in nodes if weight[v] >= c]
                answer.append(len(selected) if op == 3 else sum(selected))
    elif slug == 'crystal-list':
        k, m = next(values), next(values)
        colors = [next(values) for _ in range(n)]
        energy = [0] + [next(values) for _ in range(k)]
        for _ in range(m):
            op = next(values)
            if op == 1:
                c, e = next(values), next(values)
                energy[c] = e
            else:
                l, r, c = next(values), next(values), next(values)
                answer.append(sum(abs(energy[x]-energy[c]) for x in colors[l-1:r]))
                colors[l-1:r] = [c]*(r-l+1)
    elif slug == 'contract-summoning':
        initial = tuple(next(values) for _ in range(3))
        chars = [tuple(next(values) for _ in range(6)) for _ in range(n)]
        queue = [initial]
        seen = set()
        for attr in queue:
            for i, char in enumerate(chars):
                if i not in seen and all(attr[d] >= char[d] for d in range(3)):
                    seen.add(i)
                    queue.append(char[3:])
        answer.append(len(seen))
    elif slug == 'canister-sequence':
        m = next(values)
        colors = [next(values) for _ in range(n)]
        for _ in range(m):
            op, l, r = next(values), next(values), next(values)
            if op == 1:
                colors[l-1:r] = [next(values)]*(r-l+1)
            elif op == 2:
                colors[l-1:r] = reversed(colors[l-1:r])
            elif op == 3:
                pos = next(values)-1
                segment = colors[l-1:l-1+r]
                del colors[l-1:l-1+r]
                colors[pos:pos] = segment
            else:
                segment = colors[l-1:r]
                answer.append(1+sum(a != b for a, b in zip(segment, segment[1:])))
    else:
        raise ValueError(slug)
    assert next(values, None) is None
    return list(map(str, answer))


def compare(slug, data):
    binary = ROOT/'build/bin'/(slug+('.exe' if os.name == 'nt' else ''))
    expected = oracle(slug, data)
    result = subprocess.run([str(binary)], input=data, text=True, capture_output=True, check=True, timeout=15)
    if result.stdout.split() != expected:
        target = ROOT/'build'/f'R12-failure-{slug}.in'
        target.write_text(data, encoding='ascii')
        raise AssertionError((slug, str(target), expected[:30], result.stdout.split()[:30]))


def random_case(slug, rng, index):
    n = rng.randint(2, 36)
    m = 100
    if slug == 'factorial-recovery':
        n = index if index < 180 else rng.randrange(3000)
        fact = str(math.factorial(n))
        k = rng.randint(max(0,len(fact)-15),len(fact))
        return f'{n} {k}\n'+(fact[-k:] if k else '')+'\n'
    if slug == 'dynamic-directory':
        lines = [f'{n} {m}']
        for v in range(2,n+1):
            lines.append(f'{rng.randrange(1,v)} {v} {rng.randint(-10000,10000)}')
        for i in range(m):
            op = rng.randrange(1,5)
            a, b = rng.randint(1,n), rng.randint(1,n)
            if op == 2:
                lines.append(f'2 {a}')
            elif op == 4:
                subset = rng.sample(range(1,n+1),rng.randint(1,n))
                lines.append('4 '+str(len(subset))+' '+' '.join(map(str,subset)))
            else:
                lines.append(f'{op} {a} {b} {rng.randint(-10000,10000)}')
    elif slug == 'gran-forest':
        if index % 17 == 0:
            n = 1500
        graph = [[] for _ in range(n+1)]
        edges = []
        for v in range(2,n+1):
            if index % 17 == 0 or rng.random() < .92:
                u = v-1 if index % 17 == 0 else rng.randrange(1,v)
                edges.append((u,v))
                graph[u].append(v)
                graph[v].append(u)
        components = []
        seen = set()
        for v in range(1,n+1):
            if v in seen:
                continue
            c = [v]
            seen.add(v)
            for a in c:
                for b in graph[a]:
                    if b not in seen:
                        seen.add(b)
                        c.append(b)
            components.append(c)
        lines = [f'{n} {len(edges)} {m}', ' '.join(str(rng.randint(-10000,10000)) for _ in range(n))]
        lines += [f'{a} {b}' for a,b in edges]
        for _ in range(m):
            c = rng.choice(components)
            lines.append(f'{rng.randint(1,4)} {rng.choice(c)} {rng.choice(c)} {rng.randint(-10000,10000)}')
    elif slug == 'crystal-list':
        k = rng.randint(1,20)
        n = 0 if index % 20 == 0 else n
        lines = [f'{n} {k} {m}', ' '.join(str(rng.randint(1,k)) for _ in range(n)),
                 ' '.join(str(rng.randint(1,50000)) for _ in range(k))]
        for _ in range(m):
            if not n or rng.random() < .3:
                lines.append(f'1 {rng.randint(1,k)} {rng.randint(1,50000)}')
            else:
                l,r = sorted([rng.randint(1,n),rng.randint(1,n)])
                lines.append(f'0 {l} {r} {rng.randint(1,k)}')
    elif slug == 'contract-summoning':
        n = rng.randint(1,70)
        initial = [rng.randrange(8) for _ in range(3)]
        lines = [str(n)+' '+' '.join(map(str,initial))]
        for _ in range(n):
            lines.append(' '.join(str(rng.randrange(11)) for _ in range(6)))
    else:
        lines = [f'{n} {m}', ' '.join(str(rng.randint(1,5)) for _ in range(n))]
        for _ in range(m):
            op = rng.randint(1,4)
            l,r = sorted([rng.randint(1,n),rng.randint(1,n)])
            if op == 3:
                length = r-l+1
                lines.append(f'3 {l} {length} {rng.randint(1,n-length+1)}')
            elif op == 1:
                lines.append(f'1 {l} {r} {rng.randint(1,5)}')
            else:
                lines.append(f'{op} {l} {r}')
    return '\n'.join(lines)+'\n'


def targeted_checks():
    counts = {slug:0 for _,slug in PROBLEMS}
    rng = random.Random(2026093012)
    for index in range(16):
        n=2021
        initial=[rng.randint(-10000,10000) for _ in range(n)]
        operations=['1 1 2021 10000','2 1 2021 -10','1 1 2021 7',
                    '3 1 2021 -3','4 1 2021 -3','2 43 90 8','1 44 88 -20',
                    '4 1 2021 -100000000','3 1 2021 8']
        for _ in range(60):
            l,r=sorted([rng.randint(1,n),rng.randint(1,n)])
            operations.append(f'{rng.randint(1,4)} {l} {r} {rng.randint(-10000,10000)}')
        data=f'{n} {n-1} {len(operations)}\n'+' '.join(map(str,initial))+'\n'
        data+=''.join(f'{i} {i+1}\n' for i in range(1,n))+'\n'.join(operations)+'\n'
        compare('gran-forest',data)
        counts['gran-forest']+=1
    for n in range(26):
        value=str(math.factorial(n))
        for k in range(max(0,len(value)-15),len(value)+1):
            compare('factorial-recovery',f'{n} {k}\n'+(value[-k:] if k else '')+'\n')
            counts['factorial-recovery']+=1
    n=200000
    data=f'{n} 7\n'+''.join(f'{i} {i+1} -10000\n' for i in range(1,n))
    data+=f'4 1 {n}\n2 {n}\n4 1 1\n1 1 {n} 7\n4 1 1\n3 1 {n} -10000\n4 2 1 2\n'
    compare('dynamic-directory',data);counts['dynamic-directory']+=1
    n=500000
    data=f'{n} 2 3\n'+' '.join(['1']*n)+f'\n1 50000\n0 1 {n} 2\n1 2 1\n0 1 {n} 1\n'
    compare('crystal-list',data);counts['crystal-list']+=1
    for p in (1000000007,1000000009):
        assert all(p%d for d in range(2,math.isqrt(p)+1))
    return counts


def main():
    counts = {}
    for number, (topic, slug) in enumerate(PROBLEMS):
        rng = random.Random(2026093000+number)
        samples = sorted((ROOT/'topics'/topic/slug/'tests/samples').glob('*.in'))
        for sample in samples:
            data = sample.read_text(encoding='ascii')
            assert oracle(slug,data) == sample.with_suffix('.out').read_text(encoding='ascii').split(), sample
            compare(slug,data)
        rounds = 420 if slug == 'factorial-recovery' else 520
        for index in range(rounds):
            compare(slug,random_case(slug,rng,index))
        counts[slug] = {'random_cases': rounds, 'samples': len(samples), 'seed':2026093000+number}
        print(f'{slug}: {rounds} differential cases and {len(samples)} samples passed', flush=True)
    targeted=targeted_checks()
    for slug,count in targeted.items():
        counts[slug]['targeted_cases']=count
    print('Additional targeted cases:',sum(targeted.values()),flush=True)
    (ROOT/'build/R12-checks.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
