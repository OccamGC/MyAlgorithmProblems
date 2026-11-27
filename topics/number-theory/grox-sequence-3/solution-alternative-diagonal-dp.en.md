# Grox's Sequence III — Offline diagonal DP

[The C++17 implementation](alternative-diagonal-dp.cpp) by Codex (GPT-6) factors $a$ out of every term, giving $F(a,b)=a(b!+F(a+1,b+1))\bmod P$. The empty sum beyond either boundary is zero. The successor preserves $d=b-a$, so group queries by $d$, evaluate only requested diagonals backwards and restore input order. Each valid pair is evaluated at most once, giving $O((n+1)^2+q)$ time and $O(n+q)$ space. This removes the per-query block scan at the cost of reading the batch first.

On formal input `05`, the median of three runs was 0.1660 s for this implementation and 0.2560 s for the reference. Separately measured peak process working sets were 9.23 and 7.97 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
