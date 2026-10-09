# Nether Portal: Solution

## Algorithm and Attribution

[std.cpp](std.cpp) follows the setter's bounded relaxation and predecessor-cycle acceleration. Codex (GPT-6) completed the specification, proof, and tests, detached predecessors immediately at opening-time floors, and rescheduled every accelerated vertex. An independent [deadline algorithm](alternative-deadline.cpp) is also provided. Both share [portal-graph.hpp](portal-graph.hpp) for graph construction.

## Three Possible Answers

First check world reachability without time constraints. Waiting is allowed and every opening time is finite, so this exactly determines whether the target world is reachable. Otherwise print `YouNeedOpPermission` .

If the target world's step time is negative, arbitrarily many round trips near the target make arrival unbounded below: print `NegativeInfinity` . Otherwise the final portal arrives no earlier than $t_i+\delta_i\ge-20000$ , and subsequent movement cannot decrease time. A route using no portals also cannot arrive before 0. Thus every finite answer is at least $-20000$ . A negative intermediate world alone does not imply negative infinity, since the next portal still has an opening time.

## State Graph

A portal state records the time at its entrance, after its opening time, ready to use it. Add virtual start and target states. Connect state $i$ to $j$ when the exit of $i$ and entrance of $j$ share a world. Let their Manhattan distance be $d_{ij}$ and the world's step time be $T$ .

For $T\ge0$ , the transition is

$$x_j=\max(t_j,x_i+c_{ij}),\qquad c_{ij}=\delta_i+Td_{ij}.$$

For $T<0$ , take sufficiently many round trips and then wait until the next opening: $x_j=t_j$ . This is a reset edge. Virtual states have zero portal change and a sufficiently small opening-time sentinel. The start label is initially 0.

![Opening-time floors and resets in negative-time worlds](assets/example.svg)

There are at most 50 real entrances per world, so $V=N+2$ and $E\le52V$ . Use 64-bit arithmetic for coordinate differences, products, and time labels.

## Reference Algorithm: Relax and Accelerate

Maintain attainable earliest-known labels and scan changed states. A relaxation reaching the destination opening time clears its predecessor. Otherwise record the improving affine edge. Reset edges always clear predecessors.

Each vertex has at most one predecessor. Every predecessor cycle has negative total weight: predecessors are installed only on strict improvements, and the last installed edge closes a strictly decreasing cycle. Since labels only decrease afterwards, each recorded edge satisfies $d_v\ge d_u+c_{uv}$ .

For a cycle, compute

$$\Delta=\min_{u\to v\text{ on cycle}}(d_u+c_{uv}-t_v).$$

If $\Delta>0$ , subtract it from every cycle label and reschedule all cycle vertices. No label crosses its opening floor. Repeatedly traversing the negative cycle can reach these labels or earlier: at the proposed labels every cycle transition is still affine, with at least one candidate exactly at a floor. Waiting realizes any later recorded time. If $\Delta\le0$ , ordinary relaxation reaches a floor and breaks the predecessor cycle instead.

Finite labels are integers; real portals have fixed lower bounds, and virtual states connect through finite portal arrivals or nonnegative movement. Hence the process terminates. At termination no edge improves a label. Induction along any finite route shows that its arrival cannot beat the final label; every recorded label is also attainable. The result is therefore optimal.

For $R$ full scan rounds, time is $O(R(E+V))$ and space is $O(E+V)$ . Acceleration skips repeated traversals that only consume a large time difference; no unconditional constant bound on $R$ is assumed. Tests include long cycles, a single negative edge, positive chains, and resets, and compare the implementation below with an explicit polynomial bound.

## Alternative and Tradeoffs

The [deadline solution](solution-alternative-deadline.en.md) and [implementation](alternative-deadline.cpp) binary-search the answer while propagating latest departure times backward. Worst-case time is $O(VE\log(U+20001))$ and space is $O(V+E)$ , where $U$ is the arrival time of a feasible route. It has a direct polynomial bound but repeats the decision process; the reference retains the setter's cycle acceleration. Both pass the full data and current limit.
