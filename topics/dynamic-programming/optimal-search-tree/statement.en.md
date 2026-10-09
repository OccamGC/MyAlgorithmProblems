# Optimal Binary Search Tree

- Reference time limit: 0.5 seconds (environment R30; estimate only).
- Actual time limit: twice the standard program’s baseline time on the slowest official test file in the target environment, rounded up to a multiple of 0.5 seconds.
- Memory limit: 128 MB

## Story

A lookup system stores entries ordered by their identifiers. Frequently accessed entries benefit from shallow positions, while the layout must remain a binary search tree. Choose a layout with minimum total cost.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Use each identifier $1,\ldots,n$ exactly once in a binary search tree: every identifier in a node's left subtree is smaller, and every identifier in its right subtree is larger. The root has depth one and a child has depth one greater than its parent.

Identifier $i$ is accessed $f_i$ times. Minimize $\sum_{i=1}^n f_i d_i$ , where $d_i$ is its depth. Among all minimum-cost trees, output the lexicographically smallest preorder traversal.

Preorder visits the root, left subtree, then right subtree. Compare identifiers as integers at the first differing position, not as decimal strings. Frequencies describe complete searches; do not additionally count accesses to ancestors.

## Input Format

The first line contains $n$ . The second contains $f_1,\ldots,f_n$ .

## Output Format

Print the minimum cost on the first line. On the second, print the lexicographically smallest optimal preorder, separated by spaces.

## Sample 1

### Input

```text
3
2 10 2
```

### Output

```text
18
2 1 3
```

### Explanation

Root two gives cost $10+2\cdot2+2\cdot2=18$ .

![Circles show identifiers; adjacent labels show frequencies and depths.](assets/example.svg)

Circles show identifiers; adjacent labels show frequencies and depths.

## Sample 2

### Input

```text
4
0 0 0 0
```

### Output

```text
0
1 2 3 4
```

### Explanation

Every tree costs zero. The right chain starting at one gives the smallest preorder.

## Sample 3

### Input

```text
1
1000000000
```

### Output

```text
1000000000
1
```

### Explanation

The only node has depth one.

## Constraints and Guarantees

$1\le n\le500$ ; $0\le f_i\le10^9$ . All inputs are integers. An entry of frequency zero must still occur in the tree.

Codex (GPT-6) completed the data specification by defining these size limits, nonnegative frequencies, the zero-frequency boundary, and the test groups below.

### Test Groups

| Score | Additional restriction |
| --- | --- |
| 20% | $n\le9$ |
| 30% | $n\le100$ |
| 50% | No additional restriction |

[Reference environment and measurements](../../../docs/评测环境与性能.md)
