# A Certain Unscientific Repeated Geometric Sum

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given positive integers $n,m,a$ , define

$$F_0(x)=\sum_{i=x}^{2x}a^i,\qquad F_t(x)=\sum_{y=1}^{x}F_{t-1}(y)\quad(t\ge1,x\ge1).$$

Find the least nonnegative residue of $F_m(n)$ modulo $2147483647$ . Both endpoints of every sum are included.

## Input Format

One line contains $n,m,a$ .

## Output Format

Print one integer in $[0,2147483646]$ .

## Samples

### Sample 1

### Input

```text
3 2 2
```

### Output

```text
194
```

### Sample 2

### Input

```text
3 2 1
```

### Output

```text
16
```

### Sample 3

### Input

```text
1 1000000 7
```

### Output

```text
56
```

## Sample Explanation

The first case starts with $6,28,120$ . One aggregation gives $6,34,154$ , and the third entry after two aggregations is $194$ . The second starts with $2,3,4$ , giving $16$ after two aggregations. Only the first position matters in the third case, so every aggregation preserves $7+49=56$ .

## Constraints and Guarantees

$1\le n,a\le2\times10^9$ , $1\le m\le10^6$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
