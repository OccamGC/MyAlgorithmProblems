# The Great Cookie Swap: Solution

## Comparing solutions

The reference uses three-field summaries. With 64-bit numeric fields, the setter’s four-field summary and the three-field summary require 32 and 24 bytes per node respectively, a 25% payload reduction excluding container and allocator overhead.

The problem setter’s segment tree stores total supply, total demand, and residual supply and demand after maximizing exchanges within each interval. A merge first matches residual supply on the left to demand on the right, then does the reverse. If both kinds remain on one side, some internal exchanges on the other side are rerouted into two cross-side exchanges. Participants on opposite sides are distinct, so this is valid matching augmentation. A query merges the same summaries and subtracts residual demand from total demand.

The implementation used by Codex (GPT-6) uses the closed-form bottleneck bound proved below, storing only total supply, total demand and the largest individual supply-plus-demand. The old augmentation and the closed-form expression compute the same maximum exchange amount; the cut argument also explains why residual totals suffice in the old summary. Both build in $O(n)$ , update or query in $O(\log n)$ , and use $O(n)$ space. The new merge uses sums and a maximum instead of rerouting branches. This simplifies the summary and proof without an asymptotic speed gain.

## Three values summarize a range

For the participants in a query, define

$$\mathrm{Demand}=\sum_i d_i,\qquad \mathrm{Supply}=\sum_i s_i,\qquad \mathrm{MaxPair}=\max_i(d_i+s_i)$$

Here $\mathrm{Demand}$ is the total receiving capacity and $\mathrm{Supply}$ is the total providing capacity in the range. To obtain $\mathrm{MaxPair}$ , add each participant's two capacities and take the largest sum. These names also match the three members of `FSummary` in the reference solution.

The answer is

$$\min(\mathrm{Demand},\ \mathrm{Supply},\ \mathrm{Demand}+\mathrm{Supply}-\mathrm{MaxPair})$$

The first two bounds are total receiving capacity and total supply. For any participant $i$ , every delivery must use another participant's supply or another participant's receiving capacity, since self-delivery is forbidden. Thus the total is at most $(\mathrm{Supply}-s_i)+(\mathrm{Demand}-d_i)$ . Taking the tightest such bound gives $\mathrm{Demand}+\mathrm{Supply}-\mathrm{MaxPair}$ .

## Why the bound is attainable

For the proof, build a flow network. The source connects to provider $i$ with capacity $s_i$ , recipient $j$ connects to the sink with capacity $d_j$ , and provider $i$ connects to every recipient $j\ne i$ with infinite capacity. Integral flows correspond exactly to feasible deliveries.

Consider a finite cut, and let $A$ be the provider nodes on the source side. All their neighboring recipient nodes must also lie on that side to avoid cutting an infinite-capacity edge. Placing all other recipients on the sink side cannot increase the cut capacity. Thus, for a fixed $A$ , this placement always minimizes the cut capacity.

- If $A$ is empty, the cut has capacity $\mathrm{Supply}$ .
- If $A=\{i\}$ , all recipients except $i$ must be on the source side, giving capacity $\mathrm{Supply}-s_i+\mathrm{Demand}-d_i$ .
- If $|A|\ge2$ , every recipient is adjacent to a provider in $A$ with a different index. All recipients must therefore be on the source side, and the cut capacity is at least $\mathrm{Demand}$ .

Conversely, placing all provider and recipient nodes on the sink side gives a cut of capacity $\mathrm{Supply}$ ; placing all of them on the source side gives capacity $\mathrm{Demand}$ . Placing only provider $i$ and its neighboring recipients on the source side gives capacity $\mathrm{Supply}-s_i+\mathrm{Demand}-d_i$ .

The case analysis rules out a cut smaller than the formula, and these constructions realize every term as a cut capacity. The minimum cut is therefore exactly the stated formula. The max-flow min-cut theorem proves that this total delivery is attainable. For a singleton range, the third term is $0$ , as required.

## Segment tree

Store $\mathrm{Demand}$ , $\mathrm{Supply}$ , and $\mathrm{MaxPair}$ at each segment-tree node. Merge by adding the first two values and taking the maximum of the third.

An update changes one leaf's quantity and its $d_i+s_i$ , then recomputes ancestors. A query merges the summaries of $[l,r]$ and applies the formula; no flow network is built in the program. Three zeros form an empty summary and are the merge identity because all quantities are nonnegative.

## Complexity and numeric bounds

Building takes $O(n)$ time, each update or query takes $O(\log n)$ , total time is $O(n+m\log n)$ , and space is $O(n)$ . Totals may exceed 32-bit range, so use signed 64-bit values for every summary; $\mathrm{Demand}+\mathrm{Supply}\le6\times10^{14}$ .
