# Dynamic Directory Tree — Adjacent-pair LCA

[The C++17 implementation](alternative-pair-lca.cpp) by Codex (GPT-6) compares node counts on exposed root paths. An original vertex at depth $d$ has $2d+1$ path nodes in the expanded tree, so negative edge weights do not affect the choice. Exposing the path between two endpoints also tests adjacency: exactly three expanded nodes means they share an edge. Its middle node supplies the weight, avoiding the endpoint map.

If $c$ is the common LCA, at least one consecutive pair has LCA $c$, and the others lie in its subtree. Choose the shallowest pair LCA. For $K$ query vertices in total, amortized time is $O((n+m+K)\log(n+1))$ and space is $O(n)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
