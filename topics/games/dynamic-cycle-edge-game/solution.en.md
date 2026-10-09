# Solution: An Edge-Weight Game on a Changing Cycle

Problem setter’s data structure: an implicit splay tree maintaining the sequence and range minima. Codex (GPT-6) corrects the game criterion, proves the strategies, specifies short cycles, and aggregates the first and last minimum positions so each post-edit decision takes constant time.

## Information needed for the game

An empty cycle loses. For a nonempty sequence, let its minimum be $\mu$ . Let $L$ be the number of edges before the first minimum edge encountered clockwise from the start, and $R$ the corresponding counterclockwise count. These are the elements before the first minimum and after the last minimum in sequence order.

- If all weights are positive and $n$ is odd, the first player wins.
- Otherwise, the first player wins exactly when at least one of $L,R$ is odd.

A weight may decrease by any positive amount, so a proof considering only unit decreases is insufficient. We show that every winning state has a move to a losing state, while every move from a losing state leads to a winning state.

## A zero-weight edge already exists

Zero edges cannot be traversed, so the token's reachable component is a path. There are $L,R$ positive edges to its two boundaries.

If one side has odd length, traverse its first edge and reduce it to zero. The opponent is immediately blocked on one side and has an even number of edges on the other, leaving both lengths even.

If both lengths are even, any legal move advances along a positive even-length side. The forward length becomes odd. Reducing the traversed edge to zero gives backward length zero; retaining a positive weight increases the backward length by one, making it odd too. Thus the opponent always gets an odd side. If both lengths are zero, no move exists, agreeing with the losing criterion.

## All weights are positive

For odd $n$ , traverse either incident edge and reduce it to zero. The opponent is at an endpoint of an even-length path of $n-1$ edges, which loses by the preceding argument.

Now suppose $n$ is even. If $L$ is odd, the first clockwise edge is strictly larger than $\mu$ . Traverse it and reduce it to $\mu$ . From the new position, the first clockwise minimum has $L-1$ edges before it, while the just-traversed minimum is immediately counterclockwise. Both counts are even. The case of odd $R$ is symmetric.

Conversely, suppose both $L,R$ are even. Consider a clockwise move reducing the edge to $v$ :

- If $v<\mu$ , the traversed edge becomes the unique minimum. It is immediately counterclockwise from the new position and has $n-1$ preceding clockwise edges, an odd count. When $v=0$ , the path criterion gives the same winning result.
- If $v\ge\mu$ , the traversed edge was not a minimum, so $L>0$ . The previous first clockwise minimum remains ahead, now with $L-1$ preceding edges, an odd count.

Counterclockwise moves are symmetric. Thus a state with two even counts has no move to another losing state. Since total weight strictly decreases, these strategy arguments prove the criterion.

A positive self-loop wins by being reduced to zero. For two parallel edges, the criterion says equal weights lose and unequal weights win, agreeing with the direct two-pile game.

## Implicit splay tree

Maintain edges in their current sequence order. Each subtree stores its size, minimum, and the first and last positions of that minimum. Combine the two children and the root to update these quantities after rotations.

Place weight-101 sentinels at both ends. Legal weights are at most 100, so the sentinels cannot affect a nonempty sequence's minimum. Find edit positions by rank and use splay operations for changes, insertions, and deletions. For insertion or deletion, splay the two interval boundaries to the root and its right child to isolate the edited interval.

The root's positions include the left sentinel. If its first and last minimum positions are $f,l$ , numbered from zero, then $L=f-1$ and $R=n-l$ . The game decision therefore takes $O(1)$ time.

Building takes $O(n)$ time, and each edit takes amortized $O(\log(n+q+1))$ , for $O(n+q\log(n+q+1))$ total. The pool does not recycle deleted nodes, using $O(n+q)$ space. Build recursion is logarithmic; online rank searches and rotations are iterative.

## Counterexamples to incomplete criteria

Checking minimum positions only for values zero and one, and otherwise using cycle-length parity, misclassifies $(2,2,2,3)$ . The first player traverses the weight-3 edge and reduces it to 2, leaving an even cycle of all twos to the opponent, so the first player wins.

When zeros exist, **both side parities** must be checked. For $(0,1,1,1)$ , the counterclockwise path has length three and the first player wins. Testing whether a side position is zero cannot replace its parity.

The primary implementation therefore retains the splay-tree approach and uses the complete proven game criterion. Checks exhaust all 5461 states with lengths zero through six and weights zero through three, and compare edits against an independent sequence model. See the [standard program](std.cpp), [test recipes](tests/README.md), and [measurements](../../../docs/benchmark-R37.json).
