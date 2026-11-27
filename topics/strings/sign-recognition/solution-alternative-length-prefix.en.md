# Sign Recognition — Precomputed length counts

[The C++17 implementation](alternative-length-prefix.cpp) by Codex (GPT-6) uses two stable counting passes per suffix-doubling round. For each suffix the nearest differently owned suffix to the left maximizes the LCP on that side. Reset to the adjacent LCP at each owner change, otherwise take the minimum of the preceding result and the adjacent LCP. A reverse scan covers the other side. Each starting position contributes once for lengths in $[\mathrm{Shared}+1,\mathrm{Remaining}]$. Add that interval to a difference array, then take two prefix sums to obtain counts by length and their range sums. For total length $S$ including separators, time is $O(S\log(S+1)+q)$ and space is $O(S)$.

On formal input `long-prefixes`, the median of three runs was 0.0566 s for this implementation and 0.1197 s for the reference. Separately measured peak process working sets were 14.35 and 12.90 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
