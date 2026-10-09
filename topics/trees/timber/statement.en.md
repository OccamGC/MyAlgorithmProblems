# Timber

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for estimation only)
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 128 MB

## Story

Steve has installed a tree-cutting mod. Selecting a branch cuts every node on its path to the root, and each selected node costs one fee. For each budget, maximize the number of cut nodes; among equally productive choices, disturb as few trees as possible.

## Formal Problem Statement

You are given an undirected forest with $n$ nodes and $m$ edges. Nodes are numbered $1$ through $n$ . Each connected component is a tree rooted at its smallest-numbered node.

After selecting distinct nodes, every node on the path from a selected node to its tree root, including both endpoints, is cut. A node appearing on multiple paths counts only once.

Let $Need$ be the minimum number of selections required to cut the whole forest. For each $k=1,\ldots,Need$ , among choices of exactly $k$ nodes, find:

1. The maximum number of nodes that can be cut.
2. Among choices attaining that maximum, the minimum number of trees containing a selected node.

## Input Format

The first line contains $n,m$ . Each of the next $m$ lines contains the endpoints $u,v$ of an undirected edge.

## Output Format

Print $Need$ on the first line. On each of the next $Need$ lines, print the two optimal values for the corresponding $k$ , separated by a space.

## Example 1

### Input

```text
11 9
1 2
2 3
3 4
4 5
3 6
6 7
8 9
9 10
10 11
```

### Output

```text
3
5 1
9 2
11 2
```

## Example 2

### Input

```text
6 4
1 2
2 3
1 4
5 6
```

### Output

```text
3
3 1
5 2
6 2
```

## Example 3

### Input

```text
1 0
```

### Output

```text
1
1 1
```

## Example Explanation

In example 1, select nodes $5,11,7$ in that order. The new contributions are $5,4,2$ , giving totals $5,9,11$ across $1,2,2$ trees.

![The two rooted trees of example one, selecting nodes five, eleven, and seven](assets/forest-paths.svg)

Double circles mark selected nodes. Labels 1, 2, and 3 beside edges indicate the first selection that covers that path segment. The isolated node in example 3 is itself a tree.

## Constraints and Guarantees

All inputs satisfy $1\le n\le500000$ , $0\le m\le n-1$ , and $1\le u,v\le n$ . The input is a forest and may contain isolated nodes.

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
