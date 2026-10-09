# A Certain Unscientific Count of Monotone Sequences

- Reference time limit: 0.5 seconds (environment R30; estimate only).
- Actual time limit: twice the standard program’s baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given positive integers $n,m$ , count integer sequences with $1\le x_1\le x_2\le\cdots\le x_n\le m$ , modulo $p=998244353$ . Two sequences differ if they have different values at any position.

## Input Format

One line contains $n,m$ .

## Output Format

Print the number of sequences modulo $p$ .

## Sample 1

### Input

```text
3 2
```

### Output

```text
4
```

### Explanation

The sequences are $(1,1,1),(1,1,2),(1,2,2),(2,2,2)$ .

![Each group of three circles represents one sequence; numbers are labels.](assets/example.svg)

Each group of three circles represents one sequence; numbers are labels.

## Sample 2

### Input

```text
1 5
```

### Output

```text
5
```

### Explanation

The single element can use any available label.

## Sample 3

### Input

```text
5 1
```

### Output

```text
1
```

### Explanation

Every position must contain one.

## Constraints and Guarantees

$1\le n,m\le2000$ . All inputs are integers.

### Test Groups

| Score | Additional restriction |
| --- | --- |
| 20% | $n,m\le10$ |
| 30% | $\min(n,m)\le50$ |
| 50% | No additional restriction |

[Reference environment and measurements](../../../docs/评测环境与性能.md)
