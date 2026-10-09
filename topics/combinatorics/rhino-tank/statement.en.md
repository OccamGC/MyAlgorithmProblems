# Rhino Tank

- Indicative time limit: 0.5 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 512 MB

## Story

The Rhino Tank design team tests each new vehicle using a feature matrix. Features are generated independently, although different positions may use different probability distributions. Every row and every column must contain variation. Compute the probability that a vehicle passes.

## Formal Problem Statement

Generate an $n\times n$ matrix whose entries belong to $\{1,\ldots,m\}$ . For position $(i,j)$ , nonnegative integer weights $w_{i,j,1},\ldots,w_{i,j,m}$ specify

$$p_{i,j,c}=\frac{w_{i,j,c}}{\sum_{d=1}^{m}w_{i,j,d}}$$

as the probability of value $c$ . All positions are independent. A matrix passes if no row has all entries equal and no column has all entries equal. Find its probability of passing.

Let $P=10^9+7$ . For a probability $a/b$ , output $a\cdot b^{-1}\bmod P$ , where $b^{-1}$ is the multiplicative inverse modulo $P$ . The bounds ensure every position's weight sum lies between $1$ and $P-1$ , so this representation exists.

## Input Format

The first line contains $n,m$ . The next $n^2$ lines describe positions in row-major order, from top to bottom and left to right. Each contains $m$ integers: the weights for values $1$ through $m$ .

## Output Format

Print the probability of passing, represented modulo $P$ .

## Sample 1

### Input

```text
2 2
1 1
1 1
1 1
1 1
```

### Output

```text
125000001
```

### Explanation

Of the $16$ equally likely matrices, only the two checkerboard patterns pass. Their probability is $1/8$ , represented by $125000001$ .

## Sample 2

### Input

```text
3 3
1 1 2
3 2 1
0 0 3
1 0 2
0 3 5
1 2 3
6 7 9
3 2 1
1 1 1
```

### Output

```text
875789148
```

### Explanation

The matrix is $3	imes3$ with three possible values per position, each generated independently according to its weights.

## Sample 3

### Input

```text
1 2
3 7
```

### Output

```text
0
```

### Explanation

With one position, the only row and column are both constant, so the probability of passing is zero.

## Constraints and Guarantees

- $1\le n\le5$ and $1\le m\le7$ .
- $0\le w_{i,j,c}\le100000$ , and each position has at least one positive weight.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
