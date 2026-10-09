# Solution

Contributions: the problem setter's solution supplies repeated-pivot adjacency queries, binary search for neighbors, and growth from both ends. Codex (GPT-6) supplies the endpoint search order and 741-query bound, protocol, implementation, local judge, and verification.

## Detecting adjacency with substrings

For pivot $u$ and distinct candidates $c_1,\ldots,c_s$ , query

$$[u,c_1,u,c_2,\ldots,u,c_s,u].$$

Its length is $2s+1$ , so use $s\le49$ . The reply is at least 2 exactly when some candidate is adjacent to $u$ in the hidden permutation. Every consecutive pair in the query includes $u$ , preventing false matches between unrelated candidates. A reply of 3 is possible; only the comparison with 2 matters.

The setter's approach uses these tests and binary search, identifies and orients neighbors on both sides of a pivot, and extends both ends through unused labels. The implementation retains this adjacency principle and grows right first, then left, allowing at most one unsuccessful endpoint search.

## Initialization and growth

Answer directly for $n=1$ . Otherwise search for one neighbor of 1 among all other labels. A neighbor is guaranteed to exist. Test at most 49 candidates per binary-search step, then query `[1,v]` to orient the chosen neighbor. This gives a correctly oriented contiguous fragment.

When extending right endpoint $u$ , its left neighbor is already used. Only its right neighbor can be an adjacent unused candidate. For a subset, query

$$[u,c_1,u,c_2,\ldots,u,c_s],\qquad s\le50.$$

A reply at least 2 means the right neighbor is in that subset. To extend left, query $[c_1,u,c_2,u,\ldots,c_s,u]$ instead.

Keep the possibility that no neighbor exists. With $U$ candidates and existence unknown, test $\min(50,\lfloor(U+1)/2\rfloor)$ candidates. A positive reply eliminates the absent outcome and permits ordinary binary search. A negative reply removes the tested subset. An empty set identifies the permutation endpoint.

Grow right until the first absent neighbor, then switch permanently to the left. Every remaining label lies on that side, so no later search fails. A lone candidate still requires a query when its existence has not been established.

## Correctness and query bound

Initialization creates a correct contiguous fragment. Each successful search finds its immediate predecessor or successor, preserving that invariant. A failed right search means the fragment reaches the permutation's right endpoint. All unused labels must then extend its left side. The final fragment contains every label and is the hidden permutation.

Initialization uses at most eight neighbor tests and one orientation test. Every successful extension consumes one unused label, with $U$ decreasing from at most 118 to 1. For $U\le100$ , treating absence as one extra outcome gives at most $\lceil\log_2(U+1)\rceil$ queries. For $100<U\le118$ , the first test takes 50 candidates; at most 69 outcomes remain, requiring at most seven more queries. Conservatively charge one extra query. The single unsuccessful search costs at most eight. Thus

$$Q\le9+\sum_{U=1}^{118}\left(\lceil\log_2(U+1)\rceil+[U>100]\right)+8=741<800.$$

Every query has length at most 100. This is a worst-case bound, independent of random permutations or measured averages.

## Implementation and testing

[std.cpp](std.cpp) is the submission; [solver.hpp](solver.hpp) contains the algorithm. Flush every query and exit immediately on $-1$ or end of input. The program receives only $n$ and judge replies.

[judge.py](judge.py) holds the hidden permutation and communicates through pipes. It checks syntax, query count, the final answer, successful exit, and extra output. [simulate.cpp](simulate.cpp) is an offline test harness for the shared algorithm. It reads the hidden permutation and is not an interactive submission. See the [testing guide](tests/README.md).

For $Q$ queries and maximum query length $L$ , candidate maintenance and query construction take $O(n^2+QL)$ time and $O(n+L)$ auxiliary space. Measurements run the actual protocol. Wall time includes the Python judge and pipes; memory measures only the submission process.

## Measurements

Each formal input has five timing runs and a separate peak-memory run. The standard program's slowest median is 0.074435 seconds and peak memory is 5.28 MiB. Twice the median, rounded up to 0.5 seconds, gives a 0.5-second limit. See the [environment](../../../docs/评测环境与性能.md) and [individual measurements](../../../docs/benchmark-R34.json). Recalibrate in other environments.
