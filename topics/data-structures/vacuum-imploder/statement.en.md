# Vacuum Imploder

- Indicative time limit: **1.0 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge only supports coarser increments, round up again to a supported value.
- Memory limit: 128 MB

## Story

A battle laboratory is simulating how a Vacuum Imploder affects vehicle positions. Researchers number the vehicles, apply translations, reflections, or rotations to ranges of IDs, and inspect coordinates during the simulation. Maintain the resulting positions.

## Formal Problem Statement

There are $n$ points with fixed IDs $1$ through $n$ and initial coordinates $(x_i,y_i)$ . Process $m$ operations in input order. IDs do not change when points move. Every range $[l,r]$ is an inclusive range of IDs.

- `0 l r a` : replace $(x,y)$ by $(x+a,y)$ for these points.
- `1 l r a` : replace it by $(x,y+a)$ .
- `2 l r` : reflect across the $x$ axis, giving $(x,-y)$ .
- `3 l r` : reflect across the $y$ axis, giving $(-x,y)$ .
- `4 l r` : reflect across $x=y$ , giving $(y,x)$ .
- `5 l r` : reflect across $x=-y$ , giving $(-y,-x)$ .
- `6 l r b` : rotate counterclockwise by $b$ degrees about the origin.
- `7 i` : query the current coordinates of point $i$ .

Use Cartesian coordinates, with the $x$ axis pointing right and the $y$ axis pointing up. For $\theta=b\pi/180$ , the rotation gives

$$\bigl(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta\bigr)$$

![Panel A reflects point 2,1 across x=y to 1,2; panel B rotates the same starting point counterclockwise by 90 degrees to minus1,2](assets/transformations.svg)

Figure 1: Both panels independently start from $P=(2,1)$ . A applies operation `4` ; B applies operation `6` with angle $90$ . The circle P marks the starting point and the square Q marks the result.

Output every query result. After all operations, also output the final coordinates of every point in ID order.

## Input Format

The first line contains $n,m$ . The next $n$ lines contain the initial integer coordinates $x_i,y_i$ . The next $m$ lines describe operations in the formats above.

## Output Format

For each operation `7` , print two real numbers on one line. After all operations, print $n$ further lines, each containing the final coordinates of the corresponding point.

An absolute error of at most $0.05$ in each coordinate is accepted. The number of output rows is the number of queries plus $n$ , rather than the number of operations plus $n$ .

## Sample 1

### Input

```text
10 30
1470 7211
4180 -960
-2962 -5944
-9984 -6050
-6674 6625
-1462 -6774
-1042 -4576
-2533 1499
9729 5985
4800 179
5 4 10
2 6 10
4 5 6
5 4 9
5 4 8
0 3 4 63
5 1 1
6 2 6 99
0 4 8 35
4 6 10
5 1 2
7 7
4 3 5
4 1 7
0 9 10 87
1 5 10 -47
2 3 4
5 4 8
5 9 10
0 10 10 40
7 5
3 5 7
6 7 8 19
5 5 8
7 3
6 6 9 17
0 6 9 -38
3 3 6
2 1 10
6 3 7 46
```

### Output

```text
-1042.00 4611.00
-7581.21 -5534.39
6324.32 1933.46
7211.00 -1470.00
-294.28 4278.71
-3002.43 -5892.43
4646.96 -10709.75
-9297.98 1285.24
5216.82 4595.75
3868.25 2670.62
-2622.19 1421.68
11086.12 2948.46
266.00 4887.00
```

### Explanation

The first three rows answer the three queries; the next ten give the final positions.

## Sample 2

### Input

```text
2 6
2 1
-1 0
7 1
4 1 1
6 1 2 90
0 1 2 3
5 2 2
7 2
```

### Output

```text
2.00 1.00
1.00 -3.00
1.00 1.00
1.00 -3.00
```

### Explanation

The first point becomes $(1,2)$ , then $(-2,1)$ , then $(1,1)$ . The second point ends at $(1,-3)$ .

## Constraints and Guarantees

- $1\le n,m\le50000$ .
- Initial coordinates satisfy $\lvert x_i\rvert,\lvert y_i\rvert\le10000$ .
- $1\le l\le r\le n$ , $1\le i\le n$ , $-100\le a\le100$ , and $0\le b\le360$ .
- All input values are integers. There may be no queries; final coordinates must still be printed.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
