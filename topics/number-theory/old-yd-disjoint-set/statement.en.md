# Old yd and Disjoint Sets

Estimated time limit: 2 seconds. Memory limit: 512 MB.

The limit is 4 times the slowest median runtime of the reference program on the target platform, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

The multiplier is four to provide at least twofold measured headroom for the single-inverse-table option on the full range. See the [solution](solution.en.md) for the time and space comparison.

## Story

> “A parent's parent is still a parent — disjoint sets with path compression.”

Old yd's deep study of disjoint sets is impressive, from his maxims about family ethics and path compression to his skill with weighted disjoint sets. So he invents a function $f(x)$ on the nonnegative real numbers: it equals the constant $A$ below $B$, and from $B$ onward it follows the recurrence $C f(x-1)+D f(x-e)$, where $e$ is the base of the natural logarithm.

He has already written a brute-force program that computes $f(n)$ modulo $10^9+7$. Now he wants you to write a reference solution to check whether his brute-force program is correct. He has $M$ queries for you to answer.

## Formal Problem Statement

Given integers $A,B,C,D$ , define a function on the nonnegative real numbers by

$$f(x)=\begin{cases}A,&0\le x<B,\\C f(x-1)+D f(x-e),&x\ge B.\end{cases}$$

Here $e=\sum_{j=0}^{\infty}1/j!$ is the base of the natural logarithm, interpreted as its exact mathematical value. The guarantee $B\ge3>e$ keeps every recursive argument nonnegative. Every recursive branch terminates.

For each of $M$ integer queries $n$ , find the least nonnegative residue of $f(n)$ modulo $10^9+7$ . All queries share the same $A,B,C,D$ .

## Input Format

The first line contains $A,B,C,D$ . The second contains $M$ . Each of the next $M$ lines contains one integer $n$ .

## Output Format

Print $M$ lines containing the modular answers in query order.

## Samples

### Sample 1

### Input

```text
1 3 7 4
5
3
10
137
65
38
```

### Output

```text
11
10153081
399262231
911840238
777440793
```

### Sample 2

### Input

```text
2 5 1 1
2
5
6
```

### Output

```text
4
6
```

### Sample 3

### Input

```text
1000000000 10000000 1000000000 1000000000
1
10000000
```

### Output

```text
98
```

## Sample Explanation

In the first sample, $f(3)=7f(2)+4f(3-e)=7+4=11$ . In the second, $f(5)=4$ and $f(6)=f(5)+f(6-e)=4+2=6$ . The third expands once, giving exactly $2\times10^{18}$ and residue $98$ .

## Constraints and Guarantees

$1\le A,C,D\le10^9$ , $3\le B\le n\le10^7$ , $1\le M\le5$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
