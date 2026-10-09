# Factorial Recovery — Solution

Credits: the problem setter’s solution recovers the missing prefix with one sufficiently large modulus. Codex (GPT-6) uses two moduli and the Chinese remainder theorem for exact integer reconstruction.

## Comparing solutions

### Problem setter’s solution: one sufficiently large modulus

Let the suffix have length $k$ and integer value $s$ , and let the missing prefix be $x$ . Then $n!=x10^k+s$ and $0\le x<10^{15}$ . The problem setter’s method uses the prime $M=7\cdot2^{52}+1=31525197391593473$ , computes the factorial and suffix residues, and obtains

$$x\equiv(n!-s)(10^k)^{-1}\pmod M$$

The inverse exists because $M$ is coprime to $10$ . Since $x<M$ , the normalized residue is the complete prefix; no enumeration is needed. Print a nonzero prefix first, followed by the unchanged suffix. The problem setter’s program uses Fermat's little theorem and binary exponentiation for the inverse. Assuming constant time per exact modular multiplication, this takes $O(n+k+\log(k+1)+\log M)$ time and $O(k+1)$ space to retain the suffix.

### Two moduli used by Codex

The two-modulus method also recovers a short prefix through modular arithmetic, combining residues modulo two smaller primes with the Chinese remainder theorem. The single-modulus method requires exact modular multiplication: products must not overflow signed 64-bit integers, and floating-point quotient estimates need rigorous error handling. With correct modular multiplication, the single-modulus method is valid.

Every multiplication and reconstruction intermediate in the Codex implementation is provably within signed 64-bit range, allowing an exact implementation in standard C++17. The cost is two sets of residue calculations and an additional reconstruction step. There is no asymptotic improvement, and no speed comparison between the programs was performed. The following sections explain the Codex implementation.

## Recover only the missing prefix

Let $s$ be the integer represented by the supplied suffix, while retaining its string length $k$ . There is a nonnegative integer $x$ such that

$$n!=x\cdot10^k+s$$

At most fifteen digits are missing, so $0\le x<10^{15}$ . Computing the whole factorial requires arbitrary-precision multiplication, but reconstructing this short prefix is sufficient.

## Compute the prefix modulo two primes

Choose distinct primes $p=1000000007$ and $q=1000000009$ . Both are coprime to $10$ , and $pq>10^{15}$ .

For each modulus $t\in\{p,q\}$ , multiply the integers up to $n$ to obtain $n!\bmod t$ . Scan the suffix digits using “remainder times ten plus the new digit” to obtain $s\bmod t$ . Compute $10^k\bmod t$ by binary exponentiation and its inverse by Fermat's little theorem. Then

$$r_t=(n!-s)(10^k)^{-1}\bmod t$$

Normalize residues to $0,\ldots,t-1$ . Leading zeros do not affect a residue, but must remain in the string used for output.

## Combine the residues

Write $x=r_p+pu$ and impose its residue modulo $q$ :

$$u=(r_q-r_p)p^{-1}\bmod q$$

Taking $0\le u<q$ gives the unique number in $0\le x<pq$ satisfying both congruences. The actual prefix satisfies them and is less than $10^{15}<pq$ , so this reconstruction is exact.

If $x>0$ , print it followed by the unchanged suffix. If $x=0$ , print only the suffix: in valid input, it already contains the complete factorial, without extra leading zeros. When $k=0$ , the suffix is empty and $s=0$ , so print the reconstructed factorial itself. The product starts at $1$ , handling both $0!$ and $1!$ .

## Implementation and complexity

Let $P=\max(p,q)$ . With machine-word arithmetic for these moduli, time is $O(n+k+\log(k+1)+\log P)$ and space is $O(k+1)$ . The suffix is stored for output; the reference solution never constructs the large factorial as an integer.

Every modular product is less than $P^2<2^{63}$ , and the combined value is less than $pq<2^{63}$ . Standard signed 64-bit C++17 integers suffice, without floating-point approximations or compiler extensions.

## Validation

Small cases compare the complete output with Python's exact integer factorial. Formal cases also use exact full-output comparison. Tests cover $k=0$ , $k=D$ , a full fifteen-digit prefix, leading zeros and maximum $n$ .

See [environment and measurements](../../../docs/评测环境与性能.md) for performance measurements.
