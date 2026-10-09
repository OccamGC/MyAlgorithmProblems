# Binary Tree Traversals: Cartesian Tree

Codex (GPT-6) turns preorder ranks into Cartesian-tree priorities for this problem, then applies the established monotone-stack construction. Program: [alternative-cartesian.cpp](alternative-cartesian.cpp). See the [main editorial](solution.en.md) for interval splitting.

## Conversion to a Cartesian tree

Let $\operatorname{rank}(u)$ be the position of label $u$ in preorder. Arrange nodes in inorder and assign their preorder ranks as priorities. The original tree has this inorder sequence, and every parent has a smaller priority than its children because preorder visits a root before its descendants.

It is therefore the minimum Cartesian tree of these priorities. Distinct priorities make each interval's minimum unique; this fixes its root and recursively both subtrees. Thus there is only one tree satisfying these properties.

## Monotone-stack construction

Scan inorder positions from left to right. The stack stores the current right spine with strictly increasing ranks. For a new node, pop all larger-rank stack tops. Its left child becomes the last popped node. If the stack is still nonempty, make the new node its top's right child, then push the new node.

The popped spine lies to the left of the new position and has larger priorities, so it forms the new node's left subtree. The remaining top has a smaller priority and can be its parent. Each step preserves inorder order and the minimum-heap property. The result is the unique target tree.

## Postorder and complexity

Visit nodes with an explicit stack in root-right-left order and reverse that record to obtain left-right-root postorder. Reversing ordinary root-left-right preorder would put the two subtrees in the wrong order.

Each node enters and leaves the construction stack at most once and is traversed once, giving $O(n)$ time and $O(n)$ space. Arrays store ranks, inorder, children and the traversal record. The benefits are a different model and explicit tree structure, without an unmeasured claim of lower time or memory. See the [main measurements](solution.en.md#verification-and-use).
