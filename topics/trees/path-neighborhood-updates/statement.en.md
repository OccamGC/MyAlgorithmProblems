# Mental Omega Device

Time limit: 1 seconds. Memory limit: 512 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds; see the [environment](../../../docs/评测环境与性能.md).

## Story

The Mental Omega Device is nearly complete; only testing and final activation remain! To verify its reliability, you need to write a program that simulates its operation. The device can be modeled as a tree rooted at vertex $1$ , and its operation can be represented by the following operations.

## Formal Problem Statement

An $n$-vertex tree is rooted at vertex 1. All vertex values are initially zero. Define:

- $P(a,b)$ : the vertices on the simple path from $a$ to $b$ , including both endpoints.
- $H(a,b)$ : all vertices outside $P(a,b)$ that are adjacent to at least one path vertex. Count each vertex once.
- $T(a)$ : the rooted subtree of $a$ , including $a$ .

Process $m$ operations from this table in order.

| Operation | Set | Effect |
| --- | --- | --- |
| `1 a b v` | $P(a,b)$ | Add $v$ to every value |
| `2 a b v` | $H(a,b)$ | Add $v$ to every value |
| `3 a v` | $T(a)$ | Add $v$ to every value |
| `4 a b v` | $P(a,b)$ | Assign $v$ to every value |
| `5 a b v` | $H(a,b)$ | Assign $v$ to every value |
| `6 a v` | $T(a)$ | Assign $v$ to every value |
| `7 a b` | $P(a,b)$ | Query the maximum |
| `8 a b` | $H(a,b)$ | Query the maximum |
| `9 a` | $T(a)$ | Query the maximum |
| `10 a b` | $P(a,b)$ | Query the sum |
| `11 a b` | $H(a,b)$ | Query the sum |
| `12 a` | $T(a)$ | Query the sum |

Updating an empty neighborhood has no effect. Its sum is zero, and its maximum query prints the uppercase word `EMPTY` .

## Input Format

The first line contains `n m` . Each of the next $n-1$ lines contains a tree edge `u v` . The next $m$ lines contain operations. There is no initial-value array in the input.

## Output Format

For each operation numbered 7 through 12, print its integer answer or `EMPTY` as specified.

## Sample 1

### Input

```text
4 8
1 2
2 3
2 4
5 1 3 7
8 1 3
10 1 3
11 1 3
3 2 -2
9 2
12 2
7 1 3
```

### Output

```text
7
0
7
5
1
0
```

## Sample 2

### Input

```text
1 6
8 1 1
11 1 1
2 1 1 5
4 1 1 -7
9 1
12 1
```

### Output

```text
EMPTY
0
-7
-7
```

## Sample 3

### Input

```text
3 6
1 2
2 3
3 1 100000000
1 1 3 100000000
6 2 0
10 1 3
9 2
11 1 1
```

### Output

```text
200000000
0
0
```

## Sample Explanation

In Sample 1, $P(1,3)=\{1,2,3\}$ and $H(1,3)=\{4\}$ . Set vertex 4 to 7, then add $-2$ to $T(2)$ ; its three values become $-2,-2,5$ . Sample 2 illustrates an empty neighborhood.

![Illustration](assets/example.svg)

Blue vertices form $P(1,3)$ ; the orange vertex is its external neighborhood.

## Constraints and Scoring

$1\le n,m\le10^5$ , all vertex indices lie in $[1,n]$ , and each update value has absolute value at most $10^8$ . The input graph is a tree. Accumulated values and answers may exceed signed 32-bit integers.

Specifications redesigned by Codex (GPT-6): zero initial values, empty-neighborhood maximum and sum rules, and output for operations 7 through 12.

| Score | Additional constraints |
| --- | --- |
| 20% | $n\le30,\ m\le100$ |
| 30% | $n,m\le2000$ |
| 50% | No additional constraints |

There are 10 tests worth 10% each. See the [test recipes](tests/README.md).
