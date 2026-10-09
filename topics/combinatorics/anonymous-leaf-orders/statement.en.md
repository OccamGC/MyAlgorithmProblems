# Ordered Tree Construction with Anonymous Leaves

## Story

A park retains labels on intermediate stations but uses identical signs at terminal stations. Construction records may consistently rename the terminal stations, while the order in which passages appear still matters.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Start with $n$ vertices temporarily labeled $1,\ldots,n$ . Add undirected edges between distinct vertices, at most one per pair. The final graph must be a tree with exactly $m$ leaves, where a leaf has degree at most $1$ .

Merge records using this **complete equivalence rule**: two edge-insertion sequences are equivalent exactly when they have the same set of nonleaf labels and a single consistent renaming within their leaf set makes the undirected edge at every step identical. Nonleaf names and edge order cannot change. Different sets of nonleaf labels always count separately.

Print the number of equivalence classes modulo $998244353$ as a nonnegative residue. Equivalently, first select the nonleaf labels from $1,\ldots,n$ , then disregard the names distinguishing the remaining leaves.

For $n=0$ , the unique empty sequence has $0$ leaves. For $n=1$ , the sole vertex is a leaf. For $n=2,m=2$ , the single undirected edge gives one plan.

## Input Format

One line containing nonnegative integers `n m` .

## Output Format

Print the number of equivalence classes modulo $998244353$ on one line.

## Sample 1

### Input

```text
3 2
```

### Output

```text
3
```

## Sample 2

### Input

```text
4 2
```

### Output

```text
36
```

## Sample 3

### Input

```text
2 2
```

### Output

```text
1
```

## Sample 4

### Input

```text
0 0
```

### Output

```text
1
```

## Sample Explanation

For three vertices, the center has three possible labels. For a fixed center, renaming the two leaves interchanges the two edge orders, so the answer is 3. With four vertices and two leaves, 72 labeled records form pairs, giving 36. For two vertices, swapping endpoints leaves the sole edge unchanged; this boundary answer must not be divided by two.

![With center 2 fixed, renaming leaves 1 and 3 makes the two records equivalent.](assets/example.svg)

With center 2 fixed, renaming leaves 1 and 3 makes the two records equivalent.

## Constraints and Scoring

$0\le n,m\le10^5$ . It is not guaranteed that $m\le n$ ; print zero if no plan exists.

Specifications redesigned by Codex (GPT-6): leaf-renaming equivalence, retained nonleaf labels, insertion order, and small boundary cases.

| Score | Additional constraints |
| --- | --- |
| 20% | $n\le8$ |
| 30% | $n\le1000$ |
| 50% | No additional constraints |

## Resource Limits

Time: 0.5 seconds. Memory: 128 MiB. The limit is twice the slowest standard-program median over five runs per input, rounded up to 0.5 seconds.

[Solution](solution.en.md) · [Measurement environment](../../../docs/评测环境与性能.md) · [Measurements](../../../docs/benchmark-R33.json)
