# Minimum-Weighted Subarray Sums

Estimated time limit: 1.5 seconds. Memory limit: 2048 MB.

The limit is 2 times the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A report aggregates every contiguous segment of a sequence of readings. A segment contributes its minimum reading multiplied by its sum. Negative readings participate in both calculations.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given an integer sequence $A_1,\ldots,A_N$ , compute

$$\sum_{1\le L\le R\le N}\left(\min_{L\le i\le R}A_i\right)\left(\sum_{i=L}^{R}A_i\right).$$

Every nonempty contiguous subarray contributes once, including single-element subarrays. Print the exact integer without a modulus. The answer may be negative.

## Input Format

The first line contains $N$ . The second contains $A_1,\ldots,A_N$ .

## Output Format

Print the specified sum as one integer.

## Samples

### Sample 1

### Input

```text
7
3 4 2 -1 5 7 6
```

### Output

```text
226
```

### Sample 2

### Input

```text
5
1 1 -1 1 1
```

### Output

```text
-1
```

### Sample 3

### Input

```text
2
1000000000 1000000000
```

### Output

```text
4000000000000000000
```

## Sample Explanation

The first sample has total contribution $226$ . In the second, the totals for lengths one through five are $5,4,-3,-4,-3$ , giving $-1$ . In the third, each singleton contributes $10^{18}$ , and the length-two subarray contributes $2\times10^{18}$ .

## Constraints and Guarantees

$1\le N\le10^7$ , $-10^9\le A_i\le10^9$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
