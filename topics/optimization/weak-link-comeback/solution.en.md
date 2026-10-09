# The Weak Link Strikes Back: Solution

## Comparing solutions

The problem setter’s method uses a monotone stack to find the maximal span in which each $a_i$ can represent the minimum, with a fixed convention for ties. A segment tree over $b$ stores sums and maximum/minimum prefix and suffix sums. For fixed $i$ , a positive $a_i$ uses the best left suffix, $b_i$ , and best right prefix; a negative $a_i$ uses their minima. Either side may be empty. This finds the best interval containing $i$ and assigned to its minimum. Processing all indices takes $O(n\log n)$ time and $O(n)$ space.

The implementation used by Codex (GPT-6) preserves this decomposition by minima. A Cartesian tree organizes the spans, and a bottom-up pass combines prefix-sum extrema. Each node requires constant work, reducing time to $O(n)$ while retaining $O(n)$ space. The tree–interval correspondence and sign handling are proved below. The gain comes from removing per-index segment-tree queries, not from changing the objective.

## Organize intervals by their minimum

Build the minimum Cartesian tree of $a$ . Its inorder traversal follows array indices, and every parent value is no greater than its children's values. Break equal-value ties in favor of the smaller index: equivalently, compare pairs $(a_i,i)$ lexicographically.

Scan from left to right, keeping the current tree's rightmost path in a monotone stack. To insert node $i$ :

1. Pop while the top value is greater than $a_i$ . The last node popped becomes the left child of $i$ ; if none was popped, the left child is absent.
2. If the stack is still nonempty, make $i$ the right child of the new top.
3. Push $i$ .

The comparison is strictly greater: equal values stay on the stack, giving earlier indices priority. The bottom of the final stack is the root. Each index is pushed and popped at most once, so construction takes $O(n)$ time.

Suppose the subtree of node $i$ covers the consecutive interval $[L,R]$ . Every interval with $L\le l\le i\le r\le R$ has minimum $a_i$ . Conversely, assign any nonempty interval to the lowest common ancestor of its endpoints: that node lies in the interval, its subtree contains the interval, and its value is the interval minimum. Considering these intervals for every node therefore covers every possible answer.

## Choose endpoints with prefix sums

Let $P_0=0$ and $P_j=\sum_{k=1}^{j}b_k$ . The sum of an interval containing $i$ is $P_r-P_{l-1}$ , where the two indices can be chosen independently:

$$l-1\in[L-1,i-1],\qquad r\in[i,R]$$

- If $a_i>0$ , maximize the sum: maximum right prefix sum minus minimum left prefix sum.
- If $a_i<0$ , minimize the sum: minimum right prefix sum minus maximum left prefix sum.
- If $a_i=0$ , the product is $0$ .

For each subtree, maintain the minimum and maximum prefix sums with indices in $[L-1,R]$ . Notice that this includes one position to the left of the subtree's array interval. In the reference solution, `Prefix` stores prefix sums of $b$ , while `MinPrefix` and `MaxPrefix` store these prefix-sum extrema; they do not store extrema of $a$ .

The left subtree covers array indices $[L,i-1]$ , so its stored prefix-sum extrema cover exactly $[L-1,i-1]$ . Similarly, the right subtree provides extrema over $[i,R]$ . If a child is absent, use the single value $P_{i-1}$ or $P_i$ respectively. Once the children are processed, constant work computes the node's best product. Taking the smaller of the two minima and the larger of the two maxima gives the current subtree's summary.

## Correctness

The Cartesian tree assigns every nonempty interval to a minimum-value node inside it. For a fixed node, the two endpoint ranges are independent, so prefix-sum extrema give the largest or smallest possible interval sum. Choosing the appropriate extremum according to the sign of $a_i$ maximizes the product for that node. Taking the maximum over all nodes yields the global optimum.

Initialize the answer to the smallest signed 64-bit integer rather than $0$ : empty intervals are forbidden, and every valid product may be negative.

## Complexity

Stack construction, iterative traversal, and reverse-order evaluation all take $O(n)$ time and $O(n)$ space. No recursion is used, so million-node chains caused by monotone or equal arrays are safe.

Prefix sums have absolute value at most $10^{12}$ , and candidate products have absolute value at most $10^{18}$ . Use signed 64-bit arithmetic and promote values before multiplication.
