# Catalyst Sequence

- Indicative time limit: 5.0 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

An adventurer lines up crafting materials in the order they were obtained. The closer two energy values are, the lower the resulting catalyst’s separation level. For each level, find the longest consecutive batch of materials.

## Formal Problem Statement

Given positive integers $a_1,\ldots,a_n$ , let $U=\max_i a_i$ .

For a contiguous interval $[l,r]$ containing at least two elements, define its separation level as

$$d(l,r)=\min_{l\le i<j\le r}|a_i-a_j|$$

For every integer $d=0,1,\ldots,U-1$ , find the maximum length of an interval whose level is **exactly** $d$ . Output $0$ if no such interval exists.

Equal values may occur at different positions. A single element is not a valid interval.

## Input

The first line contains $n$ . The second line contains $a_1,\ldots,a_n$ .

## Output

Print $U$ lines. Line $d+1$ contains the maximum interval length for level $d$ .

## Sample 1

### Input

```text
10
1 3 2 1 4 7 9 8 2 3
```

### Output

```text
10
7
4
3
0
0
2
0
0
```

## Sample 2

### Input

```text
1
1
```

### Output

```text
0
```

## Sample 3

### Input

```text
3
1 3 5
```

### Output

```text
0
0
3
0
0
```

## Sample Explanation

In sample 1, the whole sequence contains equal values and has level $0$ . The seven distinct values in $[2,8]$ include consecutive integers, so this interval has level $1$ . Sample 2 has no interval of length at least $2$ . The whole interval in sample 3 has level $2$ .

![Sample 3: three elements with minimum gap two](assets/minimum-gap.svg)

The entire interval in sample 3 has length $3$ and level $2$ .

## Constraints and Guarantees

$1\le n\le100000$ ; $1\le a_i\le250000$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
