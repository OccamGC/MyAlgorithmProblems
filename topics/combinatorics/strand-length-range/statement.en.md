# Counting Paired DNA Strands over a Length Range

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is twice the slowest per-case median time of the standard program on the target judge, rounded up to a multiple of $0.5$ seconds. See the [evaluation notes](../../../docs/评测环境与性能.md).

## Story

A researcher groups paired-strand samples by length ranges. Two records may describe the same sample read from opposite ends, so the equivalence rule must be applied before counting structures in each range.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Each query gives $L,R,K$ . The alphabet has $K$ distinct complementary pairs $a_1,b_1,\ldots,a_K,b_K$ , hence $q=2K$ letters. Complementation exchanges the two letters in each pair; no letter complements itself. Letter types have fixed labels.

A paired-strand structure of length $t$ is represented by a string $s$ of length $t$ ; its other strand is uniquely determined by complementation. Define reverse complementation by

$$R_c(s)=\overline{s_t}\,\overline{s_{t-1}}\cdots\overline{s_1}$$

Two representations describe the same structure if and only if they are equal or reverse complements. Ordinary reversal, positionwise complementation, and renaming letter types are not separate equivalences. Structures of different lengths are always distinct.

Let $F(t,K)$ count structures of length $t$ . Output

$$\sum_{t=L}^{R}F(t,K)\pmod{1000000007}$$

## Input

The first line contains the query count $M$ . Each of the next $M$ lines contains $L,R,K$ .

## Output

For each query, print its least nonnegative residue modulo $1000000007$ .

## Examples

### Example 1

### Input

```text
3
1 1 1
1 4 1
2 3 2
```

### Output

```text
1
18
42
```

### Example 2

### Input

```text
2
1 2 500000004
2 2 1
```

### Output

```text
500000005
3
```

### Example 3

### Input

```text
2
1000000000 1000000000 1
1 1000000000 1000000000
```

### Output

```text
132812501
50812223
```

## Example Explanation

For $K=1$ , the counts at lengths 1, 2, 3, and 4 are 1, 3, 4, and 10, so the answer over $[1,4]$ is 18. Sample 2 also includes $2K\equiv1\pmod{1000000007}$ .

![The three classes of length two with one complementary pair](assets/strands.svg)

Let A and T be complementary. AA and TT are equivalent; AT and TA are separate fixed representations.

## Constraints and Guarantees

All data satisfy $1\le M\le100000$ , $1\le L\le R\le10^9$ , and $1\le K\le10^9$ . Queries may repeat.

Specifications redesigned by Codex (GPT-6): length-range bounds and reverse-complement equivalence with fixed letter labels are explicit.

| Score | Additional conditions |
| --- | --- |
| 20% | $M\le20$ , $R\le8$ , $K\le2$ |
| 30% | $M\le1000$ , $R\le10000$ |
| 50% | No additional conditions |
