# Service Stations on a Line: The Rightmost Station as a State

This is the setter's endpoint-placement DP, implemented in [alternative.cpp](alternative.cpp) for the full constraints. Sort the homes as $x_1\le\cdots\le x_N$ . A station can be moved to the median of its consecutive service group, so restricting stations to home coordinates retains an optimum.

## Cost between two stations

If consecutive stations lie at $x_i,x_j$ , the intermediate homes contribute

$$W(i,j)=\sum_{i<k<j}\min(x_k-x_i,x_j-x_k).$$

For fixed $i$ , increase $j$ while maintaining the last index $s$ that is at least as close to the left station. Start with $s=i$ and advance while $s+1<j$ and $x_{s+1}-x_i\le x_j-x_{s+1}$ . Coordinate prefix sums $P$ give

$$W(i,j)=P_s-P_i-x_i(s-i)+x_j(j-s-1)-(P_{j-1}-P_s).$$

The boundary moves only right. All costs take $O(N^2)$ time and space.

## States and transitions

Let $F_t(j)$ be the minimum cost for homes up to $j$ using $t$ stations with the rightmost station at home $j$ . Station indices strictly increase, although their coordinates may coincide.

$$F_1(j)=x_j(j-1)-P_{j-1},\qquad F_t(j)=\min_{t-1\le i<j}\{F_{t-1}(i)+W(i,j)\}.$$

Homes between consecutive stations choose one of those stations. Homes outside the outermost stations choose the nearer endpoint station. Thus, each transition joins the processed left part to exactly the new interval between stations. The final answer is

$$\min_{M\le j\le N}\{F_M(j)+P_N-P_j-x_j(N-j)\}.$$

## Divide-and-conquer optimization

For $i\le j\le k\le l$ , the costs satisfy $W(i,k)+W(j,l)\le W(i,l)+W(j,k)$ . Compare one home's contribution at a time. For a home in $[j,k]$ , the four distances satisfy $A\ge B$ and $C\le D$ , and

$$\min(A,C)+\min(B,D)\le\min(A,D)+\min(B,C).$$

For a home in either outer interval $[i,j]$ or $[k,l]$ , moving the available endpoint station farther away cannot reduce the distance. Endpoints contribute zero; equal coordinates cause no problem. Summing these inequalities proves the claim.

Consequently, for fixed $t$ , the smallest optimal predecessor cannot decrease as $j$ increases. Find the best predecessor of a middle target, then use it as a bound for the left and right recursive searches. Each DP layer takes $O(N\log N)$ time. The implementation uses only this monotonicity within a layer, two rolling DP arrays, 64-bit costs and a sufficiently large infinity.

Total time is $O(N^2+MN\log N)$ and space is $O(N^2)$ . This formulation directly describes service between consecutive facilities. The reference [median-grouping method](solution.en.md) saves the quadratic table through a constant-time interval formula. Both programs pass all formal data. The method is the setter's; GPT-6 supplies the proof and safe implementation. See the [measurements](../../../docs/benchmark-R25.json).
