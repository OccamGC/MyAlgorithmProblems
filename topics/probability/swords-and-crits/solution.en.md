# Quotient-State DP and Ordered Meet-in-the-Middle

Problem setter's solution: combine quotient-state DP and ordered meet-in-the-middle according to the parameters. Codex (GPT-6): application and derivation of both methods, the multiple-query specification, modular probability implementation, overflow handling, and verification data. Quotient decomposition and meet-in-the-middle are established techniques, not claimed as original inventions.

The preferred program is the self-contained [std.cpp](std.cpp). A [four-list streaming solution](solution-alternative-streaming.en.md) and its [program](alternative-streaming.cpp) trade time for memory.

## 1. Probabilities and preprocessing

Let $D=10^6$ , $P=998244353$ , and $a_i=p_iD^{-1}\bmod P$ . Use modular arithmetic for probabilities and exact integer arithmetic for multipliers; the two must remain separate.

- Remove swords with $p_i=0$ or $m_i=1$ .
- A sword with $p_i=D$ always contributes multiplier $m_i$ . Remove it and replace every threshold by $\lceil K_j/m_i\rceil$ .
- A threshold of $1$ always has answer $1$ .

The deterministic reduction requires ceiling division. For example, after removing a guaranteed multiplier of $3$ , a threshold of $5$ requires the remaining multiplier to be at least $2$ .

Below, $n$ denotes the remaining number of swords. Each remaining sword satisfies $0<p_i<D$ , so its failure probability and its modular inverse are defined. Preprocessing does not increase any threshold or the number of swords. An empty collection still has multiplier $1$ . If no swords remain, answer directly according to whether the adjusted threshold equals $1$ without building a DP or enumeration list.

## 2. Small thresholds: cumulative-probability DP

For one threshold $K>1$ , set $T=K-1$ . Let $F_i(t)$ be the probability that the first $i$ swords produce a multiplier at most the integer $t$ . Splitting on whether sword $i$ triggers gives:

$$
F_i(t)=(1-a_i)F_{i-1}(t)+a_iF_{i-1}(\lfloor t/m_i\rfloor)
$$

Initially, $F_0(0)=0$ and $F_0(t)=1$ for $t\ge1$ . The answer is $1-F_n(T)$ , with subtraction also performed modulo $P$ .

Maintaining every threshold takes $O(nK)$ time. Starting from $T$ , however, every required threshold belongs to:

$$
\mathcal Q_T=\{0\}\cup\{\lfloor T/d\rfloor:1\le d\le T\}
$$

The closure property follows from:

$$
\left\lfloor\frac{\lfloor T/d\rfloor}{m_i}\right\rfloor=\left\lfloor\frac{T}{dm_i}\right\rfloor
$$

For $d\le\sqrt T$ , there are only $O(\sqrt T)$ denominators. For $d>\sqrt T$ , the quotient is smaller than $\sqrt T$ . Hence there are only $O(\sqrt K)$ states, and every transition stays within the set.

### Array indexing without hashing or binary search

Let $s=\lfloor\sqrt T\rfloor$ and $r=\lfloor T/(s+1)\rfloor$ . Store $0,1,\ldots,s$ in increasing order, followed by the quotients for denominators decreasing from $r$ to $1$ . The index of a nonzero state is:

$$
\operatorname{index}(t)=
\begin{cases}
t,&t\le s,\\
s+r-\lfloor T/t\rfloor+1,&t>s
\end{cases}
$$

Each transition finds its destination in constant time. Process thresholds in decreasing order for each sword, so smaller thresholds retain their previous-layer values. Only one probability array is needed.

Correctness follows by induction. The initial array represents the empty collection. Each transition adds the probabilities of the two mutually exclusive triggering outcomes, and the state set includes every dependency. Thus the final array represents the required cumulative probabilities.

Processing all queries separately takes $O(n\sum_j\sqrt{K_j})$ time and $O(\sqrt{K_{\max}})$ extra state space, where $K_{\max}=\max_jK_j$ .

## 3. Few swords: ordered meet-in-the-middle

Let $M=\max_jK_j$ . Compute the probability of falling below the threshold, then subtract it from $1$ . Split the swords into two nearly equal groups and enumerate each group's triggering subsets, multipliers, and probability weights.

### A common probability factor

Extract the probability that no sword triggers:

$$
C=\prod_i(1-a_i),\qquad w_i=\frac{a_i}{1-a_i}=\frac{p_i}{D-p_i}\pmod P
$$

A triggering set $S$ has probability $C\prod_{i\in S}w_i$ . During construction, non-triggering keeps the weight unchanged, while triggering multiplies it by $w_i$ . Apply $C$ after combining both halves. Removing certain triggers beforehand makes every denominator invertible.

### Linear total construction time

