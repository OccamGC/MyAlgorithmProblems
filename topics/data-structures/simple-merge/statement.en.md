# Simple Merge

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See [environment and measurements](../../../docs/评测环境与性能.md).

## Story

Items in a warehouse form several monotone sequences of labels. Report the labels as the smallest remaining item is repeatedly removed.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

You are given $k$ nonempty integer sequences. Each is either nondecreasing or nonincreasing; their directions may differ. Equal elements are allowed within and across sequences.

Perform $m$ operations. In each operation, print the smallest value among all remaining elements, then remove one occurrence of that value. The order of removing equal occurrences does not affect the output.

## Input Format

The first line contains $k,m$ . Each of the next $k$ lines describes one sequence: its length $s_i$ , followed by its $s_i$ elements $x_{i,1},\ldots,x_{i,s_i}$ .

## Output Format

Print $m$ lines containing the removed values in order. If $m=0$ , produce no output.

## Examples

### Example 1

### Input

```text
3 10
3 1 2 3
5 1 2 3 4 8
6 1 5 7 9 10 11
```

### Output

```text
1
1
1
2
2
3
3
4
5
7
```

### Example 2

### Input

```text
3 6
2 5 -1
2 -1 -1
2 0 4
```

### Output

```text
-1
-1
-1
0
4
5
```

### Example 3

### Input

```text
1 1
1 -1000000000
```

### Output

```text
-1000000000
```

## Example Explanation

In the first example, each sequence contains one $1$ , so the first three outputs are all $1$ . The second example includes a decreasing sequence and repeated negative values; every occurrence is retained.

## Constraints and Guarantees

All inputs satisfy: $1\le k\le31$ , $s_i\ge1$ , $0\le m\le\sum s_i\le10^6$ , and $\lvert x_{i,j}\rvert\le10^9$ . Every sequence satisfies the stated monotonicity guarantee.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
