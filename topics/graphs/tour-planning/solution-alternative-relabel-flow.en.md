# Tour Planning — Zero-cost augmentation and relabeling

[The C++17 implementation](alternative-relabel-flow.cpp) by Codex (GPT-6) searches zero reduced-cost arcs. If the sink is unreachable, decrease potentials on the reachable side by the minimum outgoing slack. Reduced costs stay nonnegative and at least one outgoing arc becomes admissible. Road negative-cycle detection uses the reference criterion.

Every zero reduced-cost augmentation is shortest. If no residual edge crosses the reachable cut, the flow is maximum. Road potentials and per-origin shortest paths follow the reference. In a flow network with $e$ edges, $a$ augmentations and $r$ relabelings take $O((a+r+1)(n+e))$ time and $O(n+e)$ space.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
