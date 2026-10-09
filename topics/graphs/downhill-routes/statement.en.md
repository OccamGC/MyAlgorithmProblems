# Counting Downhill Routes

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A mountain survey records the elevations of junctions and the roads between them. A team moves only downhill and wants to count all available routes.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n$ vertices labelled $1,\ldots,n$ , with vertex $i$ at height $h_i$ . There are $m$ undirected roads. Road $i$ has identifier $i$ and joins $u_i,v_i$ .

Start at any vertex. Each move uses exactly one road to reach a vertex of **strictly smaller** height. You may stop at any time, including before making a move.

A route is represented by its starting vertex followed by the identifiers of the roads used, in order. Distinct sequences are distinct routes. Thus, parallel roads are counted separately. Equal-height roads and self-loops cannot be used. Routes making no moves are distinguished by their starting vertices.

Find the least nonnegative residue of the number of routes modulo $998246353$ . There are no routes when $n=0$ .

## Input Format

The first line contains $n,m$ . The second contains $h_1,\ldots,h_n$ . Each of the next $m$ lines contains $u_i,v_i$ , describing road $i$ . If $n=0$ , the height line is empty and $m=0$ .

## Output Format

Print the route count modulo the specified modulus.

## Samples

### Sample 1

### Input

```text
5 5
1 2 3 4 5
5 4
5 3
4 3
3 2
2 1
```

### Output

```text
18
```

### Sample 2

### Input

```text
2 3
2 1
1 2
1 2
1 1
```

### Output

```text
4
```

### Sample 3

### Input

```text
0 0
```

### Output

```text
0
```

## Sample Explanation

In the first sample, the counts ending at vertices one through five are $6,5,4,2,1$ , totalling eighteen. The second has two zero-move routes and two routes using road one or road two; its self-loop cannot be used downhill. The third has no starting vertex.

![Downhill routes counted by endpoint](assets/example.en.svg)

## Constraints and Guarantees

$0\le n,m\le10^5$ , $-10^5\le h_i\le10^5$ , $1\le u_i,v_i\le n$ .

| Score | Additional constraints |
| --- | --- |
| 50% | $n,m\le300$ |
| 50% | None |
