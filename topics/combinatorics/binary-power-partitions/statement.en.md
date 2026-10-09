# Partitions into Powers of Two

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The deployed limit is the standard program’s largest input median in the target environment multiplied by $2$ and rounded up to a multiple of $0.5$ seconds. See the [benchmark notes](../../../docs/评测环境与性能.md).

## Story

A warehouse supplies standard packs whose sizes are powers of two. An assembler needs an exact total and wants to count the different pack combinations.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

For a nonnegative integer $N$ , consider all finite nondecreasing sequences
$$
2^{e_1},2^{e_2},\ldots,2^{e_t},
\qquad 0\le e_1\le e_2\le\cdots\le e_t,
$$
with sum exactly $N$ . A size may be used repeatedly. Reordering the same multiset does not create another solution.

Count these sequences modulo $1000000000$ . The empty sequence sums to zero, so there is one solution when $N=0$ .

## Input

The input contains one integer $N$ .

## Output

Print the number of solutions modulo $1000000000$ .

## Samples

### Sample 1

### Input

```text
7
```

### Output

```text
6
```

### Sample 2

### Input

```text
8
```

### Output

```text
10
```

### Sample 3

### Input

```text
0
```

### Output

```text
1
```

## Sample explanations

The six solutions for sample one are $1+1+1+1+1+1+1$ , $1+1+1+1+1+2$ , $1+1+1+2+2$ , $1+2+2+2$ , $1+1+1+4$ , and $1+2+4$ . Sample two has ten solutions. Sample three has only the empty sequence.

## Constraints and guarantees

$0\le N\le2^{63}-1$ . Exponents are nonnegative integers.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
