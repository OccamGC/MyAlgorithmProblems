# Recognizing a Lattice of Symbols: Solution

## Method and contributions

The reference program preserves the setter's reflexivity, transitivity, and pairwise join-and-meet checks. Codex (GPT-6) organized the C++17 implementation, reused the bound check through matrix transposition, and supplied the alias and candidate-scan proofs. See [std.cpp](std.cpp). The setter's other criterion is explained in [All joins and a minimum](solution-alternative.en.md).

Do not demand antisymmetry of the symbol relation: different symbols may represent one element. First check $A_{i,i}=1$ and, for every triple, that $A_{i,j}=A_{j,k}=1$ implies $A_{i,k}=1$ . These are reflexivity and transitivity.

## Why explicit symbol merging is unnecessary

For a relation satisfying these checks, define $i\sim j$ exactly when $A_{i,j}=A_{j,i}=1$ . This is an equivalence relation. Transitivity gives equivalent symbols identical incoming and outgoing relations to every other symbol. The induced relation on equivalence classes is therefore well-defined and antisymmetric, making it a partial order.

Any valid representation must map mutually related symbols to the same element; symbols mapped to one element must also be mutually related. Thus these classes are exactly the required elements. Bounds can be checked directly in the symbol matrix without constructing the quotient. A join may have several representing symbols without violating uniqueness as an element.

## Finding a join for one pair

Fix $i,j$ and scan all common upper bounds $k$ , characterized by $A_{i,k}=A_{j,k}=1$ . Keep a candidate $c$ . Use the first bound as candidate; subsequently replace $c$ by $k$ when $A_{k,c}=1$ .

If a join $u$ exists, it is at most the current candidate when encountered, so it becomes the candidate. Any later common upper bound that replaces it must be equivalent to it. The final candidate therefore represents the join.

Without a join, the scan may still leave a candidate. A second scan is essential: verify $A_{c,k}=1$ for every common upper bound $k$ . Reject if there is no common upper bound or this test fails. If it passes, the candidate is itself a common upper bound and is below every other one, exactly satisfying the definition.

Meets are dual. Transpose the matrix and use the same all-joins function to check all meets of the original order. Print `Y` only when both kinds of bounds exist.

## Complexity

Reflexivity takes $O(n)$ and transitivity $O(n^3)$ . Each pair uses two linear scans for its join and likewise for its meet. Total time is $O(n^3)$ with $O(n^2)$ space; over multiple tests the time is $O(T+\sum n^3)$ . An all-one matrix correctly represents a one-element lattice.
