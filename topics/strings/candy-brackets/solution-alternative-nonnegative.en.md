# Candy Brackets — Nonnegative-weight subtask

[The C++17 implementation](alternative-nonnegative.cpp) by Codex (GPT-6) stores only the type and sum of each completed block. With nonnegative weights, no substring can outweigh its containing block, so comparing complete blocks suffices. Use this variant only on nonnegative inputs.

This covers the stated nonnegative subtask. An endpoint insertion can create new matches only at that end. Reduce adjacent candies, matching brackets, and candy wrapped in brackets. Total time and space are $O(N+M+1)$. The four-field reference handles the full signed domain.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
