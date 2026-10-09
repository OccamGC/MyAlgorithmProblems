# Forest Ranger

- Indicative time limit: **0.5 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments.
- Memory limit: 512 MB

## Story

A forest's trails form a tree. A ranger station stands at the entrance, and every other location is a checkpoint that needs to be inspected once.

Each day, the ranger leaves the station, patrols the trails, and returns. Returning to the station ends that day's patrol. No location may be visited more than twice in one day.

The ranger wants to finish all inspections in as few days as possible, while maximizing the cumulative number of inspected checkpoints by the end of each day. Help plan the patrol's progress.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

You are given an undirected tree with $n$ vertices, rooted at vertex $1$ . Each vertex $2,\ldots,n$ has a checkpoint with one inspection task, counted only once when completed. On each day, choose a walk that starts and ends at vertex $1$ . It must not visit vertex $1$ between its endpoints, and it may visit each vertex at most twice during that day. A task at a visited vertex may be completed if it has not been completed already.

Visits are counted as occurrences in the walk's vertex sequence, including vertex $1$ at departure and return. Vertices whose tasks are already complete may be visited again on later days.

First find the minimum number of days $D$ needed to finish every task. For each $k=1,\ldots,D$ , find the largest possible number of tasks completed by the end of day $k$ among schedules that finish all tasks within $D$ days. It can be proved that one schedule attains all these maxima simultaneously. Output only the values, not the routes.

## Input Format

The first line contains an integer $n$ . Each of the next $n-1$ lines contains two integers $u,v$ describing a tree edge.

## Output Format

Print the minimum number of days $D$ on the first line. On each of the next $D$ lines, print the maximum cumulative number of completed tasks after that day.

## Sample 1

### Input

```text
6
1 2
1 3
1 4
1 5
5 6
```

### Output

```text
4
2
3
4
5
```

### Explanation

On day one, the walk $1\to5\to6\to5\to1$ inspects vertices $5$ and $6$ . Each of the remaining three days inspects one of vertices $2,3,4$ .

## Sample 2

### Input

```text
4
1 2
2 3
3 4
```

### Output

```text
1
3
```

## Constraints and Guarantees

- $2\le n\le 1\,000\,000$ .
- The $n-1$ input edges form an undirected tree, with $1\le u,v\le n$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $n\le 10$ |
| 30% | $n\le 5\,000$ |
| 40% | No additional conditions |
