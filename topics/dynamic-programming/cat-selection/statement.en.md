# Choosing Cats

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, use twice the largest per-case median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A cat enthusiast wants to choose a fixed number of cats from a numbered list. Each cat has a score. The selected cats keep their number order, and earlier selections receive greater weights.

## Formal Problem Statement

There are $n$ cats, and cat $i$ has score $v_i$ . Select exactly $k$ distinct indices, written in increasing order as $i_1<i_2<\cdots<i_k$ . Their total score is

$$\sum_{j=1}^{k}v_{i_j}3^{k-j}$$

Find the largest possible total. Scores may be negative; negative scores do not allow selecting fewer cats. When $k=0$ , the empty selection has score zero. The selected cats may not be reordered.

## Input

The first line contains $n,k$ . The second line contains $n$ integers $v_1,v_2,\ldots,v_n$ . When $n=0$ , the second line is empty.

## Output

Output the maximum total score as an integer on one line.

## Samples

### Sample 1

### Input

```text
5 3
1 -1 -2 -3 -4
```

### Output

```text
4
```

### Sample 2

### Input

```text
5 3
1 -7 -6 -5 -8
```

### Output

```text
-14
```

### Sample 3

### Input

```text
0 0

```

### Output

```text
0
```

## Sample Explanation

In sample 1, select scores $1,-1,-2$ , giving $1\cdot9-1\cdot3-2=4$ .

In sample 2, select scores $1,-5,-8$ , giving $1\cdot9-5\cdot3-8=-14$ . A negative optimum is valid. Sample 3 selects the empty set.

## Constraints and Guarantees

For 100% of the data: $0\le k\le n\le25$ and $|v_i|\le1000$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
