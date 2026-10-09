# Forward Batched Averaging

Codex (GPT-6) provides the lower-triangular batch expansion, implementation, and verification for this problem. The [program](alternative-forward.cpp) uses the same optimal resident-by-resident strategy proved in the [main solution](solution.en.md), but directly maintains target wealth instead of evaluating backward coefficient tails.

## One Resident as a Linear Transformation

Write the target values from richest to poorest as $x_0,\ldots,x_{k-1}$ . Each resident of the current outside household initially has wealth $v$ . Subtract this constant and let $y_i=x_i-v$ . Averaging one outsider with every target in order gives

$$y'_i=\sum_{j=0}^{i}2^{-(i-j+1)}y_j.$$

Let $L$ shift a vector down by one position: $(Ly)_i=y_{i-1}$ , with zero in position 0. The one-resident matrix is $B=\tfrac12(I-L/2)^{-1}$ . Since $L^k=0$ , the negative binomial expansion for $p$ identical-mean outsiders is a finite exact identity:

$$B^p=2^{-p}\sum_{d=0}^{k-1}\binom{p+d-1}{d}2^{-d}L^d.$$

Thus one whole household updates the targets by

$$x'_i=v+2^{-p}\sum_{j=0}^{i}\binom{p+i-j-1}{i-j}2^{-(i-j)}(x_j-v).$$

Process all households richer than the initial target mean in increasing mean order. Compute the kernel, calculate every new coordinate from the old vector, then swap arrays. Do not overwrite old entries during the forward loop. Finally sum the $k$ target values.

## Correctness and Boundaries

Each matrix $B$ exactly describes all pairwise averages involving one outsider. Its power $B^p$ describes the entire household. The household order and filtering condition match the optimal strategy in the main solution, so this computes the same optimum. Reuniting the targets changes their individual means but preserves their total.

Generate kernel entries by consecutive binomial coefficients, whose denominators are at most $k-1$ . Compute mean inverses and $2^{-p}$ by binary exponentiation, avoiding tables of length $M$ . Compare actual means by integer cross-products. If no outsider is richer, the target total remains $m_1$ .

## Complexity and Tradeoffs

Let $M=\max_i p_i$ and let the modulus be $P$ . Sorting takes $O(n\log n)$ time. Overall time is $O(n\log n+n(k^2+\log P+\log M))$ , with $O(n+k)$ space.

This method omits the reference’s $O(M)$ inverse and power tables, at the cost of a quadratic convolution and exponentiations per household. It offers a direct representation of every target’s wealth, using exact modular arithmetic throughout. See the [full measurements](../../../docs/benchmark-R40.json) for its memory use and whether it meets the limit calibrated from the reference.
