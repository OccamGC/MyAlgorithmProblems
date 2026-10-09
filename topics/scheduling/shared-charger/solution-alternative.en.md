# Alternative Solution

Contributions: the problem setter's solution supplies earliest-deadline simulation. Codex (GPT-6) supplies monotone buckets, implementation, and verification.

For a fixed power, put each device still needing charge into the bucket for its next deadline $d$ . Buckets use index-based linked lists. Each minute, remove one device from the earliest nonempty bucket, charge it, and recompute its deadline. Do not reinsert a device whose total acquired energy covers the entire exam.

A deadline earlier than the current minute means failure. Empty buckets mean success. Charging never decreases a device's next deadline, so the pointer to the earliest nonempty bucket only moves forward. Even at zero power, reinserting into the same bucket is safe: time advances and the infeasible instance is rejected.

This is the earliest-deadline schedule proved in the [preferred solution](solution.en.md). A device's ungenerated later jobs have deadlines no earlier than its next job, so storing only one job per device never hides the global earliest deadline. The exchange argument proves the greedy order correct. Recording the selected device each minute recovers an explicit schedule.

Initialization, bucket scanning, and charging take $O(n+m)$ per check. Binary search takes $O((n+m)(1+\log(H+1)))$ total time and $O(n+m)$ space, where $H$ is the maximum individual deficit. The setter's min-heap simulation takes $O(n+m\log(n+1))$ per check. Integer deadlines remove heap operations at the cost of $m$ buckets.

[alternative.cpp](alternative.cpp) gives correct results on the formal data, but its slowest median is about 0.738 seconds, above the 0.5-second limit. It is a backup. Deadline counting remains preferred; the bucket simulation directly exposes the execution order.
