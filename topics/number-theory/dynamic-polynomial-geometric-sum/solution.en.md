# A Certain Unscientific Polynomial-Weighted Geometric Sum with Updates — Solution

Codex (GPT-6) applies a linear polynomial antidifference transform to this problem, including triangular preprocessing, coefficient updates, implementation, and verification. Finite differences, binomial expansion, and modular inverses are established tools.

## Find a polynomial that telescopes

To distinguish it from the modulus, write the current load polynomial as $B(x)=\sum_{j=0}^k b_jx^j$ . Construct $Q(x)$ satisfying

$$aQ(x+1)-Q(x)=B(x).$$

Substitute $x=i$ , multiply by $a^i$ , and sum to obtain

$$F(n)=a^{n+1}Q(n+1)-aQ(1).$$

It suffices to maintain $Q$ , evaluate it at two points with Horner's rule, and compute one modular power.

## Precompute one column per monomial

Find $Q_j(x)$ such that $aQ_j(x+1)-Q_j(x)=x^j$ . Linearity gives $Q(x)=\sum_jb_jQ_j(x)$ . A change in $b_j$ adds $\Delta b_j$ times this precomputed column to the coefficients of $Q$ .

For $a\ne1$ , write $Q_j(x)=\sum_{h=0}^j q_hx^h$ . Comparing coefficients of $x^t$ gives

$$(a-1)q_t+a\sum_{h=t+1}^{j}\binom ht q_h=[t=j].$$

The bracket is one when $t=j$ and zero otherwise. Solve from higher degrees downward, dividing by $a-1$ with a modular inverse.

For $a=1$ , a difference lowers the degree by one. Use degree $j+1$ and set the constant coefficient to zero. Solve downward using

$$(t+1)q_{t+1}+\sum_{h=t+2}^{j+1}\binom ht q_h=[t=j].$$

Every divisor $1,\ldots,k+1$ is below the prime modulus, so its inverse exists and can be precomputed. Base $a=0$ is covered by the first triangular system and yields zero output naturally; no inverse of zero is needed.

## Correctness and Complexity

Each triangular system has invertible diagonal entries, so coefficient comparison proves its identity. Linear combination and incremental updates preserve the correct current $Q$ for $B$ . The telescoping identity therefore gives the desired sum. Changing the upper bound does not affect the precomputed columns.

After binomial and inverse preprocessing, all columns require $O(k^3)$ time and $O(k^2)$ space; initial combination costs $O(k^2)$ . Coefficient updates and polynomial evaluation cost $O(k)$ , while a changed bound needs $O(\log n)$ exponentiation. Total time is $O(k^3+m(k+\log n))$ , with $O(k^2)$ space. The modulus is fixed; one general inverse additionally uses $O(\log P)$ exponentiation. Reduce after multiplication so signed 64-bit arithmetic suffices.

[std.cpp](std.cpp) supports every operation mix. The [moment-recurrence alternative](solution-alternative.en.md) gives constant-time coefficient-only updates, but frequent bound changes are slower, so it is published as a backup.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
