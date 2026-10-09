# Extremes after Merging Two Digits

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A number gallery has a display that can merge two digits. Its curator wants the largest and smallest numbers that can appear after exactly one operation.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

A positive base-$k$ integer has $n$ digits $a_1,\ldots,a_n$ , from most significant to least significant. Choose positions $i<j$ exactly once, set $s=a_i+a_j$ , and perform the following simultaneous update:

- If $s\ge k$ , replace digit $i$ by one and digit $j$ by $s-k$ . All other positions stay unchanged.
- If $s<k$ , delete digit $i$ and replace the digit at the original position $j$ by $s$ . All remaining digits retain their relative order. Deleting a digit shortens the number; it does not replace that digit by zero.

Remove all leading zeros afterwards. Find the maximum and minimum resulting integers. The two answers may use different pairs of positions.

## Input Format

The first line contains $n,k$ . The second contains the space-separated digits $a_1,\ldots,a_n$ , each written as a decimal integer. Digit $a_1$ is the most significant.

## Output Format

Print the maximum on the first line and the minimum on the second. On each line, print the resulting base-$k$ digits from most significant to least significant, representing each digit as a decimal integer and separating adjacent digits by one space. Omit leading zeros.

## Samples

### Sample 1

### Input

```text
4 10
1 8 9 9
```

### Output

```text
1 8 9 0
9 9 9
```

### Sample 2

### Input

```text
5 10
7 0 0 1 1
```

### Output

```text
7 0 1 1
1 8
```

### Sample 3

### Input

```text
3 10
1 2 3
```

### Output

```text
3 3
1 5
```

## Sample Explanation

In sample one, the maximum merges positions one and four: the leading one stays unchanged and the last digit becomes zero. The minimum merges positions one and two, producing three nines. In sample two, merging positions one and five for the minimum removes the highest digit and two leading zeros, giving $1,8$ . No pair carries in sample three.

## Constraints and Guarantees

$2\le n\le10^6$ , $2\le k\le10^9$ , $1\le a_1<k$ , $0\le a_i<k$ . The input contains at most $21\times10^6$ characters.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
