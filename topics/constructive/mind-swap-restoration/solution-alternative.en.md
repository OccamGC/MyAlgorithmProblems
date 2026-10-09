# Restoring Minds after Swaps — Alternative Solution

This applies the [combined-cycle construction of Evans, Huang, and Nguyen](https://arxiv.org/abs/1204.6086). Codex (GPT-6) adapted its cycle orientation and verified [alternative.cpp](alternative.cpp).

## Construction

Use the [standard solution's](solution.en.md) body-to-mind cycles $C_1,\ldots,C_c$ . For cycle $a_1,\ldots,a_t$ , its rotated order is $a_2,\ldots,a_t,a_1$ . Output zero if there are no nontrivial cycles. Otherwise:

1. Swap $y$ with the first vertex of $C_c,\ldots,C_2$ .
2. For $C_1$ , swap $(x,a_1)$ , swap $y$ along its rotated order, then swap $(x,a_2)$ .
3. Swap $x$ along each rotated order of $C_2,\ldots,C_c$ .
4. Swap $(x,y)$ .

## Invariant and Bound

Step 1 chains the displaced minds. Step 2 restores the first cycle, leaves $y$ holding $x$'s mind, and gives $x$ the next cycle's second mind. Each traversal restores that cycle and collects the next needed mind. Finally $x$ holds $y$'s mind; the last swap restores both. Pairs never repeat.

For $s$ affected bodies, use $s+c+2\le2N+1$ swaps, $O(N+M)$ time, and $O(N)$ space. This saves swaps when $c\ge3$ . No global optimality for the particular history is claimed.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
