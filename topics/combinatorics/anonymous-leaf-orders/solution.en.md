# Ordered Tree Construction with Anonymous Leaves — Solution

The setter suggested inclusion-exclusion and Stirling numbers of the second kind. Codex (GPT-6) supplied correct surjection counting, boundary cases, proofs, implementation, and verification.

## Leaves in a Prüfer sequence

For a labeled tree with $n\ge3$ , repeatedly remove its smallest labeled leaf and record its neighbor. This gives a Prüfer sequence of length $n-2$ . Conversely, choose the smallest label absent from the remaining sequence as the next leaf to reconstruct the tree uniquely. Thus all length-$n-2$ label sequences correspond bijectively to labeled trees, and label $v$ occurs $\deg(v)-1$ times.

Exactly $m$ leaves means exactly $t=n-m$ distinct labels appear, each at least once. Choose the leaf set in $\binom nm$ ways. For the remaining fixed set of $t$ labels, the number of length-$L=n-2$ surjective sequences is

$$U(L,t)=\sum_{j=0}^{t}(-1)^j\binom tj(t-j)^L.$$

Forbidding a chosen set of $j$ labels leaves $(t-j)^L$ sequences. Inclusion-exclusion over missing-label events retains exactly the sequences using every allowed label.

The $n-1$ distinct tree edges may be inserted in any order. Every subset of tree edges is acyclic, so intermediate stages impose no further restriction. The number of labeled construction records is

$$B(n,m)=\binom nm U(n-2,n-m)(n-1)!.$$

## Why subtracting adjacent terms fails

The expression $\binom nm(n-m)^{n-2}$ counts pairs consisting of a tree and a selected set of $m$ leaves. A tree with $\ell$ actual leaves is counted $\binom\ell m$ times. This is not the count of trees with at least $m$ leaves, so subtracting adjacent terms leaves incorrect multiplicities.

For $n=4,m=2$ , that subtraction followed by multiplication by $3!$ gives $120$ . Actual two-leaf trees are the $4!/2=12$ undirected paths, each with $3!=6$ orders, giving $72$ . The incorrect subtraction additionally counts stars. Full inclusion-exclusion or surjection counting is necessary.

## Implementation and Complexity

The modulus $p=998244353$ is prime, and all factorial arguments are below $p$ . Precompute factorials and inverse factorials, using one modular exponentiation for the largest factorial's inverse and a downward pass for the rest. Binomial coefficients then take constant time. Compute each power by binary exponentiation and normalize alternating terms to nonnegative residues.

Handle $n\le2$ directly from the statement. For $n\ge3$ , only $2\le m<n$ is possible. Feasible large cases take $O(n+(n-m)\log n)$ time and $O(n)$ space. Independent small checks use the Stirling recurrence $S(L,t)=tS(L-1,t)+S(L-1,t-1)$ and actual tree/edge-order enumeration. This quadratic DP is not recommended for the full range.

## Forget leaf names while preserving edge order

For a fixed nonleaf label set, there are $m!$ permutations of leaf names. When $n\ge3$ , each leaf is adjacent to a nonleaf. If a renaming preserves the entire insertion record, each leaf's unique edge must remain at the same insertion step. Its nonleaf neighbor cannot be renamed, forcing the leaf itself to remain fixed.

Only the identity renaming fixes a record. Each equivalence class therefore contains exactly $m!$ labeled records, giving

$$B(n,m)\cdot(m!)^{-1}\pmod p.$$

Different nonleaf label sets remain distinct, so the factor $\binom nm$ must remain. This is not a count of trees with every vertex unlabeled.

For $n=2,m=2$ , swapping both leaves preserves the sole undirected edge, so the free-action argument fails; return one directly. Handle $n=0,1$ directly too. Outside these boundaries, the orbit-size argument and labeled-record formula prove the answer, with unchanged complexity. See [std.cpp](std.cpp).

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
