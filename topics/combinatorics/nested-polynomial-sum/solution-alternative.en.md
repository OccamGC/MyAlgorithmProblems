# A Certain Unscientific Repeated Prefix Sum: Alternative Solution

## Setter's solution: triangular elimination of each monomial

The setter proposed eliminating monomials into the rising-binomial basis. Codex (GPT-6) implemented it in [alternative.cpp](alternative.cpp) and added batch inverses for binomial evaluation. The [main solution](solution.en.md) gives the summation identity, binomial evaluation, and the more efficient conversion recurrence.

Build the ordinary power coefficients of every $B_j$ using

$$B_j(x)=\frac{x+j-1}{j}B_{j-1}(x)$$

with $B_0=1$ . Each step multiplies by a linear polynomial, for $O(k^2)$ coefficient operations; division by $j$ uses its modular inverse. The leading coefficient of $B_j$ is $1/j!$ .

For each $x^i$ , initialize the remainder polynomial to $x^i$ and process $j=i$ down to zero. If its $x^j$ coefficient is $r_j$ , choose basis coefficient $r_jj!$ and subtract that multiple of $B_j$ . This eliminates the leading term without changing higher degrees, since $B_j$ has degree $j$ . At the end the remainder is zero, giving a complete expansion. Multiply these coefficients by $a_i$ and add them to the total weights.

Then use the identity that $m$ prefix sums turn $B_j$ into $B_{j+m}(n)$ to evaluate the answer. Each elimination step preserves “original monomial equals determined basis terms plus remainder,” proving the expansion correct. Linearity of summation proves the final result.

The implementation takes $O(m+k^3+k\log p)$ time and $O(k^2)$ space. Individual inverses of $1,\ldots,k$ cost $O(k\log p)$ , while eliminating all monomials is cubic. This method remains valid over the full range, but the recurrence conversion saves both time and space and is the reference choice.
