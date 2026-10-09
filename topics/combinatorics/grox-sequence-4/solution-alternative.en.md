# Grox's Sequence IV: Per-square FWT

**Problem setter’s solution: the space-first per-square transform.** Codex (GPT-6) organizes boundaries, modular arithmetic, and the C++17 implementation. This is a parallel option to [phased FWT](solution.en.md): lower space use and higher time complexity.

Let $L$ be the smallest power of two at least $n+1$ , and $B=\log_2L$ . Decompose the legal region $i+j\le n$ into disjoint aligned squares using the same rules as the main method.

An accepted square has side $s=2^d$ , with starting indices $a,b$ whose low $d$ bits are zero. Consequently,

$$(a+u)\circ(b+v)=(a\circ b)+(u\circ v)$$

Apply complete forward FWTs independently to the two length-$s$ segments, multiply pointwise, and inverse-transform. Use offset $a\circ b$ to add results directly to the three residue groups; no cross-level result arrays are retained. Process XOR, OR, and AND separately.

The disjoint squares cover all legal pairs. Separation of high and low bits gives the correct offsets, and complete forward/inverse transforms recover each square’s contributions. The result therefore equals the phased method’s result. The main editorial gives the butterfly rules and bitwise-convolution proof.

A level with side $s$ has $O(L/s)$ squares, each requiring $O(s(1+\log s))$ transform work. Summing levels gives $O(L(1+B)^2)$ time. The inputs and current square arrays use $O(L)$ space. Recursion depth is $O(1+B)$ ; temporary arrays are released after each square.

## Same-input measurements

See the [reference environment and performance](../../../docs/评测环境与性能.md) and [raw R14 record](../../../docs/benchmark-R14.json). The per-square method matches the reference output on all 10 formal inputs. Five alternating timing runs give a largest median of 0.892257 seconds and a peak working set of 17.16 MiB. The phased method has a largest median of 0.466883 seconds in the same comparison, with reference peak memory 125.83 MiB. Every measured formal input meets the 1.0-second indicative limit for the per-square method. This conclusion covers these inputs and the reference environment, not every implementation with the same complexity. Choose this method when space takes priority; the reference program uses phased FWT for its time margin on the full data.
