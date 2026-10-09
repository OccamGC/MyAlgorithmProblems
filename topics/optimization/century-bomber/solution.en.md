# Century Bomber — Solution

## Comparing solutions

Blocking, convolution and direct accumulation are peer methods for different parameter ranges. The reference uses direct accumulation, which fits this problem’s scale and 8 MB memory limit.

The problem setter’s blocking and convolution methods use the same linear identity: a delivery on $[l,r]$ is a suffix contribution starting at $l$ minus one starting at $r+1$ . Overlapping operations can therefore be aggregated before applying delivery starts.

The block version partitions contribution positions into blocks of length $B$ . It updates boundary blocks directly, records suffix offsets and multiplicities for complete blocks, expands these records at the end, then shifts the resulting contributions by each delivery start. Its time bound is $O(q(B+n/B)+n^2+kn+n+m)$ and space is $O(n^2/B+n+m+k)$ , with $B$ around $\sqrt n$ . The convolution version groups by suffix start and uses NTT on the supply suffix and a signed polynomial counting delivery positions. It accumulates all groups in the transform domain, then performs one inverse transform. For transform length $H=O(n+m)$ , its per-group query scans give $O(nq+qk+nH\log H)$ time and $O(H+n+q+k)$ space. Its modulus is $1004535809$ . The final nonnegative answer at each output position is at most $9q\min(n,k)\le9qn$ , below this modulus, so the final residue is the integer answer.

The implementation used by Codex (GPT-6) keeps linear aggregation but accumulates valid offsets directly and then shifts by delivery starts. It stores neither queries, block-offset tables nor NTT workspaces. With $h=\min(n,m)$ , it takes $O(n+m+k+qh+kh)$ time and $O(n+m+k)$ space. This fits the current scale and 8 MB limit and is straightforward to implement. The block method may reduce per-query work with more queries, and convolution has other useful regimes. This is a time–storage tradeoff; no direct timing comparison between the implementations is available.

## Combine contributions by offset

Every starting position uses the same list of drops. First compute the contribution for one start. Let $s_j$ be the total delivered at offset $j$ across all drops. For a drop $[l,r]$ , perform

$$s_j\gets s_j+a_{l+j}$$

for $0\le j\le\min(r-l,m-1)$ . Offsets of at least $m$ are always outside the line. Then, for each start $p_i$ , add every in-range $s_j$ to answer position $p_i+j$ .

## Correctness

The definition sums one contribution for each drop, start, and valid offset. The algorithm first sums over drops for a fixed offset, then adds that sum at each start. Reordering these finite sums preserves their values. Every discarded offset is outside the line for every start, so the final totals are exactly those required.

## Complexity and implementation

Let $h=\min(n,m)$ . Time is $O(n+m+k+qh+kh)$ and space is $O(n+m+k)$ . The bounds allow direct enumeration of the relevant offsets in each drop, without storing the queries. The reference uses fixed-capacity arrays requiring about $48$ KB.
