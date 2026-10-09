# Magic Bread

- Indicative time limit: **1.0 s** ([environment and measurements](../../../docs/评测环境与性能.md)).
- Deployment time limit: measure the reference program in the target environment, multiply the slowest case's median time by 2, and round up to the next 0.5 seconds.
- Memory limit: **512 MB**.

## Story

The farm grows two kinds of magical wheat, called Five Hues and Six Colors, represented by $0$ and $1$ . The fields form a ring, with an automatic crafting unit beside each field.

The machine divides its wheat sequence into blocks of a fixed length. It works only when every block is a palindrome and all blocks are identical. The farmer will walk at most one lap and wants the longest usable segment with each field as an endpoint.

## Formal Problem Statement

You are given a binary string $s$ of length $n$ . Positions $1,\ldots,n$ form a ring in that order.

For every position $i$ and level $j$ with $1\le j\le K$ , consider a nonempty consecutive ring segment having $i$ as **either endpoint**. You may start at $i$ and traverse in either direction. Its length must not exceed $n$ , and no position may be used twice.

A sequence of length $\ell$ can make level-$j$ bread if and only if $j$ divides $\ell$ and, when divided into consecutive blocks of $j$ characters starting at the chosen endpoint, every block is identical and is a palindrome. A palindrome reads the same forward and backward.

Let $a_{i,j}$ be the largest possible length, or $0$ if none exists. For each $i$ , output

$$X_i=\bigoplus_{j=1}^{K}\bigl(j\cdot a_{i,j}\bigr)$$

Here $\oplus$ denotes bitwise XOR. Compute the products before applying XOR.

## Input Format

The first line contains $n,K$ .

The second line contains a string $s$ of length $n$ , consisting only of `0` and `1` .

## Output Format

Print $n$ lines. Line $i$ contains the integer $X_i$ .

## Sample 1

### Input

```text
5 5
10101
```

### Output

```text
22
24
8
24
22
```

## Sample 2

### Input

```text
6 6
110011
```

### Output

```text
42
21
34
34
21
42
```

## Sample 3

### Input

```text
1 20
0
```

### Output

```text
1
```

## Sample Explanation

In sample 1, the five lengths for position $1$ are $(2,2,3,0,5)$ , giving $X_1=2\oplus4\oplus9\oplus0\oplus25=22$ . A length-$2$ segment can go backward from position $1$ to position $5$ , producing `11` .

![The sample ring and a segment crossing the numbering boundary from 1 to 5](assets/wheat-ring.svg)

Numbers label positions, and the boxes beneath them show wheat types. The arrow illustrates selecting the segment from position $1$ toward position $5$ .

In sample 2, the six lengths for position $2$ are $(4,4,3,4,0,0)$ ; multiplying by their levels and XORing gives $21$ . In sample 3, only level $1$ is possible.

## Constraints and Guarantees

For all test cases: $1\le n\le1000000$ and $1\le K\le20$ . It is possible that $K>n$ ; every $a_{i,j}$ with $j>n$ is then $0$ .

| Score | Additional restrictions |
| --- | --- |
| 100% | None |
