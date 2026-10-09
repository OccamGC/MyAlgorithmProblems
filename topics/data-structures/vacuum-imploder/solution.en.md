# Vacuum Imploder: Editorial

## Solutions and tradeoffs

**Problem setter’s solution: specialized swap, sign, rotation and translation tags.** Both representations take $O(n+m\log n)$ time and $O(n)$ space. Specialized tags are used in the reference and have lower measured peak memory. Affine matrices are somewhat faster on mixed-operation inputs and use a uniform composition formula. These are peer choices whose runtime differences depend on operation distribution and floating-point implementation.

**Programs and credits:** [std.cpp](std.cpp) implements the problem setter’s solution; Codex (GPT-6) contributed implementation details, boundary handling and proof exposition. For the affine matrices method used by Codex (GPT-6), see [alternative.cpp](alternative.cpp) and the [peer method editorial](solution-alternative.en.md).

## Canonical tag order

A tag applies coordinate swapping, independent sign changes, rotation, then translation. With swap matrix $P$ , diagonal sign matrix $D$ , rotation $R(\theta)$ , and translation $t$ , it represents

$$v\longmapsto R(\theta)DPv+t.$$

Store a swap flag, two sign flags, the rotation's sine and cosine, and two translation coordinates. Each leaf initially stores its input point as a translation. No interval coordinate sums are needed: queries request individual points, followed by a final traversal of all points.

## Appending a new transformation

Apply the new tag's components in order while preserving the canonical representation:

- Swap: exchange old translation coordinates and sign flags, toggle the swap flag, and negate the old sine.
- Negate one axis: negate that translation coordinate, toggle its sign flag, and negate the old sine.
- Rotate: rotate the old translation and combine sine and cosine by angle-addition identities.
- Translate: add the new translation to the transformed old translation.

The reflection steps use $FR(\theta)=R(-\theta)F$ . Swapping also gives $PD=D'P$ , with the two diagonal signs exchanged. These identities prove that composition applies the old tag first and the new tag second. Later reflections and rotations must transform previous translations too.

## Segment tree and correctness

Build by point index. A fully covered update appends its transformation to the node's tag. Before partial updates or point queries, append the parent tag to each child tag and reset the parent.

The invariant is that a tag represents all chronologically ordered operations not yet received by its subtree. Composition preserves this invariant. At a queried leaf, every relevant operation has acted on its initial coordinate, so the translation stored there is the answer. A final traversal yields every final point.

## Complexity and precision

Building and final output take $O(n)$ time. Each range update or point query takes $O(\log n)$ , for $O(n+m\log n)$ total time and $O(n)$ space. Recursion depth is $O(\log n)$ .

Use `long double` and print eight decimal places. Both tag representations incur floating-point rounding. The supplied [checker.cpp](tests/checker.cpp) checks each coordinate with absolute tolerance $0.05$ plus $10^{-6}$ comparison slack, and rejects missing, extra, or nonfinite output.

## Validation and performance

Timing and peak-memory measurements are available in [environment and measurements](../../../docs/评测环境与性能.md).
