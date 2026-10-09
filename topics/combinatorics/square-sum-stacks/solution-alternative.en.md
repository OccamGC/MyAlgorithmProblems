# Square-Sum Stacks: Problem Setter's Stored Layer Construction

## Proof of the Maximum Capacity

Write $C(n)=\lfloor(n+1)^2/2\rfloor-1$ .

**Upper bound.** Suppose $T=C(n)+1=\lfloor(n+1)^2/2\rfloor$ balls have been placed. Consider the largest $n+1$ labels, $T-n,\ldots,T$ . The sum of any two distinct such labels is strictly between $n^2$ and $(n+1)^2$ , so they cannot be adjacent. Labels on a stack strictly increase from bottom to top, making these large labels a contiguous top section. If a stack contained two, some two would be adjacent, a contradiction. At least $n+1$ stacks would therefore be required.

**Construction attaining the bound.** For one stack, use ball one. For odd $n>1$ , describe the first two layers from the top, with local column index $j=0,\ldots,n-1$ :

$$\text{Top}_j=C(n)-n+1+j,\qquad \text{Below}_j=C(n)-n-j.$$

Below the middle $n-2$ columns, recursively place the construction for $n-2$ stacks. Adjacent labels in the first two layers sum to $n^2$ . Where the second layer meets the recursive first layer, they sum to $(n-1)^2$ . All other adjacencies follow by induction. The two layers use the largest $2n$ labels because $C(n)-C(n-2)=2n$ , so no label is omitted or repeated.

For even $n$ , place $C(n),C(n)-1,\ldots,C(n)-n+1$ across the top layer. Put the construction for $n-1$ stacks below its first $n-1$ columns. Adjacent labels at the join sum to $n^2$ , and $C(n)-C(n-1)=n$ . This is valid and uses precisely all labels through $C(n)$ .

Every column decreases from top to bottom, so placing its labels in increasing global order respects the required operation sequence. The construction and upper bound prove that the optimum is exactly $C(n)$ .

## Implementation

Prepare one vector per stack, storing labels from top to bottom. Begin with label $C(N)$ . For even size, append decreasing labels across all columns from left to right, then retain only the first $N-1$ columns. For odd size, append one layer from right to left and another from left to right, then discard the two outer columns from the active region. Finally append ball one to the middle column.

This filling order implements the two-layer formulas above exactly. Every label is written once, and the order within each column is preserved. Print the completed columns.

![An optimal arrangement on four stacks](assets/stacks.svg)

## Complexity, Scope and Attribution

Time is $O(N^2)$ integer operations. Storing every ball costs $O(N^2)$ space; counting output characters gives $O(N^2\log N)$ time. [alternative.cpp](alternative.cpp) supports all constraints, and keeping the explicit arrangement is useful for inspection or subsequent processing. The preferred [column-streaming implementation](solution.en.md) reduces auxiliary space to a constant.

The problem setter's solution supplies the capacity formula and layer construction. GPT-6 supplied the organized proof, vector implementation and independent validation. Checks cover square sums, uniqueness, order and count; small optimal capacities are compared with bipartite maximum matching. See the [measurements](../../../docs/benchmark-R24.json).
