# A Certain Unscientific Prefix Sum of GCDs in Boxes

Indicative time limit: 2 seconds. Memory limit: 128 MiB. Recalibrate as twice the slowest standard median in the target environment, rounded up to 0.5 seconds. See the [environment](../../../docs/评测环境与性能.md).

## Story

While working through the paper for Academy City's Zeroth High School Mock Exam, Xiao A came across an interesting mathematics problem and decided to use his knowledge of algorithms to expand its input bounds.

## Formal Problem Statement

Given positive integers $n,m$ , compute

$$
\sum_{t=1}^{n}\ \sum_{x_1=1}^{t}\cdots\sum_{x_m=1}^{t}\gcd(x_1,\ldots,x_m)\pmod P
$$

Here $P=10^9+7$ . For each bound $t$ , enumerate all ordered $m$-tuples of coordinates. Coordinates may be equal. A tuple can occur for several different bounds $t$ ; count its contribution separately for each occurrence.

![GCD values in two-dimensional boxes of side one and two](assets/example.svg)

For $n=m=2$ , the side-one box contributes 1 and the side-two box contributes $1+1+1+2=5$ , giving 6 in total.

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
6
```


## Sample 2

### Input

```text
3 1
```

### Output

```text
10
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
