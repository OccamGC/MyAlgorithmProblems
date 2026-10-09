# Torch Lighting

- Indicative time limit: 1.0 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 128 MB

## Story

The village chief has opened a new farm and wants to illuminate it with torches to prevent monsters from spawning. Some locations contain dark sources that reduce brightness. Every source has a limited range. Count the cells where monsters may still spawn after all sources take effect.

## Formal Problem Statement

The farm is an $n$-row, $m$-column grid with rows and columns numbered from $1$ . Position $(i,j)$ has light value $L_{i,j}$ , radius $R_{i,j}$ , and spawn threshold $D_{i,j}$ . Every cell initially has brightness zero.

Source $(i,j)$ adds $L_{i,j}$ to every farm cell $(x,y)$ satisfying

$$|x-i|+|y-j|<R_{i,j}$$

All contributions add together. Negative light values reduce brightness. Radius zero affects no cells, and positions outside the farm are ignored.

A monster may spawn in a cell if its final brightness is at most that cell's $D_{i,j}$ . Count these cells.

![A radius-3 source affects cells at Manhattan distances 0, 1, and 2, but not cells at distance exactly 3](assets/strict-radius.svg)

Figure 1: With source $S$ and $R=3$ , only cells marked $+$ receive light. Numbers show Manhattan distance from the source.

## Input Format

The first line contains $n,m$ . Each of the next $n$ lines contains $m$ pairs $L_{i,j},R_{i,j}$ , in increasing column order. The final $n$ lines contain $m$ integers each, giving the thresholds $D_{i,j}$ .

## Output Format

Print the number of cells where monsters may spawn.

## Sample 1

### Input

```text
7 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

### Output

```text
21
```

### Explanation

The source at $(3,3)$ illuminates $13$ cells, and the source at $(7,5)$ illuminates only itself. Their ranges do not overlap, leaving $35-14=21$ cells at brightness zero.

## Sample 2

### Input

```text
1 3
10 1 -3 2 8 0
7 -3 -3
```

### Output

```text
3
```

### Explanation

Final brightness values are $7,-3,-3$ , exactly equal to the corresponding thresholds. All three cells are counted. The radius-zero source contributes nothing.

## Constraints and Guarantees

- $1\le n,m\le2200$ .
- $0\le R_{i,j}\le100000$ , $|L_{i,j}|\le10^8$ , and $|D_{i,j}|\le10^{15}$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $n,m\le80$ |
| 20% | $n,m\le300$ |
| 30% | $n,m\le1500$ |
| 20% | No additional conditions |
