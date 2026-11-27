# Passengers Need More Exercise — Slope sweep

[The C++17 implementation](alternative-slope-sweep.cpp) by Codex (GPT-6) maintains total distance in doubled coordinates. Passing a passenger with a door changes that passenger’s slope from $-1$ to $+1$. Passing with an adjacent-door midpoint switches the nearest door and changes the slope from $+1$ to $-1$. Start with slope $-M$ at the far left, accumulate changes before zero, then integrate from the known value at zero. A piecewise-linear maximum occurs at an endpoint. Sweeping in increasing order and updating only on strict improvement retains the leftmost maximizer, including ties at coincident events. Sorting takes $O(MN\log(MN+1))$ time and $O(MN)$ space.

On formal input `maximum-random`, the median of three runs was 0.0302 s for this implementation and 0.0189 s for the reference. Separately measured peak process working sets were 9.48 and 4.90 MiB, respectively. [Measurement conditions and raw data](../../../docs/benchmark-editorial-alternatives.json)

With the same 300 passengers and 300 doors but all midpoint candidates inside the stopping interval, the sweep took 0.0311 s and the reference took 0.0674 s. Out-of-range candidates are cheap for the reference to discard.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
