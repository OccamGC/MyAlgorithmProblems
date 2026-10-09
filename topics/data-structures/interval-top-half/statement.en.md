# Interval Top Half

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See [environment and measurements](../../../docs/评测环境与性能.md).

## Story

An observatory records a sequence of measurements. For every contiguous observation period, a researcher wants the sum of the larger half of its values.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given an integer sequence $a_1,\ldots,a_n$ , consider every nonempty contiguous interval $[l,r]$ . Let $L=r-l+1$ . Find the sum of the largest $\lceil L/2\rceil$ elements in that interval.

Equal values at different positions count separately. Select exactly the specified number of elements, even when values are negative.

## Input Format

The first line contains $n$ . The second line contains $n$ integers $a_1,\ldots,a_n$ .

## Output Format

Print $n(n+1)/2$ lines, each containing one integer. Order intervals by increasing length, and then by increasing left endpoint.

For example, when $n=3$ , the order is $[1,1]$ , $[2,2]$ , $[3,3]$ , $[1,2]$ , $[2,3]$ , $[1,3]$ .

## Examples

### Example 1

### Input

```text
5
2 3 9 9 1
```

### Output

```text
2
3
9
9
1
3
9
9
9
12
18
18
18
18
21
```

### Example 2

### Input

```text
4
-5 0 -5 8
```

### Output

```text
-5
0
-5
8
0
0
8
-5
8
8
```

### Example 3

### Input

```text
1
1000000000
```

### Output

```text
1000000000
```

## Example Explanation

The full interval in the first example sorts to $1,2,3,9,9$ . Its three largest elements sum to $21$ . In the second example, a one-element interval must select its element even when it is negative.

![Median and larger half of five sorted elements](assets/partition.svg)

Here $b_i$ is the $i$-th sorted value. The dashed box encloses the three largest values. Twice the middle element is also shown to distinguish the two statistics.

## Constraints and Guarantees

All inputs satisfy: $1\le n\le10^3$ and $\lvert a_i\rvert\le10^9$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
