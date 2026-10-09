# Timber — Solution

## Comparing solutions

The reference uses static longest-chain decomposition. Gain extraction takes $O(n)$ instead of the $O(n\log(n+1))$ required by dynamic subtree updates and needs no range-update arrays. Final sorting keeps total time at $O(n\log(n+1))$ .

The problem setter’s method builds a segment tree in DFS order for each tree, initially storing root-path lengths. It repeatedly selects the highest-scoring endpoint and walks upward to the used part. Each newly covered vertex subtracts one from every endpoint in its subtree. Thus a leaf's score remains the number of uncovered vertices on that root path. Each vertex triggers one subtree update, yielding all marginal gains. Gains from all trees are then sorted together, preferring activated trees on ties to minimize the number activated.

The implementation used by Codex (GPT-6) directly decomposes each tree through longest children, collects the same marginal gains and represents the tie rule with first/non-first markers, as proved below. Both take $O(n\log(n+1))$ total time and $O(n)$ space; the logarithmic factor comes from sorting. It removes range subtraction and dynamic parent-path updates and uses explicit traversal. This is a more direct alternative with the same asymptotic bounds.

## The gain sequence of one tree

Selecting an internal node cannot outperform selecting one of its descendant leaves. A budget can therefore be viewed as choosing root-to-leaf paths. Covering the whole tree requires every rooted leaf to be selected, and those selections suffice. Thus $Need$ is the number of rooted leaves in the forest, including isolated nodes.

Let $F_u(k)$ be the maximum coverage in the subtree of $u$ using at most $k$ selections, with paths ending at $u$ . Its marginal gains are successive differences, retaining only positive gains. We prove these gains are nonincreasing.

A leaf has sequence $[1]$ . For an internal node, assume its children's sequences are nonincreasing. Merge and sort those sequences in decreasing order. Their first $k$ gains give optimal child-subtree coverage for budget $k$ : whenever a later gain of one child is chosen without an earlier, no-smaller gain, exchange them. The choices can therefore always form prefixes of the child sequences.

For every $k\ge1$ , node $u$ itself contributes one additional covered node. Its gain sequence is obtained by **adding one to the largest merged gain**, leaving the others unchanged. The result remains nonincreasing. This proves both the recurrence and the diminishing-gain property.

## Avoid explicitly merging sequences

A subtree's first gain is its height measured in nodes. At each node, choose a child with maximum height. Pass that child's first gain upward and add one; retain each other child's first gain as a completed contribution. Contributions retained deeper in the tree remain unchanged. A leaf passes up $1$ , and a tree root finally retains its own contribution.

Thus each nonchosen child contributes its height and each root contributes its height. Together these are exactly the full multiset of marginal gains. No segment tree or repeated root-path deletion is needed.

## Merge the forest and minimize the number of trees

Sort all gains together. The sum of the first $k$ is the maximum coverage. Mark the gain contributed by each root as that tree's first-use gain. It is strictly larger than every other gain from the same tree: those are heights of proper subtrees and are at most the full height minus one. Any chosen nonfirst gain therefore has its tree's first gain already selected.

For equal gains, take nonfirst gains before first-use gains. All gains above the current threshold must be chosen. At the threshold, nonfirst gains come from trees already used and add no tree; each first-use gain adds one. Choosing as many nonfirst gains as possible minimizes the extra trees. Smaller gains cannot replace threshold gains while preserving maximum coverage.

Accumulate gains and first-use flags to obtain every answer. Although the recurrence uses “at most,” all marginal gains through $Need$ are positive, so each optimum is realizable with exactly $k$ selections.

## Implementation and complexity

Find unvisited components in increasing node-ID order. The first node of each component is its required root. Build parent links with an explicit traversal order and compute heights in reverse order, avoiding recursion overflow on a chain of half a million nodes.

Graph construction and heights take $O(n)$ time. Sorting at most $n$ gains gives $O(n\log(n+1))$ total time and $O(n)$ space. The independent oracle enumerates all selected-node subsets of small forests, unions their root paths directly, and compares coverage and tree counts for each budget.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
