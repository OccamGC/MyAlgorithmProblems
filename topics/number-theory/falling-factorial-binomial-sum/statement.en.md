# A Certain Unscientific Sum of Falling Factorials and Binomial Coefficients

Indicative time limit: 0.5 seconds. Memory limit: 128 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given positive integers $n,k$ , define the falling factorial

$$
i^{\underline{k}}=i(i-1)\cdots(i-k+1)
$$

If $i<k$ , this product contains a zero factor and is zero. Compute

$$
\sum_{i=1}^{n}i^{\underline{k}}\binom ni\pmod P,\qquad P=10^9+7
$$

Here $\binom ni$ counts subsets of $i$ distinct objects chosen from $n$ . Both object labels and the order of display positions distinguish arrangements.

## Input Format

One line containing `n k` .

## Output Format

Print one line containing the residue in $[0,P-1]$ .
## Sample 1

### Input

```text
3 2
```

### Output

```text
12
```


## Sample 2

### Input

```text
2 3
```

### Output

```text
0
```


## Sample 3

### Input

```text
5 5
```

### Output

```text
120
```


## Constraints and Scoring

$1\le n,k\le10^9$ . In particular, $n<P$ , but $k$ may exceed $n$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |

There are 10 formal files worth 10% each. See the [test recipes](tests/README.md).
