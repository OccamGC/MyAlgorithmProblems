# Starts and Destinations: Alternative Solution

Contribution: Codex (GPT-6) adds direct multi-source initialization of classical Dijkstra, avoiding virtual edges through a simpler state definition. The preferred virtual-node model is in the [main explanation](solution.en.md).

Define $d_v$ as the minimum distance from any source in $S$ to $v$ . Initially set every source distance to zero and insert all sources into the min-heap; other distances are infinity. Continue with ordinary Dijkstra relaxations, then take the minimum distance over $T$ .

This is exactly the state obtained after extracting a virtual source and relaxing all its zero-weight edges. Every subsequent valid extraction and relaxation has the same meaning, so the nonnegative-weight Dijkstra proof applies directly. Taking the minimum over destinations is equivalent to relaxing all zero-weight edges into a virtual sink. If the source set is empty, the heap stays empty. If the destination set is empty, the final minimum remains infinity. Both cases return minus one.

The graph stores only original edges. Time is $O((n+m)\log(n+m+1))$ and space $O(n+m)$ . This removes virtual-node and edge management without changing asymptotic complexity. Distance types, stale-entry handling, and the nonnegative-weight requirement are the same as in the preferred method. It supports every formal input.

Program: [alternative.cpp](alternative.cpp).
