# Building a Big Star

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 512 MB

## Story

A star workshop has three kinds of parts: a left shell `<` , a right shell `>` , and a glowing spark `*` . A correctly oriented pair of shells can enclose a completed pattern to make a larger star; completed patterns can also be placed side by side. Sparks add length without affecting how the shells pair up.

The workshop has a broad product range: a stretch of sparks can ship on its own, and even an empty pair of shells, `<>` , counts as a finished product. The owner calls that one the “minimalist edition.”

Parts arrive on a conveyor belt that can grow at either end. After each new part, the maker wants to know the length of the longest complete star pattern on the belt.

(This story was rewritten by GPT-6 Sol.)

## Formal Problem Statement

You are given a sequence over `<` , `>` , and `*` . A **valid segment** is a nonempty contiguous substring that becomes a balanced angle-bracket sequence after every `*` is removed. The empty sequence is balanced, so a nonempty segment containing only `*` is valid; each `*` still counts toward its length.

There are then $m$ operations. Each operation adds one mark to the left or right end of the current sequence. Output the length of the longest valid segment for the initial sequence and after every operation. If no valid segment exists, the answer is $0$ ; this includes an empty sequence.

Balanced angle-bracket sequences can be defined recursively: the empty sequence is balanced; if $A$ and $B$ are balanced, then both $AB$ and `<A>` are balanced.

## Input Format

The first line contains two integers $n,m$ : the initial length and the number of operations.

The next $n$ whitespace-separated tokens are the marks of the initial sequence, in order. If $n=0$ , there are no such tokens.

Each of the next $m$ lines contains an integer $p$ and a mark $x$ . If $p=1$ , add $x$ on the left; if $p=2$ , add it on the right.

## Output Format

Print $m+1$ lines. The first gives the answer for the initial sequence; line $i+1$ gives the answer after operation $i$ .

## Sample 1

### Input

```text
6 3
* < < < > >
2 >
1 >
1 <
```

### Output

```text
4
7
7
9
```

### Explanation

Initially, the longest valid segment is `<<>>` , of length $4$ . After the first operation, the entire sequence `*<<<>>>` is valid, of length $7$ . The `>` added on the left by the second operation cannot join this segment. The final `<` makes the entire sequence of length $9$ valid.

## Sample 2

### Input

```text
0 5
2 >
1 *
1 <
2 *
1 >
```

### Output

```text
0
0
1
3
4
4
```

### Explanation

The initial sequence is empty, and adding `>` still leaves no valid segment. The subsequent sequences are `*>` , `<*>` , `<*>*` , and `><*>*` , whose longest valid segments have lengths $1,3,4,4$ respectively.

## Constraints and Guarantees

- $0\le n,m\le 1\,000\,000$ .
- $p\in\{1,2\}$ , and $x$ is `<` , `>` , or `*` .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 20% | $n\le 25$ and $m=0$ |
| 20% | $n\le 5\,000$ and $m=0$ |
| 30% | $n,m\le 5\,000$ |
| 30% | No additional conditions |
