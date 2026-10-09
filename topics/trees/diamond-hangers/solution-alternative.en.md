# Arranging Diamond Hangers: Alternative solution

## Stream rows through horizontal chains

The supplementary [alternative.cpp](alternative.cpp), implemented by Codex (GPT-6), stores the starts of horizontal chains in the current row. Initially the only start is the root. Visit starts in order and follow each right pointer to zero, printing identifiers immediately. Append every encountered lower child to the next row's list of starts. After finishing a row, print a newline and replace the current list with the next one.

The invariant is that starts are ordered left to right and each node at the current level belongs to exactly one of their chains. Lower edges increase the level. The [width-separation argument](solution.en.md) ensures that lower chains from earlier parents lie wholly before chains from later parents. Collecting them in parent order thus preserves horizontal order. Unique parents prevent omissions and duplicate visits. The single initial root establishes the invariant.

Each node is scanned once, giving $O(n)$ time. The input tree occupies $O(n)$ space; the two row queues use $O(w)$ , where $w$ is maximum row width. This method streams output when previous rows need not be revisited. The depth-first reference keeps all rows for later access. Both support the full constraints.
