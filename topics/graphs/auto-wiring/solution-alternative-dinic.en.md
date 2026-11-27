# Automatic Connectors — Unit-capacity Dinic

[The C++17 implementation](alternative-dinic.cpp) by Codex (GPT-6) stores forward and reverse residual edges and finds layered augmenting paths with a stack. The final BFS supplies the reachable set for the minimum vertex cover.

Each unit of flow chooses one matching edge. After maximum flow, the unreachable left and reachable right vertices cover all cables and have size equal to the matching. This unit matching network takes $O((n+m)\sqrt n)$ time and $O(n+m)$ space.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
