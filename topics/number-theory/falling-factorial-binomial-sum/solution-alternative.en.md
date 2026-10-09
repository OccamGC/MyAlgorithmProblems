# A Certain Unscientific Sum of Falling Factorials and Binomial Coefficients — Constant Space: Direct Products and Wilson Complements

Codex (GPT-6): combines the falling-factorial identity with Wilson's theorem in a [constant-space program](alternative.cpp) requiring no checkpoint table. This has a clear storage advantage, but its worst-case time is higher and full stress inputs exceed the reference limit.

Use $n^{\underline{k}}2^{n-k}$ , proved in the [main solution](solution.en.md). Return zero when $k>n$ . Otherwise, multiplying $n-k+1,\ldots,n$ directly takes $k$ products.

Wilson's theorem gives $(P-1)!\equiv-1\pmod P$ . Partition the factorial into three disjoint intervals:

$$
\left(\prod_{i=n-k+1}^{n}i\right)
\left(\prod_{i=1}^{n-k}i\right)
\left(\prod_{i=n+1}^{P-1}i\right)\equiv-1\pmod P
$$

The desired falling factorial is therefore the negative inverse of the product over the other two intervals. Those intervals contain $P-1-k$ factors in total. Every factor belongs to $[1,P-1]$ , so the inverse exists. Compute whichever side is shorter, then multiply by $2^{n-k}$ .

Time is $O(\min(k,P-1-k)+\log P)$ and extra space is $O(1)$ ; when $k>n$ , time is $O(1)$ . Both branches follow from the same factorial decomposition, proving that the choice preserves correctness. The method suits short products or products nearly spanning the modulus range and provides a useful check of the checkpoint method. When $k$ is near $P/2$ , it still needs about five hundred million modular products and cannot meet the current full time limit. See the [measurements](../../../docs/benchmark-R36.json) for input sizes, five timing runs, and the standard limit.
