# Snow White: Solution

## Algorithm and Attribution

Codex (GPT-6) derived the height-wise edge bound and construction in [std.cpp](std.cpp). The same-level source/sink search order follows [Raghavan's correction to strong-connectivity augmentation](https://terpconnect.umd.edu/~raghavan/preprints/stc.pdf): stop each source search at its first unvisited sink. The treatment of height boundaries and the choice between open and closed paths are proved below.

## Components, Feasibility, and Cost

Contract the existing strongly connected components. Every component has one height because existing edges never ascend. The resulting DAG has nonincreasing heights. A single component needs cost 0 and zero new edges.

Sort the distinct heights. Every gap between consecutive heights must be crossed by an existing descending edge. Otherwise no edge, including a permitted new edge, can cross that cut downward. Check these gaps with difference counts on height indices.

The construction below also proves sufficiency. Let the minimum and maximum heights be $H_0,H_1$ . Travel from the minimum to the maximum requires at least $H_1-H_0$ total ascent, giving the lower bound

$$C=H_1-H_0.$$

Our positive-cost edges partition this height interval and attain the bound.

![One uphill edge completes a descending chain](assets/example.svg)

## Lower Bound on the Number of Edges

At height $H$ , let $a_H$ count zero-indegree components in the entire condensation and $b_H$ count zero-outdegree components. Set $q_H=\max(a_H,b_H)$ . An isolated component belongs to both counts.

At total cost $C$ , exactly one positive-cost added edge crosses every height gap. Their height intervals therefore partition $[H_0,H_1]$ . The bottom has one ascending departure, the top one ascending arrival, and each intermediate stop has one of each.

A non-stop level needs at least $q_H$ same-level edges; a stop needs at least $q_H-1$ . The bottom needs $\max(a_{H_0},b_{H_0}-1)$ and the top needs $\max(a_{H_1}-1,b_{H_1})$ . With $p$ positive-cost edges there are $p-1$ intermediate stops, so

$$
k\ge\sum_H q_H+1-[b_{H_0}>a_{H_0}]-[a_{H_1}>b_{H_1}].
$$

If all heights are equal, the answer instead is the usual DAG augmentation bound $\max(a_H,b_H)$ ; the single-component case was handled separately.

## Opening a Path Within One Level

Consider the DAG of one height. Endpoints of incoming edges from higher levels are upper entrances; starts of outgoing edges to lower levels are lower exits. Let $A,B$ be the global sources and sinks at this height.

Run DFS from each source in $A$ with shared visited marks. Stop a search immediately at its first unvisited global sink and record a pair $(s_i,t_i)$ . An unsuccessful search exhausts its reachable unvisited part. Consequently:

- Every unmatched source reaches a matched sink or a lower exit.
- Every unmatched sink is reachable from a matched source or an upper entrance.

The first claim follows from how unsuccessful searches end. For the second, trace an unmatched sink backward to a local source. It is an upper entrance or a global source. A successful global source is matched; an unsuccessful search would find this sink unless it first meets a previously successful search region. Ordinary vertices reduce to these boundaries by following the DAG forward and backward.

Join paired paths using $t_i\to s_{i+1}$ . Pair as many unmatched sinks and unmatched sources as possible with new edges. Attach any remaining sources from the main path's end, or append remaining sinks as a chain. This produces endpoints $P,Q$ with a path from $P$ to $Q$ . Every local vertex is reachable from $P$ or an upper entrance and can reach $Q$ or a lower exit. Exactly $q_H-1$ edges are added.

If there are no matched paths, first pair unmatched sinks with unmatched sources. Equal counts yield no main path and use $q_H$ edges; every vertex has access from above and toward below. Unequal counts leave vertices of one type: chain these as $P$ to $Q$ , using $q_H-1$ edges. When $a_H=b_H=0$ , add nothing.

## Closing a Path or Choosing a Stop

For an intermediate level with a main path, test reachability after those same-level additions:

1. Can an upper entrance reach $Q$ ?
2. Can $P$ reach a lower exit?

If both hold, add $Q\to P$ and omit this level from the ascending stops. Every vertex then has access from above and toward below. Otherwise leave the path open and choose it as a stop. Closing uses $q_H$ same-level edges; stopping uses $q_H-1$ , matching the lower bounds.

Choosing every open path as a stop without this test is incorrect. Sample 4 covers this failure: separate parts at one height can prevent backward connectivity along the ascending path.

At the bottom, introduce a virtual source pointing to every upper entrance and process it first. The resulting end $Q$ starts the global ascending path. The number of real same-level edges is $\max(a_{H_0}+1,b_{H_0})-1=\max(a_{H_0},b_{H_0}-1)$ . No output edge uses the virtual source. At the top, apply the symmetric procedure to reversed edges and reverse the additions back, obtaining the global endpoint with $\max(a_{H_1}-1,b_{H_1})$ edges.

Finally connect stops in increasing height order, from the previous $Q$ to the next $P$ . Positive costs telescope to $C$ . Same-level counts and stop counts cancel exactly as in the lower bound for $k$ .

## Strong Connectivity

Call the path through all stops the ascending backbone. The local properties let each vertex be entered from its local backbone start or a higher level, and leave toward its local backbone end or a lower level. Repeatedly following strictly changing heights eventually connects it to the backbone in both directions.

Suppose the final graph is not strongly connected. The backbone traverses its SCCs in order. Choose adjacent distinct SCCs along it. Put all vertices reachable from the later SCC on the later side and all others on the earlier side. There is no edge from the later side to the earlier side, and the backbone is split into a prefix and suffix.

If the split lies between different heights, the local entrance and exit properties put every lower-level vertex on the earlier side and every higher-level vertex on the later side. An existing descending edge crossing this gap contradicts the absence of a backward edge.

If the split lies inside an open path at height $H$ , all strictly lower vertices are earlier and all strictly higher vertices are later. An existing edge crossing the gap just below $H$ cannot start strictly above $H$ , or it would already cross the split backward. It must therefore leave an earlier vertex at height $H$ . The local properties force $P$ to reach a lower exit. Symmetrically, an edge crossing the gap just above $H$ forces an upper entrance to reach $Q$ . Both conditions would have caused the algorithm to close this path and omit the stop, a contradiction. Bottom and top stops each consist of one vertex, so no internal split occurs there.

Thus the backbone and all vertices belong to one SCC. The construction attains both lower bounds and is optimal.

## Complexity and Validation

Iterative Kosaraju, local DFS, local reachability tests, and gap differences take $O(n+m)$ time. Sorting heights takes $O(n\log n)$ . Total time is $O(n\log n+m)$ and space is $O(n+m)$ . No recursion risks overflowing on a 500000-vertex chain.

An independent iterative Tarjan checker verifies final strong connectivity, edge directions, total cost, and optimal edge count. Tiny graphs additionally enumerate added-edge subsets. Formal data cover full limits, impossible gaps, isolated vertices, large equal-height SCCs, and the close-path regression. See [tests and performance](tests/README.md).
