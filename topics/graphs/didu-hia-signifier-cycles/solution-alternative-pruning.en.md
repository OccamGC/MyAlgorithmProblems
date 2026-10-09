# Didu Hia's Signifier Cycles: Delete Zero-Indegree Vertices

Codex (GPT-6): apply topological pruning to count cycle vertices. [alternative-pruning.cpp](alternative-pruning.cpp) is a linear-time supplement to [path tracking](solution.en.md) and passes all formal inputs.

Compute all indegrees and enqueue every zero-indegree vertex. Remove a queued vertex $v$ and its outgoing edge, decrementing the indegree of $d_v$ . Enqueue that destination if its indegree becomes zero. Once the queue is exhausted, return $n$ minus the number of removed vertices.

A cycle vertex always retains an incoming edge from its predecessor on that cycle, so no cycle vertex is removed. Conversely, every survivor points to another survivor: otherwise its target would still have had this incoming edge when removed. Each remaining vertex has outdegree one and indegree at least one. Total indegree equals total outdegree, so every remaining indegree is also one. The survivors therefore form disjoint cycles. Removal separates non-cycle vertices from cycle vertices exactly.

Each vertex enters the queue at most once, and each edge causes one indegree decrement. Time and space are $O(n+1)$ . The implementation uses an array queue with an increasing head index, avoiding repeated front erasure. This structure is useful for further analysis of trees feeding cycles, but requires indegree and queue storage.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
