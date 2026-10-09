# Counting Sublattices: Solution

## Method and contributions

The reference program preserves the setter's forced-membership search with timestamp rollback. Codex (GPT-6) organized the C++17 implementation and supplied the search invariants and the argument for elements added during a scan. See [std.cpp](std.cpp), the [subset DP](solution-alternative.en.md), and [direct enumeration](solution-brute.en.md), each with its own program.

Both the join and the meet of any two selected elements must be selected. Decide membership in label order, while `Selected` records chosen elements, including future elements forced into the set. Labels specify search order only, not the lattice order.

## Search and rollback

On entry at position $p$ , all smaller labels have final decisions; later labels may already be forced.

1. If $p$ is not selected, first recurse on the branch omitting it.
2. Try including $p$ . For every currently selected $j$ , inspect $A_{p,j}$ and $A_{j,p}$ , which supply the two operations. If a result has label below $p$ and is absent, abandon this branch because it contradicts an earlier decision.
3. Otherwise force these results and $p$ into the set. Give only newly added elements timestamp $p+1$ ; preserve old timestamps.
4. Recurse at $p+1$ , then clear only entries with timestamp $p+1$ .

Count one at the end of all labels. This also counts the empty set, so subtract one. The answer is at most $2^{22}-1$ , fitting a signed 32-bit integer.

## Correctness

Every forced inclusion follows from a necessary closure condition. If a required element was already excluded, no valid completion exists. Otherwise every sublattice containing the current selected elements must also contain that result. Forcing it cannot remove a valid answer.

The insertion loop may encounter elements added during that same loop. A new element is $p\lor j$ or $p\land j$ , hence comparable with $p$ . Absorption and idempotence imply that operating on it and $p$ gives only itself and $p$ . Such additions cannot introduce a previously unchecked conflict with an earlier excluded element.

For any pair in the final selected set, both members are selected when the larger label is processed, and their operation results are forced in. Rollback does not remove earlier selections within that branch. Thus every counted leaf is closed under both operations. Removing the empty leaf leaves only sublattices.

Conversely, fix a sublattice and follow its membership decisions whenever a branch is free. Closure ensures that every forced element belongs to it and no conflict occurs. Exactly one corresponding leaf is reached. Distinct selected sets give distinct leaves, so every sublattice is counted once.

## Complexity and tradeoffs

The search tree has depth $n$ and at most two children per node, hence $O(2^n)$ nodes. Each node scans $O(n)$ elements, for $O(n2^n)$ time. The table takes $O(n^2)$ space; markers and the recursion stack take $O(n)$ , giving $O(n^2)$ total space.

Subset DP also takes $O(n2^n)$ time but $O(2^n+n^2)$ space. It was faster in the measurements and is useful when the additional memory is acceptable. The setter's more space-efficient search remains the reference. Direct pair enumeration takes $O(n^2\cdot2^n)$ time. Although it finished every test, it had only about $1.29$ times headroom under the $1$-second limit; it is a checking and explanatory program, without a full-range acceptance guarantee on the target judge.
