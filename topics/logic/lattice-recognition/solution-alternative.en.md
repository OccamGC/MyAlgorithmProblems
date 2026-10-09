# Recognizing a Lattice of Symbols: Alternative Solution

## All joins and a minimum

This criterion comes from the problem setter. Codex (GPT-6) organized the C++17 program and supplied the finite-lattice proof. See [alternative.cpp](alternative.cpp); the [main solution](solution.en.md) explains symbol classes and the join scan.

Check reflexivity, transitivity, and a join for every pair of symbols. Then find an all-one row, representing an element at most every other element. Print `Y` exactly when these conditions hold; no pairwise meet scan is needed.

In a nonempty finite lattice, successively taking the meet of all elements gives a global minimum. Binary joins also exist, so the conditions are necessary.

Conversely, work in the finite partial order of symbol classes and consider any $x,y$ . Their common lower bounds form a nonempty set because it contains the minimum. Successively join all these lower bounds. Each intermediate result remains at most both $x$ and $y$ : they are common upper bounds of the elements being joined, and a join is below every common upper bound. The final result is a common lower bound above every common lower bound, hence the meet. Thus every meet exists and the order is a lattice. Finiteness and the nonempty lower-bound set are both essential here.

Join checking takes $O(n^3)$ and finding an all-one row takes $O(n^2)$ . Total time is $O(n^3)$ with $O(n^2)$ space. Removing the dual pairwise scan reduces the work and was faster in the measurements, without changing the asymptotic bound.
