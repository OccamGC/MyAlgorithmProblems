# Matching in a Class of Four-Neighbor Grid Forests: Bitsets

Keep the problem setter's deduplicated offsets and candidate-set intersection. Codex (GPT-6) supplies the machine-word implementation. The [program](alternative-bitsets.cpp) supports the full range; the [preferred solution](solution.en.md) gives the shared prefix-validity proof and list method.

## Translated road masks

Store a road bitset $R_r$ for each row and a candidate-start bitset $S_r$ , initially equal to $R_r$ . For a new offset $(x,y)$ , candidate row $r$ is compared with road row $r+x$ : column $c$ survives precisely when $R_{r+x}[c+y]$ is one.

Extract the corresponding word window from the road row and AND it with the candidate word. An out-of-bounds target row supplies zero. If a window crosses two source words, combine a right-shifted word with a left-shifted successor. Negative horizontal positions require floor division, not truncation toward zero. Handle a zero remainder separately to avoid shifting by the word width. Candidate padding bits start at zero and cannot create extra starts.

Sum the population counts of the candidate words. The implementation uses portable unsigned group-counting operations without compiler-specific instructions. A repeated offset reuses the previous count. Once the set is empty or an offset coordinate reaches absolute value $n$ , all subsequent answers are zero.

## Correctness

Each retained bit is exactly the conjunction of previous validity and the current translated position being an in-bounds road cell. This is the same test as filtering individual starts. AND never restores a cleared bit, so a previously invalid start cannot recover. A repeated offset adds no condition and may be skipped.

## Complexity and applicability

Let $K$ be the number of new-offset filters actually performed and $W$ the machine-word width, sixty-four here. Each filter performs $n\lceil n/W\rceil$ word-window intersections, giving
$$
O(n^2+m+K n\lceil n/W\rceil)
$$
time. The shared argument gives $K\le n^2+1$ , hence the general bound $O(n^2+m+n^3\lceil n/W\rceil)$ . Bitsets occupy $O(n\lceil n/W\rceil)$ words, alongside $O(n^2)$ visited-offset marks.

Word-level parallelism can reduce work while many starts remain. When the candidate set is small but many new offsets occur, scanning the whole bitset can cost more than a short list. Both methods are compared on every formal output and included in the [performance calibration](../../../docs/benchmark-R28.json).
