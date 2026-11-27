# Force Shield — Forward loss DP

[The C++17 implementation](alternative-forward-loss.cpp) by Codex (GPT-6) transitions from the earliest available activation time. Skipping charges one time step. Activating charges through the cooldown and subtracts the best protection during the active interval.

The state is the earliest available time. An optimal schedule starts by skipping or activating, and scanning time in order includes every postponed activation. For $I$ input records, width $W$ and time horizon $T$, time and space are $O(I+WT)$.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
