# An Upgrade Plan for Battles: Heap Scheduling

**This uses the setter’s quotient events and monotone defence choice. GPT-6 replaces the precomputed event table with a min-heap containing one pending event per enemy type, reducing event storage.**

## Method

For attack and defence upgrade counts $x,y$ , one enemy of type $i$ takes
$$
t_i=\left\lceil\frac{h_i}{A_0+xV_A-d_i}\right\rceil
$$
rounds. Total damage is $\sum_i k_it_i\max(a_i-D_0-yV_D,0)$ , and required health is the larger of $H_0$ and total damage plus one. First raise attack enough to damage every enemy type.

Cost is discretely convex in defence count. As attack increases, the health cost saved by another defence upgrade never increases. Starting from damage-free defence and decreasing it only when cost strictly improves therefore maintains the optimum with a pointer that only moves left. Equal-cost choices retain higher defence because it requires less health. Defence buckets and exact wide-integer comparisons are the same as in the [main solution](solution.en.md).

Keep at most one event for each enemy type. If its current round count $t_i>1$ , its next event occurs at
$$
x_i'=\left\lceil
\frac{d_i+\lceil h_i/(t_i-1)\rceil-A_0}{V_A}
\right\rceil.
$$
Insert $(x_i',i)$ into a min-heap. Evaluate the first feasible attack, then repeatedly:

1. Take the smallest attack count $x$ in the heap.
2. Process every event at $x$ , updating that enemy’s round count and defence bucket.
3. After each event, compute and insert that enemy’s next event. End its event chain when one round remains.
4. Move the defence pointer and update the answer using $(\text{cost},H,D,A)$ .

Enemies already blocked by initial defence need no damage events, but their defence still constrains the first feasible attack.

## Correctness

The event formula gives the smallest single-round damage that lowers the current round count, so its attack count is strictly later. Every enemy’s event chain is ordered, and the heap always reveals the earliest unprocessed change among all enemies. After all events at one count are processed, every round count is exact.

Between events, damage and the best defence/health choice remain unchanged, while positive attack cost increases. Only the interval’s left endpoint matters. Defence convexity and monotonicity make the pointer optimal for every candidate attack; tuple comparison gives the global optimum and the requested tie-breaking.

Simultaneous combat includes the enemy’s final attack, and required health is damage plus one. Bucket values can exceed 64 bits; the implementation keeps the two-limb representation and division-based comparisons, without floating-point decisions.

## Complexity and tradeoffs

Let $E=O(\sum_i\sqrt{h_i})$ and let $Y$ be the maximum defence count. The heap contains at most $n$ entries. Total time is $O((n+E)\log n+Y)$ and space is $O(n+Y)$ . No attack-index array or complete event list is needed.

The heap removes the table method’s $R+E$ storage terms but adds logarithmic scheduling work per event. It is not faster on every input. Both are coequal full-range solutions; this implementation is useful when memory is more constrained.

[Program](alternative-heap.cpp).
