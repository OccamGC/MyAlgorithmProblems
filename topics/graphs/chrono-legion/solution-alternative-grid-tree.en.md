# Chrono Legion — Grid segment tree

[The C++17 implementation](alternative-grid-tree.cpp) by Codex (GPT-6) stores both building count and newest building per rectangle. Binary search includes radius zero and counts colocated buildings separately. The resulting graph uses the same composite-modulus determinant.

Counts are monotone in radius. At the first feasible radius, query the newest building in the entire closed square. Grid preprocessing costs $O(NM)$, and each threshold costs $O(\log(\max(N,M)+1)\log(N+1)\log(M+1))$, in addition to the common determinant stage. Graph construction uses $O(NM+K^2+S)$ memory for $S$ thresholds.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
