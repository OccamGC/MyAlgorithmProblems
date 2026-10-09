# Restoring Minds after Swaps — Solution

Use Keeler's two-helper construction, discussed with refinements by [Evans, Huang, and Nguyen](https://arxiv.org/abs/1204.6086). Codex (GPT-6) supplied the task specification, implementation, state-tracking proof, and independent checker; the underlying method is established.

## Decompose the final state into cycles

Simulate the history and let $p[u]$ be the mind currently in body $u$ . This is a permutation. Follow $p$ to find cycles of length at least two; fixed points need no work. Write one cycle as $a_1,\ldots,a_t$ , meaning body $a_i$ contains mind $a_{i+1}$ and the last body contains mind $a_1$ . Let helpers be $x=N+1,y=N+2$ .

For this cycle, output:

1. Swap $(x,a_1)$ .
2. Swap $(y,a_t)$ .
3. For $i=2,\ldots,t$ , swap $(x,a_i)$ in that order.
4. Swap $(y,a_1)$ .

This uses $t+2$ swaps. After all cycles, swap $(x,y)$ once if the number of nontrivial cycles is odd.

## Track the minds

Suppose the helper bodies initially hold minds $X,Y$ , possibly already exchanged. Step one gives $x$ mind $a_2$ and temporarily places $X$ in $a_1$ . Step two gives $y$ mind $a_1$ and temporarily places $Y$ in $a_t$ .

During step three, $x$ carries exactly the correct mind for its next target body. Each swap restores that body and picks up the next mind. Finally, it returns mind $a_t$ and takes $Y$ . Step four returns mind $a_1$ , and $y$ takes $X$ . Thus the entire cycle is restored, the helpers exchange their minds, and other bodies are unchanged. A final parity-dependent helper swap restores everyone.

## Validity, Bound, and Complexity

Every new swap involves a helper, so none repeats a historical pair. All pairs within one cycle are distinct; different cycles use different ordinary bodies; the helper pair occurs at most once, at the end.

With $c$ nontrivial cycles containing $s$ ordinary bodies, the count is $s+2c+(c\bmod2)$ . Every cycle has length at least two, so $2c\le s\le N$ and the count is at most $2N+1$ . Decomposition, construction, and output take $O(N+M)$ time, with $O(N)$ space for the permutation, visited flags, and output.

[std.cpp](std.cpp) handles cycles independently for a direct implementation and proof. The [combined-cycle alternative](solution-alternative.en.md) reduces the number of output swaps for $c\ge3$ . Both meet this task's bound.

## Output Checker

Run `python checker.py input.in contestant.out` . The checker stores unordered historical and new pairs, simulates every swap, and checks restoration including both helpers. It rejects invalid counts, indices, self-swaps, repeated pairs, missing values, and extra tokens. Exit code zero accepts and one rejects. Storing all historical pairs makes the checker's own space $O(N+M)$ .

[Statement](statement.en.md) · [Formal test plan](tests/plan.json) · [Generator](tests/generate.py) · [Measurements](../../../docs/benchmark-R33.json)
