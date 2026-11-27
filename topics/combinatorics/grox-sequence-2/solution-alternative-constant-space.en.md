# Grox's Sequence II — Constant-space evaluation

[The C++17 implementation](alternative-constant-space.cpp) by Codex (GPT-6) groups pairs by $k=i+j$. Multiplying layer $k$ by $k!$ turns its weights into binomial coefficients, counting walks with $k$ steps of $+1$ or $-1$ by residue. Symmetry gives counts $(b_0,b_1,b_1)$ with total $2^k$. One step maps them to $(2b_1,b_0+b_1,b_0+b_1)$, so $b_0-b_1=(-1)^k$. For $x=2,-1$, accumulate $H_k(x)=kH_{k-1}(x)+x^k$ from $H_0(x)=1$. This is $k!\sum_{j=0}^k x^j/j!$. Recover the three totals from their sum and difference using one inverse of $3n!$. Time is $O(n+\log P)$ and auxiliary space is $O(1)$, including $n=0$.

On formal input `10`, the median of three runs was 0.0190 s for this implementation and 0.0245 s for the reference. Separately measured peak process working sets were 4.82 and 5.98 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
