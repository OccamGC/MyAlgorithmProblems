# Spiral Numbers: Alternative Solution

Contribution: Codex (GPT-6) adds arithmetic reversal. See the preferred [two-pointer explanation](solution.en.md).

Read the input as an unsigned decimal integer; leading zeroes do not affect its value. Repeatedly remove the last digit and update $R\leftarrow10R+(V\bmod10)$ . The invariant is that $R$ contains the removed low-order digits in extraction order. At termination it is the reversed decimal value, which is compared with the original. For zero, the loop is empty and both values are zero.

If a nonzero value ends in zero, its reversal has fewer digits and cannot equal it. Thus the leading zeroes lost by integer reversal cause no false positives. Otherwise, digit lengths agree, and equality is exactly equality of all symmetric digit pairs.

Let $L$ be the input digit count. Reading and reversal take $O(L)$ time and $O(1)$ extra storage in this problem's machine-integer model. All intermediate values are below $10^{18}$ , so an unsigned 64-bit integer suffices. Unlike the string method, this avoids storing the input string but does not extend to arbitrarily large integers.

Program: [alternative.cpp](alternative.cpp).
