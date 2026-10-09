# Clue Generator: Solution

Problem setter's solution: compress prefix sums, precompute equal-value counts and index sums by blocks, and handle full blocks plus two fringes during queries. Codex (GPT-6) contributed complete block-interval answers, compact storage using occurrence-list prefix sums, proofs and standard C++17 implementation. Prefix sums, block decomposition and coordinate compression are classical methods.

## Distances between equal prefix values

Let $P_0=0$ and $P_i=\sum_{j=1}^i a_j$ . A subarray $[s,t]$ has sum zero exactly when $P_{s-1}=P_t$ , and its length is $t-(s-1)$ . A query $[l,r]$ therefore asks for the total distance $j-i$ of all equal-value pairs $i<j$ within prefix-index interval $[l-1,r]$ .

![Distances among the three equal prefix sums in the sample](assets/explanation.svg)

The zero prefix value occurs at indices zero, two and four, producing distances two, two and four, totalling eight. Prefix sums have magnitude at most $10^{14}$ ; compute them in sixty-four bits and compress them into $V\le N+1$ identifiers.

## Answers for complete block intervals

Partition the $N+1$ prefix positions into blocks of width $B=\lceil\sqrt{N+1}\rceil$ , with $K=\lceil(N+1)/B\rceil$ blocks. Precompute $H[s][t]$ , the distance sum of all equal-value pairs from the start of block $s$ through the end of block $t$ .

Fix a starting block and scan rightward from its start. For each value, maintain its preceding occurrence count $c_v$ and sum of positions $z_v$ . At position $j$ , the new contribution

$$c_vj-z_v$$

is exactly its total distance to earlier equal positions. Update the statistics and save the accumulated answer at every block end. Total scanning time is $O(NK)$ and the answer table uses $O(K^2)$ space.

Store a separate answer for every complete block interval. Subtracting two global prefix answers is insufficient: the later prefix includes equal-value pairs crossing from the excluded prefix, and subtraction does not remove these cross terms.

## Obtain middle-interval statistics in constant time

For each value $v$ , store its occurrence indices in ascending order and their local prefix sums. Also store $C[b][v]$ , the number of occurrences of $v$ strictly before the start of block $b$ .

If the complete middle covers a half-open prefix-index interval $[F,G)$ with block-aligned boundaries, the two boundary counts identify the occurrence-list index range for $v$ . A difference of local prefix sums gives its position sum. Thus both its count and position sum take $O(1)$ time. The boundary matrix uses thirty-two-bit counts, while occurrence prefix sums use sixty-four bits. No second sixty-four-bit block-by-value position-sum matrix is necessary.

## Three disjoint classes of pairs

For prefix-index interval $[L,R]$ , set

$$F=(\lfloor L/B\rfloor+1)B,\qquad G=\lfloor R/B\rfloor B.$$

If $F\ge G$ , there are at most $2B$ positions; directly scan with counts and position sums. Otherwise the complete middle is $[F,G)$ and the fringes are $[L,F)$ and $[G,R]$ .

1. Middle-to-middle pairs are answered by $H$ .
2. For a left-fringe position $i$ , let its value occur $c$ times in the middle with position sum $z$ . Its cross contribution is $z-ci$ . For a right-fringe position it is $ci-z$ .
3. Scan the left fringe followed by the right fringe in increasing index order, using temporary counts and position sums for all fringe-to-fringe pairs. This also includes pairs crossing between the two fringes.

Compute and cache middle statistics only once per value in a query. Clear only values actually visited afterward, instead of clearing the entire compressed universe. A block-aligned endpoint may still leave one block in a fringe; the complexity is unchanged.

## Correctness

Zero-sum subarrays correspond bijectively to equal-prefix pairs with the same length. Block preprocessing adds precisely the pairs whose right endpoint is the newly scanned position, making $H$ exact. Occurrence lists and boundary counts provide exact middle statistics. Every pair belongs to exactly one of the classes: both in the middle, one in the middle, or both in the fringes. The three query steps count these classes completely and without overlap. Each exact answer then correctly decodes the next query, proving the whole sequence by induction.

## Complexity and arithmetic

Preprocessing takes $O(N\log N+NK)$ time, each query $O(B)$ time, and space is $O(N+KV+K^2)$ . With square-root width, the worst-case bounds are $O(N\sqrt N+M\sqrt N+N\log N)$ time and $O(N\sqrt N)$ space. The largest count matrix occupies about one hundred twenty-seven million bytes; measured working sets include the remaining storage.

All zeros maximize the answer at $N(N+1)(N+2)/6<1.7\times10^{14}$ . Use sixty-four-bit arithmetic for count-times-index products, position sums, answers and XOR. Although raw fields are at most $10^9$ , the preceding answer must not be truncated to thirty-two bits. Update it after every answer.

The primary [std.cpp](std.cpp) retains block decomposition with constant-time middle statistics. The [occurrence-list binary-search method](solution-alternative.en.md), in [alternative.cpp](alternative.cpp), removes the block-by-value matrix and substantially reduces space. Its query bound gains a logarithmic factor, and it is a parallel option supporting the full range. Actual speed depends on value repetition and matrix access, not just asymptotic bounds.

Small tests independently enumerate subarrays. Every formal answer is also checked with Mo interval maintenance: decode all intervals using candidate preceding answers, then independently compute their values. If every value agrees, induction from the first query proves every decoding correct. This verifier needs candidate answers, so it is not a standalone solver for the encrypted problem.

See the [plan](tests/plan.json), [generator](tests/generate.py) and [measurements](../../../docs/benchmark-R26.json).
