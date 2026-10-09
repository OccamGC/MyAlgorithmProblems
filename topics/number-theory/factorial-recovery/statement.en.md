# Factorial Recovery

- Indicative time limit: **0.5 seconds** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Actual limit: measure the reference solution on the target system, take the largest median time over test files, multiply by 2, and round up to a multiple of 0.5 seconds.
- Memory limit: **128 MB**.

## Story

A computer-shop customer stored the factorial of an integer on a hard drive. A virus damaged the beginning of the file, but a suffix of its decimal digits is still correct. The technician knows the original integer and the surviving suffix, and wants to restore the complete factorial.

## Formal Problem Statement

You are given nonnegative integers $n,k$ and a decimal string $s$ consisting of exactly the last $k$ digits of $n!$ .

Let $D$ be the number of decimal digits of $n!$ . It is guaranteed that $0\le D-k\le15$ : at most the first $15$ digits are missing. Output the complete decimal representation of $n!$ .

By convention, $0!=1$ . The string $s$ may contain leading zeros. When $k=0$ , it is empty.

## Input Format

The first line contains two integers $n,k$ . The second line contains the string $s$ of exactly $k$ digits; it is an empty line when $k=0$ .

## Output Format

Output the complete decimal representation of $n!$ on one line, without leading zeros.

## Sample 1

### Input

```text
9 1
0
```

### Output

```text
362880
```

## Sample 2

### Input

```text
20 17
32902008176640000
```

### Output

```text
2432902008176640000
```

## Sample 3

### Input

```text
20 4
0000
```

### Output

```text
2432902008176640000
```

## Sample 4

### Input

```text
0 0

```

### Output

```text
1
```

## Sample Explanation

In sample 1, $9!=362880$ , whose final digit is $0$ .

Sample 2 preserves the last $17$ digits of $20!$ ; the missing prefix is `24` . Sample 3 contains four zero digits in its suffix, and all four must be retained when reading it. In sample 4, the suffix is empty and the answer is still $0!=1$ .

## Constraints and Guarantees

For all test cases: $0\le n\le500000$ and $\max(0,D-15)\le k\le D$ , where $D$ is the number of decimal digits of $n!$ . The supplied suffix is correct and has exactly $k$ digits.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
