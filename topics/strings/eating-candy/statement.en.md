# Eating Candy

- Indicative time limit: 1.0 s (reference environment: [environment and measurements](../../../docs/评测环境与性能.md); for guidance only)
- Actual time limit: 2 times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: 512 MB

## Story

You have received a string of candies, but you will only eat consecutive segments that match your tastes. Given your favorite candy strings, what is the largest number of segments you can eat? Count the segments eaten, not the number of distinct kinds.

Each candy can be eaten only once. Choose all segments from the original string without overlap; leftover pieces cannot be joined to form new segments.

## Formal Problem Statement

You are given a nonempty binary string $T$ and $n$ nonempty binary strings $P_1,\ldots,P_n$ . Choose pairwise disjoint intervals $[l_i,r_i]$ such that every substring $T[l_i\ldots r_i]$ equals at least one $P_j$ . The same $P_j$ may match several selected segments, and the list may contain duplicate strings.

Find the maximum possible number of intervals. If $n=0$ , the answer is $0$ .

## Input Format

The first line contains an integer $n$ .

The second line contains a nonempty binary string $T$ .

Each of the next $n$ lines contains a nonempty binary string $P_i$ .

## Output Format

Print one integer: the maximum number of segments that can be selected.

## Sample 1

### Input

```text
5
010101010111
010
01
11
1000
1110
```

### Output

```text
6
```

### Explanation

Choose five consecutive occurrences of `01` , followed by the final `11` , for a total of six segments.

## Constraints and Guarantees

- $0\le n\le 100\,000$ .
- $1\le |T|\le 5\,000\,000$ .
- $\sum_{i=1}^{n}|P_i|\le 5\,000\,000$ , and every $P_i$ is nonempty.

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| 30% | $\lvert T\rvert\le 1\,000$ and $\sum_{i=1}^{n}\lvert P_i\rvert\le 10\,000$ |
| 20% | $\lvert T\rvert\le 100\,000$ , $n\le 500$ , and every $\lvert P_i\rvert\le 30$ |
| 20% | All $P_i$ have the same length; both $\lvert T\rvert$ and $\sum_{i=1}^{n}\lvert P_i\rvert$ are at most $5\,000\,000$ |
| 30% | No additional conditions |
