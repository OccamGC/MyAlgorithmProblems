# Metro Delivery — Solution

## Comparing solutions

The problem setter’s method uses a heap to select the road segment with maximum current marginal gain and a segment tree to maintain waiting slack. It compresses in one batch until the next event: the budget is exhausted, a segment reaches zero, or a station's waiting slack reaches zero. The last event truncates the affected interval and updates candidates. Recomputing only at such events avoids one operation per budget unit. The marginal-gain and event-count proofs below retain this reasoning.

A station with zero resources need not wait for its supplied time; use the corresponding effective threshold. The implementation must also handle one station, zero budget and large cumulative times. Codex (GPT-6) contributed these implementation details and boundary explanations. The heap, segment tree and event-batching algorithm takes $O(n\log(n+1))$ time and $O(n)$ space.

## Arrival times and the objective

The train cannot return. If $\mathrm{Num}_i>0$ , it must collect the resources at station $i$ , so it cannot leave before $T_i$ . If $\mathrm{Num}_i=0$ , there is nothing to collect there, and its production time imposes no departure constraint. Define the effective release time $R_i=T_i$ for a positive quantity and $R_i=0$ for a zero quantity; also set $R_n=0$ .

Fix the reduced travel times $D_i$ . Extra waiting can only delay deliveries, so optimal arrival times satisfy

$$A_1=0,\qquad A_{i+1}=\max(A_i,R_i)+D_i$$

Station $j$ receives $W_j=\sum_{i<j}\mathrm{Num}_i$ resources. The total time is

$$\sum_{j=1}^{n}W_jA_j-\sum_{i=1}^{n-1}(n-i)\mathrm{Num}_iT_i$$

The second term is constant, so we minimize the weighted sum of arrival times. Define $P_j=\sum_{t=1}^{j}W_t$ to obtain sums of delivery quantities over intervals.

## The effect of one reduction

Let the slack be $S_i=A_i-R_i$ . If $S_i\le0$ , the train already waits for production before leaving. An earlier arrival cannot make its departure earlier. Such stations stop the propagation of arrival changes; the final station $n$ is also a boundary.

Reducing segment $i$ by $1$ makes arrivals at stations $i+1$ through the next boundary $r$ earlier by $1$ , including the arrival at $r$ . Later arrivals do not change. The benefit is

$$G(i,r)=P_r-P_i$$

This is the total number of resources delivered at the affected stations. All times and slacks are integers, so each positive interior slack is at least $1$ .

Between consecutive boundaries, all segments have the same right endpoint of influence. An earlier segment affects more stations and has at least as much benefit. Thus the only candidate needed for an interval is its leftmost segment whose remaining travel time is positive.

## Why the greedy choice is optimal

First consider the leftmost available segment $l$ in one interval. Suppose an optimal remaining allocation spends operations in this interval but does not choose $l$ . Let $j$ be the leftmost segment it does choose in the interval, and move one of its operations to $l$ . The receiving segment has positive length and had no reduction in that allocation, so the move is legal.

The allocation makes no reductions on segments $l$ through $j-1$ , and every intervening station currently has positive integer slack. Thus no intervening wait absorbs the transferred reduction: arrivals at stations $l+1$ through $j$ all become $1$ earlier. Crossing segment $j$ now takes $1$ longer, exactly canceling this advance. All later arrivals are unchanged, and earlier deliveries can only improve. Repeated exchanges therefore give an optimal allocation that processes the current leftmost available segment and redistributes operations whenever a new boundary appears.

Equivalently, consider the marginal benefits exposed by this process. Within an interval, the leftmost available segment has the greatest current benefit. This benefit stays constant until that segment is exhausted or the interval splits. Exhaustion moves the candidate to the right; a split leaves child intervals containing only subsets of the original stations. Since $W_j\ge0$ , every subsequent candidate has benefit at most that of its preceding phase. Existing boundaries persist because reducing travel times never makes arrivals later.

The operations in each interval can therefore be organized into phases of nonincreasing benefit, with a phase becoming available only after its predecessor is completed. Changes in different intervals do not propagate past their boundaries. Choose the largest available benefit each time: an unavailable phase cannot have a larger benefit than its predecessor, so no larger benefit is hidden behind it. By exchanging the order of operations in an optimal allocation, its next operation can agree with this choice. Repeating the exchange proves optimality.

## Process many reductions at once

Maintain each interval's candidate and benefit in a maximum heap. For the selected interval, let $l$ be its leftmost available segment and $r$ its right boundary. The benefit remains unchanged for

$$\Delta=\min\left(K,D_l,\min_{l<j<r}S_j\right)$$

operations. Treat the last term as positive infinity when there are no interior stations.

1. Subtract $\Delta$ from the remaining budget and $D_l$ .
2. Subtract $\Delta$ from all slacks in $(l,r]$ . Their arrival times decrease by the same amount.
3. Find every interior station whose slack has just become zero and split the interval there.
4. Skip exhausted segments in each child interval and insert its leftmost available candidate into the heap.

A segment tree supports range addition, range minimum queries, and finding new boundaries by pruning nodes with positive minima. A separate difference array records all interval advances. Recover the final arrival times and substitute them into the objective.

Stop when no positive benefit remains, since using fewer command blocks is allowed. The reference code uses zero-based indices: `Delivered` stores $W$ , `Prefix` stores $P$ , and `Ready` stores the effective release times $R$ .

## Complexity and integer ranges

Each complete batch exhausts an edge or creates a permanent boundary; at most one additional batch exhausts the budget. There are $O(n)$ batches. Each new boundary is inserted once, and each zero-length segment is skipped once as candidate left endpoints advance. Segment-tree and heap operations take $O(n\log n)$ total time and $O(n)$ space, independently of the numerical value of $K$ . The same implementation returns $0$ for $n=1$ .

Arrival times, slacks, and benefits fit signed 64-bit integers. The complete objective may exceed that range, so compute it modulo $10^9+9$ term by term only after optimization. Heap comparisons must use exact benefits. Reduce factors before multiplication and normalize modular subtractions. Replacing $T_i$ by $R_i$ in the production term is harmless: they differ only when $\mathrm{Num}_i=0$ .

## Validation and contribution

All 4 samples and 708 independent exhaustive comparisons passed. The oracle enumerates every vector of segment reductions within the budget and directly simulates deliveries, without the greedy boundary algorithm. Checks distinguish zero and positive quantities with identical release times, and cover empty tasks, zero travel times, budgets larger than the route, and modular arithmetic with large values.

Codex (GPT-6): contributed the segment-tree and maximum-heap implementation of batched greedy processing, zero-resource handling, modular arithmetic, boundary explanations and independent validation. See [std.cpp](std.cpp).
