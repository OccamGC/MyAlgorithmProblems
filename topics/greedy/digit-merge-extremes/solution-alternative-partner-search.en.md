# Extremes after Merging Two Digits — Left-position enumeration and segment tree

[The C++17 implementation](alternative-partner-search.cpp) by Codex (GPT-6) applies the fixed-left partner rule from the main proof, finding the first or last eligible right digit for each carry case. Range extrema prune subtrees with no partner. Represent each candidate by at most five slices or single digits, trim leading zeros, then compare length and digits. Equal-length carrying candidates preserve all positions. Equal-length non-carrying candidates delete one digit and trim equally many leading zeros. Aligned source slices therefore start at identical or adjacent positions; precomputed equal-digit runs skip their common prefix. Time is $O(n\log(n+1))$ and space is $O(n)$, providing an independent check on the linear greedy selection.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
