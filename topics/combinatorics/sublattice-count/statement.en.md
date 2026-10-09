# Counting Sublattices

Estimated time limit: 1 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A computing module provides two binary operations. You want to retain some of its elements so that applying either operation to retained elements always gives another retained element. Count the nonempty sets that can be retained.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

A lattice $S$ has $n$ distinct elements numbered $1,\ldots,n$ . A lattice is a nonempty partially ordered set in which each pair has a unique least upper bound (a common upper bound below every other common upper bound) and greatest lower bound (a common lower bound above every other common lower bound). Denote them by $i\lor j$ and $i\land j$ , respectively.

A nonempty subset $U\subseteq S$ is a sublattice exactly when every $i,j\in U$ satisfies $i\lor j\in U$ and $i\land j\in U$ . Use the operation results in the given lattice. Count these sublattices. Different element sets count separately even if their structures are isomorphic. Exclude the empty set and include the whole lattice.

## Input Format

The first line contains $n$ . The next $n$ lines each contain $n$ integers, forming matrix $A$ . For $i\le j$ , entry $A_{i,j}=i\lor j$ ; for $i\ge j$ , it is $A_{i,j}=i\land j$ . Both definitions agree on the diagonal and give $i$ .

Join and meet are each commutative. The matrix stores them in different triangular halves, so the matrix itself need not be symmetric.

## Output Format

Print the number of nonempty sublattices as one integer.

## Samples

### Sample 1

### Input

```text
8
1 1 3 7 3 6 7 6 
2 2 3 4 5 6 7 8 
1 2 3 6 3 6 6 6 
2 2 2 4 8 6 7 8 
2 2 5 2 5 6 6 8 
1 2 3 4 5 6 6 6 
1 2 1 4 2 7 7 6 
2 2 5 4 5 8 4 8
```

### Output

```text
73
```

### Sample 2

### Input

```text
1
1
```

### Output

```text
1
```

### Sample 3

### Input

```text
3
1 2 3
1 2 3
1 2 3
```

### Output

```text
7
```

## Sample Explanation

The first sample has $73$ nonempty sublattices. In the second, only the single element can be selected. The third is a three-element total order. Every nonempty subset is closed under maximum and minimum, giving $2^3-1=7$ .

![A closed subset and a nonclosed subset of a four-element lattice](assets/subsets.svg)

Element one is the minimum, four the maximum, and two and three are incomparable. Set $\{1,2,4\}$ is closed. The operations on $\{2,3\}$ give four and one, so that set is not closed.

## Constraints and Guarantees

For all inputs, $1\le n\le22$ and $1\le A_{i,j}\le n$ . The operations are guaranteed to describe a lattice. Numerical labels do not specify the partial order.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
