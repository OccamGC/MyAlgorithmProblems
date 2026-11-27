# Redstone Clock — Tabulated GCD

[The C++17 implementation](alternative-tabulated-gcd.cpp) by Codex (GPT-6) only factors the first argument $i\le n$. The linear sieve multiplies the least prime $p$ into the smallest of three factors $x$, then sorts the triple. When $x>1$, both other factors are at least $x\ge p$, so $(px)^2$ is at most the product of all three new factors. Thus factors above $\sqrt n$ are single primes. Look up small factors, test divisibility for large primes, and divide away each match. Preprocessing and all queries take $O(n)$ total time and $O(n)$ space.

On formal input `maximum-bound`, the median of three runs was 0.5296 s for this implementation and 1.4982 s for the reference. Separately measured peak process working sets were 141.54 and 4.76 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
