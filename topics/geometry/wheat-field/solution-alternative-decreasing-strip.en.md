# Wheat Field — Shrinking-strip implementation

[The C++17 implementation](alternative-decreasing-strip.cpp) by Codex (GPT-6) fixes the left boundary and moves the right boundary from the edge of the field to the left. A linked list holds the occupied rows and two sentinels. Remove a row only when its last building leaves the strip. Deleting it merges adjacent gaps, so the largest gap can only grow and takes $O(1)$ to update. Each boundary pair still uses the smaller of its width and largest gap. Initialization and scanning are linear per left boundary, giving $O((k+1)^2)$ time and $O(k+1)$ space.

On formal input `diagonal`, the median of three runs was 0.0183 s for this implementation and 0.0199 s for the reference. Separately measured peak process working sets were 4.83 and 5.27 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
