# Binary Tree Traversals

Estimated time limit: 0.5 seconds. Memory limit: 128 MB.

On the target judge, multiply the reference program's largest per-case median time by $2$ and round up to a multiple of $0.5$ seconds. See [environment and measurements](../../../docs/评测环境与性能.md).

## Story

An archivist has recorded the preorder and inorder traversals of a binary tree. Recover the missing postorder traversal.

(This story was rewritten by GPT-6.)

## Formal Problem Statement

You are given the preorder and inorder traversals of the same rooted binary tree. It has $n$ nodes labeled from $1$ to $n$ , each used exactly once. Left and right subtrees are distinguished, and either may be empty.

- Preorder: root, left subtree, right subtree.
- Inorder: left subtree, root, right subtree.
- Postorder: left subtree, right subtree, root.

Find its postorder traversal.

## Input Format

The first line contains $n$ . The second line contains the preorder traversal, and the third line contains the inorder traversal, each consisting of $n$ integers.

## Output Format

Print the postorder traversal as $n$ space-separated integers on one line.

## Examples

### Example 1

### Input

```text
8
3 1 4 5 6 2 7 8
5 4 1 6 3 2 7 8
```

### Output

```text
5 4 6 1 8 7 2 3
```

### Example 2

### Input

```text
4
1 2 3 4
4 3 2 1
```

### Output

```text
4 3 2 1
```

### Example 3

### Input

```text
3
2 1 3
1 2 3
```

### Output

```text
1 3 2
```

## Example Explanation

In the third example, the root is $2$ , with left child $1$ and right child $3$ , so the postorder is $1,3,2$ . The second example is a chain of left children.

![The binary tree in example three and its three traversals](assets/traversals.svg)

The labels `pre` , `in` and `post` denote preorder, inorder and postorder. Left and right children are drawn on their corresponding sides.

## Constraints and Guarantees

All inputs satisfy: $1\le n\le10^6$ . Both traversals are permutations of $1$ through $n$ and are guaranteed to describe the same binary tree.

| Score | Additional conditions |
| --- | --- |
| 100% | None |
