# A Certain Unscientific Polynomial-Weighted Geometric Sum with Updates

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Let $P=10^9+7$ . Given a fixed base $a$ and coefficients $b_0,\ldots,b_k$ , maintain

$$F(n)=\sum_{i=1}^{n}a^i\left(\sum_{j=0}^{k}b_j i^j\right)\pmod P.$$

Print the initial value, then process $m$ operations in order and print the value after each:

- `1 n` : replace the upper summation bound with the new $n$ .
- `2 j b` : replace coefficient $b_j$ with $b$ .

The base $a$ and maximum allowed degree $k$ remain fixed. Coefficients may be zero. Every exponent $i$ is positive, so $a=0$ gives zero weight for every term; $i^0=1$ . Print nonnegative residues modulo $P$ .

## Input Format

The first line contains `n m k a` . The second gives $k+1$ coefficients $b_0,\ldots,b_k$ . The next $m$ lines contain operations in the formats above.

## Output Format

Print $m+1$ lines: the initial value, then the value after each update.

## Sample 1

### Input

```text
3 3 1 2
1 1
1 2
2 0 0
1 1
```

### Output

```text
48
16
10
2
```

## Sample 2

### Input

```text
3 2 2 1
0 0 1
1 4
2 2 0
```

### Output

```text
14
30
0
```

## Sample 3

### Input

```text
1000000000 2 1 0
1000000006 1000000006
1 1
2 0 7
```

### Output

```text
0
0
0
```

## Sample Explanation

In sample 1, the initial value is $2(1+1)+4(1+2)+8(1+3)=48$ . Changing the bound to 2 gives 16, setting the constant term to zero gives 10, and finally setting the bound to 1 gives 2. Sample 2 is a sum of squares; sample 3 has zero base.

![The three weighted polynomial terms in sample 1 sum to 48.](assets/example.svg)

The three weighted polynomial terms in sample 1 sum to 48.

## Constraints and Scoring

Initially and after updates, $1\le n\le10^9$ ; $1\le m\le10000$ , $1\le k\le200$ , $0\le a,b_j,b<P$ , and coefficient indices satisfy $0\le j\le k$ .

Specifications redesigned by Codex (GPT-6): the fixed base input, coefficient bounds, update indices, and the initial output.

| Score | Additional constraints |
| --- | --- |
| 20% | $k\le4,\ m\le30$ , and every $n\le20$ |
| 30% | $k\le30,\ m\le300$ , and every $n\le1000$ |
| 50% | No additional constraints |

## Resource Limits

Time: 0.5 seconds. Memory: 128 MiB. The limit is twice the slowest standard-program median over five runs per input, rounded up to 0.5 seconds.

[Solution](solution.en.md) · [Measurement environment](../../../docs/评测环境与性能.md) · [Measurements](../../../docs/benchmark-R33.json)
