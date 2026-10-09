# Paper Tiger Sequence: Interval Backtracking with a Bounded Cache

Codex (GPT-6) supplies interval-based output backtracking and applies the setter's shared-suffix method to a bounded cache. Program: [alternative.cpp](alternative.cpp). It is a lower-space parallel option to the [shared-suffix reference](solution.en.md).

## Cache shorter versions

Let $B$ be a character-cache bound large enough for the initial string. The program uses $B=65536$ and chooses the largest $h$ with $L_h\le B$ . Construct $S_h$ by shared suffixes; it also contains every earlier version. Keep only lengths and growth parameters for later versions.

## Trace an output interval backward

Define $\operatorname{Emit}(v,s,c)$ to output $c$ characters of $S_v$ starting at index $s$ , in order.

- Return immediately if $c=0$ .
- If $v\le h$ , output the interval directly from its suffix inside the cache.
- Otherwise set $D=L_v-L_{v-1}$ . An index $s\ge D$ in the old suffix maps to index $s-D$ in the previous version.
- A new-prefix index maps to $(p_v+s)\bmod L_{v-1}$ . Separate the prefix intersection first. If its mapped interval crosses the old string's end, split it into the ending and beginning pieces. Finally process any remaining old-suffix part.

Since $D\le L_{v-1}$ , the prefix part wraps at most once. A call creates at most three ordered subintervals. Emit them directly without concatenating intermediate strings.

## Correctness and complexity

Shared-suffix construction proves the cache correct. Each decomposition follows the definition “cyclic copied prefix, then old string.” The mapped subintervals cover exactly the requested characters in order. Version numbers strictly decrease, so induction proves the output.

Let $Z$ count all output characters. Cache construction takes at most $O(B+N)$ . At each recursion depth, nonempty output intervals are disjoint and have total length at most $Z$ ; depth is at most $N+1$ . A safe total bound is $O(B+N+(N+1)Z)$ time and $O(B+N)$ space, excluding standard output buffering. This does not claim the reference algorithm's worst-case time guarantee.

The cache stops recursion at larger contiguous pieces instead of tracing each character to the initial version. Character storage is at most about 64 KiB. This option is useful for sparse version queries or reduced character storage. See the [main measurements](solution.en.md#measured-results).
