# Path Independence in a Dynamic Tree

Estimated time limit: 1.5 seconds. Memory limit: 256 MB.

The deployed limit is the standard program’s largest input median in the target environment multiplied by $2$ and rounded up to a multiple of $0.5$ seconds. See the [benchmark notes](../../../docs/评测环境与性能.md).

## Story

A navigation trainer stores a robot’s routes from its base in a tree, with a signal at each station. A manager adds and removes routes and compares the shared endings of routes to their destinations.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Maintain a rooted tree. Initially it contains only vertex $0$ , the root, with value $0$ . An ending path is the sequence of values from the root to a leaf, including both endpoints.

For the sequence $s_u$ ending at leaf $u$ , define
$$
I(u)=|s_u|-\max_{v\ne u,\ v\text{ is a leaf}}\operatorname{LCS}(s_u,s_v),
$$
where $\operatorname{LCS}$ denotes longest common suffix length. With only one leaf, use zero for the maximum shared suffix length. Different leaves may have identical full sequences, so independence may be zero.

Process $q$ operations:

- $1\ A\ B\ C$ : add a new child of $A$ , with ID $B$ and value $C$ .
- $2\ A$ : delete $A$ and its entire subtree.
- $3\ A$ : query the independence $I(A)$ of leaf $A$ .

A deleted ID may be reused; reinserting it creates a new vertex. The root may be deleted, which can only be the final operation under the input guarantees.

## Input

The first line contains $q$ . Each of the next $q$ lines describes an operation in the format above.

## Output

For every type $3$ operation, print its integer answer on a separate line.

## Samples

### Sample 1

### Input

```text
14
1 0 1 1
1 0 2 2
1 1 3 2
3 3
3 2
1 0 4 3
1 4 5 3
1 5 6 3
3 6
1 6 7 1
3 7
1 3 8 1
3 7
3 8
```

### Output

```text
2
1
4
5
4
3
```

### Sample 2

### Input

```text
8
1 0 1 7
1 0 2 7
3 1
2 2
3 1
1 0 2 8
3 2
3 1
```

### Output

```text
0
2
2
2
```

### Sample 3

### Input

```text
6
3 0
1 0 100000 0
3 100000
2 100000
3 0
2 0
```

### Output

```text
1
2
1
```

## Sample explanations

The first query in sample one compares $(0,1,2)$ with $(0,2)$ . Their shared suffix has length $1$ , giving independence values $2,1$ . Sample two begins with two identical paths $(0,7)$ and independence zero. Deleting one gives independence $2$ for the remaining path. Sample three covers a single leaf, the largest ID, and deletion of the root at the end.

## Constraints and guarantees

$1\le q\le100000$ . All vertex IDs and values lie in $0,\ldots,100000$ . Vertex $A$ currently exists in every operation; an inserted ID $B$ does not currently exist; a queried vertex $A$ is a leaf. All input values are integers.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
