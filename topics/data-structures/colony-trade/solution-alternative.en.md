# Colony Trade — Solution

> Peer method: an offline coordinate-compressed segment tree. This is the method used by Codex (GPT-6); see [alternative.cpp](alternative.cpp) and the [main editorial](solution.en.md) for comparison with the problem setter’s solution.


## Order goods by price and ID

Sales process $(c_i,i)$ in decreasing order. Prices change, but all operations can be read in advance. Collect each type's initial pair and every pair introduced by a price update, then sort and deduplicate them into fixed coordinates.

At any moment, each type is active only at its current price coordinate. Its old coordinate has zero stock and production. A price change moves its inventory and current production to the new coordinate. This preprocessing determines positions only; it does not execute operations early.

## Segment-tree information

For each interval, maintain four sums: exact stock $S$ , production $R$ , stock value $V$ , and production value $W$ . Store the last two modulo $P=10^9+7$ .

A production operation with parameter $t$ updates

$$S\leftarrow S+Rt,\qquad V\leftarrow V+Wt\pmod P$$

Selling all stock in an interval clears $S,V$ but keeps $R,W$ , since its goods may be produced again later.

Use lazy tags for clearing inventory and accumulating production time. Clearing discards any earlier production tag; subsequent production is accumulated afterward. Push tags in the order **clear, then produce**. Before changing a leaf, push all tags on its path so earlier production uses the earlier rates and price-coordinate assignment.

## Process a sale

Start from the higher-price side, the right child of the segment tree.

- If an interval contains at most the remaining demand $k$ , add its full value to revenue, subtract its stock from $k$ , and clear the interval.
- At a leaf containing more stock, sell exactly $k$ items at that leaf's price.
- Otherwise process the right child, then the left child if demand remains.

A sale has at most one partially sold boundary position. Other visited sibling intervals can be processed in full, so a sale takes $O(\log U)$ , where $U$ is the compressed coordinate count. Neither individual items nor individual goods types need to be scanned.

A production-rate update changes only $R,W$ at the active leaf, preserving inventory. A price update first extracts the old stock and deactivates that coordinate, then assigns the stock and production to the new coordinate and recomputes values using the new price. Pair ordering automatically gives larger IDs priority at equal prices.

## Correctness

Inductively, active leaves contain the exact current inventories and production rates, while interval sums and lazy tags represent all pending operations. Production adds the required stock, clearing removes only existing stock, and point updates preserve the quantities required by the statement. Sales consume inventory in decreasing pair order; processing a whole interval is equivalent to processing its items individually. Thus every reported modular revenue is correct.

## Numeric bounds and complexity

Inventory counts must remain exact because they are compared with sale demand. With $n$ types, $m$ operations, maximum production $p_{max}$ , and maximum production parameter $t_{max}$ , cumulative production is at most $nmp_{max}t_{max}$ . Here this is $9\times10^{18}$ , within signed 64-bit range. Reduce an item count modulo $P$ before multiplying it by a price.

Since $U\le n+m$ , preprocessing, initialization, and all operations take $O((n+m)\log(n+m+1))$ total time and $O(n+m)$ space. Operations are read in advance for coordinate compression, but outputs follow their original order.

The independent model updates arrays directly and re-sorts goods by price and ID for each sale. Tests cover equal prices, zero prices and rates, repricing existing inventory, production after sellout, one goods type, oversized sales, and large stock. Official cases also stress continuous price changes and maximum accumulated inventory.

## Program and reproduction

See [alternative.cpp](alternative.cpp) for this C++17 implementation. After compiling, run `tests/generate.py --out-dir <path-outside-the-problem> --std <program-path>` to generate inputs and answers. Seeds and case purposes are in the [test plan](tests/plan.json). Performance results are documented in [environment and measurements](../../../docs/评测环境与性能.md).
