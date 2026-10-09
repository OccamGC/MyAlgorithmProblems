# Digging the Subway: Solution

## Algorithm and Attribution

The authorized redesign sets the vertex limit to 1000. Codex (GPT-6) provides the exact connected-subtree DP in [std.cpp](std.cpp). Fixing a longest first path is unsafe: sample 6 needs only two paths to cover weight 42, whereas extending a particular single-path optimum can require three. Optimal unions for different operation counts need not be nested.

## An Optimal Union Can Be Connected

If the union is disconnected, choose paths $s_1\to t_1$ and $s_2\to t_2$ in different components. Swap their ends to obtain $s_1\to t_2$ and $s_2\to t_1$ . In a tree, their union preserves both old paths and adds the connector between them. Starts remain marked. Repeating this connects the union without increasing the number of paths or decreasing weight.

It suffices to consider connected subtrees containing a marked vertex.

## The Number of Paths for One Subtree

For a subtree $S$ with at least one edge, let $L$ be its number of leaves and $q$ its number of unmarked leaves. Its minimum required operations are

$$c(S)=\max\left(q,\left\lceil\frac L2\right\rceil\right).$$

Necessity: every leaf is an endpoint of some covering path. A path has at most two leaf endpoints, and its marked start cannot be an unmarked leaf. Thus both lower bounds apply.

For sufficiency, take $i\ge c(S)$ . Prepare $i$ marked-start slots and $i$ arbitrary-end slots. Put unmarked leaves in end slots and the remaining leaves in unused slots, preferring start slots. The inequalities $q\le i$ and $L\le2i$ ensure enough room. Fill unused starts with any marked vertex of $S$ and fill the remaining ends arbitrarily. Pair the slots into $i$ paths. Including zero-length paths as singleton vertices, their union contains every leaf. Apply the endpoint swaps above until it is connected. A connected subgraph containing every leaf of $S$ contains every edge of $S$ , completing the proof.

![Two permitted paths cover the entire regression tree](assets/example.svg)

## Tree DP

Choose any root. At $u$ , maintain a connected selected part containing $u$ with:

- leaf count $L$ and unmarked-leaf count $q$ contributed below it;
- whether it contains a marked vertex, $b$ ;
- selected child-edge count $d$ , capped at 2;
- maximum edge weight for that state.

A child's returned table assumes its parent edge is selected but excludes that edge's weight. When merging a child, either omit the whole branch or take one returned state and add the connecting edge. Add the two leaf counts, OR the marked flags, and increment $d$ with a cap of 2.

After merging children:

1. To return a state to the parent, count $u$ as a leaf exactly when $d=0$ .
2. To close a complete subtree at $u$ , require $d>0$ and a marked vertex. Count $u$ as a leaf exactly when $d=1$ . Evaluate $c(S)$ and update that answer with its weight.

Every connected subtree has a unique highest vertex, so closing states considers all candidates. Keeping only the maximum weight for each state is safe: later merges depend only on these counts and the marked flag.

Finally take prefix maxima. Repeated operations pad any solution to exactly $i$ operations. The first answer equal to the total tree weight is $\mathrm{need}$ ; positive weights make equality equivalent to covering all edges.

## Complexity and Implementation

A part of size $s$ has $O(s^2)$ states. Merging sizes $a,b$ costs $O(a^2b^2)$ . Expanding the product and charging vertex choices to the merge first joining their parts gives a total upper bound of $O(n^4)$ . Traversal is iterative.

Release each child table after merging. Retained complete tables correspond to disjoint parts, whose squared sizes sum to at most $n^2$ . Together with the reusable dense temporary table, auxiliary space is $O(n^2)$ . Timestamps avoid clearing that table at every merge; only present states are scanned.

Small tests enumerate actual path masks and their unions without the leaf formula. Large stars use two-type leaf counts; single-start trees use an independent marginal-gain merge. See [validation and performance](tests/README.md).
