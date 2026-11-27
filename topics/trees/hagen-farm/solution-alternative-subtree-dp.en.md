# Hagen Farm — Subtree expectation DP

[The C++17 implementation](alternative-subtree-dp.cpp) by Codex (GPT-6) stores each conditional expectation from Section 4 of the main editorial multiplied by its subset count. Merges sum lengths over subsets. A second pass applies the ancestor weights.

During a merge, enumerate how many vertices are chosen on each side, weighting each length total by the other side’s number of choices. Subtract subsets wholly in one child when assigning a total to its LCA, then weight by the possible generation roots. Nonempty pairs are charged at their first merge, yielding $O(n^2)$ time and space.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
