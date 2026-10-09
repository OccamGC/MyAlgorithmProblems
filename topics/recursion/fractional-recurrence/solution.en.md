# A Fractional-Power Recurrence: Solution

## Method and contributions

The reference preserves the setter's recursive evaluation with memoization below a cutoff and direct expansion above it. Codex (GPT-6) added exact integer-root verification and fallback, an explicit zero base case, an uncomputed sentinel instead of a separate visited array, and smaller allocation for small maximum inputs. See [std.cpp](std.cpp). These changes improve numerical reliability and storage within the same algorithm.

Let $U$ be the maximum query and $C=\min(10^7,U+1)$ . Allocate $C$ signed 64-bit entries initialized to $-1$ , with $Memo_0=0$ . Return a cached value when available; otherwise evaluate the recurrence and save the result only for arguments below $C$ . Repeated arguments above the cutoff are expanded again, so complexity must not assume that every argument is computed only once.

## Exact flooring of the fractional power

For $r=\lfloor x^{4/5}\rfloor$ , the equivalent condition is

$$r^5\le x^4<(r+1)^5$$

Floating-point `pow` supplies only a candidate. Accept it only after verifying both inequalities with integers; otherwise find $r$ by binary search. Correctness therefore does not depend on the rounding direction or an assumed error of at most one.

Within the bounds, $x^4\le10^{36}$ and $r<16000000$ . The program represents a wide integer as four 32-bit limbs, most significant first. Repeated multiplication by the base, using 64-bit products and carry, computes the fourth or fifth power. All such powers fit below $2^{128}$ , and each limb product plus carry fits in 64 bits. Lexicographic array comparison equals unsigned wide-integer comparison. Only standard C++17 types are used.

Binary search keeps a left endpoint whose fifth power is at most the target and a right endpoint whose fifth power exceeds it. Initially they are zero and $\min(x,16000000)+1$ . When adjacent, the left endpoint is $r$ . The exact candidate check usually avoids the full search without changing the mathematical result.

## Correctness and value bounds

At zero the equation gives $F(0)=5F(0)$ , hence $F(0)=0$ . For every positive $x$ , both recursive arguments $\max(r-1,0)$ and $\lfloor x/2\rfloor$ are smaller than $x$ . Induction on the argument proves that recursive results, and then their stated combination, are correct. Memoization only reuses this uniquely determined value, so all answers are correct and recursion terminates.

Both child arguments are nondecreasing functions of $x$ . Induction using the recurrence shows that $F$ is nondecreasing. Exact evaluation at the maximum input gives $F(10^9)=12422138161640$ , also matching the supplied sample. All values in range, and the nonnegative products in their sums, are therefore well below the signed 64-bit limit. An independent arbitrary-precision implementation checked this endpoint and the test queries.

## Complexity

Let $S$ count distinct expanded arguments that are cached, and $H$ count expansions of uncached arguments, including repetitions. We have $S\le C$ . With four limbs and fixed exponents, each integer power uses a constant number of machine operations; root search needs $O(\log(U+2))$ comparisons in the worst case. Total time is

$$O\bigl(C+N+(S+H)\log(U+2)\bigr)$$

If uncached arguments occur, $C=10^7$ . At or above that threshold both children are at most half their parent. The binary expansion tree above the threshold has $O(1+U/C)$ nodes per query, giving the coarse bound $H=O(N(1+U/C))$ . Smaller nodes share cached values. An unconditional $O(N\log U)$ claim would be inaccurate.

The array, queries, and stack take $O(C+N+\log(U+2))$ space. Arguments at least halve while sufficiently large, and the remaining small-argument depth is bounded by a constant. The largest cache uses about $80$ MB, within the original $128$ MB limit. A table through the maximum argument needs excessive memory; caching all arguments in a hash table has no established better guarantee under this limit, so neither is presented as a qualified additional algorithm.
