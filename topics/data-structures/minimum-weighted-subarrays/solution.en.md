# Minimum-Weighted Subarray Sums: Solution

Problem setter's solution: use a monotone stack to assign subarrays to their minimum positions, then aggregate with double prefix sums. Codex (GPT-6) contributed precise tie handling, numeric bounds, portable 128-bit arithmetic, proofs and implementation. Monotone stacks and prefix sums are classical methods.

## Assign each subarray to one minimum position

When several positions share the minimum, choose the rightmost. For position $i$ , let $L_i$ be the nearest strictly smaller position on its left, and $R_i$ the nearest smaller-or-equal position on its right. Use $0,N+1$ when the corresponding position does not exist.

Exactly the subarrays

$$L_i<l\le i\le r<R_i$$

belong to $i$ . Equal values are allowed on the left but excluded on the right, making the owner unique. Maintain a stack of positions with strictly increasing values. On reading $A_r$ , pop every position whose value is at least $A_r$ . For a popped position $i$ , the current index gives $R_i=r$ , and the new stack top gives $L_i$ . After input ends, explicitly flush the stack with right boundary $N+1$ . Position zero is only a boundary marker and is never compared as a value, avoiding a numeric sentinel assumption.

![The three subarrays owned by position three in the sample](assets/explanation.svg)

Here $A_3=2$ , $L_3=0,R_3=4$ . Its subarrays are $[1,3]$ , $[2,3]$ and $[3,3]$ , contributing $2(9+6+2)=34$ .

## Double prefix sums

Define $P_j=\sum_{k=1}^{j}A_k$ , with $P_0=0$ , and

$$Q_j=\sum_{k=0}^{j-1}P_k,\qquad Q_0=0.$$

Fix owner $i$ and write $L=L_i,R=R_i$ . The sum of its subarray sums is

$$\begin{aligned}S_i&=\sum_{l=L+1}^{i}\sum_{r=i}^{R-1}(P_r-P_{l-1})\\&=(i-L)(Q_R-Q_i)-(R-i)(Q_i-Q_L).\end{aligned}$$

The first term repeats each right-end prefix sum $i-L$ times. The second repeats each prefix immediately before a left endpoint $R-i$ times. The answer is $\sum_i A_iS_i$ .

After reading index $r$ , prefix sums through $Q_{r+1}$ are available, including the $Q_r$ needed by popped positions. Each position is pushed and popped once.

## Negative values and exact integer bounds

Negative values do not change minimum ownership or the prefix-sum identity. Set $U=10^9$ . A length-$d$ subarray contributes absolute value at most $U^2d$ . Therefore the sum of absolute contributions is bounded by

$$U^2\sum_{d=1}^{N}d(N-d+1)=U^2\frac{N(N+1)(N+2)}6.$$

At the largest input, this is

$$166666716666670000000000000000000000000<2^{127}-1.$$

Signed 128-bit arithmetic suffices, while sixty-four bits do not. Each $P_j$ has magnitude at most $10^{16}$ and fits in sixty-four bits; $Q_j$ needs a wide type. Compute the two parts of $S_i$ and their difference in wide arithmetic before multiplying by $A_i$ . Do not multiply the two double-prefix terms by $A_i$ separately first, or compute index products in thirty-two bits. Every complete owner contribution and every partial sum of owner contributions obeys the bound on the sum of absolute contributions.

Standard C++17 does not specify a 128-bit integer type. The `FWide` type in [std.cpp](std.cpp) stores two unsigned sixty-four-bit words in two's-complement form:

- Addition handles the low word first and carries into the high word. Negation complements both words and adds one.
- To multiply by a signed thirty-two-bit factor, take magnitudes, split the wide operand into four thirty-two-bit words, multiply each with carry, then restore the sign.
- Every single-word product with carry fits in an unsigned sixty-four-bit integer. Internal operations are modulo $2^{128}$ ; the proved mathematical bounds make their signed interpretation exact.
- For decimal output, take the magnitude and divide from the highest word to the lowest, collecting remainders. Handle zero and the negative sign explicitly.

The supplemental program's sixty-four-by-sixty-four multiplication similarly uses two thirty-two-bit words per operand and four result words. The arithmetic type has separate Python arbitrary-precision checks for signs, carries, borrows, multiplication and decimal output.

## Correctness and complexity

The boundaries assign each nonempty subarray to exactly its rightmost minimum. The double-prefix identity gives the exact sum of subarray sums owned by that position. Multiplying by its minimum produces their total contribution. Owner classes partition all subarrays, so summing them gives the required answer. The numeric bounds and word operations keep the computation exact.

Time is $O(N)$ and space is $O(N)$ . The main arrays use a four-byte value, sixteen-byte double prefix and four-byte stack index per position: about twenty-four bytes each, or two hundred forty million bytes at maximum size.

## Parallel option and verification

The primary program retains the setter's ownership and double-prefix organization. [Grouping left endpoints for each right endpoint](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), uses a different streaming DP invariant with the same linear time and space. It needs neither a value array nor a double-prefix array, but has larger individual stack entries. It runs faster in the current measurements. Both support the complete range; see the [measurements](../../../docs/benchmark-R26.json).

Small tests independently enumerate all subarrays. Every formal output is also checked by Cartesian-tree subtree aggregation using independent wide arithmetic, including the exact upper bound, negative answers, repeated minima, monotone inputs and mixed signs. See the [plan](tests/plan.json) and [generator](tests/generate.py).
