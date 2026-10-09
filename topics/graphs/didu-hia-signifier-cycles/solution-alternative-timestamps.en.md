# Didu Hia's Signifier Cycles: Increasing Visit Timestamps

Problem setter's solution from the teaching notes. Codex (GPT-6): a proof of the current-walk test and a standard implementation. [alternative-timestamps.cpp](alternative-timestamps.cpp) is a parallel option to [path tracking](solution.en.md) and passes all formal inputs.

Unvisited vertices have timestamp zero, and a global counter starts at one. Record its value $b$ when starting a new walk. Follow outgoing edges, assigning the current counter to every newly visited vertex and incrementing it afterward.

On reaching a vertex with existing timestamp $t$ , it belongs to the current walk exactly when $t\ge b$ . In that case the cycle length is the current counter minus $t$ . If $t<b$ , the walk has reached a previously processed region. Skip already visited starting vertices.

Global timestamps increase strictly. All earlier walks have timestamps below $b$ , and all vertices of this walk have timestamps at least $b$ , proving the test. Consecutive timestamps along the current path make the repeated vertex's suffix length exactly the difference between counters. The unique-outgoing-edge path-and-cycle structure supplies the remaining correctness argument.

Each vertex receives one timestamp. Total time and space are $O(n+1)$ . Only the outgoing-edge and timestamp arrays plus constant scalar storage are needed, eliminating the explicit path, position cleanup and separate visited array. The counter is at most $n+1$ , so an ordinary integer suffices here.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
