# Upgrade Toolkit — Solution

## Comparing solutions

Both implementations of the problem setter’s solution represent type $i$ by the factor $1+x+\cdots+x^{c_i}$ , where $c_i$ is its quantity cap, and multiply factors using ordinary nested-loop convolution. Each term chooses a legal quantity, so expanding the product enumerates exactly all combinations. This is the common counting proof.

Let $S_i=\sum_{j\le i}c_j$ and $S=S_n$ . Direct convolution takes $O(\sum_i(S_{i-1}+1)(c_i+1))$ time; storing all stages as the problem setter’s implementation does costs $O(n(S+1))$ space. The implementation used by Codex (GPT-6) observes that each new coefficient is a consecutive sum of old coefficients and maintains it with a sliding window. Time becomes $O(n(S+1))$ and rolling storage is $O(S+1)$ . Rolling arrays could also be applied separately to the problem setter’s convolution. The time improvement comes from window sums; the counting model is unchanged.

## Count by type

Type $i$ allows quantities from $0$ through $C_i$ , so the answers are the coefficients of

$$\prod_{i=1}^n(1+x+\cdots+x^{C_i})$$

Let $f_j$ count plans collecting $j$ toolkits from the processed types, initially $f_0=1$ . Adding a type with capacity $C_i$ gives

$$g_j=\sum_{k=0}^{C_i}f_{j-k}$$

Treat out-of-range coefficients as $0$ . Every plan uniquely splits into a plan for the previous types and a quantity for the new type, so the recurrence counts every plan exactly once.

## Sliding window

As $j$ increases, add $f_j$ and remove $f_{j-C_i-1}$ from the window sum. Maintaining that sum modulo $100000007$ makes each coefficient take constant time. Store the current and next arrays and swap them after each type.

A zero-capacity type still occupies its original ID; do not renumber subsequent types. When $n=0$ , retain the initial array and print $1$ .

Since $C_i\le\lfloor1000/i\rfloor$ , the total capacity satisfies

$$S\le\sum_{i=1}^{1000}\left\lfloor\frac{1000}{i}\right\rfloor=7069$$

Time complexity is $O(n(S+1))$ and space complexity is $O(S+1)$ . Each window update adds or removes one reduced coefficient, so ordinary integer arithmetic with immediate normalization suffices.
