# Melon Planting — Pruned maximal-matching search

[The C++17 implementation](alternative-pruned-search.cpp) by Codex (GPT-6) uses maximum matching for the initial upper bound. Each decision only changes the coverage opportunities of its neighboring cells, so feasibility checks and rollback touch at most four cells.

Every vine chooses a free neighbor or remains unmatched. In the latter case every neighbor must eventually be occupied, exactly the condition for maximality. The minimum-yield search costs $O(5^p)$ time in the worst case and $O(V+p)$ extra space. Pruning depends on the layout.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
