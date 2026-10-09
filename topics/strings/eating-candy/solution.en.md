# Eating Candy Solution

## Comparing solutions

The problem setter’s program inserts all patterns into an Aho–Corasick automaton and propagates accepting flags through failure links. While scanning the text, it counts a match as soon as one ends and resets to the root, so the next segment starts after the selected one. The earliest-ending segment can replace the first segment of an optimum without restricting later choices. The exchange proof below therefore also proves the problem setter’s algorithm.

The implementation by Codex (GPT-6) represents automaton nodes by array indices. For total pattern length $S$ and text length $L$ , time and space including stored input are both $O(S+L)$ .

## Idea

Order selected segments by their right endpoints. For the unused suffix, choosing an available segment with the **earliest finishing position** is optimal. If an optimal selection starts with a later-finishing segment, replacing it with an earliest-finishing segment cannot block any later choice. Repeating this exchange gives a greedy algorithm.

While scanning $T$ , select a segment as soon as any pattern starting after the previous selected segment ends at the current position. The particular pattern does not matter when several end at the same position.

## Finding the Earliest Ending with Aho–Corasick

Insert all $P_i$ into a binary trie and build failure transitions. Mark a state terminal if either it or a state on its failure chain ends a pattern. While scanning $T$ , follow one transition for each bit. Whenever the current state is terminal, increment the answer and reset the state to the root. The next selected segment must then start after the current position.

Resetting prevents a pattern from spanning an already selected segment, exactly as required by disjointness. If $n=0$ , the automaton contains only its root and the answer is $0$ .

## Correctness

Let the greedy algorithm choose its first segment ending at position $r$ . The first segment of any feasible selection ends no earlier than $r$ . Replacing the first segment of an optimal selection with the greedy segment leaves all later segments feasible, since they start after $r$ , and preserves the number of segments. Apply the same argument to the remaining suffix to obtain optimality.

The automaton's terminal flag covers pattern endpoints both at the current state and along its failure chain. It therefore detects exactly the positions where some pattern ends. Resetting after each selection enforces nonoverlap, so the implementation follows the proved greedy rule.

## Complexity

Let $S=\sum |P_i|$ and $L=|T|$ . Building the trie and failure transitions and scanning the text take $O(S+L)$ time. The automaton and its construction queue use $O(S+1)$ space. Since the reference program also stores the text of length $L$ , its total space usage is $O(S+L)$ .
