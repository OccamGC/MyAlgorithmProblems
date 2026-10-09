# Binary Tree Traversals

## Algorithm and attribution

Problem setter's solution: take each root from preorder, split its inorder interval into two subtrees, and output left, right, root. Codex (GPT-6) replaces recursive calls with an explicit task stack so million-node chains can be handled. The splitting principle is unchanged. Program: [std.cpp](std.cpp).

The [Cartesian-tree alternative](solution-alternative-cartesian.en.md), with [source](alternative-cartesian.cpp), uses preorder ranks as priorities and reconstructs the tree with a monotone stack. Both algorithms are linear. The reference follows the traversal definitions directly; Cartesian reconstruction provides another model.

## Roots and intervals

Store each label's position in inorder. If a subtree occupies inorder interval $[l,r]$ , the next unconsumed preorder label is its root $u$ . If its inorder position is $p$ , the left subtree occupies $[l,p-1]$ and the right subtree occupies $[p+1,r]$ .

Distinct labels make $p$ unique. Applying the same rule to both subtrees uniquely determines the tree.

## Explicit tasks

There are two task types: expand a nonempty inorder interval, or print a known root. When expanding an interval, consume its preorder root and push these tasks in order:

1. Print the root.
2. Expand the right subtree, if nonempty.
3. Expand the left subtree, if nonempty.

The stack executes them in reverse insertion order: left subtree, right subtree, root. Expansion tasks still consume preorder labels in root-left-right order; printing tasks consume none.

## Correctness

Induct on interval length. A singleton outputs its only node. For a larger interval, preorder uniquely identifies the root and inorder separates the other labels into the correct subtrees. By induction, both subtree tasks produce their correct postorders. Printing the root after them gives the postorder of the whole subtree. The initial task spans all of inorder, proving the final output.

## Complexity and implementation

Every node is expanded and printed once, for $O(n)$ time. Preorder, the inorder-position table and tasks use $O(n)$ space. At most $O(h)$ tasks are active, where $h$ is the tree height; the implementation reserves linear capacity, so allocated space remains $O(n)$ .

No recursive call stack or child arrays are required. Cartesian reconstruction stores explicit child links, making it useful when later work also needs the tree structure. It likewise takes $O(n)$ time and space. Actual time and memory are reported below.

## Verification and Use

Small explicit trees provide independently traversed preorder, inorder and postorder. Checks cover left/right chains, alternating chains, balanced and random trees. Formal inputs include million-node versions and shuffled labels.

The ten input recipes, fixed seeds and purposes are in `tests/plan.json` . After compiling the program, run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs, or use `--case 01` to select one input. Independent checks are in [check_r15.py](../../../tools/check_r15.py). See the [five-round alternating measurements](../../../docs/benchmark-R15.json) and [environment](../../../docs/评测环境与性能.md). Finite tests and timings of these implementations supplement the proofs; they do not establish a time guarantee for every implementation with the same asymptotic bound.

## Measured Results

| Program | Largest per-case median | Peak working set |
| --- | ---: | ---: |
| Reference | 0.200720 s | 24.30 MiB |
| Alternative | 0.207337 s | 28.08 MiB |

The reference limit is 0.5 seconds. Both programs agree on all ten measured formal inputs and finish within this limit. Peak working set includes process overhead; maximum time and memory may come from different inputs.
