# The Great Cookie Swap — Four-field segment tree

[The C++17 implementation](alternative-residual.cpp) by Codex (GPT-6) matches across the two children, then reroutes existing exchanges from the opposite child to increase the total.

Each child already realizes its maximum internal trade count. After direct cross-pairing, a child with both kinds of surplus can split one matched trade of the other child into two cross-trades, a net gain of one. Apply the same rule in both directions. Build in $O(n)$ time, update or query in $O(\log n)$, and store $O(n)$ nodes.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
