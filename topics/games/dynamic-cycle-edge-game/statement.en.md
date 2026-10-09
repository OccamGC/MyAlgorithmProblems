# An Edge-Weight Game on a Changing Cycle

Indicative time limit: 0.5 seconds. Memory limit: 256 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

A games club designs a two-player game on a ring of edges with counters. Members keep editing the ring and want to know whether the first player can win from a fixed starting point after each edit.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Starting from a fixed vertex $s$ , the clockwise edge-weight sequence $w_1,\ldots,w_n$ forms an undirected cycle. Two players alternate, with a token initially at $s$ . A move chooses a positive-weight edge incident to the token, moves along it, and decreases its weight to any strictly smaller nonnegative integer. A player unable to move loses. Both players play optimally.

Every move strictly decreases the sum of weights, so play terminates. Determine whether the first player has a winning strategy.

Process $q$ edits of the edge sequence in order:

- `1 R V` : change edge $R$ to weight $V$ .
- `2 R V` : insert a weight-$V$ edge immediately before the current edge $R$ . The position $R=n+1$ appends it at the end.
- `3 R` : delete edge $R$ .

After an edit, rebuild the cycle from the resulting sequence. The start remains the junction between its last and first edges. Every state starts an independent game: hypothetical decreases during play do not alter the sequence used by subsequent edits.

For short sequences, use these conventions: if $n=0$ , there is an isolated start and no move; if $n=1$ , the edge is a self-loop and moving along it leaves the token at the start; if $n=2$ , the two edges are distinct parallel edges between the same two vertices. For $n\ge3$ , the graph is the usual simple cycle.

![The start and clockwise order of four edges](assets/example.svg)

In Sample 1, the first player traverses the weight-2 edge and reduces it to zero, leaving a path of length two for the opponent, and can therefore win.

## Input Format

The first line contains `n q` . The second gives $n$ initial edge weights in clockwise order; it is empty when $n=0$ . Each of the next $q$ lines is an edit.

## Output Format

Print $q+1$ lines: the initial state followed by the state after each edit. Print 1 if the first player wins, and 0 otherwise.

## Sample 1

### Input

```text
4 0
2 5 3 0
```

### Output

```text
1
```


## Sample 2

### Input

```text
4 4
2 2 2 3
1 1 0
1 4 0
3 1
2 1 2
```

### Output

```text
1
1
0
0
1
```


## Sample 3

### Input

```text
0 3

2 1 0
1 1 7
3 1
```

### Output

```text
0
0
1
0
```

## Constraints and Scoring

Initially $0\le n\le10^5$ , and $0\le q\le10^5$ . All edge and update weights belong to $[0,100]$ . Changes and deletions satisfy $1\le R\le$ the current edge count; insertions satisfy $1\le R\le$ the current edge count plus one. The count may exceed its initial bound, but never exceeds the initial $n+q$ .

Completed by Codex (GPT-6) and recorded as a redesign: cycles of zero, one, and two edges, insertion positions, and independent games for each state are explicitly defined.

| Score | Additional constraints |
| --- | --- |
| 100% | None |

There are ten formal files worth 10% each.

See the [test recipes](tests/README.md).
