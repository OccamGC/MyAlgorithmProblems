# The Capacity of Square-Sum Stacks

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The limit is twice the slowest median runtime of the reference program, rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

Magic balls have consecutive labels starting at one, with one ball of each label. A new ball may be placed on a nonempty stack only when its label and the current top label sum to a perfect square. Any ball may start an empty stack.

## Formal Problem Statement

Each test case gives a stack count $N$ . Place balls in the order $1,2,3,\ldots$ , without skipping labels or moving previously placed balls. A ball may start an empty stack or be placed on a top ball whose label sums with its own label to a perfect square.

Find the maximum number of balls that can be placed. Print the exact answer, without taking a modulus.

## Input Format

The first line contains $T$ . Each of the next $T$ lines contains one positive decimal integer $N$ , describing an independent test case.

## Output Format

Print $T$ lines, with the exact decimal answer to each test case in order.

## Samples

### Sample 1

### Input

```text
1
4
```

### Output

```text
11
```

### Sample 2

### Input

```text
4
1
2
3
5
```

### Output

```text
1
3
7
17
```

### Sample 3

### Input

```text
1
100000000000000000000
```

### Output

```text
5000000000000000000099999999999999999999
```

## Sample Explanation

Four stacks hold at most eleven balls; one arrangement appears below. The capacities of one, two, three and five stacks are one, three, seven and seventeen. The last case requires a large exact integer.

![N=4; adjacent labels sum to 9, 16 or 4](assets/stacks.svg)

## Constraints and Guarantees

$1\le T\le1000$ , $1\le N\le2\times10^{10^5}$ . The entire input text contains at most $6\times10^5$ characters.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