Maintain a list sorted by multiplier. Inserting a sword combines the existing list and the list with each multiplier multiplied by $m_i$ . Both are sorted, so merge them in linear time.

Keep only products smaller than $M$ . All multipliers are at least $1$ , so a partial product reaching $M$ can never contribute to any query's failure event. Before merging, only states whose multiplier is at most $\lfloor(M-1)/m_i\rfloor$ may trigger. This both prunes irrelevant states and guarantees that every multiplication actually performed produces a value smaller than $M$ .

For a group of $h$ swords, list lengths are at most $1,2,4,\ldots,2^h$ , totaling $O(2^h)$ merge work. The implementation performs just one binary search per level to locate the eligible triggering prefix. Its total $O(h^2)$ cost is also bounded by $O(2^h)$ . There is no binary search for each state and no comparison sort after enumeration.

Induction shows that every retained state represents a triggering subset, and every subset with product below $M$ is retained. Different subsets with equal products may remain separate; all their weights count.

### Prefix weights and two pointers

Write the lists as $(x_i,u_i)$ and $(y_j,v_j)$ . The failure probability for a query $K$ is:

$$
C\sum_i u_i\sum_{j:x_iy_j<K}v_j\pmod P
$$

For positive integers:

$$
x_iy_j<K\iff y_j\le\left\lfloor\frac{K-1}{x_i}\right\rfloor
$$

Precompute weight prefix sums for both lists, shared by every query. Visit left multipliers $x_i<K$ in increasing order. Move a pointer backward from the right list's end until the retained prefix satisfies this inequality. The right bound only decreases as $x_i$ increases, so each right entry is passed at most once. Read its prefix weight to compute the contribution, then complement the final failure probability.

The reference settles consecutive left entries sharing the same right prefix weight as a block. With left prefix weights $U_i$ , the weight of indices $[l,r]$ is $U_r-U_{l-1}$ . This uses linearity of modular addition without changing any integer comparison. Probability products are reduced modulo the prime after every eight terms to reduce constants; reducing after each term has the same complexity.

The two halves are independent, and every failing pair is included exactly once. Thus the algorithm is correct. Let $N=2^{\lceil n/2\rceil}$ . Construction and prefix sums take $O(N)$ time, each query takes $O(N)$ time, and all queries take $O(qN)$ . Computing probability inverses additionally costs $O(n\log P)$ time. Enumeration space is $O(N)$ .

## 4. Signed 64-bit arithmetic throughout

The input satisfies $K_j\le10^{18}<2^{63}-1$ . The algorithm never computes the full product of all swords or directly multiplies the two half-products during a query.

- During construction, check $x\le\lfloor(M-1)/m\rfloor$ before evaluating $xm$ . Its result is then strictly below $M$ .
- During a query, compare $y\le\lfloor(K-1)/x\rfloor$ instead of evaluating $xy<K$ .
- Write ceiling division for a certain trigger as $(K-1)/m+1$ , avoiding $K+m-1$ .
- Compute integer square roots by testing bits with division comparisons, without floating-point operations.
- A probability product is below $(P-1)^2<10^{18}$ . A DP transition adds two such terms, staying below $2\cdot10^{18}$ and within `int64_t` .

The reduced carry plus eight probability products satisfies:

$$
(P-1)+8(P-1)^2<2^{63}-1
$$

Consequently, reducing after every eight terms is also safe. No extended integer type, big-integer implementation, logarithmic comparison, or numerical tolerance is needed.

## 5. Choosing the algorithm and total complexity

Compare the estimated quotient-DP work with enumeration and query work, then choose the smaller method. More than $44$ swords guarantees small thresholds, so use DP in that case.

Including modular inverses, the time bound for one test case is:

$$
O\left(n\log P+\min\left\{n\sum_j\sqrt{K_j},\ (q+1)2^{\lceil n/2\rceil}\right\}\right)
$$

Here $n,K_j$ are the parameters after preprocessing. Reading the original input and adjusting thresholds for certain triggers take additional $O(n_{\mathrm{original}}q)$ time. DP uses $O(n+q+\sqrt{K_{\max}})$ space; meet-in-the-middle uses $O(n+q+2^{\lceil n/2\rceil})$ space. Integer width is bounded, so these bounds count fixed-width integer operations.

Enumeration alone cannot handle the large sword counts, and quotient DP alone cannot handle large thresholds. Comparison sorting costs $O((n+q)N)$ ; binary searching for each state costs $O(qnN)$ . Repeated large constructions with few queries constrain sorting. Smaller enumerations with many queries constrain binary search.

## 6. Other approaches and verification

The [four-list streaming approach](solution-alternative-streaming.en.md) reduces enumeration space to $O(2^{\lceil n/4\rceil})$ but incurs heap costs and does not pass the full time limit. It is useful when memory is tighter and more time is available. Its complete bilingual explanation and program are provided.

