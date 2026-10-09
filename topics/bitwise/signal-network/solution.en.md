# Alien Factory Signal Network: Two Unsigned Words

Problem setter's solutions: represent the register as an integer with rotations and interval masks, or use a circular origin and segment tree. Codex (GPT-6): implement the integer method with two standard 64-bit unsigned words, handling zero rotations, word boundaries and full-word masks.

## Representation and flips

Store bits $0$ through $63$ in $L$ and bits $64$ through $127$ in $H$ , so the full value is $A=L+2^{64}H$ .

Let $P(t)$ be a 64-bit mask with its lowest $t$ bits set. For $0\le t<64$ , it equals $2^t-1$ ; handle $P(64)$ separately by returning all ones. Within one word, the mask for a closed interval $[l,r]$ is

$$P(r+1)\mathbin{\oplus}P(l)$$

Ones below $l$ cancel under XOR, leaving exactly the requested interval. Split intervals crossing the word boundary into low- and high-word pieces, subtracting $64$ from high-word indices. XOR each word with its mask.

## Right rotation

Normalize $k=(x\bmod128+128)\bmod128$ . If $k\ge64$ , swap the words and set $k\leftarrow k-64$ . Stop if the remaining $k=0$ . Otherwise $1\le k\le63$ , and compute

$$L'=(L\gg k)\mathbin{|}(H\ll(64-k))$$

$$H'=(H\gg k)\mathbin{|}(L\ll(64-k))$$

Both expressions must use old values, so save the old low word first. The two bit ranges in each expression are disjoint: bits leaving the right end of one word fill the high positions of the other. Swapping words rotates by half the register width, and the remaining rotation completes the requested operation.

C++ does not provide an automatic modulo rule for negative shift counts or counts reaching the type width. Normalize rotations explicitly, keep actual 64-bit shift counts from $0$ through $63$ , and handle full-word masks separately.

## Queries, correctness and cost

A query extracts $L\mathbin{\&}65535$ , prints uppercase hexadecimal, and then restores decimal output formatting. Zero is `0` , with no prefix or padding.

Initially both words are zero and the representation is correct. Interval masks flip exactly the requested bits, the rotation formulas send every bit to its specified destination, and queries extract the lowest sixteen bits. Induction over operations proves every output correct.

The width is fixed at $128$ , so each operation uses a constant number of word operations. Total time is $O(N+1)$ and extra space is $O(1)$ . See [std.cpp](std.cpp). The setter's [circular-origin segment tree](solution-alternative.en.md) and [alternative.cpp](alternative.cpp) make rotation an origin change and illustrate more general circular interval maintenance. The integer method is more direct for this fixed width. Both programs pass all formal inputs.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
