# Hagen Farm Editorial

**Two methods: the problem setter’s subtree expectation DP, and edge-probability summation derived by Codex (GPT-6).** Both take $O(n^2)$ time. The edge method reduces runtime space from $O(n^2)$ to $O(n)$ , so it is used in `std.cpp` . Subtree DP retains intermediate results by selected-set size. Both methods, their proofs, and their uses are described below; the choice does not rely on unmeasured runtime comparisons.

## 1. The shortest closed walk

The minimal subtree connecting all apple vertices is unique. A closed walk using one of its edges must cross that edge and return, so it traverses every such edge at least twice. A traversal of this subtree attains the bound.

Thus the distance is twice its total edge length. A single apple contributes zero. By linearity of expectation, sum the contribution of each edge.

## 2. Edge-inclusion probability for a fixed generation subtree

Consider the edge to a child $v$ whose subtree size is $t$ . It can be used only if the randomly chosen generation root $u$ is a strict ancestor of $v$ . Write $s$ for the size of $u$’s subtree. The edge separates this range into parts of sizes $t$ and $s-t$ .

With a fixed number $k$ of apples, the edge is excluded exactly when all apples lie on one side. These events are disjoint for $k\ge1$ , so the inclusion probability is

$$1-\frac{\binom tk+\binom{s-t}k}{\binom sk}$$

Treat a binomial coefficient as zero if its lower index exceeds the available size. Average over uniform $k=1,\ldots,s$ . For $0\le t<s$ :

$$\sum_{k=1}^{s}\frac{\binom tk}{\binom sk}=\frac{t}{s-t+1}$$

To prove this, include the $k=0$ term and use

$$\frac{\binom tk}{\binom sk}=\frac{\binom{s-k}{s-t}}{\binom st}$$

The binomial summation identity gives $(s+1)/(s-t+1)$ ; subtract one to obtain the result.

Consequently the edge-inclusion probability for this generation root is

$$p(s,t)=1-\frac1s\left(\frac{t}{s-t+1}+\frac{s-t}{t+1}\right)$$

If the edge length is $w_v$ , the answer is

$$E=\frac2n\sum_{v\ne1}w_v\sum_{u\text{ is a strict ancestor of }v}p(\mathrm{size}(u),\mathrm{size}(v))$$

## 3. Edge-based implementation and proof

Use explicit traversals to compute parents, edge weights, and subtree sizes. Precompute modular inverses of $1,\ldots,n+1$ . For each nonroot vertex, walk through its ancestors, evaluate the probability, and multiply the accumulated contribution by the edge length, two, and the inverse of $n$ .

The probability formula includes all three random choices: root, apple count, and uniform subset. An edge is used precisely when it belongs to the minimal connecting subtree. Linearity of expectation does not require different edges to be independent, so this sum is exactly the required expectation.

There are at most $n(n-1)/2$ ancestor-descendant pairs. Time is $O(n^2)$ and space is $O(n)$ . All denominators lie between $1$ and $n+1$ , below the prime $P$ . Zero-length edges and $n=1$ require no special adjustment.

## 4. Problem setter’s solution: subtree expectation DP

Let $s_v$ be the subtree size at $v$ . Define $D_v(k)$ as the expected total length of edges connecting $v$ to a uniformly selected size-$k$ subset of its subtree, with $D_v(0)=0$ . This deliberately forces the paths to reach $v$ ; unnecessary connections will be subtracted later.

Initially the processed part consists only of $v$ , has size one, and both states are zero. Merge a child subtree $c$ of size $t$ into a processed part of size $s$ . Conditional on selecting $k$ vertices in total, the probability that $j$ come from $c$ is

$$\frac{\binom tj\binom s{k-j}}{\binom{s+t}k}$$

The corresponding expected edge length is $D_{\mathrm{old}}(k-j)+D_c(j)+w_c[j>0]$ . Sum this expression with the above weights over valid $j$ . Conditional on the counts, choices within each part remain uniform, proving the transition.

After computing every $D_v(k)$ , define

$$L_v(k)=\binom{s_v}kD_v(k)-\sum_{c\text{ is a child of }v}\binom{s_c}k\bigl(D_c(k)+w_c\bigr)$$

Only include terms with $k\le s_c$ . This is the total minimal-subtree length over size-$k$ subsets whose lowest common ancestor is exactly $v$ . If all selected vertices lie in one child subtree, the subtraction removes their entire forced connection to $v$ . Every other subset has a minimal connecting subtree through $v$ .

Such a subset can be generated from any ancestor subtree containing $v$ . During a root-to-vertex traversal, maintain

$$W_v(k)=\sum_{u\text{ is an ancestor of }v\text{ or }u=v}\frac1{s_u\binom{s_u}k}$$

Include only terms with $k\le s_u$ . Add or remove a vertex’s contribution on entry or exit. The final result is

$$E=\frac2n\sum_v\sum_{k=1}^{s_v}L_v(k)W_v(k)$$

Every nonempty apple set has a unique lowest common ancestor, so it is counted once. Precompute binomial coefficients and their inverses. Nontrivial merge-state pairs can be charged to the first merge joining a pair of vertices, for $O(n^2)$ total work; the remaining state scans also total at most $O(n^2)$ . Both time and table space are $O(n^2)$ .

These DP states are useful if a variant asks about a particular subtree and a fixed selected count $k$ . For the single expectation under the stated distribution, edge probabilities avoid the two-dimensional tables.

## Data and validation

`tests/generate.py` covers chains, stars, balanced trees, brooms, zero-length edges, and random trees. The independent small-instance oracle enumerates the generation root, apple count, and every subset, then directly finds the connecting edges. See [environment and measurements](../../../docs/评测环境与性能.md).
