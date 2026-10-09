# Jumping through Lexicographic Permutations

## Story

A display cabinet advances its numbered models to the next permutation in lexicographic order each day. The last permutation wraps around to the first. Its curator wants to skip directly to the arrangement after several advances.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given a permutation of $1,\ldots,n$ and a nonnegative integer $k$ , arrange all $n!$ permutations in increasing lexicographic order on a cycle. Print the permutation $k$ steps forward. Lexicographic order compares values at the first differing position. The descending permutation is followed by the ascending one. For $k=0$ , retain the input permutation. Test cases are independent.

## Input Format

The first line contains $T$ . Each case consists of a line `n k` followed by a line containing the $n$ permutation values.

## Output Format

For each case, print the resulting $n$ values on one line.

## Sample 1

### Input

```text
3
3 1
1 2 3
3 1
3 2 1
3 7
1 2 3
```

### Output

```text
1 3 2
1 2 3
1 3 2
```

## Sample 2

### Input

```text
2
1 2147483647
1
4 0
2 4 1 3
```

### Output

```text
1
2 4 1 3
```

## Sample 3

### Input

```text
1
4 5
2 1 4 3
```

### Output

```text
3 1 2 4
```

## Sample Explanation

Sample 1 shows one advance, wrapping from descending to ascending order, and skipping a complete cycle. Sample 2 covers a singleton and zero steps. In sample 3, five advances from [2,1,4,3] produce [3,1,2,4].

![The six permutations of three elements form a cycle.](assets/example.svg)

The six permutations of three elements form a cycle.

## Constraints and Scoring

$1\le T\le10^5$ , each $n\ge1$ , and the sum of $n$ over all cases is at most $2\times10^6$ ; $0\le k\le2^{31}-1$ .

Specifications redesigned by Codex (GPT-6): cyclic lexicographic semantics, multiple cases, total size, and step bounds.

| Score | Additional constraints |
| --- | --- |
| 20% | $n\le8$ in each case |
| 30% | $n\le2000$ in each case |
| 50% | No additional constraints |

## Resource Limits

Time: 0.5 seconds. Memory: 128 MiB. The limit is twice the slowest standard-program median over five runs per input, rounded up to 0.5 seconds.

[Solution](solution.en.md) · [Measurement environment](../../../docs/评测环境与性能.md) · [Measurements](../../../docs/benchmark-R33.json)
