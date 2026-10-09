# Editorial for Grox's Sequence V A

**Problem setter’s solution: Stirling numbers of the second kind, falling factorials, and modular exponentiation.** Codex (GPT-6) handles exponent thresholds for non-coprime moduli and the zeroth-power branch, and stores the same Stirling recurrence in one rolling row. No factorial inverse is assumed for a composite modulus.

## Replacing the enormous sum

Handle $k=0$ separately. Since this problem defines the zeroth power of zero as zero, the answer is $2^n-1$ , giving zero when $n=0$ .

For $k>0$ , let $S(k,j)$ denote a Stirling number of the second kind and $(n)_j=n(n-1)\cdots(n-j+1)$ a falling factorial. The identity

$$i^k=\sum_{j=0}^k S(k,j)(i)_j$$

counts functions by their number of distinct values: partition the $k$ labeled objects into $j$ nonempty preimage groups and assign distinct targets to those groups. Also,

$$\binom ni(i)_j=(n)_j\binom{n-j}{i-j}$$

Interchanging the sums and applying the binomial theorem gives

$$\sum_{i=0}^n i^k\binom ni=\sum_{j=1}^{\min(n,k)}S(k,j)(n)_j2^{n-j}$$

Here $S(k,0)=0$ , and falling factorials vanish for $j>n$ . Explicitly using $\min(n,k)$ avoids negative exponents.

## Stirling recurrence and composite moduli

Use

$$S(t,j)=jS(t-1,j)+S(t-1,j-1)$$

Initially $S(0,0)=1$ , with other entries zero. Update indices in descending order to retain one row, using $O(k^2)$ time and $O(k)$ space. The setter’s full table implements the same recurrence using $O(k^2)$ space; rolling the rows does not change the counting algorithm.

Compute falling factorials by direct multiplication modulo $p$ . A factorial quotient with modular inverses is invalid in general because $p$ can be composite.

Let $\phi=\varphi(p)$ . For a nonnegative exponent $e$ , evaluate $2^e\bmod p$ using

$$\widehat e=\begin{cases}e,&e<\phi\\e\bmod\phi+\phi,&e\ge\phi\end{cases}$$

This also works for even moduli. On every odd prime-power factor of $p$ , the base $2$ is invertible and $\phi$ is a multiple of the relevant Euler totient. On a factor $2^v$ , once $e\ge\phi$ , both exponents are at least $v$ and both residues are zero. The Chinese remainder theorem combines these statements. Return zero separately when $p=1$ .

While reading decimal $n$ , retain $n\bmod p$ , $n\bmod\phi$ , and $\min(n,\phi+k)$ . The last value determines accurately whether each $n-j$ is at least $\phi$ and whether $n<k$ . Knowing only that $n\ge\phi$ is insufficient to conclude that every $n-j\ge\phi$ .

For $k=0$ , decimal exponentiation is direct: extending an exponent prefix $t$ by digit $d$ updates $2^t$ to $(2^t)^{10}2^d$ . This avoids any threshold reasoning for that branch.

## Correctness and complexity

The finite-sum identity holds over the integers. The Stirling recurrence, falling factorial products, and safe exponents yield the correct residues of each factor, so modular multiplication and addition give the answer. Normalize negative residues to their least nonnegative representatives.

Let $D$ be the number of decimal digits in the input $n$ . Trial division computes the totient in $O(\sqrt p)$ time. Total time is $O(k^2+k\log p+\sqrt p+D)$ and space is $O(k+D)$ . The boundary $n=10^{1000}$ has exactly $1001$ digits, which the input container must accommodate.

## Supplementary solution

Keep the Stirling expansion, compute $2^{n-\min(n,k)}$ directly from decimal digits and repeatedly double for all other nonnegative exponents. This removes factorization, Euler totients and per-term exponentiation. Worst-case time is $O(k^2+D)$ , with Stirling columns also truncated to the needed range; it is a simpler full-range parallel implementation.

[Complete editorial and measurements](solution-alternative-decimal.en.md) · [Program](alternative-decimal.cpp)
