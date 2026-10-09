# Counting Paired DNA Strands over a Length Range — Alternative

**Codex (GPT-6) alternative: closed-form geometric sums.** The [main solution](solution.en.md) proves the fixed-length count and prefix formula. Only the computation of $s=G(h)$ changes.

When $q\not\equiv1\pmod P$ ,

$$G(h)=q(q^h-1)(q-1)^{-1}\pmod P$$

Use binary exponentiation for $q^h$ and $(q-1)^{P-2}$ . Both prefixes of one query share the inverse, and the values are substituted into the main formula for $H(n)$ . When $q\equiv1\pmod P$ , every term is one, so set $G(h)=h\bmod P$ without attempting to invert zero.

The geometric-series identity and prime-modulus inverse prove the general branch correct. The all-ones sum proves the special branch correct, and subtracting prefixes gives the answer. Reduce $2K$ modulo the modulus first: the valid input $K=500000004$ reaches the special branch.

Each query takes $O(\log(R+1)+\log P)$ time and $O(1)$ space; the modulus is fixed here. Block merging avoids inverses, while this [program](alternative.cpp) uses fewer state variables. Both pass the full data.
