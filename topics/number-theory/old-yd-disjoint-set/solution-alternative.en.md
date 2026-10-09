# Old yd and Disjoint Sets: Single Inverse Table

Contribution: the problem setter supplied terminal-path enumeration. Codex (GPT-6) added rolling weighted binomial coefficients, exact floors, proofs and implementation. Modular inverses and adjacent binomial ratios are classical formulas. This is a parallel option to the [factorial-table solution](solution.en.md), trading additional constant-time work for less space.

## The same count with different coefficient storage

Use $t=n-B$ , $L_b,R_b$ and the exact floors proved in the main solution. The term without any $e$ step is $C^{t+1}$ . For $b\ge1$ , its lowest term is

$$W(a,b)=\binom{a+b}{a}C^aD^b,\qquad a=L_b.$$

Higher $j\in[L_b+1,R_b]$ contribute $\binom{j+b-1}{j}C^jD^b$ . The terminal conditions and counts are unchanged; only the coefficient computation changes.

Precompute $\operatorname{inv}[i]=i^{-1}\bmod p$ for $p=10^9+7$ and $1\le i\le T=\max(n-B+1)$ :

$$\operatorname{inv}[1]=1,\qquad\operatorname{inv}[i]=p-\lfloor p/i\rfloor\operatorname{inv}[p\bmod i]\bmod p.$$

Because $i<p$ , no inverse of zero is required. Obtain $C^{-1}$ by exponentiation; the input guarantees $1\le C<p$ .

## Two adjacent moves

Start at $(a,b)=(t+1,0)$ with $W=C^{t+1}$ . Before processing the next level $b$ , keep the old second coordinate $b-1$ and decrease $a$ to $L_b$ , repeatedly using

$$W(a-1,b-1)=W(a,b-1)\frac{a}{a+b-1}C^{-1}.$$

Then increase the second coordinate from $b-1$ to $b$ :

$$W(a,b)=W(a,b-1)\frac{a+b}{b}D.$$

Replace division by multiplication with modular inverses. Add this lowest term. The first higher coefficient is

$$V_{a+1}=W(a,b)\frac{b}{a+1}C,$$

and subsequent coefficients satisfy

$$V_j=V_{j-1}\frac{j+b-1}{j}C.$$

There are at most two higher terms per level. Keep their temporary variable separate from $W$ , since the next level continues from the lowest term.

## Correctness, range and complexity

Both coordinate moves and the higher-term recurrence follow directly from factorial ratios of binomial coefficients. Every denominator is a nonzero residue from $1,\ldots,T$ . Inductively, the maintained $W$ equals its defined weighted binomial coefficient. The enumerated terms are exactly the terminal-path terms in the main solution, so the answer is identical.

Within a query, $a$ only decreases from $t+1$ to zero, and $b$ only increases, giving $O(t+1)$ moves. Total time is $O(T+\sum(n-B+1)+M\log p)$ and space is $O(T)$ . The largest inverse array uses about forty million bytes. The exact rational floor certificate, sixty-four-bit modular multiplication and original input range all remain applicable.

This program supports the full data range. It is useful when saving memory is the priority; factorial tables have smaller query constants. See the [five-run measurements](../../../docs/benchmark-R26.json) for observed times and peak working sets.

Program: [alternative.cpp](alternative.cpp). Checks include independent recursive expansion, complete comparison with factorial tables and comparison with the setter's program.
