# Garden Click Coefficient: Solution

## Algorithm and Attribution

Codex (GPT-6) completed the specification, dominance proof, enumeration, and implementation in [std.cpp](std.cpp). The formulas use the stated 20% neighbor boost and add no constant term to click or milk bonuses.

## Remove Two Dominated Choices

Fix the N cells and the soil. Each remaining cell has a fixed effect $F$ with $0<F\le3.4375$ , so all penalty factors are nonnegative.

Replacing E by B increases production without reducing any other factor. An optimum therefore needs no E cells.

For a D cell, let $P\ge1$ be the production factor from the other cells. Its production increase and click penalty contribute

$$
(P+0.03F)(1-0.05F)
=P+F(0.03-0.05P)-0.0015F^2\le P.
$$

Replacing D by E cannot decrease the score; replacing that E by B cannot decrease it either. Neither replacement changes the N neighborhood. Only B, T, W, N, and G remain necessary.

## Enumeration

Let $g=nm$ . Enumerate both soils and every mask of N cells. Count neighboring N cells in all eight directions and calculate each remaining cell's effect. Recursively assign B, T, W, or G to those cells.

Maintain the sums of the effects for B, T, W, and G, together with the product of G production penalties. Evaluate the stated formula at each leaf. Include the empty N mask and the all-N mask; the latter has zero click coefficient.

![Neighbor boosts and plant placement](assets/example.svg)

An N cell affects other cells whose row and column differences are both at most one, including diagonal neighbors.

## Correctness

The replacements prove that some optimum contains neither E nor D. The enumeration includes its soil, all its N positions, and every remaining plant. The maintained sums and product reproduce the formula exactly in real arithmetic. Taking the maximum therefore gives the global optimum.

## Complexity and Numerics

A mask containing $t$ N cells has $4^{g-t}$ assignments, so the total is

$$\sum_{t=0}^g\binom gt4^{g-t}=5^g.$$

Time is $O(g^2 2^g+5^g)$ and auxiliary space is $O(g)$ . The implementation uses `long double` and prints scientific notation with 18 digits after the decimal point. Formal answers come from an independent complete-layout enumeration and 60-digit Decimal rescoring. Small boards also compare all seven plant types, including E and D.

See the [test documentation](tests/README.md) for recipes, seeds, and measurements.
