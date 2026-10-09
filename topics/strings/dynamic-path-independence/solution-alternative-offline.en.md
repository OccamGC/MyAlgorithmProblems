# Dynamic Path Independence: Offline Doubling Order

**This keeps the setter’s reversed paths and neighbour property. GPT-6 uses offline doubling to obtain exact global ranks, reducing comparisons during operations and ordered-map storage.**

## 1. Read all entities first

Simulate existence in input order. Assign a fresh internal ID to every insertion and record its parent and value. Translate each operation’s external IDs into the entities they identify at that moment. Delete subtrees with an explicit stack; a reused external ID maps to a different entity.

All entities ever created now form a fixed creation tree: each points to the entity that was its parent at creation. It contains vertices from different moments and is used only for ancestor strings. Operation replay must still track which entities are alive.

## 2. Exact lexicographic ranks by doubling

A reversed string follows parents from its vertex to the root. Use value plus one as its length-one rank. Missing ancestors have rank zero, representing an end marker smaller than every real value.

Let $R_k(u)$ be the lexicographic rank of the next $2^k$ values, padding short strings with end markers. Sort entities by
$$
\left(R_{k-1}(u),R_{k-1}(\mathrm{up}[u][k-1])\right).
$$
Assign equal pairs the same rank and increase the rank for each distinct pair. Induction proves that every level reflects both equality and lexicographic order exactly. Since the end marker is smallest, a proper prefix comes before its extension.

Once block length reaches the largest path length, the final rank orders whole reversed strings. The implementation reaches $2^{17}$ , covering paths of up to $100001$ vertices. Use entity IDs only to break ties between identical complete strings.

## 3. Replay the operations

Use $(\text{final rank},\text{internal ID})$ as the ordered key for current leaves.

On insertion, remove the parent if it was a leaf and add the new leaf. On subtree deletion, erase its still-live leaves, then add the surviving outside parent if it becomes a leaf. Internal IDs prevent confusion when external IDs are reused. Initially only the root is alive; future insertions must not participate in queries.

For a query, inspect only the predecessor and successor. Strings sharing a fixed prefix form a contiguous lexicographic interval, so a farther candidate’s common prefix is also shared by an intervening neighbour.

Find an LCP by checking doubling ranks from largest to smallest. Compare and skip a block only when both remaining paths are at least that long, preventing padded end markers from contributing to the answer. Identical complete strings, a single leaf, and final root deletion are handled directly.

## 4. Correctness and complexity

The creation tree preserves each entity’s true, fixed ancestor string. Doubling gives exact order and block equality. Replay maintains the correct current leaf set, and the neighbour property gives the correct maximum LCP. The results therefore match sequential execution of the problem.

Let $N\le q+1$ be the total number of entities. Each doubling level sorts in $O(N\log N)$ time, with $O(\log N)$ levels. During replay, set comparisons use integer ranks, so insertion, deletion, and lookup take $O(\log N)$ ; LCP also takes $O(\log N)$ . Each entity is deleted at most once. Total time is
$$
O(N\log^2 N+q\log N),
$$
and space is $O(N\log N+q)$ . This implementation uses comparison sorting, not a claimed linear-time radix sort.

The method needs the full input in advance; the [online solution](solution.en.md) can answer incrementally. Offline ranks avoid ordered-map allocation overhead and use less memory on the measured large cases. Both support the full range.

[Program](alternative-offline.cpp).
