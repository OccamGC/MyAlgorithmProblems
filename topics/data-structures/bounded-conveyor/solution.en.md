# Solution: A Conveyor with Limited Capacity

Problem setter’s solution: a circular queue with one reserved slot. Codex (GPT-6) provides implementation cleanup, portable buffered input, and explanations of zero capacity, zero-valued elements, and signed endpoints.

## Invariant

Allocate $n+1$ integer slots. Let $Head,Tail$ denote the first element and the next write position. Indices wrap to zero at $n+1$ . The occupied slots form the circular half-open interval $[Head,Tail)$ . At most $n$ slots are used, reserving one slot to distinguish empty from full.

- The queue is empty exactly when $Head=Tail$ .
- It is full exactly when $Next(Tail)=Head$ .
- A successful insertion writes at $Tail$ and advances $Tail$ .
- A successful removal prints the value at $Head$ and advances $Head$ .

Initially both indices are zero, so the invariant holds. Insertion extends the occupied interval at its end; removal deletes its first item. The full and empty checks prevent capacity violations, so the operations implement FIFO order. Ignored operations leave the state unchanged.

For $n=0$ , the array length is one, and both empty and full are true. Both operations are ignored. An element equal to zero cannot serve as an empty-slot marker because zero is a legal value.

## Implementation and complexity

Each operation takes $O(1)$ time: $O(m)$ time and $O(n)$ space overall. A small input buffer avoids storing the operation stream. Read the magnitude and apply the sign using a 64-bit integer before converting to 32 bits; this safely handles $-2^{31}$ .

The [standard program](std.cpp) encapsulates the queue in a structure. Maintaining a count also distinguishes full from empty, but is the same circular-queue method. Linked nodes add storage overhead and do not merit a separate solution here.

See the [test recipes](tests/README.md) and [measurements](../../../docs/benchmark-R36.json).
