# The Weak Link Strikes Back

- Indicative time limit: 0.5 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 512 MB

## Story

Each stall in a row at a creative fair has two scores, and either score may be negative. The judges will choose a consecutive group of stalls. Its final score is the lowest first score in the group multiplied by the sum of its second scores.

The judges hope this will encourage everyone to improve their weakest point. The stallholders quietly turn to the page of their mathematics textbook about multiplying two negative numbers.

Choose a group with the highest possible score. It must contain at least one stall.

(This story was rewritten by GPT-6 Astra.)

## Formal Problem Statement

Given two integer sequences $a_1,\ldots,a_n$ and $b_1,\ldots,b_n$ representing the first and second scores of the stalls, respectively, find

$$\max_{1\le l\le r\le n}\left(\min_{l\le i\le r}a_i\right)\left(\sum_{i=l}^{r}b_i\right)$$

In words, maximize “the minimum first score in the interval × the sum of second scores in the interval” over all nonempty consecutive intervals.

The interval must be nonempty. Both sequences may contain positive values, zero, and negative values. The answer may also be negative.

## Input Format

The first line contains $n$ .

The second line contains $a_1,\ldots,a_n$ .

The third line contains $b_1,\ldots,b_n$ .

## Output Format

Print one integer: the maximum value.

## Sample 1

### Input

```text
3
1 -1 1
1 2 3
```

### Output

```text
3
```

### Explanation

Choose $[3,3]$ to obtain $1\times3=3$ .

## Sample 2

### Input

```text
3
-2 -1 -3
-2 -4 1
```

### Output

```text
15
```

### Explanation

Choose the whole interval to obtain $(-3)\times(-5)=15$ .

## Sample 3

### Input

```text
1
2
-3
```

### Output

```text
-6
```

### Explanation

The only nonempty interval scores $-6$ . An empty interval is not an option.

## Constraints and Guarantees

- $1\le n\le1\,000\,000$ .
- $-1\,000\,000\le a_i,b_i\le1\,000\,000$ .

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 20% | $n\le300$ |
| 20% | $n\le2\,000$ |
| 20% | $n\le10\,000$ |
| 40% | No additional conditions |
