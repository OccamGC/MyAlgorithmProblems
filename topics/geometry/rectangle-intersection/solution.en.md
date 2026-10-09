# Rectangle Intersection: The Top-Edge Method

Problem setter's solution: choose the rectangle with the highest top edge and test the other rectangle's top edge. The teaching notes also give projection and center-distance methods. Codex (GPT-6): retaining the top-edge method, removing nonstandard array initialization and using 64-bit coordinates consistently.

## Normalize endpoints and detect an empty intersection

Represent each shape $X$ as the product of closed intervals $[l_X,r_X]\times[b_X,t_X]$ , using its left, right, bottom and top bounds. Zero-length intervals are allowed.

Swap the shapes so that $t_A\ge t_B$ . Their intersection is empty exactly when at least one condition below holds:

$$t_B<b_A\quad\text{or}\quad r_A<l_B\quad\text{or}\quad r_B<l_A$$

The last two conditions detect horizontal separation. Only the first vertical condition is needed: $t_A\ge t_B\ge b_B$ already rules out separation in the opposite vertical order.

## Correctness

If any strict inequality holds, one coordinate axis has no common coordinate, so the shapes cannot intersect. Otherwise, their horizontal intervals overlap and $t_B$ lies in both vertical intervals. Pairing any common horizontal coordinate with $t_B$ gives a shared point. The condition is therefore necessary and sufficient. Strict less-than comparisons preserve boundary contact and degenerate points.

## Complexity and comparison

Each pair takes $O(1)$ time and $O(1)$ extra space; total time is $O(T+1)$ . No area calculation or product of coordinate differences is needed. All implementations use 64-bit integers, including safe sums for center coordinates.

The preferred program is [std.cpp](std.cpp). Two parallel alternatives have the same complexity and support the full data:

- [Symmetric projections](solution-alternative-projection.en.md), with [alternative-projection.cpp](alternative-projection.cpp), directly intersect the coordinate intervals without swapping the shapes.
- [Center distances](solution-alternative-center.en.md), with [alternative-center.cpp](alternative-center.cpp), compare center distances with sums of half-widths, multiplying by two to keep all arithmetic integral.

The top-edge method follows a geometric observation. Projections avoid ordering the shapes by height. Center distances provide a different geometric formulation but need wider integers when combining coordinates. There is no asymptotic difference, and code length or tiny timing fluctuations do not establish an algorithmic advantage.

Checks cover all eight-coordinate combinations over $\{-1,0,1\}$ , reversed endpoints, containment, contact, degeneracies and coordinate extremes. See the [test plan](tests/plan.json) and [measurements](../../../docs/评测环境与性能.md).
