# Psychic Commando — Row blocks and column segment trees

[The C++17 implementation](alternative-row-blocks.cpp) by Codex (GPT-6) use a common tag and a base-sum tree per block, with individual row trees at the boundaries.

A full block update changes its common tag. A partial update changes individual rows and their block sum. Adding the two parts in a query counts every cell exactly once. With $H$ rows, $W$ columns and block size $B$, a rectangle operation costs $O((H/B+B)\log(W+1))$ time and storage is $O(HW)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
