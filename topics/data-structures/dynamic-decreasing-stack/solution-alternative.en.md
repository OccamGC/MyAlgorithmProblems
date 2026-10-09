# Alternative Solution

Contributions: Codex (GPT-6) supplied the block algorithm, proof, implementation, and verification.

Scan each block from right to left and retain strict record maxima. Stored in this order, their values are strictly increasing. A query also moves right to left, maintaining maximum $t$ already seen. The records of a full block greater than $t$ are exactly its contribution; one `upper_bound` gives their count. Then update $t$ with the block maximum. Process fringe positions individually. An update rebuilds only its block.

Correctness follows from the right-record equivalence in the [preferred solution](solution.en.md). A nonrecord is already blocked by a later element in its own block. A record survives exactly when it exceeds the maximum outside the block to its right. Updating that threshold from right to left therefore counts full blocks and fringes correctly.

For block length $B$ and $K=\lceil n/B\rceil$ blocks, preprocessing costs $O(n)$ , updates $O(B)$ , queries $O(B+K\log(B+1))$ , and space $O(n)$ . The implementation uses $B=224$ .

[alternative.cpp](alternative.cpp) has a simpler structure, with higher worst-case update and query complexity than the segment tree. It passes the complete data; the segment tree remains preferred.
