"""Input and output checks for the resolved analysis problems."""
from pathlib import Path
MOD=998244353

def validate(slug,path):
    with Path(path).open(encoding='ascii') as stream:
        n=int(stream.readline())
        if slug=='power-call-count':
            assert 0<=n<=2100000
            total=0
            for _ in range(n):
                bits=stream.readline().rstrip('\n')
                assert bits and set(bits)<={'0','1'}
                total+=len(bits)
            assert total<=2100000
            result=dict(q=n,total_length=total)
        else:
            assert 1<=n<=300
            a=list(map(int,stream.readline().split()))
            assert len(a)==n and all(1<=x<=n for x in a)
            result=dict(n=n,values=a)
        assert not stream.read().strip()
    return result

def check_output(slug,output,dimensions):
    rows=output.decode('ascii').splitlines()
    if slug=='power-call-count':
        assert len(rows)==dimensions['q']
        values=[int(row) for row in rows]
        assert all(0<=v<4200000 for v in values)
        return values
    n=dimensions['n']
    a=dimensions['values']
    if slug=='shuffle-expectation':
        assert len(rows)==1
        values=list(map(int,rows[0].split()))
        assert len(values)==n and all(0<=v<MOD for v in values)
        assert sum(values)%MOD==sum(a)%MOD
        assert values[-1]==sum(a)*pow(n,MOD-2,MOD)%MOD
        return values
    assert len(rows)==n
    matrix=[list(map(int,row.split())) for row in rows]
    assert all(len(row)==n and all(0<=v<MOD for v in row) for row in matrix)
    assert all(sum(row)%MOD==1 for row in matrix)
    counts=[a.count(j+1) for j in range(n)]
    assert [sum(row[j] for row in matrix)%MOD for j in range(n)]==counts
    assert matrix[-1]==[v*pow(n,MOD-2,MOD)%MOD for v in counts]
    return matrix
