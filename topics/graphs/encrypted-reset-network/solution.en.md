# Solution: Encrypted Packets and Network Resets

Codex (GPT-6): applies incremental nonnegative shortest paths with distances truncated at the specified threshold, including logical-edge accounting, efficient resets, and a complexity proof.

## Keep only distances within the threshold

Store $d_v=\min(\operatorname{dist}(1,v),T+1)$ , using $T+1$ as a common unusable distance. With nonnegative weights, extending a path already longer than $T$ cannot bring it back within the threshold. Truncation therefore preserves the reset decision.

Compute these distances after reading the initial graph, without resetting it. When inserting an arc $(u,v,x)$ , improve $d_v$ and push it into a min-heap if $d_u+x<d_v$ . Repeatedly pop a current distance and relax its outgoing arcs; discard stale heap entries. A bidirectional logical edge adds two arcs but increases the logical-edge count by only one.

## Why propagating improvements is sufficient

Distances are correct before insertion. Any newly shorter path must use a new arc. Its first use triggers an endpoint relaxation, after which improvements propagate through existing arcs. Every finite stored label corresponds to a real path, so labels cannot underestimate shortest distances.

When propagation ends, every arc satisfies the truncated relaxation inequality. Induction along any path shows that a label is at most that path's length or $T+1$ . Together with the real-path bound, this proves that labels equal the truncated shortest distances. Hence $d_n\le T$ is exactly the reset condition.

Zero-weight edges and cycles are safe: only strict improvements enter the heap, so equal-length cycles do not propagate indefinitely. Nonnegative weights give each propagation the usual Dijkstra ordering of valid heap removals.

## Decryption and reset accounting

Compute $(b+3)(c+37)$ in 64 bits, reduce modulo the encryption modulus, then XOR each field. Never use an encrypted value as a vertex identifier before decoding it.

Maintain a separate current logical-edge count $e$ , initially $m$ , increasing it once per packet. On reset, set $b\gets b+e$ and $e\gets0$ , then remove all arcs. This separate counter correctly handles initial and bidirectional edges.

A reset visits only adjacency heads actually used in this period and distances that actually became reachable. Restore the source distance to zero and other reached distances to $T+1$ . Scanning every vertex at each reset could add $O(nk)$ work when repeated direct edges trigger frequent resets.

## Complexity and tradeoffs

Let $A\le2(m+k)$ be the total number of directed arcs appearing in the input. Between consecutive resets, a vertex's integer distance can strictly decrease at most $T+1$ times from its initial value $T+1$ . Thus a live arc is scanned from its source at most $T+1$ times, and every input arc belongs to only one such period.

There are $O(A(T+1))$ arc scans and heap operations, giving $O(n+A(T+1)\log(n+A))$ time. Within one propagation, nonnegative Dijkstra scans an arc at most once, producing at most one heap candidate per arc; space is $O(n+A)$ . Total reset work is linear in the vertices, arcs, and periods actually used and is included in the bound.

Restarting Dijkstra for every packet is a useful small oracle but may rescan nearly the same graph $k$ times. The bound relies on $T\le100$ . Increasing that threshold requires a new performance assessment.

See the [standard program](std.cpp), [test recipes](tests/README.md), and [measurements](../../../docs/benchmark-R37.json).
