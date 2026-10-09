# Counting Paired DNA Strands: Solution

## Method and contributions

The problem setter's solution counts symmetry cases, derives parity-dependent formulas, and evaluates them with binary exponentiation. Codex (GPT-6) supplied the self-contained reverse-complement model and involution proof and organized [std.cpp](std.cpp). For many queries, a [two-level power table](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) trade preprocessing space for constant-time queries.

Let $R(s)$ be the reverse complement of $s$ . Complementing and reversing twice restores the string, so $R(R(s))=s$ . Each molecule corresponds to one or two strings.

## The setter's first-asymmetry count

Start with length $2h$ . Compare the beginnings of $s$ and $R(s)$ , determining letters at opposite ends together.

- If they always agree, the first $h$ letters each have four choices and determine the other half, giving $4^h$ possibilities.
- If the first difference occurs at pair $i$ , the earlier pairs give $4^{i-1}$ choices. The differing letters form an unordered pair, with $\binom42=6$ choices. Their order fixes a representative strand direction, after which the middle $2h-2i$ letters are arbitrary.

The even-length count is therefore

$$4^h+6\sum_{i=1}^{h}4^{i-1}4^{2h-2i}=2^{2h-1}(1+2^{2h})$$

For length $2h+1$ , a symmetric outer portion leaves two choices for the central complementary pair. If the outer portion already differs, the representative direction is fixed and the central letter has four choices. Hence

$$2\cdot4^h+4\left(6\sum_{i=1}^{h}4^{i-1}4^{2h-2i}\right)=2^{4h+1}$$

## Involution interpretation and implementation

Alternatively, count fixed strings. An odd length would require the central letter to equal its complement, which is impossible. At even length, the first half determines everything, giving $4^{n/2}$ fixed strings. All other strings pair up, so the count is

$$\frac{4^n+[n\text{ is even}]4^{n/2}}{2}$$

This agrees with the earlier formulas. For odd length the program computes $2^{2n-1}$ . For even length it computes $z=2^{n-1}\bmod p$ and then $z(2z+1)\bmod p$ , where $p=10^9+7$ . Reduce each query's count first, then XOR it into the answer. Repeated queries cancel according to XOR.

## Correctness and complexity

Classification by the first differing pair is disjoint and covers every representation. The fully symmetric case and the fixed representative direction remove precisely the duplication from exchanging strands. The involution argument likewise shows that every nonfixed representation has exactly one distinct partner. Thus the formula counts exactly the required equivalence classes. Binary exponentiation evaluates the modular powers exactly, and successive XOR gives the requested aggregate.

Each query takes $O(\log(n+1))$ time and $O(1)$ auxiliary space; total time is the sum over queries. The largest exponent is $1999999999$ , and multiplication uses signed 64-bit integers. The power table is faster for many queries but has initialization and storage costs. Binary exponentiation remains the space-efficient reference.
