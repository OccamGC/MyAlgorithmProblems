# Distances in an Infinite Binary Tree

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The deployed limit is twice the largest per-input median runtime of the reference program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [reference measurements](../../../docs/评测环境与性能.md).

## Story

In a puzzle game, you build an infinite binary tree whose vertices are labeled with positive integers. A white rabbit plans journeys along its roads and asks how many edges separate different locations.

## Formal Problem Statement

The vertices of an undirected graph are all positive integers. For every positive integer $i$ , there is an edge from $i$ to $2i$ and an edge from $i$ to $2i+1$ , with no other edges.

For each query $a,b$ , find the number of edges on a shortest path from vertex $a$ to vertex $b$ . Equal endpoints are allowed and have distance zero.

![First four levels of the infinite tree and the path from vertex one to vertex ten](assets/tree.svg)

Only the first four levels are shown. The path $1\to2\to5\to10$ contains three edges.

## Input

The first line contains the number of queries $m$ . Each of the next $m$ lines contains two integers $a,b$ .

## Output

For query $i$ , print `Case #i: ans` , replacing `i` and `ans` with the query number and answer. Query numbering starts at $1$ , and exactly one space follows the colon.

## Samples

### Sample 1

### Input

```text
6
1 10
5 5
10000 10001
2 4
2 5
50000 60000
```

### Output

```text
Case #1: 3
Case #2: 0
Case #3: 2
Case #4: 1
Case #5: 1
Case #6: 28
```

### Sample 2

### Input

```text
4
1 1000000000000000000
576460752303423488 576460752303423487
1000000000000000000 1000000000000000000
576460752303423488 864691128455135232
```

### Output

```text
Case #1: 59
Case #2: 117
Case #3: 0
Case #4: 118
```

### Sample 3

### Input

```text
1
1 1
```

### Output

```text
Case #1: 0
```

## Sample explanations

In Sample 1, both $10000$ and $10001$ have parent $5000$ , so their distance is $2$ . A vertex has distance zero from itself. Sample 2 includes large labels and paths crossing between the two sides of the root.

## Constraints and guarantees

For all inputs: $1\le m\le10^5$ and $1\le a,b\le10^{18}$ .

| Score | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
