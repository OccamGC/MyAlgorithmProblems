# Square-Sum Stacks

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

Magic balls have consecutive labels starting at one, with one ball of each label. A new ball may be placed on a nonempty stack only when its label and the current top label sum to a perfect square. Any ball may start an empty stack.

## Formal Problem Statement

Given $N$ stacks, place balls in the order $1,2,3,\ldots$ . Do not skip labels or move balls already placed. Each ball must be placed on an empty stack or on a top ball whose label sums with the new label to a perfect square.

Output any final arrangement containing the maximum possible number of balls. List the $N$ stacks in any fixed order.

## Input Format

One line contains $N$ .

## Output Format

Print $N$ lines. Line $i$ lists stack $i$ **from top to bottom**, with spaces between labels. Every optimal arrangement is accepted.

## Samples

### Sample 1

### Input

```text
4
```

### Output

```text
8 1
11 5 4
9 7 2
10 6 3
```

### Sample 2

### Input

```text
1
```

### Output

```text
1
```

### Sample 3

### Input

```text
3
```

### Output

```text
5 4
6 3 1
7 2
```

## Sample Explanation

The first arrangement contains labels one through eleven. The figure shows this optimal arrangement from top to bottom; each adjacent pair sums to a square. No arrangement on four stacks can include ball twelve.

![N=4; adjacent labels sum to 9, 16 or 4](assets/stacks.svg)

## Constraints and Guarantees

$1\le N\le1000$ .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
