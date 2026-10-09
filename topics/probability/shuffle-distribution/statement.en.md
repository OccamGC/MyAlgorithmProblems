# Random Analysis: Probabilities

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See the [reference environment](../../../docs/评测环境与性能.md).

## Story

A laboratory shuffles numbered cards using random swaps in a fixed order. A researcher wants to determine the final value distribution at each position.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Given an integer sequence $a_1,\ldots,a_n$ indexed from $1$ , perform the following operations on the current sequence. Values may repeat.

```text
for i = 1, 2, ..., n:
    r = uniformly_random_integer(1, n)
    swap(a[i], a[r])
```

Each random choice is independent and uniform over all integers from $1$ to $n$ , including $i$ . Each swap immediately changes the sequence used by subsequent rounds. Let the final sequence be $A_1,\ldots,A_n$ .

Find the full matrix $P_{i,j}=\Pr(A_i=j)$ for $1\le i,j\le n$ . Rows represent positions and columns represent values. Distinct elements with the same value contribute to the same column; an absent value has a zero column.

Represent results modulo $M=998244353$ : for a nonnegative rational result $p/q$ with $q>0$ , print the representative of $p\cdot q^{-1}\bmod M$ in $[0,M-1]$ . Print $0$ for a zero result. The constraints ensure that the required denominators are invertible modulo $M$ .

## Input Format

The first line contains $n$ . The second line contains $n$ integers $a_1,\ldots,a_n$ .

## Output Format

Print $n$ lines of $n$ integers. Entry $j$ in line $i$ represents $P_{i,j}$ modulo $M$ .

## Examples

### Example 1

### Input

```text
1
1
```

### Output

```text
1
```

### Example 2

### Input

```text
3
1 2 3
```

### Output

```text
332748118 813384288 850356301
332748118 850356301 813384288
332748118 332748118 332748118
```

### Example 3

### Input

```text
3
1 1 3
```

### Output

```text
147888053 0 850356301
184860066 0 813384288
665496236 0 332748118
```

## Example Explanation

There are $3^3=27$ equally likely sequences of random choices in the second example. Counting final outcomes gives the numerator matrix below, with denominator $27$ in every cell. In the third example, both elements of value $1$ contribute to the first column, while the second column is zero.

![Final probabilities for three positions and three values](assets/probabilities.svg)

Rows are final positions and columns are values. Divide each count by $27$ to obtain its probability.

## Constraints and Guarantees

All inputs satisfy $1\le n\le300$ and $1\le a_i\le n$ .

Codex (GPT-6) specifies the size bound $n\le300$ for this edition; the element range is $1\le a_i\le n$ .

| Score | Additional conditions |
| --- | --- |
| 100% | None |
