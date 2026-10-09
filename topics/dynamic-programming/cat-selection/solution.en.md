# Choosing Cats: Dynamic Programming by Selection Count

Problem setter's solutions: subset enumeration and weighted dynamic programming. Codex (GPT-6): rolling the DP into one array, explicit unreachable states, 64-bit bounds and pruning validation.

## Preferred dynamic program

The final selection count $k$ is fixed, so the $j$-th selected score receives weight $3^{k-j}$ . Let $f_{i,j}$ be the maximum contribution of exactly $j$ selected cats among the first $i$ , using their weights in the final answer.

Initialize $f_{0,0}=0$ and all other states as unreachable. Cat $i$ is either skipped or selected:

$$f_{i,j}=\max\left(f_{i-1,j},\ f_{i-1,j-1}+v_i3^{k-j}\right)$$

Only transition from reachable states, and keep $f_{i,0}=0$ . Precompute powers of three. The answer is $f_{n,k}$ .

With one array, update $j=\min(i,k),\ldots,1$ in descending order. Then $f_{j-1}$ still belongs to the previous row, preventing cat $i$ from being selected twice. For $k=0$ , no transition occurs and the answer stays zero.

## Correctness

Every selection of $j$ cats among the first $i$ either excludes or includes cat $i$ . The first case is represented by $f_{i-1,j}$ . In the second, cat $i$ has the largest selected index, so it is the $j$-th selection and contributes $v_i3^{k-j}$ ; the remainder is represented by $f_{i-1,j-1}$ . These two cases are disjoint and exhaustive. Taking the maximum is therefore correct. Induction proves all states and the final answer.

Negative scores do not remove the requirement to select exactly $k$ cats. Unreachable states must not be initialized to zero. The program uses a sentinel below all valid answers and checks reachability before addition.

## Numeric bounds and complexity

Every valid selection satisfies

$$|\mathrm{score}|\le1000\sum_{j=0}^{k-1}3^j=1000\frac{3^k-1}{2}$$

For $k\le25$ , this is at most $423644304721000$ , requiring 64-bit integers. C++ `long` is not guaranteed to be 64 bits on every platform; the program uses `long long` .

Time is $O(n(k+1)+1)$ and space is $O(k+1)$ , including powers and the rolling array. Using $k+1$ also covers reading the input when no cats are selected.

See [std.cpp](std.cpp). The setter's [subset search](solution-alternative.en.md), implemented in [alternative.cpp](alternative.cpp), remains a backup with $O(2^n)$ worst-case time and $O(n+1)$ space. It passes the formal data at the current $n\le25$ bound. The DP merges states sharing a prefix and selection count, giving better asymptotic time and making it preferred. The [test plan](tests/plan.json) covers negative values, zero/all selections, middle selection counts and extreme scores. See the [measurements](../../../docs/评测环境与性能.md).
