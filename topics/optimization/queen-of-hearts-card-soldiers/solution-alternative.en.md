# The Queen of Hearts' Card Soldiers: Alternative Solution

## Strictly decreasing subsequences with a Fenwick tree

Codex (GPT-6) supplied this method and its C++17 implementation, [alternative.cpp](alternative.cpp). The sorting reduction and the setter's algorithm are in the [main solution](solution.en.md).

Sort by increasing attack and then increasing armor. Let $D_i$ be the longest strictly decreasing armor subsequence ending at soldier $i$ . Then

$$D_i=1+\max_{j<i,\ Armor_j>Armor_i}D_j$$

Use zero for the maximum of an empty set. Sort and deduplicate negated armor values for coordinate compression; larger armor gets a smaller rank. A maximum Fenwick tree stores the best $D$ at each rank. Query the prefix strictly before the current rank, add one, and update the current rank. The largest $D_i$ is the answer, or zero for an empty input.

Removing the last item from any feasible subsequence ending at $i$ gives one of the recurrence's candidates, and every such candidate can be extended by $i$ . This proves the recurrence. Before processing $i$ , the tree contains precisely the best values from earlier positions, proving every $D_i$ by induction. Earlier soldiers with the same attack have armor at most the current value, so the strict query excludes them. Grouped delayed updates are unnecessary.

Sorting, compression, queries, and updates take $O(n\log(n+1))$ time and $O(n)$ space. Negation is safe within the attribute bounds. The method provides an explicit DP interpretation and a range-statistics structure, but has the same asymptotic complexity, more arrays, and a larger measured constant than the reference chain cover; it is not an unconditional optimization.
