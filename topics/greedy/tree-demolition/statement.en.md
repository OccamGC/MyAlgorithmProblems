# Dismantling Devices on a Tree

Estimated time limit: 1.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A device station is closing. Each device may still earn revenue or incur maintenance costs before it stops. Its dismantling order must respect the dependencies.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

A tree has $n$ vertices, numbered $1,\ldots,n$ , and is rooted at vertex $1$ . Vertex $i$ produces an integer value $p_i$ per hour, possibly negative.

Starting at time zero, dismantle exactly one vertex per hour. A vertex may be dismantled only after all its children have been dismantled. Dismantling takes one hour, and production stops as soon as it starts. Thus the $k$-th removed vertex has produced for $k-1$ hours. For order $v_1,\ldots,v_n$ , the total value is
$$
\sum_{k=1}^{n}(k-1)p_{v_k}.
$$
Maximize this value and output the lexicographically smallest sequence of vertex IDs among all optimal legal orders. Lexicographic order compares IDs at the first differing position.

## Input Format

The first line contains $n$ . The second contains $p_1,\ldots,p_n$ . Each of the next $n-1$ lines contains two vertices $u,v$ joined by an undirected edge. Rooting the tree at $1$ determines the parent-child directions.

## Output Format

Print the maximum total value on the first line. On the second, print the $n$ IDs in the lexicographically smallest optimal dismantling order.

## Samples

### Sample 1

### Input

```text
5
-1 -1 -2 -2 -1
1 2
2 3
3 4
4 5
```

### Output

```text
-13
5 4 3 2 1
```

### Sample 2

### Input

```text
5
1 2 1 2 4
2 1
3 1
3 5
2 4
```

### Output

```text
17
4 2 5 3 1
```

### Sample 3

### Input

```text
5
0 0 0 0 0
1 2
2 5
1 3
3 4
```

### Output

```text
0
4 3 5 2 1
```

## Sample Explanation

Sample one has a unique legal order, giving $0(-1)+1(-2)+2(-2)+3(-1)+4(-1)=-13$ . In sample two, order $4,2,5,3,1$ gives $17$ . Every legal order in sample three has value zero, so the lexicographic tie rule still matters.

## Constraints and Guarantees

$1\le n\le500000$ , $|p_i|\le1000000$ . The edges form a tree.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
