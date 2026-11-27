# Century Bomber — Block aggregation

[The C++17 implementation](alternative-blocks.cpp) by Codex (GPT-6) counts complete offset blocks by the supply interval’s left endpoint and applies the partial block directly. Expand full blocks before shifting the result to each starting position.

A counter records how many drops from a given supply index cover an entire offset block. Multiply it by each corresponding supply value during expansion. With block length $B$, time is $O(q(B+n/B)+n^2+kn+n+m)$ and space is $O(n^2/B+n+m+k)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
