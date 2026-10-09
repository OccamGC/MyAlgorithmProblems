# A Queue Made of Stacks

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

A storage controller has only stacks but must carry out a sequence of queue operations. It knows the operations in advance and wants to deliver every element on time using as few stack operations as possible.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

There are $n$ initially empty stacks. Implement $m$ operations on an initially empty queue: `0` means enqueue and `1` means dequeue. A dequeue must return the earliest enqueued element that has not yet been returned. A dequeue from an empty queue does nothing.

Queue operation $t$ takes place in time interval $t$ . Although the entire operation string is known, an input element can be read only during its enqueue interval, and an output must occur during its prescribed dequeue interval. During each interval, you may perform any nonnegative number of these operations:

1. Push the current input element onto a stack, at cost one.
2. Pop a stack top and output that element, at cost one.
3. Pop a stack top and push that element onto another stack, at cost two.

Elements are stored in the stacks. Only the dequeue results within these $m$ operations must be correct; no state is required for later queue operations. Minimize the total number of stack pushes and pops. The input specifies only operation types; element values need not be supplied or printed.

## Input Format

The first line contains $n,m$ . The second is a string of $m$ characters from `0` and `1` . For $m=0$ , this line is empty.

## Output Format

Print the minimum total cost as one integer.

## Samples

### Sample 1

### Input

```text
2 10
0001110011
```

### Output

```text
12
```

### Sample 2

### Input

```text
2 0

```

### Output

```text
0
```

### Sample 3

### Input

```text
2 6
110010
```

### Output

```text
2
```

## Sample Explanation

In sample one, two of the first three elements can start at separate stack bottoms; the third is transferred once, costing eight operations in total. The next two elements each need one push and one pop, adding four. Sample two has no operations. In sample three, the first two dequeues are ineffective and only the first enqueued element is eventually dequeued; storing and outputting it costs two.

## Constraints and Guarantees

$2\le n\le10^9$ , $0\le m\le4\times10^6$ . The operation string contains only `0` and `1` .

| Score | Additional constraints |
| --- | --- |
| 100% | None |
