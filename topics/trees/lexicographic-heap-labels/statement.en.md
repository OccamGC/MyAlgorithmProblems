# Lexicographically Largest Heap Labels

Estimated time limit: 2.5 seconds. Memory limit: 512 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $4$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

This multiplier provides at least twice the measured runtime of the static-sorting alternative.

## Story

A gallery is decorating a tree with lamps of different brightnesses. Every lamp must be brighter than its ancestors. When inspecting vertices by number, the curator wants the earliest possible vertices to be as bright as possible.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

A tree has $N$ vertices numbered $1,\ldots,N$ and root $K$ . Assign the integers $1,\ldots,N$ bijectively as labels $a_1,\ldots,a_N$ . Every nonroot vertex must have a strictly larger label than its parent.

Among valid assignments, maximize the array $(a_1,\ldots,a_N)$ lexicographically: at the first vertex number where two assignments differ, the larger label makes the larger assignment.

For the optimal permutation, define its zero-based Cantor rank by

$$R=\sum_{i=1}^{N} c_i (N-i)!,\qquad c_i=\#\{j:i<j\le N,\ a_j<a_i\}$$

Thus, $R$ counts permutations preceding it when all $N!$ permutations are sorted in increasing lexicographic order. Output $R$ modulo $100000007$ and modulo $100000009$ , in that order.

## Input Format

The first line contains $N,K$ . Each of the next $N-1$ lines contains an edge $u,v$ .

## Output Format

Print the two residues on one line. Do not print the label permutation itself.

## Samples

### Sample 1

### Input

```text
5 1
1 2
2 3
2 5
3 4
```

### Output

```text
3 3
```

### Sample 2

### Input

```text
5 4
4 2
4 3
4 1
5 4
```

### Output

```text
118 118
```

### Sample 3

### Input

```text
4 3
3 4
4 1
1 2
```

### Output

```text
16 16
```

## Sample Explanation

The first two optimal arrays are $(1,2,4,5,3)$ and $(5,4,3,1,2)$ , with zero-based ranks three and one hundred eighteen. Sample three is a chain rooted at vertex three; its only valid array is $(3,4,1,2)$ , with rank sixteen.

## Constraints and Guarantees

$2\le N\le500000$ , $1\le K,u,v\le N$ . The input edges form a tree.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
