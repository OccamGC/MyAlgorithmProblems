# The Capacity of Square-Sum Stacks: Exact Integer Squaring

## Proof of the Maximum Capacity

Write $C(n)=\lfloor(n+1)^2/2\rfloor-1$ .

**Upper bound.** Suppose $T=C(n)+1=\lfloor(n+1)^2/2\rfloor$ balls have been placed. Consider the largest $n+1$ labels, $T-n,\ldots,T$ . The sum of any two distinct such labels is strictly between $n^2$ and $(n+1)^2$ , so they cannot be adjacent. Labels on a stack strictly increase from bottom to top, making these large labels a contiguous top section. If a stack contained two, some two would be adjacent, a contradiction. At least $n+1$ stacks would therefore be required.

**Construction attaining the bound.** For one stack, use ball one. For odd $n>1$ , describe the first two layers from the top, with local column index $j=0,\ldots,n-1$ :

$$\text{Top}_j=C(n)-n+1+j,\qquad \text{Below}_j=C(n)-n-j.$$

Below the middle $n-2$ columns, recursively place the construction for $n-2$ stacks. Adjacent labels in the first two layers sum to $n^2$ . Where the second layer meets the recursive first layer, they sum to $(n-1)^2$ . All other adjacencies follow by induction. The two layers use the largest $2n$ labels because $C(n)-C(n-2)=2n$ , so no label is omitted or repeated.

For even $n$ , place $C(n),C(n)-1,\ldots,C(n)-n+1$ across the top layer. Put the construction for $n-1$ stacks below its first $n-1$ columns. Adjacent labels at the join sum to $n^2$ , and $C(n)-C(n-1)=n$ . This is valid and uses precisely all labels through $C(n)$ .

Every column decreases from top to bottom, so placing its labels in increasing global order respects the required operation sequence. The construction and upper bound prove that the optimum is exactly $C(n)$ .

## Large Integers with NTT

Compute $\lfloor(N+1)^2/2\rfloor-1$ exactly. Remove leading zeros, store $N$ as little-endian base-100 digits, add one, and square its digit polynomial. Carry the convolution coefficients to obtain $(N+1)^2$ . Divide from the most significant digit by two, discard the remainder, subtract one, and print.

Use $p=1004535809=479\times2^{21}+1$ and primitive root three. The number $N+1$ has at most $100001$ decimal digits, or $50001$ base-100 digits. Every coefficient before carrying is at most

$$50001\times99^2=490059801<p.$$

Thus one modular convolution recovers the actual integer coefficients, without the Chinese remainder theorem. Choose the smallest power-of-two transform length at least twice the digit count; it is at most $2^{17}$ and avoids cyclic aliasing. Forward NTT, pointwise squaring and inverse NTT produce the exact coefficients. Carrying, halving and subtracting one are ordinary integer operations. The modulus is only a convolution tool; the output is not reduced modulo it.

## Correctness and Complexity

The capacity proof supplies the required expression. The coefficient bound ensures that NTT recovers an integer square. The remaining base-100 operations perform floor division and subtraction, so the printed value is the capacity.

Let $d$ be a case's decimal length after normalization and $B$ the total number of input characters. Total time is $O(B+\sum d\log(d+1))$ . Auxiliary space is $O(B_{\max}+d_{\max})$ , where $B_{\max}$ is the longest input number string. Cases are processed one at a time. All products and modular powers use standard 64-bit integers.

## Algorithm Choice and Attribution

The problem setter's solution uses the capacity formula and NTT integer squaring. The preferred [std.cpp](std.cpp) retains this approach, shortening transforms with base 100 and proving a coefficient bound for exact single-modulus recovery. This is an implementation improvement within the same algorithm. GPT-6 supplied the numerical bounds, sequential case handling and boundary implementation.

The [Karatsuba solution](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) replace modular transforms with three recursive squarings. Its time is $O(d^{\log_2 3})$ and its space is linear. This independent method needs no NTT modulus or roots and supports the full constraints. NTT remains preferred for its lower asymptotic time. Both were checked against Python exact integers, including maximum inputs, carry chains and leading zeros. See the [measurements](../../../docs/benchmark-R24.json).

![An arrangement attaining capacity eleven for four stacks](assets/stacks.svg)
