# Rhino Tank — Row-state DP

[The C++17 implementation](alternative-row-dp.cpp) by Codex (GPT-6) factors the setter’s subset transitions by column. Color $c$ survives with the probability that the new cell has color $c$, and otherwise becomes mixed. After all independent column updates, subtract the monochromatic rows of each color, which deterministically mix every column of a different color. Each row takes $O((n+m)(m+1)^n+nm)$ time, with $O((m+1)^n)$ DP workspace.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
