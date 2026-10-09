# String Functions in Contiguous Memory — Alternative

**Problem setter's solution; implementation organized by Codex (GPT-6).** Keep a contiguous byte array and prefix sums, scan for the terminating zero, and apply modifications byte by byte.

The [main solution](solution.en.md) specifies the error and warning order: validate everything before mutation, and reject overlapping copy intervals including their terminators. Scanning finds the exact string length. Every binary string is a run of ones followed by zero, so writing that sequence reproduces the source exactly. The array equals the specified memory byte for byte before and after every operation; induction proves all outputs correct.

Prefix sums and initial memory take $O(n+S)$ time. An operation takes worst-case $O(S)$ , giving total time $O(n+S+kS)$ and space $O(n+S)$ . This method is direct and has small storage constants; the segment tree has better asymptotic time for query-heavy inputs. This [program](alternative.cpp) passes the current full data within the estimated limit and is a useful simple alternative.
