# Factorio: Technology Tree

Estimated time limit: 1.0 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See [environment and measurements](../../../docs/评测环境与性能.md).

## Story

In Factorio, the technology tree can have a graph of research dependencies. Some technologies are already unlocked. Schedule the remaining research to finish everything as early as possible.

## Formal Problem Statement

There are $n$ technologies numbered from $1$ to $n$ . If $t_i=-1$ , technology $i$ is already complete at time zero. Otherwise, researching it takes $t_i$ units of time.

A dependency $(u,v)$ means that technology $u$ can start only after technology $v$ is complete. An unfinished technology must wait for all its dependencies. Its completion time equals its start time plus its duration. Any number of technologies may be researched concurrently.

Completed technologies need no further research; their listed dependencies do not revoke their completed status. Self-dependencies and repeated dependencies are allowed. Even a dependency cycle with only zero durations cannot start by treating its unfinished members as already complete.

Find the minimum time needed to complete every technology, or report that completion is impossible.

## Input Format

The first line contains the numbers of technologies and dependencies, $n,m$ . The second line contains $t_1,\ldots,t_n$ . Each of the next $m$ lines contains $u,v$ , meaning that $u$ depends on $v$ .

## Output Format

If every technology can be completed, print the minimum time as one integer. The answer is $0$ if all technologies are already complete. Otherwise, print `bad idea` .

## Examples

### Example 1

### Input

```text
5 5
3 5 -1 2 4
2 1
4 1
5 2
5 4
1 3
```

### Output

```text
12
```

### Example 2

### Input

```text
2 2
0 0
1 2
2 1
```

### Output

```text
bad idea
```

### Example 3

### Input

```text
3 3
-1 0 7
1 3
2 1
3 2
```

### Output

```text
7
```

## Example Explanation

In the first example, technology $3$ is already complete. Technology $1$ finishes at time $3$ , technologies $2,4$ at times $8,5$ , and technology $5$ at time $12$ . The zero-duration cycle in the second example has no technology that can start. In the third example, technology $1$ is already complete, so technology $2$ finishes at time zero and technology $3$ then takes seven time units.

![Dependencies and completion times in example one](assets/research.svg)

Arrows point from a prerequisite to its dependent. Here $t_i$ is the input duration and $T_i$ is the finish time. The dashed node is already complete.

## Constraints and Guarantees

All inputs satisfy: $1\le n\le10^6$ , $0\le m\le2\times10^6$ , $-1\le t_i\le10^9$ , and $1\le u,v\le n$ . The dependency graph is not guaranteed to be acyclic.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
