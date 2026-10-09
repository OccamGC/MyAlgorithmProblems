# Editorial for Grox's Sequence IV

**Problem setter’s solution: aligned-square decomposition and phased FWT.** Codex (GPT-6) organizes the implementation, the zero-index boundary, and modular arithmetic. Transform types are processed separately, with residues stored as 32-bit integers and products computed in 64 bits.

## Aligned-square decomposition

Let $L$ be the smallest power of two at least $n+1$ , and let $B=\log_2L$ . Pad both inputs with zeros to length $L$ . Contributing ordered pairs lie in the triangle $i+j\le n$ .

Start with $[0,L-1]\times[0,L-1]$ . Consider an aligned square of side $s=2^d$ with lower-left corner $(a,b)$ . If $a+b>n$ , discard it. If $a+b+2s-2\le n$ , accept the whole square. Otherwise split it into four equal children. A single-cell square necessarily falls into one of the first two cases.

Accepted squares are disjoint and cover exactly the legal pairs. Within a square, the low $d$ bits of $a,b$ are zero. Thus for any bitwise operation $\circ$ ,

$$ (a+u)\circ(b+v)=(a\circ b)+(u\circ v)\qquad(0\le u,v<s)$$

Compute the appropriate bitwise convolution of the two local segments and place its result at offset $a\circ b$ . Add the results for all three operations, then group indices by their residues modulo $3$ .

![Aligned squares covering the legal ordered pairs for n equal to six](assets/triangle-blocks.svg)

Each cell represents an ordered pair. Cells inside a common outline form an accepted square; unshaded pairs contribute nothing.

## Phased FWT

A transform of length $2^d$ consists of $d$ butterfly layers. Executing layer $d$ advances every aligned local transform of length $2^{d-1}$ in the global array to length $2^d$ . Complete transforms need not be repeated for individual squares.

Process $d$ in increasing order. At stage $d$ , each aligned input segment of length $2^d$ contains its transformed values. For all accepted squares at that level, multiply corresponding frequency entries and accumulate them into $R_d$ at the appropriate high-bit offset.

Process results in decreasing order of $d$ : undo one butterfly layer on $R_d$ , then add it to $R_{d-1}$ . Both arrays now use the transform domain on the low $d-1$ bits, so the addition is valid. Finally, $R_0$ contains the ordinary indexed convolution sums.

The rules for a pair $(x,y)$ are:

| Operation | Forward transform | Inverse transform |
| --- | --- | --- |
| XOR | $(x+y,x-y)$ | $((x+y)/2,(x-y)/2)$ |
| OR | $(x,x+y)$ | $(x,y-x)$ |
| AND | $(x+y,y)$ | $(x-y,y)$ |

All arithmetic is modulo $P=1004535809$ , with division by $2$ implemented using $(P+1)/2$ . The convolution property can be checked for the four pairings of single bits. Tensor products of these two-entry transforms handle multiple binary bits.

## Correctness

The decomposition counts every legal pair exactly once. High and low bits separate inside each square, so its local convolution computes precisely its contribution. Phased input transforms equal independent local transforms; descending inverse layers and additions maintain the corresponding transform domain and eventually recover every contribution. Since $i\circ j\le i+j\le n$ , all nonzero contributions lie within the required output index range. Grouping by residue gives the requested three results.

## Complexity and the parallel option

At a level with side length $s$ , there are at most $O(L/s)$ squares split along the boundary. Their pointwise products total $O(L)$ work, as do global butterflies at that level. The reference program uses $O(L(1+B))$ time and $O(L(1+B))$ space. When $n=0$ , $L=1,B=0$ , and all three operations contribute to index zero.

The setter’s **per-square FWT** performs complete transforms independently on each accepted square, taking $O(L(1+B)^2)$ time and $O(L)$ space. Its space advantage makes it a parallel option. `std.cpp` uses the phased method for its lower time complexity; the [complete per-square editorial](solution-alternative.en.md) and `alternative.cpp` provide the space-first choice. The same-input measurements in that editorial state whether it meets the current indicative limit.

## Supplementary solution

Residue-valued tensor transforms accumulate directly into three residue classes, keeping $O(L(1+B))$ time while reducing space to $O(L)$ . Three-component working values replace cross-level convolution results, giving a parallel option with different constants from both FWT methods.

[Complete editorial and measurements](solution-alternative-residue.en.md) · [Program](alternative-residue.cpp)
