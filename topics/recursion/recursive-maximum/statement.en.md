# Recursion Practice: Maximum

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The deployed limit is twice the largest per-input median runtime of the reference program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [reference measurements](../../../docs/评测环境与性能.md).

## Story

A revision exercise asks you to find the largest integer in a sequence. The exercise requires recursion for the maximum computation.

## Formal Problem Statement

Given an integer sequence $a_1,\ldots,a_n$ , output its largest value.

The implementation must compute the maximum recursively. Any recursive structure is allowed, including removing one element or splitting an interval. Loops may be used for input. This implementation requirement needs source inspection; output checking alone cannot establish compliance.

## Input

The first line contains an integer $n$ . The second line contains $n$ integers $a_1,\ldots,a_n$ .

## Output

Print one integer: the maximum value in the sequence.

## Samples

### Sample 1

### Input

```text
5
-10000 -2000 -222222 -161616 -1026
```

### Output

```text
-1026
```

### Sample 2

### Input

```text
1
-1000000000
```

### Output

```text
-1000000000
```

### Sample 3

### Input

```text
7
3 9 -5 9 0 8 9
```

### Output

```text
9
```

## Sample explanations

Every value in Sample 1 is negative, and the maximum is $-1026$ , not zero. Sample 2 has one element. The maximum $9$ occurs several times in Sample 3, but only its value is printed.

## Constraints and guarantees

For all inputs: $1\le n\le100$ and $|a_i|\le10^9$ .

| Score | Additional conditions |
| --- | --- |
| 100% | No additional conditions |
