# Clue Generator

Estimated time limit: 2.5 seconds. Memory limit: 1024 MB.

The limit is 2 times the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

> “Old PJ is sneaky! Something fishy must have happened!”

Readers may prove for themselves that UNR 2018 Day 2, Problem 3 is a sequence of length $N$. Each element is an inteRger with absolute value at most $10^9$.

Old ZY discovers that a zero-sum interval can produce clues. With enough clues, he can build a Clue Generator. Define an interval's clue intensity as the sum of the lengths of all zero-sum subarrays within it.

Old ZY now selects $M$ intervals from the sequence and asks for the clue intensity of each. To prevent offline processing, every query is encrypted using the previous answer, which is taken to be zero before the first query.

## Formal Problem Statement

Given an integer sequence $a_1,\ldots,a_N$ , answer $M$ queries. For a decoded inclusive interval $[l,r]$ , the answer is

$$\sum_{l\le s\le t\le r}\left[\sum_{j=s}^{t}a_j=0\right](t-s+1).$$

Brackets denote an indicator: one when the condition holds, zero otherwise. Thus, the answer sums the lengths of all nonempty zero-sum subarrays contained in the query interval.

Let `last` be the preceding answer, initially zero. After reading raw integers $u,v$ , compute

$$x=((u\mathbin{\mathrm{XOR}}\mathrm{last})\bmod N)+1,\qquad y=((v\mathbin{\mathrm{XOR}}\mathrm{last})\bmod N)+1,$$

then set $l=\min(x,y)$ and $r=\max(x,y)$ . `XOR` is bitwise exclusive OR on nonnegative integers. Use the complete previous answer without truncating it to thirty-two bits. Print the current answer and update `last` . Queries do not modify the sequence, and answers are not reduced modulo anything.

## Input Format

The first line contains $N,M$ . The second contains $a_1,\ldots,a_N$ . Each of the next $M$ lines contains two **raw, undecoded** integers $u,v$ .

## Output Format

Print $M$ lines containing the answers in query order.

## Samples

### Sample 1

### Input

```text
4 2
1 -1 2 -2
0 3
0 0
```

### Output

```text
8
0
```

### Sample 2

### Input

```text
7 2
0 0 0 0 0 0 0
0 6
0 6
```

### Output

```text
84
56
```

### Sample 3

### Input

```text
1 2
0
0 0
1000000000 1000000000
```

### Output

```text
1
1
```

## Sample Explanation

The first query of sample one is $[1,4]$ . Its zero-sum subarrays are $[1,2]$ , $[3,4]$ and $[1,4]$ , with total length eight. With `last=8` , the next query decodes to $[1,1]$ and answers zero. Sample two first queries seven zeros, giving $7\times8\times9/6=84$ . The next query decodes to $[1,6]$ and gives fifty-six. Sample three always queries its only zero.

## Constraints and Guarantees

$1\le N,M\le10^5$ , $|a_i|\le10^9$ , $0\le u,v\le10^9$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
