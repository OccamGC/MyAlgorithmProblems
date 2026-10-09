# Journey with Limited Fuel Supplies — Alternative Solution

Codex (GPT-6): deque DP, flow and stop-state models, proofs, implementations, and verification for this problem, using established dynamic-programming and flow methods.

## Cost: each fuel unit supplies a road segment

Sort and include the start and destination. Let consecutive distances be $d_i$ and effective capacity be $C$ . Any $d_i>C$ is immediately infeasible. Create station vertices plus a source and sink:

- Source to station $i$ : capacity $\min(s_i,C)$ and cost $c_i$ , representing purchase.
- Station $i$ to sink: capacity $d_i$ and zero cost, representing this segment's consumption.
- Station $i$ to the next station: capacity $C-d_i$ and zero cost, representing fuel remaining after driving this segment.

Require total flow $L=\sum_i d_i$ . All consumption capacities sum to $L$ , so full flow saturates each one. Flow conservation says purchased plus arriving fuel equals segment consumption plus carried fuel. The latter is at most $d_i+C-d_i=C$ , exactly the tank bound. Conversely, any full flow reconstructs a valid purchasing plan.

Nonnegative prices allow an optimal plan that arrives empty: trace fuel consumption and remove purchases of fuel never consumed. This preserves feasibility and cannot increase cost. Restricting total purchases to $L$ therefore preserves an optimum. No single purchase can exceed tank capacity, justifying the source-edge truncation.

Use successive shortest augmenting paths with potentials. Initial forward costs are nonnegative, so zero potentials work. After Dijkstra, update potentials by finite distances, preserving nonnegative reduced costs on reachable residual edges. Integral capacities ensure each augmentation sends at least one unit, so at most $L$ augmentations occur. Insufficient flow means unreachable.

## Stops: maximum remaining fuel at each count

Scan stations and let $fuel[t]$ retain the maximum fuel with $t$ refueling stops, initially only $fuel[0]=0$ . Skipping a purchase preserves the state. If there is room and stock, buy up to $\min(C,fuel[t]+s_i)$ and update count $t+1$ . Update counts downward to avoid buying repeatedly at the same station. Subtract the next distance and discard negative states.

For minimizing stops, more remaining fuel dominates less at the same used count. Without a purchase the advantage persists; with a purchase, $\min(C,f+s)$ is monotone in $f$ . If extra fuel makes some future purchase unnecessary because the tank is already full, omit that stop and use no more stops. Thus discarding lower-fuel states at an exact count cannot discard the minimum achievable count. At the destination, take the smallest surviving $t$ .

## Complexity, Contributions, and Tradeoffs

The graph has $O(N+1)$ vertices and edges. Flow takes $O(L(N+1)\log(N+2))$ time; the stop DP takes $O((N+1)^2)$ , plus sorting. Space is $O(N+1)$ , with no table indexed by tank capacity. Costs and potentials use signed 64-bit integers.

Formal measurements are slower than the [fuel-state deque method](solution.en.md). This model explains conservation and capacity constraints and independently checks minimum costs. The published time limit includes measured room for both complete methods. Codex (GPT-6) supplied [alternative.cpp](alternative.cpp).

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
