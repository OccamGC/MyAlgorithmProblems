# Magic Bread Editorial

Solution contribution: Codex (GPT-6) used the small level limit to combine exact bit encoding, a recurrence for consecutive equal blocks, and scans in both directions, obtaining $O(nK)$ time and $O(n+K)$ space. Bit encoding and dynamic programming are established techniques; the contribution is their application, proof, and implementation here.

## Comparing solutions

The problem setter’s solution doubles the circular string and builds palindromic trees in both directions, considering only palindromes of length at most $n$ . For node $v$ and level $j$ , it stores the greatest length $best[v][j]$ on its failure chain that repeats one palindromic block. Let $f$ be its failure node. If $len(v)=best[f][j]+j$ , the value is $len(v)$ ; otherwise it inherits $best[f][j]$ .

If a suffix of length $len(v)-j$ repeats a palindromic block $P$ , the whole string's symmetry forces its first block to be $P$ too. Conversely, deleting the first block of a repetition of $P$ leaves a palindromic suffix on the failure chain. This proves the recurrence. Storing every level at every node, and scanning both directions, gives maximum block counts for all starts. Both time and space are $O(nK)$ .

The Codex implementation processes one level at a time. Exact integer encodings of short binary windows test palindrome status and equality, followed by a recurrence for consecutive equal blocks. It immediately accumulates the final XOR and reuses temporary arrays. Time remains $O(nK)$ while space falls to $O(n+K)$ . It removes the node-by-level table, but relies on $K\le20$ so windows fit exactly in a machine word. The palindromic-tree approach remains useful for longer blocks.

## Fix one level

Fix a block length $j\le\min(n,K)$ . A valid sequence is exactly a repetition of one palindromic block of length $j$ . Thus we need the longest run of equal palindromic blocks extending in each direction from each position.

Unroll the ring in one direction into a sequence of length $2n-1$ . With zero-based indices, ending positions $n-1$ through $2n-2$ cover every ring position exactly once, and each has a complete lap available before it.

## Exact block equality and palindrome checks

A binary block of length $j$ has an exact unsigned-integer encoding. Since $j\le20$ , a 32-bit integer suffices. No hashing or collision probability is involved.

When reading a new bit $b\in\{0,1\}$ , maintain the forward encoding $F$ and reversed encoding $G$ of the window:

$$F'=((F\ll1)\mathbin{\mathrm{OR}}b)\mathbin{\mathrm{AND}}(2^j-1)$$

$$G'=(G\gg1)\mathbin{\mathrm{OR}}(b\ll(j-1))$$

Once the window contains $j$ characters, it is a palindrome exactly when $F=G$ . All compared blocks have the same length, so leading zeros do not affect the uniqueness of their encodings.

## Recurrence for equal consecutive blocks

Let $f_t$ be the maximum valid sequence length ending at position $t$ in the unrolled string. If the last block is incomplete or not palindromic, set $f_t=0$ . Otherwise let $q_t$ be the last block's encoding:

$$f_t=\begin{cases}j+f_{t-j},&t\ge j\ \text{and}\ q_t=q_{t-j}\\j,&\text{otherwise}\end{cases}$$

Missing predecessor states are treated as zero. An equal last block can extend the previous valid sequence; otherwise a new run begins with the current block. Store the previous encoding and run length in circular arrays of size $j$ , indexed by the scan position modulo $j$ . The previous entry in that slot is exactly the one for $t-j$ .

The segment cannot exceed one lap, so the directional answer is

$$\min\bigl(f_t,\lfloor n/j\rfloor j\bigr)$$

This truncates by whole blocks. All retained blocks remain identical palindromes, so the truncated sequence is valid.

## Combine the directions

Scan forward and store the maximum length ending at each position. Scan backward to obtain the maximum length extending the other way. Their maximum is $a_{i,j}$ . Reversing a palindromic block leaves it unchanged, so reading a ring segment from its other endpoint preserves validity.

After processing each $j$ , XOR $j\cdot a_{i,j}$ directly into $X_i$ . Only one length array and one answer array are needed, rather than a two-dimensional table for all levels. Skip $j>n$ , whose answers are all zero.

## Complexity and boundaries

For each level, both scans process $2n-1$ characters. Time is $O(n\min(n,K))$ , also bounded by $O(nK)$ , and space is $O(n+K)$ . This bound uses the machine-word model applicable here: each length-$j$ block fits in one integer.

Handle single-position rings, constant strings, segments crossing the numbering boundary, $K>n$ , and adjacent palindromic blocks that differ. The largest product is at most $nK$ . The reference uses 32-bit unsigned integers for bit windows and integers for lengths and XOR results.

Validation enumerates every binary ring of length at most 8, then checks random rings using direct extraction, reversal, and block comparison. Formal data include million-character constant strings, alternating strings, palindromic periods, and periodic strings with one changed character. For performance measurements, see [environment and measurements](../../../docs/评测环境与性能.md).
