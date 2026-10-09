# Spiral Numbers

Estimated time limit: 0.5 seconds. Memory limit: 256 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

After reading Junji Ito's Uzumaki manga, you are deeply shaken. Spirals seem rather complicated, and so do spaces of two or more dimensions. So you decide to define a “spiral number” and determine whether a given nonnegative integer is one.

Your definition is simple: write the number in decimal without unnecessary leading zeroes. If every pair of digits at corresponding positions, working inward from the two ends, is equal, it is a spiral number.

## Formal Problem Statement

Given nonnegative integers, ignore leading zeroes in the input and determine whether each decimal representation reads identically from left to right and from right to left. The representation of zero is `0` , so zero is a spiral number.

## Input Format

The first line contains an integer $T$ . Each of the next $T$ lines contains a nonempty string of decimal digits representing a nonnegative integer $X$ . Leading zeroes are allowed.

## Output Format

For each integer, print `Y` if it is a spiral number, or `N` otherwise, on its own line. The letters are uppercase.

## Samples

### Sample 1

### Input

```text
10
1453
1026
1212
114514
666
1919810
12345678987654321
123456789987654321
11011
010
```

### Output

```text
N
N
N
N
Y
N
Y
Y
Y
N
```

### Sample 2

### Input

```text
7
0
000000000000000000
00100
00121
0007
999999999999999999
100000000000000000
```

### Output

```text
Y
Y
N
Y
Y
Y
N
```

## Sample Explanation

In Sample 1, `1212` is not a spiral number, and `010` represents ten, which is not a spiral number. In Sample 2, an all-zero string represents zero, while `00121` represents the spiral number one hundred and twenty-one.

## Constraints and Guarantees

For 100% of the data: $1\le T\le1000$ and $0\le X<10^{18}$ . Each input string has between $1$ and $18$ digits, including leading zeroes.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
