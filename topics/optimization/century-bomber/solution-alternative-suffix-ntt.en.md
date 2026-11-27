# Century Bomber — Suffix convolution

[The C++17 implementation](alternative-suffix-ntt.cpp) by Codex (GPT-6) registers each drop as a positive suffix at $l$ and a negative suffix at $r+1$ shifted by $r-l+1$. The starting-position polynomial is common to every drop, so multiply by it once after summing in the transform domain. Each truncated drop has degree below $n$, and the final degree is below $n+m$. Padding to that bound avoids wraparound. Time is $O(q+k+nH\log H)$ and space is $O(q+n+H)$ for transform length $H$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
