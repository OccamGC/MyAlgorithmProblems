# Boards with No All-Black Line — Offline column-coverage DP

[The C++17 implementation](alternative-column-dp.cpp) by Codex (GPT-6) factors each row transition by cell. A covered column permits black or white; white in an uncovered column sets its bit. Subtract the unchanged all-black row from each state, then use inclusion-exclusion with coefficients $1,-2,1$ for zero, one and two forced black diagonals. For one order this reduces time from $O(n3^n)$ to $O(n^2 2^n)$ with $O(2^n)$ space. The two largest state arrays alone occupy 8 MiB, making this a table regenerator outside the online memory limit.

The empty board contributes one. For a positive order, start with no covered columns and read only the all-covered mask after the final row.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
