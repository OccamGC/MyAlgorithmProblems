# Just a Little More — Full materialization

[The C++17 implementation](alternative-materialize.cpp) by Codex (GPT-6) builds through the largest requested version and writes the corresponding prefix for each query.

Every step appends a prefix, so all requested versions are prefixes of the longest one. For $V$ versions, $Q$ requests, longest length $L$ and $C$ output characters, time is $O(V+Q+L+C)$ and space is $O(L+V+Q)$.

On formal input `maximum-output`, the median of three runs was 0.0658 s for this implementation and 0.1841 s for the reference. Separately measured peak process working sets were 7.94 and 5.27 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

The 7.94 MiB working set on this input leaves little headroom under the stated 8 MB limit. The reference streams the output when memory is tight.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
