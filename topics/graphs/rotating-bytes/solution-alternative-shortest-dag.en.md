# Rotating Bytes — Shortest-path DAG implementation

[The C++17 implementation](alternative-shortest-dag.cpp) by Codex (GPT-6) runs Dijkstra backwards and keeps the tight edges. Each label block on a shortest path has one aligned position, so advance synchronously from eligible starts, retaining the least bit and deduplicating blocks. Mark vertices reachable using tight edges matching the selected string. From the destination, repeatedly taking the smallest reachable predecessor minimizes the reverse sequence. With a binary heap allowing duplicate entries, time is $O((n+m)\log(n+m+1)+L)$ and space is $O(n+m+L)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
