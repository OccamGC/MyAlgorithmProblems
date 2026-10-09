# Cloning Vat — Solution

## Comparing solutions

The problem setter’s construction considers an unchanged or changed center separately and pairs the two halves. Equal pairs cost zero or two edits; unequal pairs cost one or two. It initially chooses the smaller character in each pair, prioritizes lowering characters to zero, then scans from right to left while keeping candidates for the two parities of remaining edits. It records transitions, reconstructs candidates and compares the center choices. Lexicographic order is decided at the leftmost difference, so extra cost is repaired as far right as possible; the parity states distinguish whether the final unit of cost can be consumed. Its passes take $O(n)$ time and auxiliary space.

The implementation used by Codex (GPT-6) keeps lexicographic greedy selection but tests each character using the continuous interval of feasible remaining costs proved below, leaving the center undecided. Time remains $O(n)$ ; space beyond the input/output string is $O(1)$ . Feasibility and its proof are more direct, and candidate/backtracking arrays disappear. This is an alternative with the same time order.

## Feasibility of the remaining positions

Pair position $i$ with $h+1+i$ . If the original characters match, making the pair equal costs either $0$ or $2$ changes. If they differ, the cost is $1$ or $2$ . With four available characters, a differing pair can always choose a third character and pay $2$ . The middle character costs either $0$ or $1$ .

Suppose the undecided part contains $e$ equal pairs, $d$ unequal pairs, and the middle position. Its achievable change counts are exactly

$$[d,\ 2(e+d)+1]$$

To prove this, assign the mandatory cost $1$ to each unequal pair. Those pairs can contribute another $0$ through $d$ changes, and the middle adds $0$ or $1$ , giving every extra count from $0$ through $d+1$ . The equal pairs contribute any even count from $0$ through $2e$ . Translating the first interval by these even counts produces adjacent or overlapping intervals, covering precisely the stated range.

## Greedy construction

First count unequal pairs. If there are more than $m$ , no solution exists. Otherwise a solution exists.

Decide the left half from left to right. Before deciding a pair, remove it from the remaining pair counts. Try `0` , `1` , `2` , `3` in order. Let $c$ be the cost of setting both positions to that character. Choose the first character for which $m-c$ lies in the remaining feasibility interval, then subtract $c$ from the budget.

After all pairs are decided, the remaining budget is $0$ or $1$ . Keep the middle character for budget $0$ ; for budget $1$ , choose the smallest character different from its original value. The right half is already fixed by the left half.

## Correctness and complexity

The feasibility interval exactly determines whether a candidate character can be extended to a valid string. Each step therefore chooses the smallest character that permits completion. Any lexicographically smaller string would use an infeasible character at its first differing position. Choosing the middle character by the same rule completes the lexicographically smallest valid result.

Each pair tries at most four characters. Time is $O(n)$ per query and $O(\sum n)$ overall. The program writes the result into the input string, using $O(1)$ additional space beyond it and $O(\max n)$ peak storage.
