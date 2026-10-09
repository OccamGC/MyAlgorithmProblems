# Permuting Grilled Cuttlefish

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A cook repeatedly rearranges a row of distinct grilled cuttlefish using the same rule. He wants the fewest positive number of rearrangements that restores the original order.

## Formal Problem Statement

You are given a permutation $a$ of $1,\ldots,N$ . One operation on any permutation $b$ produces $b'$ satisfying

$$b'_{a_i}=b_i\qquad(1\le i\le N)$$

Thus the element at position $i$ moves to position $a_i$ . Repeat the operation using the same $a$ . Find the smallest positive number of operations that restores the initial permutation, and output this number modulo $998244353$ . Since all elements are distinct, the answer does not depend on the particular initial order $b$ .

## Input Format

The first line contains $N$ . The second contains $a_1,\ldots,a_N$ . There is exactly one test case.

## Output Format

Print the smallest positive operation count modulo $998244353$ on one line.

## Samples

### Sample 1

### Input

```text
5
2 1 4 5 3
```

### Output

```text
6
```

### Sample 2

### Input

```text
1
1
```

### Output

```text
1
```

### Sample 3

### Input

```text
6
2 3 4 1 6 5
```

### Output

```text
4
```

## Sample Explanation

In the first sample, positions $1,2$ return every two operations and positions $3,4,5$ every three. The first simultaneous return is after six operations. The second sample never changes, but the required count is positive, so its answer is one.

![The two permutation cycles in the first sample](assets/cycles.svg)

Arrows show the movement in one operation; numbers below the cycles are their lengths. In the third sample, the cycle lengths are four and two, so four operations restore both.

## Constraints and Guarantees

For all inputs, $1\le N\le10^6$ , and $a$ is a permutation of $1,\ldots,N$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
