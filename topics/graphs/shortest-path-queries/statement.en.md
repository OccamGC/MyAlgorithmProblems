# Two Kinds of Shortest-Path Queries

Estimated time limit: 1 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A route service answers shortest-path queries between stations. Some networks are large but receive only one query. The remaining networks have few stations and may receive many queries.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

An undirected graph has $n$ vertices numbered $1,\ldots,n$ and $m$ nonnegative weighted edges. Answer $q$ queries in order. Each query specifies two vertices and asks for the minimum sum of edge weights along a path between them. Output $-1$ if they are disconnected.

Every input satisfies $q=1$ or $n\le500$ . Parallel edges, self-loops, zero-weight edges, and repeated queries are allowed. A vertex can reach itself using no edges, so its distance to itself is zero.

## Input Format

The first line contains $n,m,q$ . Each of the next $m$ lines contains $u,v,c$ , describing an undirected edge of weight $c$ between $u,v$ . Each of the following $q$ lines contains two vertices $u,v$ for one query.

## Output Format

Print $q$ lines in query order. Each line contains the shortest-path weight, or $-1$ if the queried vertices are disconnected.

## Samples

### Sample 1

### Input

```text
4 4 4
1 2 9
1 2 2
2 3 4
1 3 10
1 3
3 1
1 4
4 4
```

### Output

```text
6
6
-1
0
```

### Sample 2

### Input

```text
4 3 1
1 2 1000000000
2 3 1000000000
3 4 1000000000
1 4
```

### Output

```text
3000000000
```

## Sample Explanation

In the first sample, choose the weight-two edge between $1,2$ , then the weight-four edge to $3$ , for distance six. The reverse query also has distance six because the graph is undirected. Vertex $4$ is disconnected from the others, but its distance to itself is zero.

The second sample has just one simple path between $1,4$ , of total weight $3000000000$ .

## Constraints and Guarantees

For all inputs, $1\le n,m,q\le5\times10^5$ , $1\le u,v\le n$ , $0\le c\le10^9$ , and $q=1$ or $n\le500$ . The graph need not be connected.

| Score share | Additional conditions |
| --- | --- |
| 30% | $q=1$ |
| 40% | $q=1$ and $n\le500$ |
| 30% | $n\le500$ |
