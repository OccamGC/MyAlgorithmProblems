# Crop Unlock Conditions: Solution

## Method and contribution

Codex (GPT-6) models expressions as a standard Boolean circuit and implements iterative parsing and event propagation in [std.cpp](std.cpp). Availability is monotone: crops only change from unavailable to available, and expressions contain no negation, so intermediate conditions also change only from false to true.

## Build a circuit

Create one variable node per crop. Each AND or OR creates a two-input gate with one directed edge from each operand node. Connect the expression root to the crop it unlocks. References to the same crop share its variable node, while operator gates are created separately.

Parse left to right using value and operator stacks. Push identifiers and left parentheses. A right parenthesis reduces pending operations back to its matching left parenthesis. Before pushing a binary operator, reduce operators of at least its precedence until reaching a left parenthesis or a lower-precedence operator. Reduce the remainder at the end. Each reduction pops the right and then left operand and creates a gate. Each token enters and leaves a stack once; deeply nested parentheses require no recursive calls.

## Propagate true events

An AND gate initially needs two true inputs, an OR gate one, and each derived variable one true event from its condition root. Mark every base variable true and enqueue it.

Remove a newly true node and scan its outgoing edges. For each still-false destination, decrease its remaining count. When it reaches zero, mark and enqueue that destination. A true node is never enqueued again. Base variables have no prerequisites.

Retain duplicate input edges. For $A\land A$ , two edges leave $A$ for the same gate; activation of $A$ decrements its count twice. Deduplicating these edges while still requiring two events is incorrect. An OR gate ignores later events after its first activation.

## Correctness

Stack reductions respect precedence and parentheses, so every gate represents its subexpression. Induct on events: base variables are available; an AND gate receives two true inputs, an OR gate one, and a derived variable a true condition. Every marked crop is therefore obtainable. A cycle cannot manufacture an initial event.

Conversely, induct on any legal unlocking sequence. All initial base crops are enqueued. Whenever available variables make an expression true, the relevant gates eventually activate from its leaves to its root, then activate its crop. Thus every obtainable crop is found. When the queue empties, the result is the least fixed point starting from the base crops, independent of unlocking order.

## Complexity and boundaries

Let $S$ be total expression length. The graph has $O(N+M+S)$ nodes and edges. Each node is enqueued at most once and each edge is scanned once. Including parsing, time and space are both $O(N+M+S)$ . Flat adjacency lists avoid allocating a container per node.

If $N=0$ , no event starts and every derived crop remains unavailable. If $M=0$ , output is empty. Self-dependencies and cycles need no special detection: without an external trigger, they remain false. Repeatedly rescanning all expressions is simpler but takes quadratic work on long chains, so it is not a full-range reference implementation.

## Data generation and validation

Run the Python 3 standard-library script `tests/generate.py --out-dir <directory>` to generate inputs from [plan.json](tests/plan.json). Repeat `--case` to select identifiers; pass `--std <executable>` to generate outputs as well. Compile the desired source as C++17 first. Fixed recipes and seeds reproduce the inputs. Store large generated data outside the problem directory.

[Measurements](../../../docs/benchmark-R30.json) record input and source hashes, five timings per case, and peak working set. All delivered variants pass the full test set. 303 small inputs use independent expression evaluation and repeated fixed-point recomputation. Official long chains, inactive and triggered cycles, deep parentheses and wide expressions have directly provable expected outputs.
