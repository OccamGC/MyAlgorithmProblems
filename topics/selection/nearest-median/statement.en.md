# Values Nearest to the Median

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is twice the slowest per-case median time of the standard program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [evaluation notes](../../../docs/评测环境与性能.md).

## Story

An observation station receives positive and negative measurements and keeps several records closest to the center. When two records are equally far from the center, it prefers the larger value.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given $n$ integers $a_1,\ldots,a_n$ and $k$ , sort all values into $b_1\le\cdots\le b_n$ . Define the median as

$$m=\begin{cases}b_{(n+1)/2},&n\text{ is odd},\\(b_{n/2}+b_{n/2+1})/2,&n\text{ is even}.\end{cases}$$

Choose $k$ positions by increasing $|a_i-m|$ . At equal distance, prefer the larger value. Positions with the same value count separately; choosing among equal values does not affect the answer. Output the sum of the selected values. The median is always determined from the complete input sequence.

## Input

The first line contains $n,k$ . The second contains the $n$ integers $a_i$ .

## Output

Print one integer: the sum of the selected values.

## Examples

### Example 1

### Input

```text
5 3
1 2 3 10 11
```

### Output

```text
6
```

### Example 2

### Input

```text
8 5
1 1 1 1 4 7 7 7
```

### Output

```text
8
```

### Example 3

### Input

```text
4 1
-9 -1 1 9
```

### Output

```text
1
```

## Example Explanation

In sample 1 the median is 3, so choose 1, 2, and 3, totaling 6. In sample 2 the median is 2.5; the four ones and the value 4 all have distance 1.5, so all five are selected, totaling 8. In sample 3 the median is 0; the tie is resolved in favor of 1.

![Sample 1 selects 1, 2, and 3 by distance from the median](assets/median.svg)

Double circles mark the three selected values; distances from the median are shown below.

## Constraints and Guarantees

All data satisfy $1\le k\le n\le10^6$ and $|a_i|<10^9$ .

Specifications redesigned by Codex (GPT-6): for even size, the median is the arithmetic mean of the two middle values, and distance is the absolute numerical difference. Boundaries and examples use this definition throughout.

| Score | Additional conditions |
| --- | --- |
| 20% | $n\le20$ |
| 30% | $n\le10000$ |
| 50% | No additional conditions |
