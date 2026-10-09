# Nether Portal

Reference time limit: 0.5 s; memory limit: 128 MiB. Use twice the slowest formal-file median on the target platform, rounded up to 0.5 seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

Little B, the mayor of Brookbend Village, is a capable member of the Public Works Office. He knows rail transport inside out, but is still a beginner when it comes to portals. He asks you to help Steve work out the earliest time at which he can reach his destination from the starting point.

The server that hosts Greenmaple Town has $N$ portal entrances. A chunk is large enough to contain several entrances. The server administrators have also built one-way portals, so a portal's destination chunk need not contain a portal of its own.

If Steve's current chunk contains portals, he may enter any one of them or choose not to enter. He may also move up, down, left, or right to a neighboring chunk. Each move adds that world's value $T_w$ to the current time. He may wait in place for any nonnegative amount of time. Each portal has a creation time and a time change applied when it is used.

At time zero, Steve appears in chunk $(x_0,y_0)$ of world $w_0$. He wants to reach chunk $(x_1,y_1)$ of world $w_1$ as early as possible.

## Formal Problem Statement

There are $M$ worlds, each an infinite integer grid. In world $w$ , moving one cell up, down, left, or right adds $T_w$ to the current time. This value may be negative or zero. Waiting at a cell for any nonnegative duration is allowed.

You start at time zero at $(x_0,y_0)$ in world $w_0$ . Find the earliest arrival at $(x_1,y_1)$ in world $w_1$ . Even when the start equals the destination, you may leave and return.

Portal $i$ leads from $(x_i,y_i)$ in world $w_i$ to $(x'_i,y'_i)$ in world $w'_i$ . It exists permanently from time $t_i$ onward. At its entrance, it may be used whenever the current time is at least $t_i$ . Using it adds $\delta_i$ to the time and moves you to its exit. The portal works only in the specified direction; its exit need not contain another portal. A cell may have several entrances, and you may choose any available one or continue walking.

Print `YouNeedOpPermission` if the destination is unreachable, `NegativeInfinity` if arrival times have no finite lower bound, or the finite earliest arrival time otherwise.

![Opening times limit the benefit of negative-time walking](assets/example.svg)

In Example 4, walking can move the clock arbitrarily far backward in the first world. However, the portal cannot be used before $-7$ , so the earliest arrival at the destination is $-4$ .

## Input Format

The first line contains `N M` , the numbers of portals and worlds.

The second line contains `w_0 x_0 y_0 w_1 x_1 y_1` .

The third line contains $T_1,\ldots,T_M$ .

Each of the next $N$ lines contains `w_i x_i y_i w'_i x'_i y'_i t_i delta_i` .

## Output Format

Print one line containing either special string or the integer earliest arrival time.


## Example 1

### Input

```text
2 2
1 0 0 1 1000 1000
1 1
1 995 1000 2 505 505 -1000 2
2 505 500 1 1000 1000 -990 -50
```

### Output

```text
-1040
```

## Example 2

### Input

```text
2 2
1 0 0 2 1000 1000
1 -1
1 995 1000 1 505 505 -1000 2
2 505 500 1 1000 1000 -990 -50
```

### Output

```text
YouNeedOpPermission
```

## Example 3

### Input

```text
2 2
1 0 0 1 1000 1000
-1 -1
1 995 1000 2 505 505 -1000 2
2 505 500 1 1000 1000 -990 -50
```

### Output

```text
NegativeInfinity
```

## Example 4

### Input

```text
1 2
1 0 0 2 0 0
-1 0
1 0 0 2 0 0 -7 3
```

### Output

```text
-4
```


## Constraints and Guarantees

$0\le N\le3000$ , $1\le M\le200$ , and $-10\le T_w\le10$ . Each world contains at most 50 portal entrances. Every world identifier is in $1,\ldots,M$ . Every input coordinate, opening time, and portal time change lies in $[-10000,10000]$ .

Redesign by Codex (GPT-6): supply the lower bound on the number of portals and bounds for start, destination, and exit fields; use one output line with an optional final newline; and state explicitly that leaving and returning is allowed when start and destination coincide. Movement, waiting, and portal availability retain their original rules.

| Score | Additional conditions |
| --- | --- |
| 100% | None |

Ten formal files, worth 10% each. [Generation guide](tests/README.md).
