# Psychic Control Tree: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: keep-heavy/clear-light traversal with root-path unions.** Root-path unions are used in the reference and have lower measured peak memory. Cyclic distance sums run faster on some tree shapes. These peer methods have the same asymptotic time and space bounds. Both implementations use explicit traversal and 64-bit weights.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the small-to-large sets with cyclic DFS-distance sums method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [peer method editorial](solution-alternative.en.md).

## The minimum connecting subtree

For a control subtree $u$ , let $S$ contain its controlled targets. Every gathering route union must contain the minimum subtree $H$ connecting $S$ . Gathering inside $H$ achieves this bound. Since weights are positive and controlled vertices cost nothing, the answer is the weight of $H$ minus the weights of $S$ .

## Inserting root paths in DFS order

Root the target tree at $1$ . Let $d_x$ sum vertex weights from the root to $x$ , excluding the root. Keep $S$ ordered by DFS entry time. Maintain $W$ , the weight of the union of root-to-target paths minus selected-target weights, and maintain their common LCA $g$ .

For the first target $x$ , set $W=d_x+v_1-v_x$ . Otherwise let $a,b$ be its cyclic predecessor and successor, and let $z$ be the deeper of $\operatorname{LCA}(a,x)$ and $\operatorname{LCA}(b,x)$ . Update

$$W\leftarrow W+d_x-d_z-v_x.$$

To justify the intersection point $z$ , recall that a rooted subtree occupies a contiguous DFS interval. If such an interval around $x$ contains a selected target, at least one of $x$'s ordered neighbors lies in it. Thus the deepest intersection with any existing root path is attained by a neighbor. Only the segment strictly below $z$ is new, and the new selected target must be exempted from cost. If $x$ was already in the union, the new segment is empty but its exemption is still necessary.

Update $g\leftarrow\operatorname{LCA}(g,x)$ . The union contains an unnecessary prefix from the root to just above $g$ , whose weight is $d_g+v_1-v_g$ . Therefore

$$\operatorname{answer}=W-d_g-v_1+v_g.$$

## Keeping the heavy subtree

Compute control-subtree sizes and choose a largest child. Process each light child and clear its temporary set, then process the heavy child and retain its set. Finally insert the current target and all targets from light subtrees. The set is now exactly $S$ ; record its answer and clear it unless the caller requests retention.

An explicit task stack stores the phase and keep flag. Contiguous DFS intervals enumerate light subtrees. The control mapping is a permutation, so a set contains no duplicate targets.

## Correctness and complexity

Insertion maintains the exact root-path union minus selected weights. The LCA correction removes exactly the unnecessary common prefix. Keeping heavy sets changes only computation order, not the target set at each answer.

Each target is reinserted across at most $O(\log(n+1))$ light edges. Ordered insertion and binary-lifting LCA cost $O(\log(n+1))$ each, for $O(n\log^2(n+1))$ total time. The set and traversal state use $O(n)$ space; including the LCA table gives $O(n\log(n+1))$ . Set clearing is charged to the corresponding insertions.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
