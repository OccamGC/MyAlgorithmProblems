# Grox's Sequence II — Divide-and-conquer NTT

[The C++17 implementation](alternative-divide-ntt.cpp) by Codex (GPT-6) computes all $2n+1$ coefficients as in Section 3 of the main editorial, then groups them by residue.

After setting $t=n-j$, valid pairs satisfy $i\le t$. Convolve pairs first split between children and handle pairs in the same terminal interval directly. Each pair contributes once. Time is $O(n\log^2(n+2))$ and space is $O(n)$. This variant is useful when all coefficients are needed.

On formal input `10`, the median of three runs was 0.1922 s for this implementation and 0.0245 s for the reference. Separately measured peak process working sets were 8.96 and 5.98 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
