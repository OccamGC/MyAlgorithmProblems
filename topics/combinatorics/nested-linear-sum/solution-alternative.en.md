# A Certain Unscientific Weighted Sum of First Values of Monotone Sequences: Alternative solution

## Shared product: the setter's solution

Let $P=m(m+1)\cdots(m+n-1)$ . Share this product and the denominator $(n+1)!$ between the two coefficients from the main editorial:

$$\mathrm{Answer}=P\,((n+1)!)^{-1}\bigl(k(n+m)+c(n+1)\bigr)\pmod p$$

[alternative.cpp](alternative.cpp) computes the product and factorial, then one modular power. Correctness follows from $A=P/n!$ and $B=P(n+m)/(n+1)!$ . If $m=0$ , $P$ contains zero and gives the correct answer automatically. Every positive factor of $(n+1)!$ is smaller than $p$ , so the inverse exists even when the numerator crosses the modulus.

Time is $O(n+\log p)$ and space is $O(1)$ . Sharing the product avoids duplicate work for large domains; the [reference symmetric-product method](solution.en.md) uses fewer factors for small domains. Both pass the full tests. The formula and sharing strategy belong to the setter; Codex (GPT-6) supplied the portable implementation and boundary reasoning.
