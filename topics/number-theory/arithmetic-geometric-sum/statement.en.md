# A Certain Unscientific Arithmetic-Geometric Sum

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

There are $m$ independent queries. Each gives positive integers $l,r,a,b,c,d$ . Compute

$$\sum_{i=l}^{r}(a+ib)c^{d+ib}\pmod{10^9+7}$$

Interpret multiplication, exponentiation, and summation as exact integer operations, and output the least nonnegative residue. Both interval endpoints are included.

## Input Format

The first line contains $m$ . Each of the next $m$ lines contains six integers $l,r,a,b,c,d$ describing one query.

## Output Format

Print $m$ lines, one answer per query in input order. Each answer lies in $[0,10^9+6]$ .

## Samples

### Sample 1

### Input

```text
3
1 3 1 1 2 1
2 4 3 2 1 5
1 1 1 1 1 1
```

### Output

```text
96
27
2
```

### Sample 2

### Input

```text
1
1 1 1 500000003 4 1
```

### Output

```text
2
```

### Sample 3

### Input

```text
1
1000000000 1000000000 1000000000 1000000000 1000000000 1000000000
```

### Output

```text
612694578
```

## Sample Explanation

The first query of the first sample gives $2\cdot2^2+3\cdot2^3+4\cdot2^4=96$ . The second has base one and gives $7+9+11=27$ . The third has a single term and gives two.

The second sample is also a singleton interval. Its integer expression is $500000004\cdot4^{500000004}$ , whose residue modulo $10^9+7$ is two. The third sample covers a singleton at the numerical upper bounds.

## Constraints and Guarantees

For all inputs, $1\le m\le100000$ , $1\le l\le r\le10^9$ , and $1\le a,b,c,d\le10^9$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
