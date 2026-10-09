# Century Bomber

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 8 MB

## Story

The Allies are testing supply drops with Century Bombers. Soldiers carry different amounts of supplies. Each crew chooses a consecutive group of soldiers and drops a copy of that group at every designated starting position. Determine the supplies delivered to each position along the line.

## Formal Problem Statement

You are given a sequence $a$ of length $n$ , a line of length $m$ , and $k$ distinct starting positions $p_1,\ldots,p_k$ . Positions are numbered from $1$ to $m$ , and initially contain no supplies.

A drop specifies an interval $[l,r]$ . For every start $p_i$ and every $0\le j\le r-l$ , add $a_{l+j}$ units to position $p_i+j$ if it is at most $m$ . Ignore contributions beyond the line. Contributions from different drops and starts are added together; the sequence $a$ never changes.

Output the total at every position after all $q$ drops.

## Input Format

The first line contains $n,m,k,q$ . The second contains $n$ integers $a_i$ . The third contains $k$ integers $p_i$ and is empty when $k=0$ . Each of the next $q$ lines contains $l,r$ .

## Output Format

Print $m$ integers: the totals at positions $1$ through $m$ , in order.

## Sample 1

### Input

```text
5 1 1 5
1 2 3 4 5
1
1 1
2 2
3 3
4 4
5 5
```

### Output

```text
15
```

### Explanation

The five drops choose one soldier each. The only position receives $1+2+3+4+5=15$ units.

## Sample 2

### Input

```text
4 5 2 2
1 2 3 4
1 4
2 4
1 2
```

### Output

```text
3 5 4 3 5
```

### Explanation

The combined contributions at offsets $0,1,2$ are $3,5,4$ . Add this sequence starting at positions $1$ and $4$ , discarding the part beyond position $5$ .

## Sample 3

### Input

```text
1 3 0 0
9

```

### Output

```text
0 0 0
```

### Explanation

There are no starting positions or drops, so all totals are zero.

## Constraints and Guarantees

- $1\le n,m\le2000$ , $0\le k\le m$ , and $0\le q\le30000$ .
- $0\le a_i\le9$ and $1\le p_i\le m$ ; all starting positions are distinct.
- Every drop satisfies $1\le l\le r\le n$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
