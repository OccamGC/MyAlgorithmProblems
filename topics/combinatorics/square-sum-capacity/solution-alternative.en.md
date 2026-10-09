# The Capacity of Square-Sum Stacks: Exact Karatsuba Squaring

## Proof of the Maximum Capacity

Write $C(n)=\lfloor(n+1)^2/2\rfloor-1$ .

**Upper bound.** Suppose $T=C(n)+1=\lfloor(n+1)^2/2\rfloor$ balls have been placed. Consider the largest $n+1$ labels, $T-n,\ldots,T$ . The sum of any two distinct such labels is strictly between $n^2$ and $(n+1)^2$ , so they cannot be adjacent. Labels on a stack strictly increase from bottom to top, making these large labels a contiguous top section. If a stack contained two, some two would be adjacent, a contradiction. At least $n+1$ stacks would therefore be required.

**Construction attaining the bound.** For one stack, use ball one. For odd $n>1$ , describe the first two layers from the top, with local column index $j=0,\ldots,n-1$ :

$$\text{Top}_j=C(n)-n+1+j,\qquad \text{Below}_j=C(n)-n-j.$$

Below the middle $n-2$ columns, recursively place the construction for $n-2$ stacks. Adjacent labels in the first two layers sum to $n^2$ . Where the second layer meets the recursive first layer, they sum to $(n-1)^2$ . All other adjacencies follow by induction. The two layers use the largest $2n$ labels because $C(n)-C(n-2)=2n$ , so no label is omitted or repeated.

For even $n$ , place $C(n),C(n)-1,\ldots,C(n)-n+1$ across the top layer. Put the construction for $n-1$ stacks below its first $n-1$ columns. Adjacent labels at the join sum to $n^2$ , and $C(n)-C(n-1)=n$ . This is valid and uses precisely all labels through $C(n)$ .

Every column decreases from top to bottom, so placing its labels in increasing global order respects the required operation sequence. The construction and upper bound prove that the optimum is exactly $C(n)$ .

## Three Recursive Squares

Represent $N+1$ by a little-endian base-10000 digit polynomial, padded to a power-of-two length. Split it into low part $A$ and high part $B$ , with half-length $h$ :

$$\left(A+x^hB\right)^2=A^2+x^h\left((A+B)^2-A^2-B^2\right)+x^{2h}B^2.$$

Recursively compute only $A^2,B^2,(A+B)^2$ , then combine them in linear time. For length at most thirty-two, use ordinary multiplication and double off-diagonal terms by symmetry. Delay carrying until the complete convolution is available. Carry in base 10000, divide by two and subtract one to produce $\lfloor(N+1)^2/2\rfloor-1$ .

## Correctness and Numerical Safety

The divide-and-conquer identity gives exactly the low, middle and high parts of the square. Induction proves that each recursive call returns the exact convolution coefficients. Carrying preserves the represented value, and floor division followed by subtraction evaluates the proved capacity formula.

There are at most $25001$ base-10000 digits, whose sum is at most $25001\times9999$ . Adding high and low halves preserves this sum. Hence the sum of all nonnegative convolution coefficients in any recursive subproblem is bounded by $(25001\times9999)^2<2^{63}$ . Subtracting the two squares produces a nonnegative cross term; the subtracted components and accumulated results also satisfy this bound. Standard signed 64-bit arithmetic is sufficient, without extended integers or floating point.

## Complexity and Scope

For normalized length $d$ , the recurrence $T(d)=3T(d/2)+O(d)$ gives time $O(d^{\log_2 3})$ . Simultaneously live vectors form a geometric series in size, giving $O(d)$ auxiliary space. Reading the raw input string adds its linear time and space. Across cases, sum the times and take the maximum space.

[alternative.cpp](alternative.cpp) supports the full constraints and demonstrates integer divide-and-conquer multiplication without a modulus or roots. The preferred [NTT square](solution.en.md) has lower asymptotic time. Karatsuba is classical; GPT-6 supplied its application here, the 64-bit bound, implementation and validation. The capacity formula and construction proof come from the problem setter's solution. Both integer programs were compared with Python exact integers; see the [measurements](../../../docs/benchmark-R24.json).
