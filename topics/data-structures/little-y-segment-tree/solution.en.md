# Little Y's Segment Tree: Process Queries by Right Endpoint

## An interval stack is a suffix of a prefix stack

Position $i$ survives after processing through $r$ exactly when no $j$ with $i<j\le r$ has $a_j\ge a_i$ . The first such later value would remove it. If none exists, every later value is smaller and cannot remove it. Thus, survival depends only on elements to the right.

It follows that independently processing $[l,r]$ leaves exactly the positions at least $l$ in the final stack for prefix $[1,r]$ . This includes equal values because the removal condition includes equality.

## Algorithm

Bucket queries by right endpoint, recording each left endpoint and original query index. Scan the sequence from left to right, storing **position indices** in a stack. At position $r$ , pop while $a_{\text{top}}\le a_r$ , then push $r$ .

Stack indices remain increasing. For every query ending at $r$ , binary-search the first index at least $l$ . The size of that suffix is the answer. Store answers by query index and print them in input order.

The stack operations implement the definition exactly. The survival criterion proves that selecting the suffix agrees with independent processing of the queried interval, establishing correctness.

![Stack states after five insertions](assets/example.en.svg)

## Complexity and implementation

Each position is pushed once and popped at most once, for $O(N)$ total stack work. Bucketing takes $O(N+M)$ and each binary search costs $O(\log N)$ . Total time is $O(N+M\log N)$ and space is $O(N+M)$ . Values and answers fit signed 32-bit integers. `lower_bound` searches position indices, not element values.

[std.cpp](std.cpp) is the reference. The following complete alternatives all support the full constraints:

| Method | Time | Space | Role |
| --- | --- | --- | --- |
| Right-endpoint buckets and monotone stack | $O(N+M\log N)$ | $O(N+M)$ | Reference; linear maintenance of prefix stacks |
| Setter's offline segment tree | $O(N\log N+M\log M+M\log N)$ | $O(N+M)$ | Maintains surviving positions with minima and counts |
| Predecessor binary lifting | $O((N+M)\log N)$ | $O(N\log N)$ | Answers queries as read, without storing or sorting them |

The segment tree's operations, correctness and amortized bound are in its [full explanation](solution-alternative.en.md) and [alternative.cpp](alternative.cpp). The predecessor-path interpretation is in the [binary-lifting explanation](solution-alternative-binary-lifting.en.md) and [alternative-binary-lifting.cpp](alternative-binary-lifting.cpp). Binary lifting uses a larger precomputed table to answer each query immediately in input order.

Setter contribution: deletion and interval-count segment tree with right-endpoint ordering. GPT-6 applies classical monotone stacks and binary lifting to provide the other formulations, proofs, safe implementations and bilingual materials. These underlying techniques are established methods. Small cases use direct simulation of every query; formal cases also use independent predecessor jumps. See the [measurements](../../../docs/benchmark-R25.json).
