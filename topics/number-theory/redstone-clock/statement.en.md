# Redstone Clock

- Indicative time limit: 3.0 seconds (reference environment: [environment and measurements](../../../docs/评测环境与性能.md))
- Actual time limit: twice the reference program's baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds; round up further if the platform requires a coarser unit.
- Memory limit: 512 MB

## Story

The village chief is building a redstone alarm for long delays. Two clocks start together, and the alarm rings whenever both finish a cycle simultaneously. Test a sequence of generated period pairs and summarize the first ringing time for each pair.

## Formal Problem Statement

Given positive integers $n,a$ , perform $2n$ queries. Two clocks with periods $s,t$ start at time $0$ . Their query answer is the first positive time when both finish a cycle; time $0$ is excluded.

Let $U=10000000$ . For $i=1,\ldots,n$ , carry out these steps in order:

1. Query periods $i,a$ for query $2i-1$ and record the answer.
2. Set $a\gets(a+10007)\bmod U+1$ .
3. Query periods $i,a$ for query $2i$ and record the answer.
4. Set $a\gets(a^2+1)\bmod U+1$ .

Output the bitwise XOR of answers to odd-numbered queries, followed by the bitwise XOR of answers to even-numbered queries.

## Input Format

Read two integers $n,a$ on one line, where $a$ is the initial value.

## Output Format

Print two lines: the XOR of odd-query answers, then the XOR of even-query answers.

## Sample 1

### Input

```text
5 7
```

### Output

```text
8312897
24761077
```

### Explanation

Generate ten queries in the specified order. Each updated value of $a$ is used by the next query.

## Sample 2

### Input

```text
1 1
```

### Output

```text
1
10009
```

### Explanation

The first periods are $1,1$ , so the answer is $1$ . Updating $a$ gives $10009$ , which is the answer to the second query with period $1$ .

## Constraints and Guarantees

- $1\le n\le10000000$ and $1\le a\le10000000$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 25% | $n\le1000000$ |
| 75% | No additional conditions |
