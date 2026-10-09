# Paired DNA Strands with Many Pair Types: Solution

## Method and contributions

Codex (GPT-6) applies equivalence-class counting for the reverse-complement involution and evaluates the numerator modulo $2P$ , making halving exact for every modulus. See [std.cpp](std.cpp). Counting orbits of an involution is a standard method; the contributions here are its application, numerical handling, proof, and implementation.

Let $q=2K$ be the alphabet size. A structure is represented by a string $s$ , and exchanging strands gives its reverse complement $R(s)$ . Since $R(R(s))=s$ , an equivalence class has one or two representations.

## Counting classes

There are $q^N$ strings in total. For odd $N$ , a fixed string would require its central letter to complement itself, contradicting the pairing definition. For even $N$ , choosing the first half determines the second, giving exactly $q^{N/2}$ fixed strings.

Each fixed string forms its own class; all other strings form pairs. The exact integer count is

$$C=\frac{q^N+[N\text{ is even}]q^{N/2}}{2}$$

## Exact halving with any modulus

$P$ may be one, even, or composite, so the implementation does not rely on an inverse of two. Let the integer numerator be $A$ and compute $r=A\bmod(2P)$ . Both $A$ and $2P$ are even, so $r$ is even. From $A=2Pt+r$ ,

$$C=Pt+r/2,\qquad C\bmod P=r/2$$

The final value is already in $[0,P-1]$ and can be XORed into the aggregate.

For odd length, compute $q^N\bmod(2P)$ . For even length, one exponentiation is enough: with $h=q^{N/2}\bmod(2P)$ , the numerator residue is $(h^2+h)\bmod(2P)$ . Each query therefore needs one binary exponentiation.

## Correctness and complexity

Classification into fixed strings and two-element classes proves the counting formula. The equation modulo $2P$ proves that ordinary integer halving yields the correct residue modulo $P$ . XORing those individual residues matches the required output.

Each query takes $O(\log(N+1))$ time and $O(1)$ auxiliary space, allowing streamed processing. Since $2P\le2\times10^9$ , the largest multiplication-plus-addition is below $4\times10^{18}$ and fits signed 64-bit integers. Factoring out $K$ also avoids inverses, but is an equivalent numerical form of the same counting formula rather than a separate algorithm.
