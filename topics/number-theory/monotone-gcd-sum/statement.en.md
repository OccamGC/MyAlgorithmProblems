# A Certain Unscientific GCD Sum over Monotone Sequences

Indicative time limit: 1 seconds. Memory limit: 128 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given positive integers $n,m$ , compute

$$
\sum_{1\le x_m\le x_{m-1}\le\cdots\le x_1\le n}\gcd(x_1,\ldots,x_m)\pmod P
$$

Here $P=10^9+7$ . The sequence must be non-increasing, with equal adjacent values allowed. Count each sequence satisfying these conditions once.

![Length-two sequences over three values](assets/example.svg)

For $n=3,m=2$ , the six sequences are $(1,1),(2,1),(2,2),(3,1),(3,2),(3,3)$ , contributing $1,1,2,1,1,3$ , respectively.

## Input Format

One line containing `n m` .

## Output Format

Print one line containing the residue in $[0,P-1]$ .
## Sample 1

### Input

```text
2 2
```

### Output

```text
4
```


## Sample 2

### Input

```text
3 2
```

### Output

```text
9
```


## Sample 3

### Input

```text
1 100000
```

### Output

```text
1
```


## Constraints and Scoring

$1\le n\le10^9$ and $1\le m\le10^5$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |

There are 10 formal files worth 10% each. See the [test recipes](tests/README.md).
