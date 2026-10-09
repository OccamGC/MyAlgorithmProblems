# Random Analysis: Direct Expectation Updates

The expectation recurrence from the accompanying editorial; Codex (GPT-6) uses rolling storage and makes simultaneous-update ordering explicit. Program: [alternative-direct-expectation.cpp](alternative-direct-expectation.cpp). See the [main editorial](solution.en.md) for the preferred method.

## Method and proof

Write $M=998244353$ .

Initialize $x_j=a_j$ and the invariant mean $\mu=n^{-1}\sum a_j$ . In round $i$ , save the old value $c=x_i$ and update every $j\ne i$ by

$$x_j\gets(n-1)n^{-1}x_j+n^{-1}c\pmod M$$

Finally set $x_i=\mu$ . Independent uniform sampling makes position $j$ receive the old value at $i$ with probability $1/n$ , otherwise leaving it unchanged. Position $i$ receives a uniformly sampled position value. Thus the formulas describe the round exactly, and induction proves the final expectations.

Save $c$ before updating. Do not use the new value of $x_i$ for other positions in the same round. Only each position's own old value and the shared $c$ are needed, so historical rounds need not be stored.

## Complexity and applicability

Time is $O(n^2+\log M)$ and space is $O(n)$ . The formulas also work for $n=1$ without inverting $n-1$ . This method follows the round recurrence directly; the affine method combines its shared updates to process the rounds linearly.

This is a correct backup over the full constraints. See [measurements](solution.en.md#measured-results) for the current limit; a higher asymptotic time bound does not imply a timeout at this size.
