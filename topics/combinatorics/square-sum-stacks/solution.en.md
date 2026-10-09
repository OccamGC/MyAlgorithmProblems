# Square-Sum Stacks: Layer Construction with Column Streaming

## Proof of the Maximum Capacity

Write $C(n)=\lfloor(n+1)^2/2\rfloor-1$ .

**Upper bound.** Suppose $T=C(n)+1=\lfloor(n+1)^2/2\rfloor$ balls have been placed. Consider the largest $n+1$ labels, $T-n,\ldots,T$ . The sum of any two distinct such labels is strictly between $n^2$ and $(n+1)^2$ , so they cannot be adjacent. Labels on a stack strictly increase from bottom to top, making these large labels a contiguous top section. If a stack contained two, some two would be adjacent, a contradiction. At least $n+1$ stacks would therefore be required.

**Construction attaining the bound.** For one stack, use ball one. For odd $n>1$ , describe the first two layers from the top, with local column index $j=0,\ldots,n-1$ :

$$\text{Top}_j=C(n)-n+1+j,\qquad \text{Below}_j=C(n)-n-j.$$

Below the middle $n-2$ columns, recursively place the construction for $n-2$ stacks. Adjacent labels in the first two layers sum to $n^2$ . Where the second layer meets the recursive first layer, they sum to $(n-1)^2$ . All other adjacencies follow by induction. The two layers use the largest $2n$ labels because $C(n)-C(n-2)=2n$ , so no label is omitted or repeated.

For even $n$ , place $C(n),C(n)-1,\ldots,C(n)-n+1$ across the top layer. Put the construction for $n-1$ stacks below its first $n-1$ columns. Adjacent labels at the join sum to $n^2$ , and $C(n)-C(n-1)=n$ . This is valid and uses precisely all labels through $C(n)$ .

Every column decreases from top to bottom, so placing its labels in increasing global order respects the required operation sequence. The construction and upper bound prove that the optimum is exactly $C(n)$ .

## Generating One Column at a Time

[std.cpp](std.cpp) evaluates the construction in output order, column by column. For even size, output the top ball of the current column. The last column then ends; the others enter the odd-size construction for $n-1$ . For odd size, output the two layer formulas. Boundary columns end; an interior column decreases its local index by one and its size by two, then continues. Output ball one upon reaching size one.

This follows one column through the recursive construction with exactly the same formulas, so the output is correct. Only the current size and local column index are stored.

![An optimal arrangement on four stacks](assets/stacks.svg)

The algorithm performs $O(N^2)$ integer outputs and uses $O(1)$ auxiliary space, excluding fixed output buffering. Counting output digits gives $O(N^2\log N)$ characters. The largest label, $C(1000)=500999$ , fits in a signed 32-bit integer.

## Stored Construction and Attribution

The problem setter's solution uses the same layer construction, stores the arrangement, and then prints its columns. A complete [stored-construction explanation](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) are retained. It also takes $O(N^2)$ integer operations, with $O(N^2)$ auxiliary space. Both programs support the full constraints. Column streaming is preferred for its lower auxiliary space; it implements the same construction and capacity formula.

Problem setter's solution: the capacity formula, odd/even layer construction and optimality approach. GPT-6: the top-interval upper-bound proof, streamed implementation, complete bilingual proof and witness validator. Small capacities were independently verified by bipartite maximum matching. Full cases check label uniqueness, descending order, square sums and optimal total count. Run `python tests/checker.py input.in contestant.out` for independent judging; exit code zero means accepted and one means rejected. See the [measurements](../../../docs/benchmark-R24.json).
