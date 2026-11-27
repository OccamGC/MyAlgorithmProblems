# Contract Summoning — Fenwick tree of dynamic segment trees

[The C++17 implementation](alternative-fenwick-range-tree.cpp) by Codex (GPT-6) inserts in descending order of the third requirement. Each leaf list can then consume eligible entries from its head. Inner trees and lists use integer pool indices.

Decompose the first-coordinate prefix into disjoint Fenwick buckets and prune each inner tree by the second-coordinate prefix and minimum third requirement. Consume each copy once and enqueue each newly reachable character once. Time and space are bounded by $O(n\log^2(n+1))$. The bucket-sized static reference tree reduces storage.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
