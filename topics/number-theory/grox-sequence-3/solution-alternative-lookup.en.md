# Grox's Sequence III — Full lookup table

[The C++17 implementation](alternative-lookup.cpp) by Codex (GPT-6) fills all rows in descending order of $a$ using $F(a,b)=a(b!+F(a+1,b+1))\bmod P$. If either coordinate exceeds $n$, the defining sum is empty and the boundary value is zero. The [offline diagonal editorial](solution-alternative-diagonal-dp.en.md) derives the recurrence. Online queries take one indexed access. Preprocessing time and storage are both $O((n+1)^2)$. At $n=5000$ the table occupies about 95.5 MiB within the 512 MB limit. This version suits streamed queries when memory is available.

On formal input `05`, the median of three runs was 0.1312 s for this implementation and 0.2560 s for the reference. Separately measured peak process working sets were 100.21 and 7.97 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
