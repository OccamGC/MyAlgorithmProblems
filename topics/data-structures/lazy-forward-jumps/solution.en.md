# Solution: Forward Jumps with Batched Operations

Problem setter’s solution: maintain a valid suffix of jump answers and repair downward on demand. Codex (GPT-6) clarifies positive jumps and batch guarantees, cleans up the implementation, and proves the work bounds. A standard link-cut-tree application is also provided.

## Maintain only the needed suffix

Positive jumps guarantee $i+K_i>i$ . Let $f_i$ be the number of jumps from pad $i$ :

$$f_i=\begin{cases}1,&i+K_i>n\\1+f_{i+K_i},&i+K_i\le n\end{cases}$$

Values can be computed in descending index order. Maintain a boundary $h$ : every cached answer strictly above $h$ is correct; no promise is made about smaller positions. Initially $h=n$ .

Changing $K_A$ can affect only answers at positions at most $A$ , so set $h\gets\max(h,A)$ . For a query $C\le n$ , repair positions from $h$ down through $C$ , leaving $h=C-1$ . If $h<C$ already, no repair is needed. Each recurrence depends on a larger index, whose answer is already correct. A query $C>n$ returns zero without changing the boundary.

Induction over initialization, updates, and downward repairs maintains the invariant and proves every returned $f_C$ correct.

## Why the batch guarantees bound the work

Let $R$ be the total number of repaired positions. Time is $O(n+q+R)$ and space is $O(n)$ . The following bounds use the stated guarantees; they do not claim constant work on arbitrary streams.

1. Use $h+1$ as a potential. Each repair reduces it by one; an update increases it by at most $A+1$ . Thus $R\le n+1+\sum(A+1)$ . Group 1 bounds the sum of update positions, and the update count is at most $q$ .
2. Group 2 has at most 110 contiguous update runs: the 100 selected intervals plus at most ten exceptional updates. Following each run, consecutive queries repair at most $n+1$ positions. There may also be an initial query run, so $R\le111(n+1)$ .
3. Group 3 similarly has at most 110 query runs. No updates occur within a run, so the boundary only decreases and $R\le110(n+1)$ .
4. Let $s$ be the number of local segments and $W$ the maximum position span. The first query of a segment repairs at most the whole array. Every subsequent repair costs at most $W+1$ , since updates and queries stay within that local interval. Hence $R\le s(n+1)+q(W+1)$ , with $s\le100,W\le500$ here.

These are upper bounds; actual work is often smaller. Arbitrary operation streams can require $O(nq)$ time, so the batch guarantees cannot simply be removed.

## Output and an alternative

XOR grouping uses the full operation number, not the query number. Each answer is at most $n+1$ ; use a 64-bit total. A jump destination fits a signed 32-bit integer because $i+K_i\le300000+10^9$ .

The [standard program](std.cpp) uses the setter's method. The [link-cut-tree solution](solution-alternative.en.md) and [program](alternative.cpp) support arbitrary operations in $O(\log n)$ amortized time, independent of batch shape. Its larger constants produce a slowest formal median of about 3.50 seconds, exceeding the 0.5-second limit calibrated from the standard program. It is retained as a tradeoff for more general streams. The standard program's slowest median is about 0.20 seconds.

See the [test recipes](tests/README.md) and [individual measurements](../../../docs/benchmark-R37.json).
