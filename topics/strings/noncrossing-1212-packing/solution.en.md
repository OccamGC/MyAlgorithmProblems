# Solution: Noncrossing 1212 Subsequences

Problem setter’s modeling: treat 1 and 2 as parentheses and use stack matching to obtain a nesting forest. Codex (GPT-6) gives an exchange proof, identifies a counterexample to the longest-stem greedy, and provides a linear streaming dynamic program using matching deficiencies in the forest's incomparability graph.

## Fix the 1-to-2 pairs first

Treat 1 as an opening parenthesis and 2 as a closing one. Scan left to right, matching each 2 with the most recent unmatched 1, or ignoring it if none exists. Unmatched openings do not become nodes. Each matched pair becomes a node, with direct containment defining a forest.

Why may these pairs be fixed? Equivalently, repeatedly delete an adjacent 12 from the remaining string and fix it as a pair. Start with any optimal legal selection and consider the next adjacent endpoints $p,q$ :

- If neither is used, leave this fixed pair unselected.
- If they are already paired together, keep them.
- If exactly one endpoint belongs to a selected pair, shorten that pair to $(p,q)$ , releasing its other endpoint. Its 1212 group remains legal because shortening cannot intersect the group's other, disjoint pair.
- If the endpoints belong to two different selected pairs, those pairs must cross, which is forbidden.

Adjacency is measured after deleting previously fixed pairs. No still-unfixed endpoint lies between the two positions. Previously fixed pairs cannot span a still-undeleted endpoint, so shortening cannot cross them either. Each adjustment preserves the number of selected groups. Once reduction ends, the remaining string consists of some 2s followed by some 1s and cannot contain an unfixed 1-to-2 pair. Thus an equally large solution exists using only stack pairs.

Conversely, stack pairs never cross. Two incomparable forest nodes correspond to two disjoint pairs in left-to-right order, whose four endpoints form 1212. The task is therefore maximum matching on forest nodes, allowing an edge exactly when neither node is an ancestor of the other.

## Join matchings across trees

For tree $i$ , let $s_i$ be its size and $d_i$ the number of unmatched nodes in an internal maximum matching, its matching deficiency. Any two nodes from different trees may be paired. With $S=\sum s_i$ , the forest's minimum unmatched count is

$$D=\max\left(S\bmod2,\ \max_i(d_i+s_i-S)\right)$$

The empty forest has $D=0$ . To prove the formula, parity requires at least $S\bmod2$ unmatched nodes. Tree $i$ can internally match at most $s_i-d_i$ nodes, and only $S-s_i$ outside nodes can pair with it. Thus at least $d_i-(S-s_i)$ of its nodes remain. These are lower bounds.

To attain the bound, start with an internal maximum matching in every tree. Pair unmatched nodes from different trees until any remaining unmatched nodes all belong to one tree $T$ . If at least two remain, take an existing matched edge entirely outside $T$ and replace it with two edges joining its endpoints to two unmatched nodes in $T$ , increasing the matching size by one.

Continue until zero or one node remains, attaining the parity bound, or until no matched edge lies entirely outside $T$ . In the latter case, every outside node is matched into $T$ . The original internal maximum matching in $T$ is untouched, so the remaining count is exactly $d_T+s_T-S$ . The lower bound is therefore attainable.

A tree root cannot pair with any of its descendants. First combine its child trees as a forest, then add one to both size and deficiency.

## Two integers summarize a stack frame

Each frame stores the total child size $S$ and $M=\max_i(s_i+d_i)$ . When an opening closes, its subtree has

$$s=S+1,\qquad d=1+\max(S\bmod2,M-S)$$

Merge this subtree into its parent's frame. At end of input, unmatched openings are not nodes: merge their child forests directly into the enclosing frame without adding a node or deficiency. The virtual root represents the complete forest, whose answer is $(S-D)/2$ .

Each character enters and leaves the stack at most once. Time and space are $O(n)$ . The implementation stores only two integers per frame, avoiding an explicit tree and recursive traversal on deep chains.

## Counterexample to longest-stem greedy

The setter's greedy chooses a branch with the longest single-child stem, pairs its root with a root from an arbitrary other branch, then exposes their children. This does not guarantee optimality. On

```text
11221122111112222122
```

it obtains four groups, but the following five groups of positions are legal:

$$
(1,4,9,20),\quad(2,3,10,17),\quad(5,8,11,16),\quad(6,7,12,15),\quad(13,14,18,19)
$$

They use all 20 positions and have no crossing 1-to-2 pairs, attaining the upper bound of five. Stem length does not describe how much matching assistance a whole branch needs from outside; the deficiency formula retains that information. The counterexample persists after fixing the input-character mapping and is not merely a parsing failure.

The [standard program](std.cpp) uses deficiency DP. Verification directly checks all 8191 binary strings through length 12 and uses closed-form forest shapes at ten million characters. See the [test recipes](tests/README.md) and [measurements](../../../docs/benchmark-R37.json).
