# Bridge Tales: The First Plan Is Out

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 512 MB

## Story

An engineer submits the cheapest bridge network connecting a group of floating islands. The reviewer immediately stamps the cover: “No first plan. Absolutely not!”

“What if I change a few bridges but keep the same total cost?” asks the engineer. “That's just the first plan with a new cover,” says the reviewer. The engineer must therefore find a network that still connects every island and costs **strictly more** than the minimum. Since the extra expense is unavoidable, they want the cheapest qualifying network.

(This story was rewritten by GPT-6 Sol.)

## Formal Problem Statement

You are given a connected undirected graph with $n$ vertices and $m$ edges of positive integer weight. Vertices are numbered from $1$ to $n$ . Parallel edges are allowed; self-loops are not. A plan is a spanning tree of the graph, and its cost is the sum of its edge weights. Let $W_{\min}$ be the minimum cost of any spanning tree.

Find the smallest spanning-tree cost strictly greater than $W_{\min}$ . Such a spanning tree is guaranteed to exist. If several minimum spanning trees exist, all of them still cost $W_{\min}$ and do not count as the answer.

## Input Format

The first line contains two integers $n,m$ .

Each of the next $m$ lines contains three integers $u,v,w$ , describing an undirected edge of weight (cost) $w$ between $u$ and $v$ . Parallel edges are distinct candidates.

## Output Format

Print one integer: the required minimum cost.

## Sample 1

### Input

```text
3 5
1 2 3
1 2 5
2 3 4
2 3 9
1 3 3
```

### Output

```text
7
```

### Explanation

The minimum cost is $3+3=6$ . Choosing the edge $(1,3)$ of cost $3$ and the edge $(2,3)$ of cost $4$ gives the least strictly larger cost, $7$ .

## Sample 2

### Input

```text
3 4
1 2 1
2 3 1
1 3 1
1 2 3
```

### Output

```text
4
```

### Explanation

Any two of the first three edges form a minimum spanning tree of cost $2$ . The cheapest tree using the last edge costs $4$ ; no spanning tree costs $3$ .

## Constraints and Guarantees

- $2\le n\le 100\,000$ .
- $n\le m\le 200\,000$ .
- $1\le w\le 5\,000$ .
- $1\le u,v\le n$ and $u\ne v$ .
- The graph is connected, and at least one spanning tree has cost strictly greater than $W_{\min}$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 20% | $n\le 10$ and $m\le 20$ |
| 30% | $n\le 5\,000$ and $m\le 10\,000$ |
| 50% | No additional conditions |
