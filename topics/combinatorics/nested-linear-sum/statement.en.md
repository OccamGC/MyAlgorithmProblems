# A Certain Unscientific Weighted Sum of First Values of Monotone Sequences

- Reference time limit: 0.5 seconds (environment R30; estimate only).
- Actual time limit: twice the standard program’s baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given integers $n,m,k,c$ , assign weight $kx_1+c$ to each integer sequence satisfying $1\le x_1\le x_2\le\cdots\le x_n\le m$ . Find the sum of these weights modulo $p=998244353$ .

$$\sum_{x_n=1}^{m}\sum_{x_{n-1}=1}^{x_n}\cdots\sum_{x_1=1}^{x_2}(kx_1+c)\pmod p$$

For $n=1$ there is one sum. For $m=0$ there are no valid sequences and the answer is zero.

## Input Format

One line contains $n,m,k,c$ : the length, largest section number, first-value coefficient, and constant term.

## Output Format

Print one integer, the remainder in $[0,p-1]$ .

## Sample 1

### Input

```text
2 3 2 1
```

### Output

```text
26
```

### Explanation

The six sequences have weights $3,3,3,5,5,7$ , totalling $26$ .

![The six valid sequences and their weights.](assets/example.svg)

The six valid sequences and their weights.

## Sample 2

### Input

```text
1 0 9 4
```

### Output

```text
0
```

### Explanation

There are no valid sequences.

## Sample 3

### Input

```text
1 998244353 0 1
```

### Output

```text
0
```

### Explanation

There are $998244353$ one-element sequences, each of weight one.

## Constraints and Guarantees

$1\le n\le10^7$ ; $0\le m,k,c\le10^9$ . All inputs are integers.

### Test Groups

| Score | Additional restriction |
| --- | --- |
| 20% | $n,m\le12$ |
| 30% | $m\le2000$ |
| 50% | No additional restriction |

[Reference environment and measurements](../../../docs/评测环境与性能.md)
