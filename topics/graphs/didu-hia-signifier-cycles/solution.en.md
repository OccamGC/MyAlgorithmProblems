# Didu Hia's Signifier Cycles: Track the Current Walk

Problem setter's solutions: follow outgoing edges and use current-path positions to detect a new cycle; the notes also provide timestamps and doubling. Codex (GPT-6): repair the input helper, provide an iterative C++17 implementation and proofs, and add indegree pruning.

## Preferred algorithm

Keep global visited flags and positions within the current path, initially $-1$ . Start from each unvisited vertex and follow its unique outgoing edge. On reaching a new vertex, append it to the path, record its position and mark it visited.

Stop on reaching a visited vertex $v$ . If its current-path position is $p$ , the suffix from $p$ to the end forms a cycle of length $|P|-p$ ; add this length. If it is absent from the current path, this walk has entered an already processed region and adds nothing. Clear positions for the current path afterward, keeping the global visited flags.

## Correctness

Following unique outgoing edges in a finite graph must eventually revisit a vertex. All vertices before the stopping point are distinct within the current path. Repeating a vertex of that path closes its suffix into a cycle with no internal repetition; the prefix only leads into it. Repeating a vertex from an earlier path enters a fully determined continuation whose cycle has already been processed.

Each vertex first enters only one path, and each new cycle is found only on first entering its region. Thus no cycle vertex is missed or counted twice. A self-loop is a suffix of length one. For an empty graph, the loop is skipped and the answer is zero.

## Complexity and alternatives

Each vertex is appended and has its position cleared at most once. Time and space are $O(n+1)$ . An explicit path array avoids a linear recursive call depth on long chains.

[std.cpp](std.cpp) retains current-path tracking. Each alternative has a complete explanation and passes all formal inputs:

- [Timestamps](solution-alternative-timestamps.en.md), [source](alternative-timestamps.cpp): the setter's increasing visit numbers distinguish the current walk, eliminating the path array and separate visited flags. This is a parallel option with lower storage overhead.
- [Indegree pruning](solution-alternative-pruning.en.md), [source](alternative-pruning.cpp): Codex (GPT-6) applies zero-indegree deletion and counts the survivors in linear time, using a different structural approach.
- [The image after doubling](solution-alternative-doubling.en.md), [source](alternative-doubling.cpp): the setter's approach takes $O(n\log(n+1)+1)$ time and is a backup. Codex chooses rounds from the input size and counts distinct destinations with marks instead of sorting.

Timestamps remove arrays from this implementation, but small measured timing differences do not establish stable speedups. Inputs include hundred-thousand-vertex chains, large cycles, all self-loops, multiple cycles and random relabeling.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
