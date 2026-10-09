# Recognizing a Lattice of Symbols

Estimated time limit: 2 seconds. Memory limit: 128 MB.

The actual time limit is twice the slowest-case median runtime of the reference solution on the target judge, rounded up to a multiple of $0.5$ seconds. See the [benchmark environment](../../../docs/评测环境与性能.md).

## Story

A directory allows several symbols to name one object and uses a relation table to describe an order among objects. Determine whether the table can represent a lattice exactly.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

A partial order $\le$ is reflexive, antisymmetric, and transitive: $x\le x$ ; if $x\le y$ and $y\le x$ , then $x=y$ ; if $x\le y$ and $y\le z$ , then $x\le z$ .

An upper bound $u$ of $x,y$ satisfies $x\le u$ and $y\le u$ . An upper bound that is at most every other upper bound is their least upper bound, or join. Lower bounds and the greatest lower bound, or meet, reverse these comparisons. A nonempty partially ordered set is a lattice if every pair has both a join and a meet.

Symbols are different from elements: several symbols may represent the same element. Let $f$ map each symbol to one element, with every element represented by at least one symbol. A symbol relation represents the partial order when a relation between symbols $i,j$ exists exactly when $f(i)\le f(j)$ . The element set and the mapping $f$ may be chosen; they are not supplied as input.

You are given $n$ symbols and an $n\times n$ matrix $A$ . Entry $A_{i,j}=1$ means relation $(i,j)$ exists; zero means it does not. Decide whether there are an element set, a surjection $f$ , and a lattice on that set such that

$$A_{i,j}=1\quad\Longleftrightarrow\quad f(i)\le f(j)$$

The matrix cannot be changed and no symbol can be omitted. Several symbols may represent one element, so relations in both directions between distinct symbols are not necessarily invalid.

## Input Format

The first line contains the test-case count $T$ . Each case begins with $n$ , followed by $n$ rows of $n$ integers describing matrix $A$ .

## Output Format

Print `Y` for each matrix that can represent a lattice, or `N` otherwise, one character per line.

## Samples

### Sample 1

### Input

```text
5
6
1 1 1 1 1 1
0 1 0 1 1 1
0 0 1 1 1 1
0 0 0 1 0 1
0 0 0 0 1 1
0 0 0 0 0 1
5
1 1 1 1 1
0 1 0 0 1
0 0 1 0 1
0 0 0 1 1
0 0 0 0 1
5
0 1 1 1 1
0 1 0 0 1
0 0 1 0 1
0 0 0 1 1
0 0 0 0 1
5
1 1 0 1 1
0 1 0 0 1
0 0 1 1 1
0 0 0 1 1
0 0 0 0 1
5
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
```

### Output

```text
N
Y
N
N
Y
```

### Sample 2

### Input

```text
3
1
0
1
1
2
1 1
1 1
```

### Output

```text
N
Y
Y
```

## Sample Explanation

The second case of the first sample has a minimum, three incomparable middle elements, and a maximum, forming a lattice. Its third case lacks a reflexive relation and is invalid. Its fifth case has every relation present; all symbols can represent one element, making it valid.

![Two incomparable minimal upper bounds prevent a least upper bound](assets/bounds.svg)

This separate diagram gives an invalid partial order: a lower element is below a higher one when an upward path connects them. The minimal upper bounds $u,v$ of $a,b$ are incomparable, so neither is below every upper bound.

## Constraints and Guarantees

Each case satisfies $1\le n\le50$ and $A_{i,j}\in\{0,1\}$ . The sum of $n$ over the input file is at most $50000$ .

| Score share | Additional conditions |
| --- | --- |
| 100% | None |
