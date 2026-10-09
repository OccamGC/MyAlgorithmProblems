# Factorio: Circuit Board Test

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A circuit-board test station in Factorio receives an integer signal. A signal passes only when all required tests succeed.

## Formal Problem Statement

For an integer $x$ , define three predicates:

- $p(x)$ : $x$ is a positive integer.
- $q(x)$ : $x^3<3000$ and $x^2\ge10$ .
- $h(x)$ : $x^2>2000$ or $x^2<700$ .

Let $P(x)=p(x)\land q(x)\land h(x)$ . Here $\land$ denotes logical AND; OR is true when at least one condition is true.

Determine whether $P(x)$ is true for every supplied $x$ . Powers and comparisons are defined using exact mathematical integers.

## Input Format

The first line contains a nonnegative integer $T$ , the number of tests. Each of the next $T$ lines contains one integer $x$ .

## Output Format

Print $T$ lines. Print the uppercase letter `T` when $P(x)$ is true and the uppercase letter `F` otherwise. For $T=0$ , print nothing.

## Examples

### Example 1

### Input

```text
5
0
-1
1
101
5
```

### Output

```text
F
F
F
F
T
```

### Example 2

### Input

```text
4
3
4
14
15
```

### Output

```text
F
T
T
F
```

### Example 3

### Input

```text
3
-1000000000000000000
1000000000000000000
10
```

### Output

```text
F
F
T
```

## Example Explanation

Only $x=5$ satisfies all conditions in the first example. The second illustrates the boundaries: the square of $3$ is below $10$ , the cube of $15$ is at least $3000$ , and both $4$ and $14$ satisfy all three predicates.

The third shows that inputs may exceed the range in which direct machine-integer powers are safe. The answer must remain exact.

## Constraints and Guarantees

$0\le T\le1000$ and $|x|\le10^{18}$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