[std.cpp](std.cpp) is a complete C++17 program that can be compiled or submitted alone and includes only standard-library headers. Auxiliary programs define `SWORDS_LIBRARY_ONLY` to reuse its functions; ordinary compilation of the reference does not require this macro.

Verification covers independent exhaustive enumeration, forced execution of both branches, integer and probability boundaries, samples, and input validation. Sorting and binary-search witnesses share the same pruning, prefix sums, weight-block aggregation, and batched modular products. See the [test notes](tests/README.md) and [measurement record](../../../docs/benchmark-swords-and-crits.json) for five-run timings and source/input hashes. Finite tests describe specific implementations rather than proving lower bounds for every program in an asymptotic class. Recalibrate on the target judge.

## 7. Two correct implementations that exceed the time limit

Both programs below retain quotient DP for small thresholds and change only the meet-in-the-middle branch. Their answers are correct, but the supplied implementations do not pass the full time limit. Again let $N=2^{\lceil n/2\rceil}$ . The bounds below omit the shared input preprocessing and $O(n\log P)$ work for probability inverses. All three implementations use $O(n+q+N)$ space.

### 7.1 Unsorted enumeration followed by comparison sorting

The [sorting program](tests/slow-sort.cpp) splits the swords into two halves. When adding a sword, it visits the existing states and appends each eligible triggered state with its updated product and weight. List lengths form a geometric sequence, so enumeration itself still takes only $O(N)$ time. However, the arrays are not kept sorted. Both must be sorted with `std::sort` before computing prefix weights and answering queries with two pointers.

The program enumerates the same triggering subsets as the reference and uses the same pruning before multiplication. Sorting changes only their order, so the subsequent probability calculation remains correct. The extra work comes from comparison sorting: each half has at most $N$ states, requiring $O(N\log N)=O(nN)$ sorting time. Each query still takes $O(N)$ time after construction, giving total time:

$$
O(N\log N+qN)=O((n+q)N)
$$

Sorting is paid only once per sword collection and can be amortized over many queries on that collection. Consequently, formal test file 08 contains five independent collections with $n=44,q=1$ . Each requires another large construction but answers only one query. The multipliers are distinct integers, preventing direct grouping by equal sword multipliers. On the reference environment, this program's median over five runs on that file is approximately **2.932 seconds**, exceeding the **2-second** limit.

The reference instead merges two already sorted lists whenever it adds a sword. This processes only $O(N)$ states in total, eliminating the $\log N$ factor during construction.

### 7.2 An independent binary search for every left state

The [binary-search program](tests/slow-binary.cpp) already uses the reference's ordered merge construction and precomputes weight prefix sums. For each query, it computes the following bound separately for each left state $(x,u)$ :

$$
L=\left\lfloor\frac{K-1}{x}\right\rfloor
$$

It then calls `std::upper_bound` on the entire right list to find the first multiplier greater than $L$ . The preceding prefix contains exactly the right states satisfying $xy<K$ . Multiplying that prefix's weight by $u$ gives the current contribution. Summing these contributions and taking the complement still produces the correct answer.

The problem is that each left state starts another $O(\log N)$ search. One query takes $O(N\log N)=O(nN)$ time, and construction plus all queries take:

$$
O(N+qN\log N)=O(qnN)
$$

Here the extra factor is paid on every query. Formal test file 09 therefore uses $n=28,q=5600$ : the enumeration lists are smaller, but the same lists must answer many queries. All multipliers are distinct primes, so distinct subsets also have distinct products. Merging duplicate products cannot substantially shorten the lists. On the reference environment, this program's median over five runs on that file is approximately **2.627 seconds**, exceeding the **2-second** limit.

The reference uses the fact that $L$ never increases as the left multiplier increases. Its right pointer moves only toward the beginning of the prefix. Across one query, all states are scanned only $O(N)$ times in total; independent binary searches do not reuse this monotonicity.

### 7.3 Complexity comparison

| Meet-in-the-middle implementation | Construction | One query | Construction and all queries |
| --- | --- | --- | --- |
| Ordered merges and two pointers (reference) | $O(N)$ | $O(N)$ | $O((q+1)N)$ |
| Unsorted enumeration, comparison sorting, and two pointers | $O(nN)$ | $O(N)$ | $O((n+q)N)$ |
| Ordered merges and a binary search per state | $O(N)$ | $O(nN)$ | $O(qnN)$ |

When $q=1$ , both slower implementations take $O(n2^{\lceil n/2\rceil})$ time, but their bottlenecks differ with multiple queries. Repeated large constructions with few queries constrain comparison sorting; smaller lists with many queries constrain independent binary searches. These two families separately test the optimizations that make construction and querying linear.
