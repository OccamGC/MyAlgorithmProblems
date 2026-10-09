# Two-Color Badges

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments.
- Memory limit: 512 MB

## Story

At a craft fair, every participant will receive a red or a blue badge. Before a single badge is handed out, the suggestion box is full: “The two of us must not wear the same color!”

The organizers process these requests in order. They accept a request if some assignment of colors satisfies both it and every previously accepted request; otherwise, they return the new request. Someone has even written their own name in both spaces on the form. The organizers decide to apply the rules as written.

The purchasing clerk has a simpler concern: red badges are on sale. After each request, the clerk wants to know the largest number of red badges that can be handed out while satisfying all accepted requests.

(This story was rewritten by GPT-6 Sol.)

## Formal Problem Statement

There are $n$ vertices and initially no edges. Process $m$ undirected edge requests $(u,v)$ in order. Accept and retain a request if adding its edge leaves the graph bipartite; otherwise reject it and leave the graph unchanged. Self-loops and duplicate requests are allowed.

A proper two-coloring assigns color $0$ or $1$ to every vertex so that the endpoints of each edge have different colors. After each request, output whether it was accepted and the maximum number of color-$0$ vertices over all proper two-colorings of the current graph. A new coloring may be chosen each time; previous color assignments need not be preserved.

## Input Format

The first line contains two integers $n,m$ .

Each of the next $m$ lines contains two integers $u,v$ representing an edge request.

## Output Format

For every request, print two integers on one line: $1$ if it is accepted or $0$ if it is rejected, followed by the maximum possible number of color-$0$ vertices.

## Sample 1

### Input

```text
5 5
1 2
1 3
2 3
4 5
4 1
```

### Output

```text
1 4
1 4
0 4
1 3
1 3
```

### Explanation

The third edge would create an odd cycle with the first two edges, so it is rejected. Finally all vertices form one component whose color classes have sizes $3$ and $2$ .

## Sample 2

### Input

```text
1 3
1 1
1 1
1 1
```

### Output

```text
0 1
0 1
0 1
```

## Constraints and Guarantees

- $1\le n,m\le 500\,000$ .
- $1\le u,v\le n$ ; self-loops and duplicate edges are allowed.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $n,m\le 15$ |
| 30% | $n,m\le 5\,000$ |
| 40% | No additional conditions |
