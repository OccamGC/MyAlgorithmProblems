# Upgrade Toolkit

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge only supports coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

An armed miner has found upgrade toolkits of several types. Each type has its own value, available stock, and value budget. The dispatcher wants to count the possible type quantities for every possible total number of collected toolkits.

## Formal Problem Statement

There are $n$ toolkit types numbered $1$ through $n$ . Each toolkit of type $i$ has value $i$ . At most $K_i$ are available, and the total value collected from this type must not exceed $V_i$ .

A plan is an integer vector $(c_1,\ldots,c_n)$ satisfying

$$0\le c_i\le K_i,\qquad i c_i\le V_i$$

Toolkits of the same type are indistinguishable. Plans differ exactly when some type quantity differs. Each type has its own value bound; there is no shared value bound across all types.

Let $C_i=\min(K_i,\lfloor V_i/i\rfloor)$ and $S=\sum_{i=1}^n C_i$ . Count plans collecting $0,1,\ldots,S$ toolkits, respectively, modulo $100000007$ . When $n=0$ , only the empty plan exists and $S=0$ .

## Input Format

The first line contains $n$ . The next $n$ lines contain $K_i,V_i$ for types $i=1,\ldots,n$ .

## Output Format

Print $S+1$ integers on one line. The $(j+1)$-th integer is the number of plans with total quantity $j$ , modulo $100000007$ .

## Sample 1

### Input

```text
3
10 2
1 10
1 10
```

### Output

```text
1 3 4 3 1
```

### Explanation

The capacities are $2,1,1$ . The four plans collecting two toolkits are $(2,0,0),(1,1,0),(1,0,1),(0,1,1)$ .

## Sample 2

### Input

```text
0
```

### Output

```text
1
```

### Explanation

There is exactly one empty plan.

## Sample 3

### Input

```text
3
0 1000
3 5
1000 2
```

### Output

```text
1 1 1
```

### Explanation

Only type $2$ can be collected, up to two copies. An unavailable earlier type does not change later IDs or values.

## Constraints and Guarantees

$0\le n\le1000$ and $0\le K_i,V_i\le1000$ . All input values are integers.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
