# Spice Routes — Solution

> Peer method: three-state tree DP. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.


## Compute the probability of having no trading route

After failed edges are removed, no connected component may contain both a low-price and a high-price node. Otherwise a trading route exists. Compute the probability of this complement event, then subtract it from one.

Root the tree anywhere. For each subtree, require all components already separated from its root to be valid, and record the marks in the component containing that root:

- State $0$ : neither category.
- State $1$ : low-price nodes only.
- State $2$ : high-price nodes only.

Discard state $3$ , which contains both categories. Let $dp_u[s]$ be the probability of a valid subtree with root-component state $s$ . Initialize the single node $u$ with probability one in its own state. If it has both marks, all three probabilities start at zero.

## Merge across an edge

Suppose the edge to child $v$ fails with probability $z$ . For current state $a$ and child state $b$ , a failed edge keeps the components separate and contributes

$$next[a]\mathrel{+}=dp_u[a]dp_v[b]z$$

If the edge survives, the merged state is the bitwise OR $a\mathbin{|}b$ . If it is not $3$ , add

$$next[a\mathbin{|}b]\mathrel{+}=dp_u[a]dp_v[b](1-z)$$

The edge cases are disjoint and exhaustive. Child subtrees and connecting edges are independent, so their probabilities multiply. Merge children one at a time. The final answer is

$$1-dp_{root}[0]-dp_{root}[1]-dp_{root}[2]$$

Inductively, retained states account exactly for configurations whose completed components are valid. At the full root there is no external connection left, proving the complement calculation. The algorithm does not require the special limit of two high-price nodes, although the statement retains that input range.

## Modular arithmetic and complexity

Let $P=10^9+7$ and let $U$ be the largest input denominator. Precompute inverses from $1$ to $U$ with

$$inv[1]=1,\qquad inv[i]=-(P\mathbin{//}i)\,inv[P\bmod i]\pmod P$$

This follows from $P=(P\mathbin{//}i)i+(P\bmod i)$ . Every $i<P$ , so all inverses exist. Represent a failure probability by $q_i inv[p_i]\bmod P$ , and normalize subtractions to $[0,P-1]$ .

There are constantly many states per edge, giving $O(n+U)$ time and space. An explicit parent-first traversal, processed backward, avoids recursion on long chains. Repeated IDs only set a mark once. An empty category gives probability zero; overlapping categories give probability one.

The independent oracle enumerates all surviving/failed edge configurations of small trees, checks components directly, and multiplies the exact modular edge probabilities for each configuration.

## Program and reproduction

See [alternative.cpp](alternative.cpp) for this C++17 implementation. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
