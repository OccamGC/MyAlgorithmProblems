# Snow White

Reference time limit: 2.5 s; memory limit: 512 MiB. Calibrate to twice the slowest formal-file median, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

Snow White asks you to help redesign her ski runs.

The runs connect locations at different elevations. Each run allows travel only in its specified direction, toward a location at the same or a lower elevation. You may build lifts that also operate in one direction, toward locations at the same or a higher elevation.

Snow White wants every location to be reachable from every other location using the runs and lifts. First minimize the total elevation gained by all lifts, then build as few lifts as possible among solutions with that minimum total.

## Formal Problem Statement

There are $n$ vertices and $m$ directed edges. Vertex $u$ has height $h_u$ . Every existing edge $u\to v$ satisfies $h_u\ge h_v$ . Equal-height edges still allow travel only in their specified direction. Existing parallel edges and self-loops are allowed.

You may add directed edges $s\to t$ satisfying $s\ne t$ and $h_s\le h_t$ . Each costs $h_t-h_s$ . Make the final graph strongly connected: every vertex must be able to reach every other vertex along directed edges.

First minimize the total cost of added edges. Among solutions of that cost, minimize the number of added edges. Output any optimal solution, or `-1` if none exists.

![A descending chain and one uphill edge joining its ends](assets/example.svg)

Black edges are existing ski runs and the blue edge is a new lift. The total cost is $3-0=3$ , using one new edge.

## Input Format

The first line contains $n,m$ . The second contains $h_1,\ldots,h_n$ . Each of the next $m$ lines contains $u,v$ , specifying an existing edge $u\to v$ .

## Output Format

If impossible, print only `-1` on one line. Otherwise print the minimum total cost, then the minimum number $k$ of added edges at that cost, then $k$ lines containing endpoints $s,t$ of added edges $s\to t$ . Print no edge lines when $k=0$ .

## Sample 1

### Input

```text
3 2
3 1 0
1 2
2 3
```

### Output

```text
3
1
3 1
```

## Sample 2

### Input

```text
3 1
2 1 0
1 2
```

### Output

```text
-1
```

## Sample 3

### Input

```text
3 2
5 5 5
1 2
1 3
```

### Output

```text
0
2
2 3
3 1
```

## Sample 4

### Input

```text
7 3
4 5 1 0 5 4 4
5 1
7 1
7 4
```

### Output

```text
5
5
1 6
6 7
2 5
4 3
3 2
```

## Constraints and Guarantees

$1\le n\le500000$ , $1\le m\le2000000$ , $-10^9\le h_u\le10^9$ , $1\le u,v\le n$ . Existing edges satisfy $h_u\ge h_v$ .

Codex (GPT-6) completed the impossible-case output and the conventions for self-loops and parallel edges, recorded as a redesign. Vertex, edge, and height limits and both optimization objectives are preserved.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, 10% each. See [test generation](tests/README.md).
