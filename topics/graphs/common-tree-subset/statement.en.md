# A Common Connected Set in Several Trees

Estimated time limit: 3 seconds. Memory limit: 512 MB.

The deployed limit is the standard program’s largest input median in the target environment multiplied by $2$ and rounded up to a multiple of $0.5$ seconds. See the [benchmark notes](../../../docs/评测环境与性能.md).

## Story

Observation stations must support several communication layouts. The selected stations must stay connected in every layout, and the planner wants the largest total reward.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n$ vertices, numbered $1,\ldots,n$ , with integer weights $a_i$ that may be negative. You are given $m$ trees on this same vertex set.

Choose a set $S$ whose induced subgraph is connected in every tree: the unique path between any two selected vertices may contain only selected vertices. The empty set is allowed, is considered feasible, and has weight zero.

Maximize $\sum_{i\in S}a_i$ .

## Input

The first line contains $n,m$ . The second contains $a_1,\ldots,a_n$ . Then follow $m$ blocks of $n-1$ lines each. Every line contains two endpoints $u,v$ of an undirected edge in that block’s tree.

## Output

Print one integer: the maximum total weight.

## Samples

### Sample 1

### Input

```text
3 1
-6 3 4
1 2
1 3
```

### Output

```text
4
```

### Sample 2

### Input

```text
7 2
-10 -3 3 5 7 2 1
1 2
1 3
2 4
2 5
3 6
3 7
1 2
1 7
2 4
2 5
7 6
7 3
```

### Output

```text
9
```

### Sample 3

### Input

```text
2 2
-2 -7
1 2
2 1
```

### Output

```text
0
```

## Sample explanations

In sample one, selecting vertex $3$ alone gives $4$ . Selecting both $2,3$ also requires $1$ , giving only $1$ . In sample two, $\{2,4,5\}$ is connected in both trees and gives $-3+5+7=9$ . In sample three, select the empty set.

## Constraints and guarantees

$1\le n\le20000$ , $1\le m\le5$ , and $|a_i|\le10^9$ . Endpoints lie in $1,\ldots,n$ , and each block describes a tree.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
