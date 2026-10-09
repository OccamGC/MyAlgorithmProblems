# Factorio: Technology Tree

## Algorithm and attribution

Problem setter's solution: remove completed technologies and compute earliest finish times in topological order. Codex (GPT-6) replaces recursive readiness propagation with an explicit queue and compact adjacency arrays, preserving the model and asymptotic time bound. Program: [std.cpp](std.cpp).

The [three-state depth-first alternative](solution-alternative-depth-first.en.md), with [source](alternative-depth-first.cpp), evaluates dependencies directly and detects cycles. It is a different traversal with the same asymptotic bounds; the queue remains preferred.

## Completed technologies and graph direction

A completed technology no longer waits for its dependencies and cannot block another technology. Keep only dependencies whose two endpoints are both unfinished. For input $(u,v)$ , add an edge $v\to u$ to propagate readiness from prerequisite to dependent.

Repeated dependencies may remain: count each edge in the indegree and decrement it once when its source is processed. An unfinished self-loop cannot be removed and causes impossibility.

## Earliest finish times

Let $T(u)$ be the earliest finish time of technology $u$ . In the remaining graph,

$$T(u)=t_u+\max_{v\to u}T(v)$$

Use zero for a maximum over no predecessors. Maintain the number of unprocessed incoming edges. Enqueue all zero-indegree nodes with finish times equal to their durations. When processing $u$ , update each outgoing edge $u\to v$ by

$$T(v)\gets\max\{T(v),T(u)+t_v\}$$

Decrement the indegree of $v$ , enqueuing it when it becomes zero.

## Correctness and impossibility

Every technology must wait for all its prerequisites, so the recurrence is a lower bound on any schedule. Unlimited parallelism permits each technology to start immediately after its last prerequisite finishes, attaining that bound. Induction in topological order proves all computed finish times are optimal. Their maximum is the answer.

If nodes remain unprocessed, the remaining finite directed graph contains a cycle. The first technology to start on that cycle would still have an unfinished prerequisite on the cycle, a contradiction. This includes cycles of zero durations. Conversely, every nonempty acyclic graph has a zero-indegree node, so topological processing finishes every node.

## Complexity and implementation

Time and space are $O(n+m)$ . The explicit queue handles a chain of length $n$ without a deep call stack. Adjacency uses `Head` , `To` and `Next` arrays.

If the maximum nonnegative duration is $U$ , the answer in a feasible instance is at most $nU$ , reaching $10^{15}$ under these constraints. Use 64-bit finish times. All-complete instances return zero; with no dependencies, the answer is the maximum remaining duration. Three-state traversal has the same $O(n+m)$ bounds and organizes computation along dependencies using unseen, active and finished states.

## Verification and Use

An independent event simulator starts ready jobs and advances to the next completion. Tests include three-node directed graphs, self-loops, duplicate edges, zero-duration cycles and completed technologies. Formal data reach a million nodes and two million dependencies.

The ten input recipes, fixed seeds and purposes are in `tests/plan.json` . After compiling the program, run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs, or use `--case 01` to select one input. Independent checks are in [check_r15.py](../../../tools/check_r15.py). See the [five-round alternating measurements](../../../docs/benchmark-R15.json) and [environment](../../../docs/评测环境与性能.md). Finite tests and timings of these implementations supplement the proofs; they do not establish a time guarantee for every implementation with the same asymptotic bound.

## Measured Results

| Program | Largest per-case median | Peak working set |
| --- | ---: | ---: |
| Reference | 0.447671 s | 43.34 MiB |
| Alternative | 0.376580 s | 36.67 MiB |

The reference limit is 1.0 seconds. Both programs agree on all ten measured formal inputs and finish within this limit. Peak working set includes process overhead; maximum time and memory may come from different inputs.
