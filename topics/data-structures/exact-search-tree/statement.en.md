# A Binary Search Tree with an Exact Shape

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

The actual limit is the reference program's slowest median runtime on the target platform multiplied by $2$ , rounded up to a multiple of $0.5$ seconds. See the [evaluation environment](../../../docs/评测环境与性能.md).

## Story

An archive stores integer-keyed entries in a binary search tree. Its administrator must update multiplicities while preserving the prescribed tree shape and occasionally print the current structure.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

Maintain an initially empty binary search tree. Each node stores an integer key and a positive multiplicity. Every key in its left subtree is smaller, and every key in its right subtree is larger.

- Insert a key by searching from the root. If it exists, increment its multiplicity. Otherwise create a node of multiplicity one at the empty child reached by the search. Do not rotate or rebuild the tree.
- Delete a key by ignoring it if absent, or decrementing its multiplicity if present. Physically remove a node only when its multiplicity becomes zero.
- Print keys in preorder: root, left subtree, right subtree. Print each node once.

Physical deletion follows these exact rules. Remove a leaf directly. Replace a node with one child by that child. For a node with two children, exchange its data, including key and multiplicity, with its immediate inorder successor, then delete the physical successor node. The successor is the smallest-key node in the right subtree and has no left child, so one of the first two deletion cases applies. Exchanging data does not exchange parent or child links.

## Input Format

The first line contains $M$ . Each of the next $M$ lines specifies an operation: `0` prints the tree, `1 x` inserts key $x$ , and `2 x` deletes key $x$ .

## Output Format

For each print operation, output one line of space-separated keys. Multiplicities are neither printed nor used to repeat keys. Print an empty line for an empty tree.

## Samples

### Sample 1

### Input

```text
20
0
1 5
1 5
1 7
1 3
1 3
2 3
0
2 5
0
2 5
0
2 7
0
2 3
0
2 3
0
1 3
0
```

### Output

```text

5 3 7
5 3 7
7 3
3


3
```

### Sample 2

### Input

```text
11
1 4
1 2
1 7
1 5
1 5
1 6
2 4
0
2 5
0
0
```

### Output

```text
5 2 7 6
5 2 7 6
5 2 7 6
```

### Sample 3

### Input

```text
6
1 -2147483648
1 2147483647
2 0
0
2 -2147483648
0
```

### Output

```text
-2147483648 2147483647
2147483647
```

## Sample Explanation

Sample one prints eight lines; lines one, six and seven are empty. Duplicate keys are printed once, and removing key five twice is necessary to delete the root physically. In sample two, deleting root four moves both the key five and its multiplicity two to the root, so one subsequent deletion of five leaves that node present. Sample three uses both endpoints of the signed thirty-two-bit range.

## Constraints and Guarantees

$0\le M\le10^5$ , $-2^{31}\le x\le2^{31}-1$ . There are at most ten print operations. Deep vertices are not accessed frequently; no numerical height bound is specified.

| Score | Additional constraints |
| --- | --- |
| 100% | None |
