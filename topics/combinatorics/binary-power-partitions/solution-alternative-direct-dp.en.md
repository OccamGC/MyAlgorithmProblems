# Partitions into Powers of Two — Direct block DP

[The C++17 implementation](alternative-direct-dp.cpp) by Codex (GPT-6) enumerates both boundary exponents explicitly and can be checked against the suffix-sum version.

Classify a split by the extremal exponents in its two halves and multiply their counts. For bit length $L$, the direct recurrence takes $O(L^5)$ time and $O(L^3)$ space. The suffix-sum reference reuses the repeated inner sums.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
