# One Shared Charger

Time limit: 0.5 seconds. Memory limit: 128 MiB. See the [reference environment and measurements](../../../docs/评测环境与性能.md).

## Story

An exam allows laptops, but the candidates have only one shared charger. The organizer can choose its fixed power and wants the smallest power that keeps every laptop running until the exam ends.

## Formal Problem Statement

There are $n$ devices. Device $i$ starts with energy $a_i$ and consumes $b_i$ per minute. The exam lasts $m$ minutes, numbered $0,\ldots,m-1$ .

Choose a fixed nonnegative integer power $X$ . At the start of each minute, charge at most one device by $X$ energy units; then every device consumes its $b_i$ . Only end-of-minute energy is checked. Every device must have nonnegative energy at every such check; zero is allowed. Battery capacity is unlimited, and a device may be charged in several different minutes.

Find the smallest feasible $X$ , or print $-1$ if no power is feasible.

## Input Format

The first line contains `n m` . The second contains the $n$ values $a_i$ . The third contains the $n$ values $b_i$ .

## Output Format

Print the minimum power, or $-1$ , on one line.

## Sample 1

### Input

```text
7 7
75 96 111 18 26 5 67
11 14 16 13 4 1 11
```

### Output

```text
73
```

## Sample 2

### Input

```text
10 10
6461509295841908 38 62 49 89 113 8 7 26 1
4 6 14 6 12 19 11 2 9 1
```

### Output

```text
91
```

## Sample 3

### Input

```text
10 6
5418305720373823 1522295577184932 68 14 9738943766183541 12 28 64942086170874 58 50
13 5 19 10 14 18 6 7 11 17
```

### Output

```text
96
```

## Sample 4

### Input

```text
7 8
6826325183988349 2889182368658500 114922354894933 144 73 6452986168515306 3965505639613541
5 12 19 20 12 15 15
```

### Output

```text
6
```

## Sample 5

### Input

```text
2 2
0 0
1 1
```

### Output

```text
-1
```

## Sample 6

### Input

```text
2 5
0 10
0 2
```

### Output

```text
0
```

## Sample Explanation

In Sample 5, both devices need charging in minute zero, but only one can be charged, so no solution exists. In Sample 6, the initial energy suffices and the answer is zero.

![Example for one device: $a=1,b=2,X=3$ . Charging in minutes 0 and 1 gives end-of-minute energies $2,3,1$ .](assets/example.svg)

Example for one device: $a=1,b=2,X=3$ . Charging in minutes 0 and 1 gives end-of-minute energies $2,3,1$ .

## Constraints and Scoring

$1\le n,m\le5\cdot10^5$ , $0\le a_i\le10^{16}$ , and $0\le b_i\le10^9$ . There are 40 test cases worth 2.5% each.

| Score | Additional constraints |
| --- | --- |
| 30% | $n,m\le50,\ b_i\le5$ |
| 20% | $n,m\le200,\ b_i\le20$ |
| 20% | $n,m\le200$ |
| 20% | $n,m\le50000$ |
| 10% | No additional constraints |
