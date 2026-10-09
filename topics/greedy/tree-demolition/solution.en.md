# Dismantling Devices on a Tree — Solution

## Method and contribution

Use the problem setter's density contraction, priority queue and disjoint-set approach. Codex (GPT-6) supplies the exchange argument for signed weights, the lexicographic tie rule, whole-block reconstruction and a standard C++17 implementation. Density scheduling and disjoint sets are classical techniques.

## Reverse the removal order

Reverse a removal order into a parent-before-child construction order. Let $j_v$ be the zero-based construction position of vertex $v$ . The original objective becomes
$$
(n-1)\sum_v p_v-\sum_v j_vp_v.
$$
The first term is fixed, so minimize the weighted construction-position sum. The identity also holds for negative weights.

A block is a sequence already required to be consecutive. Block $B$ has length $L_B$ , total weight $W_B$ , and density $W_B/L_B$ . Blocks form a rooted tree, and each non-root block must follow its parent block. Initially every vertex forms a block.

## Density contraction and the tie rule

Repeatedly select the non-root block $B$ of greatest density. Among equal densities, select the block whose last construction vertex has the largest ID. Append all of $B$ to its parent block and combine their lengths and weights. Reverse the final root block to obtain the removal order.

All weights in the figure are zero. The last-ID tie rule still matters: the final removal order is $4,3,5,2,1$ .

![Removal order for a zero-weight tree](assets/example.svg)

**Exchange argument.** Suppose the current block partition admits a legal block order with globally optimal value and smallest removal sequence. Move the selected $B$ immediately after its parent block. No crossed block can be an ancestor of $B$ , since its parent block has already appeared; moving $B$ earlier also preserves the requirements of its descendants.

For a crossed block $X$ , replacing $XB$ by $BX$ decreases the weighted position sum by
$$
L_XW_B-L_BW_X\ge0.
$$
This follows from the maximum density of $B$ and does not require nonnegative weights. Repeating these exchanges cannot worsen the primary objective.

A strict improvement would contradict optimality, so every crossed block must have the same density as $B$ . In the reversed removal sequence, the first difference compares the last vertex of $B$ with the last vertex of the last crossed block. Blocks are disjoint, so these IDs differ, and the selected tail is the largest. Placing a crossed block later in construction therefore places a smaller ID first in the removal sequence. The move cannot worsen the lexicographic objective.

Consequently an optimal order makes the parent block and $B$ consecutive, and contracting them is safe. Induction proves both objectives for the final sequence. The root block must be excluded because it has no parent to join.

## Implementation and complexity

- Compare densities by cross multiplication. Each product has absolute value at most $2.5\times10^{17}$ and fits signed 64-bit arithmetic.
- Store each block as a linked list with a head, tail and successor array. Append the entire block. Adding an edge to the original parent and using ordinary DFS cannot represent all required interleavings of original subtrees.
- A disjoint set locates the block containing an original parent. Iterative path compression avoids recursion on deep trees.
- Heap entries contain density, last ID and a version snapshot. Discard entries whose block has merged or whose version is obsolete.
- Traverse the tree, reverse the final list and produce the output iteratively. Compute the value directly from removal positions.

There is at most one new heap entry per merge. Total time is $O(n\log n)$ and space is $O(n)$ . The disjoint set uses path compression without rank linking, so no separate inverse-Ackermann claim is needed. The absolute objective is at most $10^6n(n-1)/2$ ; use signed 64-bit arithmetic.

[Reference program](std.cpp). Enumerating all legal orders independently checks both objectives on small instances, but is unsuitable for the full range.

## Data and reproduction

The statement contains three samples. The [test plan](tests/plan.json) defines ten scored inputs. The [generator](tests/generate.py) uses only the Python standard library and accepts --plan, --out-dir, --case and --std. Large generated inputs and executables are kept outside the published package. See the [reference measurements](../../../docs/benchmark-R28.json) for runtime and memory.
