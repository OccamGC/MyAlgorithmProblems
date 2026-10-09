# Variable Lists: Indexed Nodes and Doubly Linked Lists

Problem setter's solution: IDs index a node pool, while previous/next pointers maintain multiple doubly linked lists. Codex (GPT-6): explicit initialization, stable storage, ID validation and empty-list checks.

## Storage and operations

Keep a head and tail pointer for each list. A node stores its predecessor, successor, note, owner list and alive flag. Its pool index equals its ID, and the largest assigned ID only increases.

Let $C=\sum c_i$ . After reading the operation count $m$ , allocate $C+m+1$ nodes once. There can be at most $m$ insertions, so this capacity suffices. Never resize it afterward, ensuring stable pointers. Initialize the lists through tail insertion in the required ID order.

- Query: first check that the ID is assigned and alive. Print three `NULL` entries if invalid; otherwise read the two neighboring pointers and the node's own note.
- Delete: link the predecessor to the successor in both directions. Update the head if there is no predecessor and the tail if there is no successor, then clear the alive flag.
- Insert at either end: allocate a new ID and connect it at that endpoint. If the list was empty, set both the head and tail.
- Edit: change only the note of a valid, alive node, leaving its ID and links intact.

## Invariants and correctness

Maintain these invariants: following next pointers from a list's head visits exactly its alive variables in order; adjacent nodes have matching forward and backward links; the head has no predecessor and the tail has no successor; an empty list has two null endpoints. Every assigned ID also identifies one unique pool node.

Initialization by tail insertion establishes the invariants. Insertion adds one endpoint and its neighboring links. Deletion reconnects the removed node's two sides and handles endpoints. Editing leaves the structure intact, and invalid operations leave the state unchanged. Thus the invariants remain true after every operation, and querying reads exactly the three requested positions.

## Complexity and implementation details

Each operation takes worst-case $O(1)$ time. Total time and space are $O(n+C+m)$ , including one-time pool initialization and all input. At most $10^6$ actual nodes are allocated, plus an unused zero slot.

Check the ID range before indexing the pool, so negative and very large IDs cannot access invalid memory. Deleted nodes remain in the pool but must be rejected by their alive flags. Never reuse their IDs. Allocate the large array on the heap and explicitly initialize every pointer and flag.

See [std.cpp](std.cpp). Array-index links, explicit pointers and standard-library lists represent the same adjacency-maintenance algorithm; this implementation uses the setter's explicit pointers. A container substitution does not form a separate algorithm. A balanced search tree would require ordering keys and costlier operations that this operation set does not need. Formal inputs cover emptying and rebuilding a list, repeated deletion, future IDs, equal notes, a million cumulative IDs and the maximum operation count.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
