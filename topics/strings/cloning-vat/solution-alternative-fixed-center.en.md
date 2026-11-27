# Cloning Vat — Fixed-center parity construction

[The C++17 implementation](alternative-fixed-center.cpp) by Codex (GPT-6) considers keeping and changing the center separately. With the center fixed, $d>0$ unequal and $e$ equal pairs realize every cost from $d$ to $2(d+e)$: unequal pairs give a contiguous interval, shifted by even costs for equal pairs. If $d=0$, only even costs are feasible. This gives a greedy reconstruction for each center without storing backpointers. Take the lexicographically smaller feasible candidate in $O(n)$ time and space per query.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
