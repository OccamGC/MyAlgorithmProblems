# Equipment Amplification

- Indicative time limit: 1.0 seconds.
- Judge time limit: twice the reference program’s largest per-case median on the target platform, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB.
- [Reference environment and measurements](../../../docs/评测环境与性能.md)

## Story

Equipment amplification may succeed or downgrade an item. A smith is investigating a success rule based on digits and wants to count the successful values in several ranges.

## Formal Problem Statement

Write a nonnegative integer $S$ in binary and decimal. In both representations, number positions from the least significant digit as $0,1,\ldots$ and pad with infinitely many leading zeros. Let the digits be $b_i$ and $d_i$ .

Call $S$ successful if $b_i\ge d_i$ at every position. For example, decimal $10$ is binary $1010$ and is successful. Decimal $1010$ is binary $1111110010$ ; its binary digit at position $3$ is smaller than its decimal digit, so it is unsuccessful.

For each of $q$ queries, given a nonnegative integer $N$ , count the successful integers satisfying $0\le S\le N$ . Apply the same rule to $0$ .

## Input

The first line contains $q$ . Each of the following $q$ lines contains a decimal integer $N$ .

## Output

Print $q$ lines, one count for each query.

## Sample 1

### Input

```text
2
55
6
```

### Output

```text
4
2
```

## Sample 2

### Input

```text
4
0
1
10
1010
```

### Output

```text
1
2
3
10
```

## Sample 3

### Input

```text
3
999999999999999999999999999999
111111111111111111111111111111
0
```

### Output

```text
715704
715704
1
```

## Sample Explanation

In sample 1, the successful values at most $55$ are $0,1,10,11$ . Those at most $6$ are $0,1$ .

## Constraints and Guarantees

$1\le q\le100$ ; $0\le N\le10^{30}-1$ . The source-code size limit is 50 KB.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
