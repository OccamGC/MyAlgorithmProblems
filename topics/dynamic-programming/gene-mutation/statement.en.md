# Gene Mutation

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 128 MB

## Story

After testing the cloning vats, Yuri's laboratory begins studying gene mutations. A gene is a sequence of digits. Mutation preserves the digits but changes each position's contribution to its ability. Given a standard gene and a numerical upper bound, count the genes whose mutated ability exceeds the standard.

## Formal Problem Statement

You are given two base parameters $n,m$ . Write a nonnegative integer $x$ in base $n$ , then replace each positional weight, a power of $n$ , with the corresponding power of $m$ . If its digits from least to most significant are $x_0,\ldots,x_{L-1}$ , its mutated ability is

$$F(x)=\sum_{i=0}^{L-1}x_i m^i$$

Each digit satisfies $0\le x_i<n$ . A digit may be at least $m$ : evaluate the formula directly, without requiring valid base-$m$ digits.

The standard gene $A$ and upper bound $B$ are both given in base $n$ . Count the integers $x$ satisfying $0\le x\le B$ and $F(x)>F(A)$ , modulo $10^9+7$ . The upper-bound comparison uses ordinary base-$n$ values; the ability comparison uses $F$ .

## Input Format

The first line contains $n,m,L_A,L_B$ . The second line contains the $L_A$ digits of $A$ , most significant first. The third contains the $L_B$ digits of $B$ in the same order.

## Output Format

Print the required count modulo $10^9+7$ .

## Sample 1

### Input

```text
10 2 1 3
0
1 0 0
```

### Output

```text
100
```

### Explanation

The standard ability is zero. Every integer from $1$ through $100$ has positive ability.

## Sample 2

### Input

```text
10 2 1 2
1
1 0
```

### Output

```text
9
```

### Explanation

Among integers from $0$ through $10$ , only $0,1$ have ability at most $F(A)=1$ , leaving $9$ valid integers.

## Sample 3

### Input

```text
10 2 1 3
5
1 0 0
```

### Output

```text
88
```

### Explanation

For integers from $0$ through $99$ , decimal digits $a,b$ give ability $2a+b$ . Exactly $6+4+2=12$ have ability at most $5$ . The ability of $100$ is $4$ , so it also fails. The answer is $101-13=88$ .

## Sample 4

### Input

```text
2 3 2 2
1 0
1 1
```

### Output

```text
1
```

### Explanation

The candidates are binary $0,1,10,11$ , with abilities $0,1,3,4$ . Only $11$ strictly exceeds the standard ability of $10$ .

## Constraints and Guarantees

- $2\le n,m\le30$ and $1\le L_A,L_B\le20000$ .
- Every digit is between $0$ and $n-1$ .
- Neither number has leading zeros; zero is represented by one digit $0$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
