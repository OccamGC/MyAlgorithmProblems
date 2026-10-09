# Factorio: Roboport Network

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

In Factorio, robots rely on roboports to coordinate their work. The roboports form a ring. As mines close and production lines open, roboports must be removed or added, and the current control position must move through the network.

## Formal Problem Statement

Initially, $n$ roboports numbered $1,2,\ldots,n$ form a ring in that order. The current roboport is $1$ .

Direction $0$ follows $1\to2\to\cdots\to n\to1$ ; direction $1$ is the reverse. After insertions or deletions, these directions follow the corresponding neighboring links of the ring.

Process $m$ operations in order:

- `0` : remove the current roboport and make its direction-$0$ successor current. Removing the only roboport makes the ring empty. Ignore this operation on an empty ring.
- `1` : insert a new roboport between the current roboport and its direction-$0$ successor, keeping the current roboport unchanged. On an empty ring, insert the only roboport and make it current.
- `2 x` : move $x$ steps in direction $0$ .
- `3 x` : move $x$ steps in direction $1$ .
- `4` : report the current roboport number, or `-1` if the ring is empty.

Each insertion receives one more than the largest number ever assigned. Numbers are never reused. A negative step count means movement in the opposite direction. Ignore movement on an empty ring. In a one-roboport ring, both successors are the roboport itself.

![Current positions after insertion and deletion in a ring](assets/ring.svg)

Arrows show direction $0$ ; double circles mark the current roboport. The rows show the initial state, the result of `1` , and the result of a subsequent `0` . Direction $1$ opposes the arrows.

## Input

The first line contains $n,m$ . Each of the next $m$ lines contains an operation in the format above.

## Output

Output one line for each `4` operation. If there are no queries, the output is empty.

## Samples

### Sample 1

### Input

```text
3 26
4
2 100
4
3 -100
4
1
4
2 1
4
2 0
4
0
4
0
4
0
4
0
4
1
4
1
1
4
2 2
4
```

### Output

```text
1
2
3
3
4
4
1
2
3
-1
5
5
6
```

### Sample 2

### Input

```text
4 51
4
2 1
4
2 1
4
2 1
4
2 1
4
3 1
4
0
4
2 1
4
3 1
4
3 1
4
1
4
2 1
4
3 1
4
2 2
4
0
4
0
4
0
4
0
4
0
4
1
4
2 1000
4
1
1
1
1
1
1
2 1000
4
3 -5000
4
```

### Output

```text
1
2
3
4
1
4
1
2
1
3
3
5
3
1
2
3
5
-1
-1
6
6
7
12
```

### Sample 3

### Input

```text
1 12
4
0
4
2 -1000000000
1
4
1
3 -1
4
0
4
4
```

### Output

```text
1
-1
2
3
2
2
```

## Sample Explanation

Samples 1 and 2 illustrate wraparound, negative steps, insertion, and repeated deletion. Inserting into a nonempty ring does not move to the inserted roboport.

In sample 3, removing the only roboport leaves an empty ring. The next insertion receives number $2$ . Another insertion creates number $3$ , and `3 -1` moves one step in direction $0$ .

## Constraints and Guarantees

For 100% of the data: $1\le n,m\le10^5$ , and $-10^9\le x\le10^9$ .

For every movement on a nonempty ring, let $s$ be its current size and $r$ the nonnegative remainder of $x$ modulo $s$ . It is guaranteed that $\min(r,s-r)\le500$ : after removing full laps and choosing the shorter direction, at most $500$ steps are needed. This condition does not apply to movement on an empty ring.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
