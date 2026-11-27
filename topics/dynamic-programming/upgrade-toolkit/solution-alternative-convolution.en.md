# Upgrade Toolkit — Direct convolution

[The C++17 implementation](alternative-convolution.cpp) by Codex (GPT-6) enumerates each allowed quantity as in the setter’s recurrence. Rolling the two adjacent stages uses $O(S+1)$ space.

Choosing a quantity picks exactly one exponent from its factor. If type $i$ has cap $c_i$ and the caps through $i$ sum to $S_i$, the nested loops take $O(\sum_i(S_{i-1}+1)(c_i+1))$ time. This version directly checks the sliding-window boundaries.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
