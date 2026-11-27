# Sign Recognition — Suffix treap with integer ranks

[The C++17 implementation](alternative-suffix-treap.cpp) by Codex (GPT-6) inserts suffixes from right to left. Compare first characters and break ties by the current in-order ranks of their tails, computed from subtree sizes and parent links. This avoids floating-point label collisions across rotations. A search makes at most $h$ comparisons at $O(h)$ per rank lookup, giving construction time $O(Sh^2)$ for maximum intermediate height $h$. Priorities use a fixed seed. The resulting order feeds the reference LCP and owner scans.

On formal input `long-prefixes`, the median of three runs was 0.2783 s for this implementation and 0.1197 s for the reference. Separately measured peak process working sets were 14.11 and 12.90 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
