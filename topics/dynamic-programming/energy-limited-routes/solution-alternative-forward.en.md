# Routes with Limited Energy — Forward propagation

[The C++17 implementation](alternative-forward.cpp) by Codex (GPT-6) initializes one zero-move route per start. Process each layer by decreasing height so that free moves arrive before their destination is processed. Every nonempty route has a unique last edge, and every route may stop at its endpoint. Costs increase by at most two, so three rolling layers match the reference time and space.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
