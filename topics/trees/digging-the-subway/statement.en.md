# Digging the Subway

Reference time limit: 2 s; memory limit: 512 MiB. Calibrate to twice the slowest formal-file median, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

The Public Works Office has planned a subway network shaped like a tree, with $n$ stations and $n-1$ railway sections. Each section's tunnel has a digging difficulty.

Little B is about to dig the subway. Digging by hand is far too slow, so he decides to blast the tunnels open. There are $k$ stations where a blast may start, and each may be used repeatedly. A blast starts at any of these stations and ends at any station, opening every tunnel along the path between them. Passing through tunnels that are already open has no adverse effect.

Little B wants to know the minimum number of blasts needed to open every tunnel, denoted by $\mathrm{need}$. He may not be able to carry out that many blasts, so he also asks for the maximum total digging difficulty of the tunnels opened with each of $1,2,\ldots,\mathrm{need}$ blasts. Count each tunnel only once.

## Formal Problem Statement

An undirected tree has $n$ vertices numbered $1,\ldots,n$ , positive integer edge weights, and $k$ distinct marked vertices.

One operation chooses a marked vertex $s$ and any vertex $t$ and covers every edge on their unique path. Marked starts and paths may be reused, and $s=t$ is allowed. Each covered edge contributes its weight only once.

Let $\mathrm{need}$ be the minimum number of operations covering every edge. For each $i=1,\ldots,\mathrm{need}$ , independently maximize the total weight covered by exactly $i$ operations. The optimal choices for different values of $i$ need not share any paths.

![Two paths from marked starts cover all edges](assets/example.svg)

Stars mark vertices 6 and 7. Paths $6\to3$ and $7\to4$ cover all edges, whose total weight is 42.

## Input Format

The first line contains $n,k$ . The second contains the $k$ distinct marked vertices. Each of the next $n-1$ lines contains $u,v,w$ , describing an undirected edge of weight $w$ .

## Output Format

Print $\mathrm{need}$ on the first line. On each of the next $\mathrm{need}$ lines, print the maximum covered weight for exactly $i$ operations, in increasing order of $i$ .

## Sample 1

### Input

```text
4 1
1
1 2 2
2 3 2
2 4 1
```

### Output

```text
2
4
5
```

## Sample 2

### Input

```text
6 2
1 5
1 2 1
2 3 10
2 4 1
5 4 1
6 4 1
```

### Output

```text
2
12
14
```

## Sample 3

### Input

```text
6 2
1 2
1 2 3
2 3 10
2 4 1
5 4 1
6 4 1
```

### Output

```text
3
13
15
16
```

## Sample 4

### Input

```text
9 3
4 6 9
1 2 10
2 3 10
3 4 10
3 5 1
2 6 1
3 7 1
7 8 1
7 9 1
```

### Output

```text
3
30
33
35
```

## Sample 5

### Input

```text
5 1
1
1 2 2
1 3 3
1 4 4
1 5 5
```

### Output

```text
4
5
9
12
14
```

## Sample 6

### Input

```text
7 2
6 7
2 1 5
3 2 5
4 1 9
5 1 4
6 5 10
7 2 9
```

### Output

```text
2
28
42
```

## Constraints and Guarantees

$2\le n\le1000$ , $1\le k\le n$ , $1\le w\le100$ . The input is a tree and all marked vertices are distinct.

Authorized redesign: the vertex limit is 1000, enabling an exact algorithm. Coverage rules, both output objectives, and the edge-weight range are preserved. Specification and reference implementation: Codex (GPT-6).

| Score share | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, 10% each. See [test generation](tests/README.md).
