# Factorial Recovery — Single-modulus reconstruction

[The C++17 implementation](alternative-single-modulus.cpp) by Codex (GPT-6) uses repeated doubling and modular addition for exact multiplication. Sums stay below $2M$, with at most $O(\log M)$ additions per multiplication.

The prime $M=7\cdot2^{52}+1$ is coprime to ten and exceeds the missing prefix. Thus $(n!-s)10^{-k}\bmod M$ uniquely recovers the prefix. Printing the supplied suffix verbatim preserves its leading zeros. Storage consists of the $k$ suffix digits and a constant number of integers.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
