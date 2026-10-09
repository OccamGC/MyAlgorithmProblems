# Automatic Connectors

- Indicative time limit: **0.5 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Deployment time limit: measure the reference program in the target environment, multiply the slowest case's median time by 2, and round up to the next 0.5 seconds.
- Memory limit: **128 MB**.

## Story

A computer workshop is installing automatic connectors on cables between computers and workbenches. A cable can connect automatically if either endpoint has a connector. One connector serves every cable incident to its port.

Connectors may be installed on either side. Use as few as possible to cover all cables.

## Formal Problem Statement

There are $n$ ports numbered $1,\ldots,n$ . Port $i$ has type $a_i$ : $0$ means a workbench port and $1$ means a computer port.

There are $m$ cables, each connecting a workbench port to a computer port. Choose a set $S$ of ports so that every cable has at least one endpoint in $S$ , while minimizing $\lvert S\rvert$ . Output any optimal set.

## Input Format

The first line contains $n,m$ .

The second line contains $a_1,\ldots,a_n$ .

Each of the next $m$ lines contains $u,v$ , describing a cable between ports $u$ and $v$ .

## Output Format

On the first line print the minimum number of connectors $c$ .

On the second line print $c$ distinct port IDs in any order. The checker verifies optimal size and coverage of every cable; your chosen set need not match the sample.

## Sample 1

### Input

```text
6 5
0 1 0 1 1 0
1 2
2 3
3 4
6 4
5 6
```

### Output

```text
3
1 3 6
```

## Sample 2

### Input

```text
4 3
0 1 1 1
1 2
1 3
1 4
```

### Output

```text
1
1
```

## Sample 3

### Input

```text
4 2
0 0 1 1
1 3
2 3
```

### Output

```text
1
3
```

## Sample Explanation

In sample 1, ports $1,3,6$ cover every cable. Cables $(1,2)$ , $(3,4)$ , and $(5,6)$ have pairwise disjoint endpoints, so at least three connectors are necessary.

![The sample bipartite graph with connectors on workbench ports 1, 3 and 6](assets/connector-cover.svg)

Double circles mark installed connectors. Workbenches are on the left and computers on the right.

In sample 2, the star center, port $1$ , suffices. In sample 3, computer port $3$ suffices; isolated port $4$ needs no connector.

## Constraints and Guarantees

For all test cases: $1\le n\le100000$ , $1\le m\le200000$ , $a_i\in\{0,1\}$ , and $1\le u,v\le n$ . Every cable satisfies $a_u\ne a_v$ . Isolated ports and parallel cables are allowed.

| Score | Additional restrictions |
| --- | --- |
| 100% | None |
