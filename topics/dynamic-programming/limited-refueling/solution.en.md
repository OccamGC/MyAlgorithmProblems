# Journey with Limited Fuel Supplies — Solution

Codex (GPT-6): deque DP, flow and stop-state models, proofs, implementations, and verification for this problem, using established dynamic-programming and flow methods.

## Fuel states and independent objectives

Sort stations by position. Insert a virtual zero-stock station at the start if needed, and append the destination. Unlimited capacity can be replaced by $C=L$ : reduce purchases in any plan with leftover fuel until total purchases are $L$ . Nonnegative prices prevent a cost increase, stop count cannot increase, and carrying at most $L$ suffices. For finite capacity, use $C=R$ .

Maintain separate tables for arriving with fuel $g$ : minimum cost $dp[g]$ and minimum stops $cnt[g]$ . Initially only zero fuel is feasible. Optimize the tables independently; the stop count of a cheapest plan need not answer the second objective.

For price $c$ and stock truncated to $s=\min(s_i,C)$ , the cost of departing with fuel $f$ is

$$new[f]=cf+\min_{\max(0,f-s)\le g\le f}(dp[g]-cg).$$

As $f$ increases, eligible indices form a sliding window. Maintain its minimum with a monotone deque in $O(C)$ time per station. Do not insert unreachable states.

For stop counts, distinguish no purchase from a positive purchase:

$$next[f]=\min\left(cnt[f],\ 1+\min_{\max(0,f-s)\le g<f}cnt[g]\right).$$

The second window excludes $f$ , ensuring a positive purchase; an empty window is unreachable. A monotone deque again gives linear time per station.

After purchasing, let the next distance be $d$ . Keep departure states with fuel at least $d$ and subtract $d$ from their indices. At the destination, minimize each table over all remaining fuel quantities. If unreachable, print two $-1$ values.

## Correctness

Given arrival fuel $g$ and departure fuel $f$ , the unique purchase is $f-g$ . Window bounds express precisely nonnegative purchasing, stock, and tank limits. Its cost is $c(f-g)$ , and it adds one stop exactly when positive. The recurrences therefore enumerate all and only legal decisions. Travel shifts likewise enumerate exactly the states able to reach the next position. Induction over stations proves that each table independently stores its optimal objective; minimizing at the destination gives the answers.

## Complexity and Contributions

Time is $O(N\log N+(N+1)C)$ and space is $O(N+C)$ . Cost is at most $10^9L$ ; use signed 64-bit integers and a sufficiently large unreachable sentinel, excluding it before arithmetic. Codex (GPT-6) completed the specification, derived the deque transitions, and implemented and verified [std.cpp](std.cpp).

The [flow and stop-state alternative](solution-alternative.en.md) offers a different model and space dependence.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
