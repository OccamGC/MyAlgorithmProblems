# Spode Seminary Editorial

**Problem setter’s solution: reverse reachability in a residual network, incremental augmentation, and latest feasible ranks.** Codex (GPT-6) supplies the monotonicity proof and replaces recursive searches with explicit traversals. The reference program preserves the algorithm.

## 1. Fix tiers while allowing reassignment within a tier

Process students by rank. An admitted student has capacity-one edges only to mentors in the student’s determined admission tier. Each mentor has an edge to the sink with capacity equal to its quota. Every admitted student sends one unit of flow to a mentor.

Do not fix a particular mentor permanently. Residual alternating paths through a mentor, an admitted student, and another mentor can rearrange assignments within the same tiers, freeing a seat without changing any earlier admission tier.

## 2. Mentors that can accept one more student

Traverse from the sink in the reverse direction of residual edges. This marks precisely the vertices that can reach the sink in the residual network. A mentor is marked exactly when it can accept an additional student while retaining all earlier tiers.

Sufficiency follows by augmenting along a residual path from that mentor to the sink, either consuming a free seat or obtaining one through reassignment.

For necessity, subtract the current assignment from any feasible assignment with one extra student at that mentor. The difference contains a residual augmenting path from the mentor to the sink; other differences decompose into cycles and do not supply the extra unit.

Scan the current student’s mentors and select the smallest tier containing a marked mentor. If none exists, leave the student unassigned. Otherwise add edges to the marked mentors in that tier and augment one unit from the student. At most three edges are added per student.

Unmarked mentors can be omitted permanently. If such an assignment became feasible later, removing all later students would make it feasible now, contradicting the failed reachability test.

## 3. Minimum promotion

Suppose the current student is ranked $r$ . Immediately before processing rank $t$ , update every currently feasible mentor’s latest feasible rank to $t$ . Unmarked mentors retain their earlier records.

As more admission requirements are fixed, a mentor can only lose the ability to accept another student. Adding requirements cannot enlarge the set of feasible assignments for earlier students. This argument does not depend on which particular flow is stored.

Among mentors within the current student’s satisfaction threshold, take the largest recorded rank $t_{\max}$ . If none has ever been feasible, satisfaction is impossible. Otherwise the answer is

$$r-t_{\max}$$

Moving this student to position $t$ leaves exactly the original first $t-1$ students ahead. Their priority admission results do not depend on later students, so the saved feasibility at that prefix is exactly the feasibility needed by the promotion query. Monotonicity makes the latest feasible position the one requiring the fewest moves. If $t_{\max}=r$ , the answer is zero.

## Correctness and complexity

Induct on rank. Residual reachability identifies exactly the feasible mentors while preserving earlier tiers, so choosing its smallest tier implements the admission rule. Augmentation preserves quotas and all established tiers. This proves the admission results. The prefix correspondence and monotonicity prove the promotion results.

Let $n$ be the student count, $m$ the mentor count, and $q$ the number of rankings. The network has $O(n+m)$ vertices and edges. Each student requires one reverse traversal, at most one augmentation, and a scan of $m$ preferences. Total time is $O(qn(n+m))$ ; space is $O(nm)$ for preferences plus $O(n+m)$ for the network.

Reset the network and latest-reachability records for every ranking. Satisfaction threshold zero, zero quotas, unlisted mentors, same-tier reassignment, and unassigned students all follow the same logic.

## Data and validation

`tests/generate.py` uses fixed seeds and accepts a compiled reference program with `--std` . Cases include shared preferences, three mentors per tier, augmenting chains, zero quotas, and ample quotas. The independent oracle enumerates every legal assignment, selects the lexicographically smallest tier vector in ranking order, and repeats the enumeration for every possible promotion position. See [environment and measurements](../../../docs/评测环境与性能.md).
