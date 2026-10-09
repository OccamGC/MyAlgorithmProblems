# Colony Trade: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: an online splay tree.** The online splay tree is the reference: future prices need not be known, space is $O(n)$ , and each operation takes amortized $O(\log(n+1))$ time. The offline segment tree needs pre-reading and $O(n+m)$ space, but guarantees worst-case $O(\log(n+m+1))$ per operation. It is a peer choice when pre-reading is allowed and individual-operation latency matters.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the offline coordinate-compressed segment tree method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [peer method editorial](solution-alternative.en.md).

## Ordering by price and identifier

Each good occupies one Splay node, ordered increasingly by $(c_i,i)$ . Sales start on the right, giving higher prices priority and breaking ties by larger identifiers. Goods can be located directly by identifier; only price changes require removal and reinsertion.

Each subtree stores total stock $S$ , production rate $R$ , stock value $V$ , and value produced per unit parameter $W$ . Reduce the last two modulo $P=10^9+7$ , but keep stock and rates exact. A node also stores its own quantities; subtree aggregates sum them with both children.

## Production and clearing tags

Producing with parameter $t$ performs

$$S\leftarrow S+Rt,\qquad V\leftarrow V+Wt\pmod P.$$

Selling an entire subtree clears $S,V$ while preserving $R,W$ . Clearing overrides earlier pending production; later production accumulates in a fresh time tag. Push clearing before production. Before Splay rotations, push tags from the auxiliary root down to the accessed node so rotations do not change which goods an update affects. Recompute aggregates after rotations.

## Sales and point changes

A sale descends along one boundary path. If the right subtree contains more stock than needed, descend right. Otherwise consume its entire value and clear it, then sell the current good and descend left only if demand remains. Only one boundary can be partially consumed; other visited high-price regions are handled wholesale. Splay the last visited node afterward and repair aggregates.

To change a rate, splay the good to the root, push tags, update its own rate, and rebuild aggregates while preserving stock. For a price change, first splay and push, detach the node, join its left and right subtrees, then reinsert it using the new key. Its stock and rate move with it. Read and execute operations in input order without future-price preprocessing.

## Correctness and complexity

The search-tree invariant gives the required sale order. Production and clearing tags match individual-good execution; clearing preserves future production capacity. Pushing before point changes applies old production with old rates. Consuming a whole subtree is equivalent to selling its goods in order, so the reported revenue is correct.

Boundary searches end in a Splay access. Point changes, removal, insertion, and joining require only a constant number of standard Splay accesses. Operations take amortized $O(\log(n+1))$ time, although an individual operation may take $O(n)$ . Including initial sorting, total time is $O((n+m)\log(n+1))$ and space is $O(n)$ .

Total production is bounded by $nmp_{max}t_{max}\le9\times10^{18}$ , within signed 64-bit range. Reduce quantities before multiplying them by prices modulo $P$ . Traversal and Splay propagation use explicit stacks; initial balanced-tree construction has logarithmic recursion depth.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
