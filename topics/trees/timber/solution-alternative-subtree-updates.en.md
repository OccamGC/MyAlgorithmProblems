# Timber — DFS-order segment tree

[The C++17 implementation](alternative-subtree-updates.cpp) by Codex (GPT-6) repeatedly chooses the endpoint whose root path has the most uncovered vertices. Each newly covered vertex subtracts one from its subtree before the gains are merged with the stated tie rule.

DFS order turns each subtree into an interval. Every newly covered vertex is subtracted once, giving $O(n)$ parent steps, $O(n\log(n+1))$ time including range updates and final sorting, and $O(n)$ space.

On formal input `maximum-balanced`, the median of three runs was 0.2525 s for this implementation and 0.1518 s for the reference. Separately measured peak process working sets were 54.73 and 36.95 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
