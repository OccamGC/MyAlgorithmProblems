# The Queen of Hearts' Card Soldiers: Solution

## Method and contributions

The reference program preserves the problem setter's greedy chain-cover algorithm. Codex (GPT-6) organized the C++17 implementation and supplied the strictness, duplicate-attribute, and optimality arguments. See [std.cpp](std.cpp) and the [Fenwick-tree alternative](solution-alternative.en.md).

Sort soldiers by increasing attack, breaking ties by increasing armor. A valid lineup corresponds exactly to a strictly decreasing subsequence of armor values. Soldiers with different attacks must have armor in the opposite order. Two soldiers with equal attacks cannot coexist, and their sorted segment cannot supply a decreasing pair either.

The answer is therefore the longest strictly decreasing subsequence length. The setter partitions the sequence into as few nondecreasing chains as possible. Keep their tails in increasing order in `Chains` . For an armor value $x$ , replace the largest tail at most $x$ by $x$ . If no such tail exists, prepend $x$ . Output the number of chains. The predecessor of `upper_bound(x)` is the required tail.

## Correctness

Each chain is nondecreasing, so a strictly decreasing subsequence uses at most one position from each chain. The chain count is an upper bound on the answer.

Reverse the increasing tail array to obtain a strictly decreasing array $D$ . Its invariant is that $D_k$ is the largest possible last value of a strictly decreasing subsequence of length $k$ in the processed prefix. The empty prefix satisfies this invariant. For $x$ , the algorithm replaces the first entry with $D_k\le x$ , or appends if there is none.

For $k>1$ , the preceding entry satisfies $D_{k-1}>x$ , so its subsequence can be extended by $x$ . For $k=1$ , choose $x$ alone. Replacing the old $D_k\le x$ improves or preserves that maximum last value. Shorter lengths already have larger last values. A longer subsequence ending in $x$ would, after removing $x$ , give a subsequence of length at least $k$ ending above $x$ , contradicting the old $D_k\le x$ . The append case follows the same argument. Thus the invariant is preserved.

The array length is the longest strictly decreasing subsequence length, hence the optimum lineup size. It equals the chain count, proving the output correct. Equal armor values replace tails instead of increasing the answer. An empty input gives zero.

## Complexity and implementation

Sorting and binary searches take $O(n\log(n+1))$ time and $O(n)$ space; an empty input takes constant work. A `deque` supports random access, so binary search is logarithmic and prepending is constant time. Both attributes fit signed 32-bit integers.

The reference program's largest measured median was about $0.296$ seconds, giving a $1$-second estimated limit. The Fenwick method has the same asymptotic complexity and more arrays; its largest median was about $0.489$ seconds, with close to twofold headroom. These measurements describe the tested environment and data.
