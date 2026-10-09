# Hagen Farm

- Indicative time limit: 0.5 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 512 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

> Apples are an Obi Island specialty. You simply have to try them. — Logistics Expert
>
> The apples at Hagen Farm do you good. Have some more, have some more. — Egg Dancer

Hagen Farm has a huge apple tree that has borne hundreds of millions of apples. The tree has $n$ vertices, is rooted at vertex $1$, and each branch has its own length.

Whenever a little Obi visits, the tree chooses a vertex uniformly at random and grows a batch of apples in its subtree. The number of apples is chosen uniformly from $1$ to the size of that subtree. Once this number is fixed, a subset of that many vertices is chosen uniformly, and one apple grows at each selected vertex.

The visitor then takes an apple-picking pole and sets off. They may start at any vertex, follow the branches to collect every apple, and return to the starting point. Find the expected shortest distance and report the answer modulo $1000000007$.

## Formal Problem Statement

Given an undirected tree with $n$ vertices numbered $1,\ldots,n$ , rooted at vertex $1$ , each edge has a nonnegative integer length. Generate apples in this order:

1. Choose a vertex $u$ uniformly from all $n$ vertices.
2. Let its subtree have size $s$ . Choose an integer $k$ uniformly from $1,\ldots,s$ .
3. Choose uniformly among all size-$k$ subsets of that subtree. Place one apple at every chosen vertex.

After seeing the apples, the visitor may start at any vertex, walk along edges to visit all apple vertices, and return to the starting vertex. Edges may be traversed repeatedly; each traversal contributes its length.

Let $E$ be the expected shortest walk length. Print $E$ modulo $P=1000000007$ : if $E=A/B$ , the answer is $A\cdot B^{-1}\bmod P$ . The bounds ensure that the required denominators are invertible modulo $P$ .

## Input

The first line contains $n$ . Each of the following $n-1$ lines contains $u,v,w$ , describing an edge of length $w$ between vertices $u,v$ .

## Output

Print the expected distance modulo $P$ .

## Sample 1

### Input

```text
3
1 2 1
1 3 1
```

### Output

```text
407407411
```

## Sample 2

### Input

```text
3
1 2 1
2 3 1
```

### Output

```text
740740747
```

## Sample 3

### Input

```text
1
```

### Output

```text
0
```

## Sample Explanation

The expectation is $20/27$ in sample 1 and $29/27$ in sample 2. Sample 3 has a single vertex, so the visitor starts at the apple and travels distance $0$ .

![Shortest closed walks for two selected apple vertices in each sample tree](assets/apple-walks.svg)

Asterisks mark apples. Each diagram shows one particular selected set; the problem averages over all random choices.

## Constraints and Guarantees

$1\le n\le2000$ ; $1\le u,v\le n$ ; $0\le w\le10000$ . The edges form a tree.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
