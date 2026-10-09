# Counting Paired DNA Strands: Alternative Solution

## Two-level tables for a fixed base

The counting formula is the setter's. Codex (GPT-6) supplied the two-level modular-power implementation [alternative.cpp](alternative.cpp). See the [main solution](solution.en.md) for the formula and counting proof.

Every required power is $2^e\bmod p$ , with $0\le e\le E=1999999999$ . Choose block size $B=32768$ and write $e=tB+r$ , where $0\le r<B$ . Precompute

$$Low_r=2^r\bmod p,\qquad High_t=(2^B)^t\bmod p$$

Build the low table by repeated multiplication by two and the high table by $2^B$ . A query returns $High_tLow_r\bmod p$ , which is correct by addition of exponents. Substitute it into the same parity-dependent counting formula and XOR the results.

Preprocessing time and space are $O(B+E/B)$ ; each query is $O(1)$ , for total time $O(B+E/B+m)$ . The two 32-bit tables occupy about $375$ KB. Using the fixed bound avoids storing the queries.

This reduces multiplications across many queries at the cost of preprocessing and table space. Binary exponentiation uses constant auxiliary space and is suitable for fewer queries. Both methods have useful settings; the table is not unconditionally better.
