# Harvest Office

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for estimation only)
- Actual time limit: twice the reference program's benchmark time on its slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds, then to the platform's supported granularity if coarser.
- Memory limit: 512 MB

## Story

Qingchuan Town's Harvest Office has published the exact shares of several crops in the total harvest, without publishing their quantities. The village head wants to infer the smallest possible total harvest. Quantities are whole units, and the announcement may omit some crops.

## Formal Problem Statement

You are given $n$ exact ratios $r_i$ , with $0\le r_i\le1$ and $0<\sum r_i\le1$ . Find the smallest positive integer $H$ such that every $Hr_i$ is a nonnegative integer. Unlisted crops may account for the remaining share.

Each ratio is represented by two strings separated by one space: a finite prefix $F$ and a repeating part $P$ . The prefix contains one integer digit, a decimal point, and zero or more fractional digits. The nonempty digit string $P$ repeats forever after $F$ . For example, `0.7 142857` means $0.7142857142857\ldots$ , and `0. 3` means $1/3$ . An all-zero repeating part represents a terminating decimal. Leading zeros, repeated copies of a period, and repeating $9$s are allowed.

## Input Format

The first line contains $n$ . Each of the next $n$ lines contains two strings $F,P$ .

## Output Format

Print the full decimal representation of the minimum total $H$ , without taking a modulus or using scientific notation.

## Example 1

### Input

```text
3
0.3 00
0.15 00
0.5 0
```

### Output

```text
20
```

## Example 2

### Input

```text
1
0.7 142857142857
```

### Output

```text
7
```

## Example 3

### Input

```text
3
0.33 3
0.3 33333
0. 3
```

### Output

```text
3
```

## Example 4

### Input

```text
2
0. 0
0. 9
```

### Output

```text
1
```

## Example Explanation

In example 1, a total of $20$ gives quantities $6,3,10$ , leaving $1$ unit for other crops. The ratio in example 2 is $5/7$ . All three representations in example 3 equal $1/3$ . The ratios in example 4 are $0$ and $1$ .

## Constraints and Guarantees

All inputs satisfy $1\le n\le10$ . The combined length of $F$ and $P$ on each line is at most $200$ , including the decimal point and excluding the separating space. The integer digit of $F$ is `0` or `1` ; all other characters follow the format above.

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
