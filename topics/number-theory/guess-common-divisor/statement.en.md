# Guess the Common Divisor

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A warehouse holds several batches of parts. Its manager wants to choose a specified number of batches and pack each batch exactly into boxes of one common capacity. The capacity should be as large as possible without exceeding its limit.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given a sequence of $n$ positive integers $a_1,a_2,\ldots,a_n$ and integers $m,k$ , find the largest positive integer $x\le k$ for which exactly $m$ distinct indices can be selected such that $x\mid a_i$ for every selected index $i$ .

Repeated values count separately at their respective indices. Selecting exactly $m$ entries is equivalent to having at least $m$ entries divisible by $x$ . When $m=0$ , the empty selection is allowed, so every integer satisfying $1\le x\le k$ meets the divisibility condition.

## Input

The first line contains $n,m,k$ .

The second line contains $n$ positive integers $a_1,a_2,\ldots,a_n$ . When $n=0$ , this line is empty.

## Output

Output the largest valid $x$ on one line.

## Samples

### Sample 1

### Input

```text
5 2 10
12 18 20 30 7
```

### Output

```text
10
```

### Sample 2

### Input

```text
0 0 9

```

### Output

```text
9
```

### Sample 3

### Input

```text
4 3 8
36 36 25 36
```

### Output

```text
6
```

## Sample Explanation

In sample 1, select $20$ and $30$ to obtain the answer $10$ .

In sample 2, select the empty set; the answer is the capacity limit $9$ .

In sample 3, select the three different positions containing $36$ . Their largest common divisor at most $8$ is $6$ . Repeated values must not be deduplicated.

## Constraints and Guarantees

For 100% of the data: $0\le\lfloor n/5\rfloor\le m\le n\le1000$ , $1\le k\le10^9$ , and $1\le a_i\le10^9$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
