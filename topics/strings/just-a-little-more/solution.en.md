# Just a Little More: Solution

## Comparing solutions

Full materialization and on-demand output are peer methods. Materialization avoids recursive expansion and searches; on-demand output avoids storing the largest string and is used in the reference.

The problem setter’s solution first reads all queries, finds the largest requested version, and constructs it by repeatedly copying the specified prefix to the end. Every version is a prefix of this largest string, so a query simply outputs a prefix of the appropriate length. For maximum version $V$ , maximum length $L_{max}$ , $Q$ queries and $C$ output characters, this takes $O(V+Q+L_{max}+C)$ time and $O(L_{max}+V+Q)$ space.

The implementation used by Codex (GPT-6) stores only the initial string and version lengths, recursively expanding a requested prefix according to the same concatenations. This is equivalent to materializing the copies. Extra space falls to $O(V+|s_1|)$ , fitting the memory limit; the time bound is $O(V+(C+Q)\log(V+1))$ . Recursion and version searches add overhead, and all $C$ output characters still have to be written. No overall speed improvement is claimed.

## Compute lengths first

Let $L_k=|s_k|$ . Then

$$L_1=|s_1|,\qquad L_k=L_{k-1}+\left\lceil L_{k-1}/5\right\rceil$$

Use integer arithmetic `(L + 4) / 5` for the ceiling. Lengths strictly increase, and every version is a prefix of every later version. Store only the 70 lengths and the initial string.

## Print a prefix recursively

Define `PrintPrefix(t)` to print the first $t$ characters of any version of length at least $t$ . Every shorter version is a prefix of every longer one, so the choice of a sufficiently long version does not affect the result.

- If $t\le L_1$ , print the first $t$ characters of $s_1$ directly.
- Otherwise, binary-search for the smallest $k$ with $L_k\ge t$ . Since $L_{k-1}<t$ , the desired prefix consists of all of $s_{k-1}$ followed by its first $t-L_{k-1}$ characters. Recursively print the prefix of length $L_{k-1}$ , then the prefix of length $t-L_{k-1}$ .

For query $x$ , recursively print the prefix of length $L_x$ and then a newline. Characters go directly to the output stream; the full large string is never stored. The reference solution uses a zero-based `Lengths` array, so version $x$ has length `Lengths[x - 1]` .

## Correctness

A prefix of the initial string is printed correctly. For $t>L_1$ , the smallest suitable version $k$ satisfies $L_{k-1}<t\le L_k$ . By definition, the first $L_{k-1}$ characters of $s_k$ form $s_{k-1}$ , and the remaining characters form a prefix of that same string. Both recursive lengths are smaller than $t$ , so induction proves that their concatenation is the required prefix. Every query therefore prints the correct version.

## Complexity and memory

Let $V=70$ be the maximum version index, and let $C$ count all output characters excluding newlines. Every internal recursive call splits into two nonempty parts, so there are $O(C+Q)$ calls. Each binary search costs $O(\log V)$ , giving $O(V+(C+Q)\log V)$ time and $O(V+|s_1|)$ auxiliary space, plus the output stream's buffer.

Version indices strictly decrease along recursive calls, so depth is at most $V$ . Avoiding storage of the full string keeps memory use suitable for the 8 MB limit.
