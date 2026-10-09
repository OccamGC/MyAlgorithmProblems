# Service Stations on a Line: Consecutive Groups and Medians

## Turn placement into grouping

Sort the coordinates as $x_1\le\cdots\le x_N$ . In station order, each station can serve a consecutive interval of homes; distance ties can also be assigned consecutively. For any fixed group, a median minimizes the sum of absolute distances. Thus, an optimum exists with every station at a home coordinate.

We may use exactly $M$ nonempty groups. If a station serves no home, $M\le N$ lets us split a group containing at least two homes and add a station without increasing the cost. Duplicate coordinates do not affect this argument.

Let $P_i=\sum_{j=1}^ix_j$ and $P_0=0$ . The minimum cost of serving $[l,r]$ with one station is

$$C(l,r)=x_q(q-l+1)-(P_q-P_{l-1})+(P_r-P_q)-x_q(r-q),\qquad q=\lfloor(l+r)/2\rfloor.$$

Prefix sums evaluate it in constant time.

## Dynamic programming and monotone decisions

Let $D_t(r)$ be the minimum cost of splitting the first $r$ homes into $t$ groups. Set $D_0(0)=0$ and every other infeasible state to infinity. Then

$$D_t(r)=\min_{t-1\le j<r}\{D_{t-1}(j)+C(j+1,r)\},\qquad r\ge t.$$

Direct evaluation costs $O(MN^2)$ . The interval cost is Monge: for $a\le b\le c\le d$ ,

$$C(a,c)+C(b,d)\le C(a,d)+C(b,c).$$

To prove this, consider the increment

$$C(l,r+1)-C(l,r)=x_{r+1}-x_{\lfloor(l+r+1)/2\rfloor}.$$

For fixed $r$ , this increment cannot increase as $l$ increases. Summing the increments from $c$ to $d$ proves the inequality. Adding $D_{t-1}(j)$ to candidate column $j$ preserves it, so the smallest optimal split is nondecreasing with $r$ . If two optima cross, the inequality allows exchanging them without increasing the cost; choosing the smallest split on ties rules out a strict inversion.

## Divide and conquer within one layer

Suppose targets $[L,R]$ have optimal splits in $[A,B]$ . Evaluate the middle target $r$ by trying $[A,\min(B,r-1)]$ . If its best split is $j$ , recurse on the left targets with upper bound $j$ , and on the right targets with lower bound $j$ . Each layer starts with targets $[t,N]$ and candidates $[t-1,N-1]$ . Update the best split only for a strictly smaller value to keep the smallest-index tie rule.

The recurrence considers every possible final group. Monotonicity ensures that the restricted recursive searches retain an optimum. Therefore, the answer is $D_M(N)$ .

## Implementation, complexity and comparison

Each recursion depth scans $O(N)$ candidates in total, and there are $O(\log N)$ depths per layer. Including sorting, time is $O(N\log N+MN\log N)$ and extra space is $O(N)$ with two rolling layers. Costs are at most $N\cdot10^8$ ; use 64-bit integers and $2^{60}$ as infinity.

[std.cpp](std.cpp) is the reference. The setter's method tracks the rightmost station and precomputes the cost between consecutive stations. Its complete [endpoint-placement explanation](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) are provided. It takes $O(N^2+MN\log N)$ time and $O(N^2)$ space. Median grouping removes the quadratic table. Both support the full constraints; see the [measurements](../../../docs/benchmark-R25.json).

Setter contribution: endpoint states, interval costs and divide-and-conquer optimization. GPT-6 applies classical median grouping and Monge optimization, and supplies proofs, bilingual explanations and standard C++17 programs for both methods. Small cases use naive interval DP; formal cases use an independent SMAWK row-minimum algorithm.
