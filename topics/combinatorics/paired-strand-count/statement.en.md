# Counting Paired DNA Strands

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

In this model of double-stranded, non-circular DNA, the two strands are complementary and run in opposite directions. Count molecule types for a given number of base pairs. The string definition below specifies when two representations describe one molecule.

## Formal Problem Statement

The alphabet is `A` , `T` , `C` , `G` , with complementary pairs `A`–`T` and `C`–`G` . Every letter has exactly one complement.

A molecule with $n$ base pairs is represented by a string $s=s_1\cdots s_n$ of length $n$ . Its reverse complement is

$$R(s)=\overline{s_n}\,\overline{s_{n-1}}\cdots\overline{s_1}$$

An overline means taking the complementary letter. Two strings describe the same molecule exactly when they are equal or one is the reverse complement of the other.

Each query gives $n$ and asks for the number of molecule types modulo $10^9+7$ . There are $m$ queries; output only the bitwise XOR of their individual residues.

## Input Format

The first line contains $m$ . Each of the next $m$ lines contains a query length $n$ .

## Output Format

Print one nonnegative integer: first reduce each query count modulo $10^9+7$ , then take their bitwise XOR.

## Samples

### Sample 1

### Input

```text
3
1
2
3
```

### Output

```text
40
```

### Sample 2

### Input

```text
4
1
1
2
2
```

### Output

```text
0
```

### Sample 3

### Input

```text
1
4
```

### Output

```text
136
```

## Sample Explanation

For lengths one, two, and three, the counts are $2,10,32$ , so the first sample gives $2\mathbin{\oplus}10\mathbin{\oplus}32=40$ . Each length occurs twice in the second sample, making the XOR zero. Length four has $136$ types, giving the third sample.

![Exchanging strand representations pairs AA with TT and leaves AT fixed](assets/strands.svg)

Arrows apply reverse complementation. `AA` and `TT` form one class; `AT` is its own reverse complement. Each diagram counts as one molecule.

## Constraints and Guarantees

For all inputs, $1\le m\le500000$ and $1\le n\le10^9$ . Queries may repeat.

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
