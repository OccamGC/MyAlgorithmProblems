# Lottery Plugin — Skip list

[The C++17 implementation](alternative-skip-list.cpp) by Codex (GPT-6) orders towers by lucky value and ID and uses predecessor and successor for the draw. Each ID reuses its tower. Sorted initialization appends directly at each level. Heights use a fixed seed and a cap, so one search may still take linear time in the worst case.

Use the last key with value at most the target and the first strictly larger key. Their key order implements the ID tie rules. Heights are capped at 24, so an update rewires at most 24 levels after its search. A search costs $O(n)$ in the worst case. With this fixed cap, space is $O(n+q+k)$ for participants, queries and changes.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
