# A Queue Made of Stacks — Explicit-stack simulation

[The C++17 implementation](alternative-explicit-stacks.cpp) by Codex (GPT-6) performs the greedy pushes, transfers and pops. Each element records its stack and predecessor. A free list and a list of occupied stacks select a destination in constant time. Each retained item moves at most once, giving $O(m+1)$ time and space while exposing the operations charged to the answer.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
