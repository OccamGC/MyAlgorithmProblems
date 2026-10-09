# Apostle Luke's Password — Solution

Setter method: factorial reduction and nine-base Miller–Rabin. Codex (GPT-6): safe modular multiplication, boundary and deterministic proofs, and the progression-sieve alternative.

## From factorials to primality

Set $f=(p-1)!$ . Since $p!=pf$ , the radicand is $(f+1)^2/p^2$ , whose square root is exactly $(f+1)/p$ . The inner floor is an integer, so

$$H(p)=\left\lfloor\frac{f+1}{p}\right\rfloor-\left\lfloor\frac f p\right\rfloor.$$

The two floors differ by one exactly when $f\equiv-1\pmod p$ . Direct substitution gives $H(1)=1$ ; $H(0)=0$ is a separate definition.

For $p\ge2$ , Wilson's theorem says this congruence holds exactly for primes. For a prime modulus, pair each nonzero element with its inverse; only $1,-1$ pair with themselves, leaving product $-1$ . For composite $p$ , a proper prime divisor $q<p$ divides $(p-1)!$ , so it cannot divide $(p-1)!+1$ . Each contribution therefore asks whether the argument is $1$ or prime.

## Deterministic Miller–Rabin

For an odd candidate, write $p-1=d2^s$ with odd $d$ . For each base $a$ , compute $x=a^d\bmod p$ . Accept this base if $x$ is $1$ or $p-1$ ; otherwise square up to $s-1$ times and require a result of $p-1$ . A failing base proves compositeness. Handle small primes and their multiples first, including candidates equal to a base.

Use bases $2,3,5,7,11,13,17,19,23$ . The largest argument here is $204999000000000$ , below the smallest common strong pseudoprime for these nine bases, $3825123056546413051$ . Thus the test is deterministic throughout the allowed range. [Jiang and Deng's paper](https://arxiv.org/abs/1207.0063) establishes this bound. The range guarantee is part of the proof.

Multiply modulo $p$ by binary doubling and addition. Each addition combines two values below $p<2^{48}$ , so unsigned 64-bit addition is safe. Direct multiplication of two residues could overflow; floating-point quotient approximations are unnecessary.

Process each $p=k(G+i-1)+b$ , add its contribution to the running total, and print that total.

## Correctness

The algebra proves the primality criterion with the two exceptional arguments. The bounded deterministic test recognizes primes exactly, and safe modular multiplication preserves each modular operation. Starting from zero and adding the current term maintains precisely the required prefix sum by induction.

## Complexity and Contributions

Let $U$ be the largest argument. Nine fixed bases take $O(N\log^2 U)$ time and $O(1)$ extra space, with streamed output. The setter's factorial-to-primality reduction and nine-base Miller–Rabin approach are retained. Codex (GPT-6) supplied boundary specifications, the deterministic bound, safe multiplication, proofs, and tests. See [std.cpp](std.cpp).

The [arithmetic-progression sieve](solution-alternative.en.md) provides an independent method without a pseudoprime bound.

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R32.json)
