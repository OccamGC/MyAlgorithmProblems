# Prism Tank

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

FutureTech has fitted a Prism Tank with an enhanced laser and a chronospatial link, and sent the prototype to demonstrate them at Yuri's outpost. Its beam can refract between buildings; the link can block selected paths in advance.

The prototype is expensive and has no escort. It must retreat after a single shot. The director has already drafted the publicity announcement; all that remains is a defensible figure for “maximum expected damage.”

## Formal Problem Statement

You are given a forest with $n$ vertices numbered $1$ through $n$ and $e$ undirected edges. Hitting vertex $i$ causes damage $d_i$ ; its refraction probability is $p_i$ .

Before firing, each vertex may select at most $b$ incident edges to block. **An edge is blocked if either endpoint selects it.** It uses the allowance only of endpoints that actually select it. Choose one vertex for the initial hit.

Each vertex can be hit at most once. When vertex $i$ is hit, let $C$ contain its neighbors connected by unblocked edges that have not yet been hit:

- If $C$ is empty, propagation stops there.
- Otherwise, with probability $p_i$ , all vertices of $C$ are hit. With probability $1-p_i$ , one uniformly chosen vertex of $C$ is hit.
- Newly hit vertices propagate in the same way. Random choices are independent.

Total damage is the sum of $d_i$ over all hit vertices. The initial target and all blocking decisions are fixed before the random process begins. Let $V$ be the maximum expected total damage and $\delta$ the rounding offset supplied in the input. Output $\lfloor V+\delta+0.5\rfloor$ .

## Input Format

The first line contains, in order, the vertex count $n$ , per-vertex blocking allowance $b$ , edge count $e$ , and rounding offset $\delta$ . The first three values are integers; the last is real.

The next $e$ lines each contain two integers $u,v$ , describing an edge.

The next line contains $n$ real numbers $d_1,\ldots,d_n$ .

The final line contains $n$ real numbers $p_1,\ldots,p_n$ .

## Output Format

Output the integer $\lfloor V+\delta+0.5\rfloor$ .

## Sample 1

### Input

```text
3 1 2 0.00
3 2
1 3
1.00 2.00 3.00
0.500 0.500 0.800
```

### Output

```text
6
```

### Explanation

With no edges blocked, hitting vertex $1$ reaches all three vertices and causes total damage $6$ .

## Sample 2

### Input

```text
6 0 5 0.50
2 3
4 6
4 3
1 2
2 5
1.00 2.00 3.00 4.00 5.00 6.00
0.500 0.500 0.500 0.500 0.500 0.500
```

### Output

```text
20
```

### Explanation

Starting at vertex $6$ hits vertices $6,4,3,2$ in that order, for damage $15$ . At vertex $2$ , the beam hits both remaining vertices with probability $0.5$ ; otherwise it chooses one of them uniformly. Their expected contribution is $0.5\times(1+5)+0.5\times(1+5)/2=4.5$ . The total expectation of $19.5$ is the maximum over all strategies. Adding $\delta=0.50$ and rounding gives $20$ .

## Sample 3

### Input

```text
5 1 4 0.00
1 2
1 3
1 4
1 5
0.00 10.00 9.00 0.00 0.00
0.000 0.000 0.000 0.000 0.000
```

### Output

```text
19
```

### Explanation

Let vertex $4$ select edge $(1,4)$ and vertex $5$ select edge $(1,5)$ for blocking. Each vertex selects at most one edge, and vertex $1$ does not need to select either edge.

Starting at vertex $2$ then hits vertices $2,1,3$ in order, for damage $19$ . This is the sum of all vertex damages, so it is optimal.

## Constraints and Guarantees

- $1\le n\le2000$ , $0\le e\le n-1$ , and $0\le b\le e$ .
- $1\le u,v\le n$ . There are no loops, parallel edges, or cycles; the forest may be disconnected.
- $0\le d_i\le5000$ , $0\le p_i\le1$ , and $0\le\delta\le1$ .
- Damage values and $\delta$ have at most two decimal places; probabilities have at most three.
- With $z=V+\delta$ , the guarantee is $\lvert z-\lfloor z+0.5\rfloor\rvert\le0.3$ , keeping the result away from rounding boundaries.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
