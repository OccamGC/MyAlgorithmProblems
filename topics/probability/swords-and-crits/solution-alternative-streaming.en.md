# Four Lists and Sorted Product Streams

A space-oriented companion approach. Codex (GPT-6): adaptation of the Schroeppel–Shamir four-list and heap-generation idea to weighted product-threshold probabilities, implementation, and verification of [alternative-streaming.cpp](alternative-streaming.cpp). It retains the [main solution](solution.en.md)'s small-threshold DP, deterministic preprocessing, and common probability factor, replacing only the large-threshold branch. It has a substantial space advantage but does not pass the full time limit.

## Four small lists

Split the swords into two nearly equal halves, then split each half into two nearly equal groups. Generate a sorted multiplier-and-weight list for each group, keeping only partial products below the maximum threshold. Call the lists $A,B,C,D$ . Each list has at most $2^{\lceil n/4\rceil}$ entries.

The full left distribution consists of all $A_iB_j$ products, and the right distribution consists of all $C_iD_j$ products. Instead of materializing them, generate their next entries on demand.

## Merge product rows using a heap

For fixed $A_i$ , the sequence $A_iB_0,A_iB_1,\ldots$ is sorted because multipliers are positive and $B$ is sorted. Put the first entry of each row into a min-heap. Pop the smallest product and insert the next entry from the same row. This yields the complete left distribution in increasing order.

For the right distribution, start each row at its last entry and use a max-heap to obtain decreasing order. A heap node stores its row, column, product, and the product of the two probability weights. Equal multipliers still correspond to different patterns, whose weights must be retained.

For one query, initialize the total weight of all right rows as the product of the total weights in $C$ and $D$ . Consume left entries with multiplier $x<K$ . Remove right entries whose multiplier exceeds $\lfloor(K-1)/x\rfloor$ , subtracting their weights from the remaining total. The left weight times the remaining right weight contributes to the failure probability. Sum these contributions, apply the common factor, and subtract from $1$ .

Rebuild the streams for each query, reusing the four small lists. Cap heap products at the maximum threshold $M$ : first test $a>\lfloor(M-1)/b\rfloor$ ; if true, store $M$ , otherwise evaluate $ab$ . All operations use `int64_t` . A quarter-pattern reaching $M$ is pruned because it can never fail any query. Two retained quarter-patterns whose combined product reaches $M$ may remain as a capped heap node and are excluded by the scan.

## Correctness

Each small list contains exactly the patterns of its group that can still participate in a failure event. Every product row is monotone in its column index. Popping the smallest or largest of the row heads therefore generates the full half-distribution in order, without omitting or duplicating a pair.

As left multipliers increase, removed successful right entries remain successful. Remaining right entries are in decreasing order, so after the inner loop their total weight is exactly the weight of right entries failing with the current left entry. Every failing pattern has all four quarter-products below the maximum threshold, so none was pruned prematurely. Sum the paired weights, apply the common probability factor, and take the complement to obtain the answer.

## Complexity and applicability

Let $N=2^{\lceil n/2\rceil}$ and $H=2^{\lceil n/4\rceil}$ . The four lists and heaps occupy $O(H)$ space. Each query produces at most $O(N)$ stream entries, each requiring $O(\log H)$ heap work. The large-threshold branch thus uses:

$$
O(n\log P+H+qN\log H)\text{ time},\qquad O(n+q+H)\text{ space}
$$

The small-threshold branch is unchanged. The exponent of the space bound is approximately halved, but full half-distributions cannot be reused between queries, and every query incurs heap costs. This approach is useful when memory is scarce and time is less restrictive. The main solution matches this problem's time constraints. See the [test notes](tests/README.md) for independent small checks and a timed formal stress test.

The companion reuses the DP and basic functions from the complete [std.cpp](std.cpp). Defining `SWORDS_LIBRARY_ONLY` while compiling the companion only disables the reference entry point.
