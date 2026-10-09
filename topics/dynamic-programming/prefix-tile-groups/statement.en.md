# Feasible Tile Partitions of Prefixes

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is 2 times the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

An organizer reveals tiles in increasing order of their numbers. After each new number, they check whether the revealed tiles form ordinary groups, or ordinary groups together with exactly one pair.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There is one tile type, with numbers $1,\ldots,n$ . Number $i$ has $a_i$ tiles. For every $i$ , consider all tiles numbered $1,\ldots,i$ and answer two separate questions:

1. Can they be partitioned into any number of three-tile runs and identical triples?
2. Can they be partitioned into those groups together with **exactly one** pair of equal-numbered tiles?

A run contains three consecutive numbers, one tile of each number. An identical triple contains three equal numbers. Both runs and identical triples may be repeated. Each partition must use every considered tile exactly once and cannot use a number greater than $i$ . Different prefixes are evaluated independently.

## Input Format

The first line contains $n$ . The second contains $a_1,\ldots,a_n$ .

## Output Format

Print $n$ lines. Line $i$ contains two space-separated integers, answering the questions in the stated order. Use `1` for a feasible partition and `0` otherwise.

## Samples

### Sample 1

### Input

```text
6
1 1 1 2 2 2
```

### Output

```text
0 0
0 0
1 0
0 1
0 0
1 0
```

### Sample 2

### Input

```text
1
2
```

### Output

```text
0 1
```

### Sample 3

### Input

```text
3
3 3 3
```

### Output

```text
1 0
1 0
1 0
```

## Sample Explanation

In the first sample, prefix three is a run. Prefix four adds a pair of fours. Prefix six can use two copies of the run $(4,5,6)$ . The second sample consists only of a pair and cannot be partitioned without one. In the third, every prefix consists of identical triples; its tile count is divisible by three, so a partition with exactly one pair is impossible.

## Constraints and Guarantees

$1\le n\le5\times10^6$ , $1\le a_i\le10^9$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
