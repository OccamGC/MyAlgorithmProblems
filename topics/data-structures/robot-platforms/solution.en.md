# Roboport Network: Doubly Linked Ring

Problem setter's solution: a doubly linked ring with modulo reduction and shortest-direction movement. Codex (GPT-6): explicit empty-ring invariants, bilingual proofs and validation, plus an implicit treap alternative that represents circular positions by rank.

## Preferred solution

Index arrays by roboport number and store the direction-$0$ successor and direction-$1$ predecessor of each roboport. Also store the current number, active size, and largest number ever assigned. Initially connect $1,2,\ldots,n$ into a ring.

To insert $z$ after the current node $u$ with successor $v$ , replace $u\to v$ with $u\to z\to v$ , updating reverse links as well. To delete $u$ with predecessor $p$ and successor $v$ , connect $p\to v$ and make $v$ current. When inserting into an empty ring, both links point to the new node itself. Removing the last node sets the current number to zero. Queries use the active size to detect an empty ring.

For a nonempty ring of size $s$ , normalize movement to $r=((x\bmod s)+s)\bmod s$ . If $s-r<r$ , reverse direction and walk $s-r$ steps; otherwise walk $r$ steps in the requested direction. C++ remainders can be negative, so normalization is necessary.

## Correctness

Maintain the invariant that each active node's links point to its successor and predecessor, the two directions are inverse relations, and the current number is valid whenever the ring is nonempty. The initial ring satisfies it. Insertion replaces one neighboring pair; deletion connects the removed node's neighbors. Other links are unchanged, and empty and singleton rings are handled by definition. Thus insertion, deletion and queries are correct.

Walking $s$ steps in either direction returns to the starting node, so removing full laps preserves the destination. Walking $r$ steps forward reaches the same node as walking $s-r$ steps backward. Choosing the shorter route therefore preserves the destination as well. All operations are correct.

## Complexity and comparison

Let $B$ be the guaranteed upper bound on the shortest movement; here $B=500$ . Initialization takes $O(n)$ time. Insertion, deletion and queries take $O(1)$ time, and movement takes $O(B+1)$ . Total time is $O(n+m(B+1))$ , and arrays covering all assigned numbers use $O(n+m)$ space. Deleted numbers are not reused, so their array slots need not be reclaimed.

See [std.cpp](std.cpp). The [implicit treap](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), moves by rank using constant-time integer arithmetic. Insertion, deletion and queries take expected $O(\log(n+m))$ time. It removes dependence on the step bound, at the cost of more storage, tree operations, and a balance assumption on random priorities. Both are parallel options and pass the full data. With the stated step bound, the linked ring remains preferred for its direct, deterministic operation bounds.

Tests cover rebuilding an empty ring, never reusing numbers, reversed directions, insertion into a two-node ring, extreme signed steps, and repeated $500$-step movements. See the [test plan](tests/plan.json) and [measurements](../../../docs/评测环境与性能.md).
