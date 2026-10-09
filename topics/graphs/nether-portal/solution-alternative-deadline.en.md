# Nether Portal: Deadline Feasibility

Codex (GPT-6) provides the independent backward decision algorithm in [alternative-deadline.cpp](alternative-deadline.cpp). The [main solution](solution.en.md) retains the setter's predecessor-cycle acceleration. Both pass all tests. This version has an explicit polynomial worst-case bound but requires multiple decisions.

## Shared Model

Each portal state is its ready time after opening, with virtual start and target states. A nonnegative-step world gives $x_v=\max(t_v,x_u+c_{uv})$ ; a negative-step world resets directly to $t_v$ . There are $V=N+2$ vertices and $E\le52V$ edges. Handle unreachable targets and negative-time target worlds first; see the [main solution](solution.en.md) for the full reduction.

## Decision and Binary Search


For a deadline $X$ , propagate backward the latest ready time $L_u$ that can still reach the target in time. Initialize the target to $X$ . An affine edge gives $L_u=L_v-c_{uv}$ , usable only when it is at least $t_u$ . Reaching the start with $L_0\ge0$ proves feasibility.

A backward-reached reset edge with a forward-reachable source also proves feasibility: its source can arrive arbitrarily late and still take enough negative-time round trips. Improvements persisting for $V$ rounds imply a positive-gain backward cycle. Repeating it permits arbitrarily late entry; forward reachability and waiting then connect the start to it. Without a beneficial cycle, a witness can be simplified to at most $V-1$ edges, proving the round criterion.

Binary search $[-20000,U]$ , where $U$ comes from an actual traversal along any reachable world route. Time is $O(VE\log(U+20001))$ and space is $O(V+E)$ . This reverses the direction and uses feasibility rather than direct minimization, providing an independent comparison. Its worst-case bound is simpler, at the cost of repeated decisions. Both implementations pass the formal time limit; see [test details](tests/README.md).
