# Potion Wool — Solution

## Comparing solutions

The problem setter’s solution precomputes shortest paths between the start, flocks and chests. Each flock has three states: unshorn, all wool retained, or only beneficial wool retained. A transition goes directly to the next flock or detours through a chest to discard wool that increases travel time. Beneficial wool need not be discarded, as proved below. The shorn set only grows, so transitions can be processed by its size.

The problem setter’s program uses two bits per flock, reserving a pointer table for $4^p$ encodings and allocating DP only for valid three-state combinations. The implementation used by Codex (GPT-6) numbers them contiguously in base three, removing invalid encodings and separate allocations. Both have $O(3^p p^2(c+1))$ main transition work, plus key-point BFS and other preprocessing. The DP itself needs $O(p3^p)$ space; the problem setter’s pointer table adds $O(4^p)$ . The Codex implementation removes that table. Full bounds follow below. The three-state meaning and chest transitions are inherited.

## Which wool should remain in the inventory?

Negative-effect wool can only reduce step time, and there is no inventory capacity. Postponing its deposit until the final chest cannot increase any travel cost. Positive-effect wool should all be deposited whenever a chest is used: unloading earlier only makes later travel cheaper and prevents no action. Zero-effect wool may be handled with either category.

Each flock therefore needs three states: unshorn; shorn with positive-effect wool deposited; shorn with positive-effect wool still carried. Negative-effect wool from every shorn flock is retained until the end. Individual inventory quantities need not be enumerated.

Let $N_i$ and $P_i$ be the sums of all negative and positive effects in flock $i$ . If $S$ is the set of shorn flocks and $C\subseteq S$ contains those whose positive wool is still carried, the step time is

$$v(S,C)=\max\left(1,t+\sum_{i\in S}N_i+\sum_{i\in C}P_i\right)$$

Sum all effects before applying the lower bound of $1$ . Clamping after each wool item would give incorrect results.

## Compress movement on the map

Run BFS from the start, every flock, and every chest to obtain shortest step distances $d(u,v)$ between these locations. Between inventory changes, the step time is fixed, so shortest step routes are optimal. Passing a flock or chest without taking action is allowed.

Between consecutive shearings, either visit no chest or visit one chest to unload all positive wool. After unloading, the inventory does not change until the next shearing. Additional chest visits bring no benefit and can be replaced by a shortest route.

## Ternary-state dynamic programming

Let $dp[S,C,u]$ be the minimum elapsed time immediately after shearing flock $u$ . Only these states are stored, so $u\in C$ , even if its total positive effect is zero. Three choices per flock give $3^p$ states.

Initially, go directly from the start $S_0$ to any flock $u$ , at cost $t\,d(S_0,u)$ . For the next flock $v\notin S$ , consider:

1. Direct travel: add $d(u,v)v(S,C)$ and enter $(S\cup\{v\},C\cup\{v\},v)$ .
2. Unload at chest $h$ : add $d(u,h)v(S,C)+d(h,v)v(S,\varnothing)$ and enter $(S\cup\{v\},\{v\},v)$ .

Enumerate all chests for the second option. Both transitions strictly enlarge the shorn set, so process its binary masks in increasing order. Increasing ternary-state order is insufficient because unloading decreases some ternary digits.

Once every flock is shorn, travel to a chest and deposit everything, including negative-effect wool. Minimize over final states and chests.

## Correctness

The exchange arguments show that some optimal route keeps negative wool until the end and unloads positive wool at any chest it uses. After compressing movement, each leg between shearings has one of the two forms above. The DP enumerates every shearing order and necessary chest choice, charges the exact movement cost, and finishes with all wool deposited. Its minimum is therefore the optimum.

## Complexity and boundaries

Let $c$ be the number of chests and $V=ab$ . Time is $O(pk+(p+c)V+3^p p^2c)$ , and a space upper bound is $O(3^p p+(p+c)^2+V+pk)$ . The implementation reads flock counts directly into effect sums, omitting the $pk$ storage term. Use 64-bit integers for total times.

The independent small-map oracle runs Dijkstra over position, shorn set, and the exact set of carried wool items. It permits depositing any subset, including early deposits of negative wool, thereby checking the state compression itself. Samples also cover obstacle detours, the minimum step time, and partial deposits.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
