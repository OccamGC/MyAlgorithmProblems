"""Independent small-instance models for the six R13 reference programs."""
import itertools
import json
import math
import os
from pathlib import Path
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (
    ('data-structures', 'catalyst-sequence'),
    ('number-theory', 'equipment-amplification'),
    ('graphs', 'spode-seminary'),
    ('combinatorics', 'grox-sequence-2'),
    ('number-theory', 'grox-sequence-3'),
    ('trees', 'hagen-farm'),
)


def oracle(slug, text):
    data = iter(map(int, text.split()))
    if slug == 'catalyst-sequence':
        n = next(data)
        a = list(data)
        answer = [0] * max(a)
        for l in range(n):
            for r in range(l + 1, n):
                gap = min(abs(a[i]-a[j]) for i in range(l, r+1) for j in range(i+1, r+1))
                answer[gap] = max(answer[gap], r-l+1)
        return answer
    if slug == 'equipment-amplification':
        next(data)
        result = []
        for bound in data:
            assert bound <= 200000, 'direct integer oracle is deliberately small'
            count = 0
            for value in range(bound+1):
                digits = list(map(int, str(value)[::-1]))
                count += all(((value >> i) & 1) >= digit for i, digit in enumerate(digits))
            result.append(count)
        return result
    if slug == 'grox-sequence-2':
        n = next(data)
        mod = 1004535809
        inv = [pow(math.factorial(i), -1, mod) for i in range(n+1)]
        answer = [0, 0, 0]
        for i in range(n+1):
            for j in range(n-i+1):
                answer[(i-j) % 3] += inv[i]*inv[j]
        return [v % mod for v in answer]
    if slug == 'grox-sequence-3':
        n, q = next(data), next(data)
        answer = []
        for _ in range(q):
            a, b = next(data), next(data)
            value = sum(math.factorial(i+b-a)*math.prod(range(a, i+1)) for i in range(a, min(n, n+a-b)+1))
            answer.append(value % 921260340)
        return answer
    if slug == 'spode-seminary':
        n, m, q = next(data), next(data), next(data)
        satisfaction = [next(data) for _ in range(n)]
        capacity = [next(data) for _ in range(m)]
        preference = [[next(data) for _ in range(m)] for _ in range(n)]
        rankings = [[next(data)-1 for _ in range(n)] for _ in range(q)]
        choices = [[-1]+[j for j in range(m) if preference[i][j] != -1] for i in range(n)]
        feasible = []
        for assignment in itertools.product(*choices):
            if all(assignment.count(j) <= capacity[j] for j in range(m)):
                feasible.append(tuple(m+1 if j == -1 else preference[i][j] for i, j in enumerate(assignment)))

        def admission(order):
            return min(feasible, key=lambda tiers: tuple(tiers[i] for i in order))

        answer = []
        for order in rankings:
            best = admission(order)
            answer.extend(-1 if v == m+1 else v for v in best)
            promotion = [-1]*n
            for position, student in enumerate(order):
                for change in range(position+1):
                    new = order[:]
                    new.pop(position)
                    new.insert(position-change, student)
                    if admission(new)[student] <= satisfaction[student]:
                        promotion[student] = change
                        break
            answer.extend(promotion)
        return answer
    if slug == 'hagen-farm':
        n = next(data)
        graph = [[] for _ in range(n)]
        for _ in range(n-1):
            a, b, w = next(data)-1, next(data)-1, next(data)
            graph[a].append((b, w))
            graph[b].append((a, w))
        parent = [-1]*n
        order = [0]
        weight = [0]*n
        for v in order:
            for u, w in graph[v]:
                if u != parent[v]:
                    parent[u] = v
                    weight[u] = w
                    order.append(u)
        sub = [{i} for i in range(n)]
        for v in order[:0:-1]:
            sub[parent[v]].update(sub[v])
        mod = 1000000007
        answer = 0
        for nodes in sub:
            size = len(nodes)
            for k in range(1, size+1):
                subtotal = 0
                for chosen in itertools.combinations(nodes, k):
                    chosen = set(chosen)
                    subtotal += 2*sum(weight[v] for v in range(1, n) if 0 < len(chosen & sub[v]) < k)
                answer += subtotal * pow(size*math.comb(size,k), -1, mod)
        return [answer*pow(n,-1,mod) % mod]
    raise ValueError(slug)


def run(slug, text):
    binary = ROOT/'build/bin'/(slug + ('.exe' if os.name == 'nt' else ''))
    return list(map(int, subprocess.check_output([str(binary)],input=text.encode('ascii'),timeout=30).split()))


def random_case(slug, rng):
    if slug == 'catalyst-sequence':
        n = rng.randint(1, 22)
        upper = rng.choice([1, 8, 70, 250000])
        return f'{n}\n'+ ' '.join(str(rng.randint(1,upper)) for _ in range(n))+'\n'
    if slug == 'equipment-amplification':
        return f'1\n{rng.randrange(3000)}\n'
    if slug == 'grox-sequence-2':
        return f'{rng.randrange(110)}\n'
    if slug == 'grox-sequence-3':
        n = rng.randrange(40)
        return f'{n} 12\n'+''.join(f'{rng.randrange(45)} {rng.randrange(45)}\n' for _ in range(12))
    if slug == 'spode-seminary':
        n, m = rng.randint(1,5), rng.randint(1,4)
        lines = [f'{n} {m} 2',' '.join(str(rng.randrange(m+1)) for _ in range(n)), ' '.join(str(rng.randrange(3)) for _ in range(m))]
        for _ in range(n):
            row = [rng.choice([-1,*range(1,m+1)]) for _ in range(m)]
            if len(set(row)) == 1 and row[0] != -1 and m == 4:
                row[0] = -1
            lines.append(' '.join(map(str,row)))
        for _ in range(2):
            ranking = list(range(1,n+1)); rng.shuffle(ranking)
            lines.append(' '.join(map(str,ranking)))
        return '\n'.join(lines)+'\n'
    n = rng.randint(1,9)
    return f'{n}\n'+''.join(f'{rng.randrange(1,v)} {v} {rng.randrange(10)}\n' for v in range(2,n+1))


def main():
    report = {}
    counts = [400, 350, 220, 180, 400, 320]
    for index, (topic, slug) in enumerate(PROBLEMS):
        rng = random.Random(2026093013+index)
        samples = 0
        for file in sorted((ROOT/'topics'/topic/slug/'tests/samples').glob('*.in')):
            text = file.read_text(encoding='ascii')
            expected = list(map(int,file.with_suffix('.out').read_text().split()))
            assert run(slug,text) == expected, (slug,file)
            if slug != 'equipment-amplification' or max(map(int,text.split()[1:])) <= 200000:
                assert oracle(slug,text) == expected, (slug,file,'oracle')
            samples += 1
        for trial in range(counts[index]):
            text = random_case(slug,rng)
            expected = oracle(slug,text)
            actual = run(slug,text)
            assert actual == expected, (slug,trial,text,actual,expected)
        report[slug] = {'seed':2026093013+index,'random_cases':counts[index],'samples':samples}
        print(slug,report[slug],flush=True)
    (ROOT/'build/R13-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
