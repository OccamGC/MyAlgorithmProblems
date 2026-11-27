# Timber — Linear counting sort

[The C++17 implementation](alternative-counting.cpp) by Codex (GPT-6) counts gains by chain length and first-use flag. Every length is in $[1,n]$. Descending length order, taking non-first gains before first gains on ties, reproduces the proved ordering. Scanning $n$ buckets and writing at most $n$ results gives $O(n)$ total time and space.

On formal input `maximum-balanced`, the median of three runs was 0.1557 s for this implementation and 0.1518 s for the reference. Separately measured peak process working sets were 37.43 and 36.95 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
