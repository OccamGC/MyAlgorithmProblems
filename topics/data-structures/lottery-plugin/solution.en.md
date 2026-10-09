# Lottery Plugin — Solution

## Comparing solutions

The problem setter’s solution orders users by current value and index in a randomized skip list. The target's predecessor and successor suffice to choose the winner by distance and tie rules; updates erase the old key and insert the new one. More distant ordered keys cannot improve the result, as proved below. A skip list with ideal randomized heights has expected $O(\log n)$ search time. The supplied code caps the height, and a search can still take $O(n)$ in the worst case; it has no deterministic logarithmic guarantee.

The implementation used by Codex (GPT-6) uses a standard ordered set for the same operations, with $O(\log(n+1))$ worst-case operations. It also merges operation sequences by time without storing a complete array of $m$ events. Total time is $O(n+m\log(n+1))$ ; space changes from $O(n+m+q+k)$ for events, nodes and input to $O(n+q+k)$ . Container maintenance and complexity guarantees are clearer. Tree-node allocations still have constant overhead; speeds were not measured against each other.

## Maintain active participants as pairs

Store $(\text{lucky number},\text{participant ID})$ in a lexicographically ordered set. An array remembers each person's last assigned lucky number, even after leaving, so their pair can be located directly for deletion.

For an update, erase the old pair and insert the new pair. Erasing an absent pair has no effect. A leave event also erases the corresponding pair, which handles repeated departures without a special case.

## A query needs only two candidates

For target $t$ , find the first pair greater than $(t,n+1)$ . This right candidate has the smallest lucky number greater than $t$ and the smallest ID among people with that number. Its predecessor is the left candidate: the largest lucky number at most $t$ , with the largest ID among equal numbers.

No other person can be better: they are farther from $t$ on the same side, or lose the ID tie for the same lucky number. Compare the two distances and prefer the left candidate on a tie because its lucky number is smaller. If only one side exists, use it. If the set is empty, output zero.

The full pair order matters. Keeping one fixed representative per lucky number is insufficient because the required ID direction changes depending on which side of the target it lies.

## Events and arithmetic

Query positions and update positions are already sorted. Two pointers identify the current event. Advance the generated sequence once at the start of every event, then perform the action.

Initially $A,B\le10^9$ and $AB+C\le10^{18}+10^9$ , so signed 64-bit arithmetic suffices. Later sequence values are at most $n$ . A 32-bit multiplication would be unsafe.

Insert the initial sorted pairs into `std::set` with an end-position hint for amortized linear initialization. Subsequent operations take $O(\log(n+1))$ each, giving $O(n+m\log(n+1))$ total time and $O(n+q+k)$ space. The implementation does not store all $m$ targets or event types.

## Correctness and verification

Induction over events shows that the set contains exactly the active participants' current pairs. The candidate argument implements every tie rule, so each query answer is correct.

The independent model stores active participants in a dictionary and scans them using the statement's three priorities. Tests cover duplicate lucky numbers, exact targets, equal distances, rejoining, repeated departures, empty sets, zero events, and maximum generator parameters.

## Program and reproduction

See [std.cpp](std.cpp) for the C++17 reference. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
