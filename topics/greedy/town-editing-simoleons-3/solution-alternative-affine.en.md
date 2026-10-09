# Edit Town and Simoleons 3: Evaluating the Optimal Moving Route

Codex (GPT-6) provides this batched affine evaluation of the optimal moving route. The route and its upper-bound proof are in the [main solution](solution.en.md). This method evaluates household money along that route instead of substituting into the final closed formula.

## Route and bulk moves

Keep the notation $k,l,N,r$ . Write total money as $S=m_1+m_2$ and current money in A as $x$ . Return $m_1$ for an empty other household or a target household that is initially at least as rich per person.

Otherwise choose $h=\lfloor N/2\rfloor$ and follow the population route $k\to h$ , then $r$ repetitions of $h\to h+1\to h$ , then $h\to l$ . The main solution proves that this route is legal and optimal, with all targets finally in B.

For a monotone segment changing A's population from $s$ to $t$ :

- If $t<s$ , residents leave A successively and its per-person wealth stays constant, so $x'=xt/s$ .
- If $t>s$ , residents leave B successively and its per-person wealth stays constant, so $x'=S-(S-x)(N-t)/(N-s)$ .
- If $s=t$ , money is unchanged.

Each of the two monotone segments takes a constant number of modular operations.

## Repeated round trips

Starting with $h$ residents in A, move one resident from B to A and then one from A to B. The successive amounts in A are

$$
x'=x+\frac{S-x}{N-h},\qquad
x''=\frac h{h+1}x'=\alpha x+\beta,
$$

where

$$
\alpha=\frac h{h+1}\left(1-\frac1{N-h}\right),\qquad
\beta=\frac{hS}{(h+1)(N-h)}.
$$

Apply binary exponentiation to $f(x)=\alpha x+\beta$ . Squaring gives coefficients $(\alpha^2,\alpha\beta+\beta)$ . For each set exponent bit, apply the corresponding function to the current money.

After the final monotone segment, A contains all outsiders and B all targets. The answer is $S-x$ .

## Correctness, complexity, and scope

Each bulk transfer is equivalent to the corresponding individual moves. Affine exponentiation performs exactly $r$ round trips. Thus the program evaluates precisely the route already proved optimal in the main solution and returns the same maximum wealth.

All denominators are positive and below the modulus. When $N=2$ , the round trip temporarily empties one slot, but both moves remain legal and the formulas never divide by zero.

For maximum initial population $M$ , each town takes $O(\log P+\log M)$ time and $O(1)$ extra space. This method supports all constraints and is provided alongside the closed formula. It follows the moving process more directly; both implementations pass the reference limit. See [alternative-affine.cpp](alternative-affine.cpp).
