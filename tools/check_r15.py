"""Independent models for R15; executables are built separately in build/bin."""
from pathlib import Path
import functools
import itertools
import json
import random
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = (
    ('number-theory','recursive-statistics'), ('data-structures','simple-merge'),
    ('data-structures','interval-top-half'), ('data-structures','interval-median'),
    ('graphs','technology-tree'), ('trees','binary-traversals'),
)

@functools.lru_cache(None)
def statistics_value(n):
    if n <= 0:
        return n
    return (n + sum(statistics_value(n // i) for i in range(2, n + 1))) % 998244353

def oracle(slug, text):
    tokens = iter(map(int, text.split()))
    n = next(tokens)
    if slug == 'recursive-statistics':
        return [statistics_value(next(tokens)) for _ in range(n)]
    if slug == 'simple-merge':
        m = next(tokens)
        values = []
        for _ in range(n):
            values.extend(next(tokens) for _ in range(next(tokens)))
        return sorted(values)[:m]
    if slug.startswith('interval-'):
        a = list(tokens)
        answers = []
        for length in range(1, n + 1):
            for l in range(n - length + 1):
                ordered = sorted(a[l:l + length])
                if slug == 'interval-top-half':
                    answers.append(sum(ordered[length // 2:]))
                else:
                    answers.append(ordered[(length - 1) // 2] + ordered[length // 2])
        return answers
    if slug == 'technology-tree':
        m = next(tokens)
        duration = [next(tokens) for _ in range(n)]
        depends = [set() for _ in range(n)]
        for _ in range(m):
            u, v = next(tokens) - 1, next(tokens) - 1
            depends[u].add(v)
        # Event simulation: start every available job, then advance to the next finish.
        done = {u for u in range(n) if duration[u] == -1}
        pending = set(range(n)) - done
        running = {}
        now = 0
        while pending or running:
            for u in list(pending):
                if depends[u] <= done:
                    running[u] = now + duration[u]
                    pending.remove(u)
            if not running:
                return 'bad idea'
            now = min(running.values())
            for u in list(running):
                if running[u] == now:
                    done.add(u)
                    del running[u]
        return [now]
    raise ValueError(slug)

def run(slug, text, suffix=''):
    value = subprocess.check_output([str(ROOT/'build/bin'/f'{slug}{suffix}.exe')],input=text.encode(),timeout=20).decode().strip()
    return value if value == 'bad idea' else list(map(int,value.split()))

def make_tree(left, right, labels):
    pre, ino, post = [], [], []
    def visit(u):
        if u == -1:
            return
        pre.append(labels[u])
        visit(left[u])
        ino.append(labels[u])
        visit(right[u])
        post.append(labels[u])
    visit(0)
    return f'{len(labels)}\n'+' '.join(map(str,pre))+'\n'+' '.join(map(str,ino))+'\n',post

def main():
    rng = random.Random(2026093015)
    counts = {s:0 for _,s in PROBLEMS}
    originals = {s:0 for _,s in PROBLEMS}
    def check(slug, text, expected=None):
        expected = oracle(slug,text) if expected is None else expected
        for suffix in ['', '-alternative']:
            actual = run(slug,text,suffix)
            assert actual == expected, (slug,suffix,text,actual,expected)
        if counts[slug] < 100:
            assert run(slug,text,'-original') == expected,(slug,'original',text)
            originals[slug] += 1
        counts[slug] += 1
    check('recursive-statistics','0\n')
    check('recursive-statistics','1003\n'+'\n'.join(map(str,[-1000000000,-1,0,*range(1,1001)]))+'\n')
    for _ in range(100):
        values = [rng.randrange(-100,501) for _ in range(rng.randrange(1,101))]
        check('recursive-statistics',f'{len(values)}\n'+'\n'.join(map(str,values))+'\n')
    for _ in range(300):
        k = rng.randrange(1,32)
        rows = []
        total = 0
        for _ in range(k):
            values = sorted(rng.choices([-1000000000,-9,-1,0,1,9,1000000000],k=rng.randrange(1,16)))
            if rng.randrange(2): values.reverse()
            total += len(values)
            rows.append(' '.join(map(str,[len(values),*values])))
        m = rng.choice([0,total,rng.randrange(total+1)])
        check('simple-merge',f'{k} {m}\n'+'\n'.join(rows)+'\n')
    for n in range(1,7):
        for values in itertools.product([-2,0,3], repeat=n):
            text = f'{n}\n'+' '.join(map(str,values))+'\n'
            for slug in ['interval-top-half','interval-median']:
                check(slug,text)
    for _ in range(100):
        values = [rng.randrange(-1000000000,1000000001) for _ in range(rng.randrange(1,61))]
        text = f'{len(values)}\n'+' '.join(map(str,values))+'\n'
        for slug in ['interval-top-half','interval-median']:
            check(slug,text)
    for mask in range(1 << 9):
        edges = [(u+1,v+1) for u in range(3) for v in range(3) if mask & (1 << (3*u+v))]
        duration = [rng.choice([-1,0,2,5]) for _ in range(3)]
        text = f'3 {len(edges)}\n'+' '.join(map(str,duration))+'\n'+''.join(f'{u} {v}\n' for u,v in edges)
        check('technology-tree',text)
    for _ in range(200):
        n = rng.randrange(1,15)
        duration = [rng.choice([-1,0,1,1000000000]) for _ in range(n)]
        edges = [(rng.randrange(1,n+1),rng.randrange(1,n+1)) for _ in range(rng.randrange(n*n+1))]
        check('technology-tree',f'{n} {len(edges)}\n'+' '.join(map(str,duration))+'\n'+''.join(f'{u} {v}\n' for u,v in edges))
    for n in range(1,81):
        for mode in ['left','right','zigzag','balanced','random']:
            left, right = [-1]*n, [-1]*n
            slots = [(0,0),(0,1)]
            for i in range(1,n):
                if mode == 'balanced': parent, side = (i-1)//2, (i-1)%2
                elif mode == 'random':
                    at = rng.randrange(len(slots))
                    parent, side = slots.pop(at)
                    slots.extend([(i,0),(i,1)])
                else: parent, side = i-1, int(mode=='right' or mode=='zigzag' and i%2==0)
                (left if side==0 else right)[parent]=i
            labels = list(range(1,n+1))
            rng.shuffle(labels)
            text, expected = make_tree(left,right,labels)
            check('binary-traversals',text,expected)
    report = dict(seed=2026093015,cases=counts,original_comparisons=originals,total=sum(counts.values()))
    (ROOT/'build/R15-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__ == '__main__':
    main()
