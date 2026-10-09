# Random Analysis: Probabilities

## Algorithms and attribution

The preferred algorithm builds value indicators and applies global affine updates. Program: [std.cpp](std.cpp). Codex (GPT-6) applies the expectation recurrence to indicators of equal-valued elements, giving quadratic round processing and a proof that duplicates are aggregated correctly.

The problem setter's element-location recurrence also applies. See [element probabilities](solution-alternative-element-probabilities.en.md) and [source](alternative-element-probabilities.cpp). Codex (GPT-6) aggregates its final contributions by value to produce the matrix.

## A probability is an indicator expectation

Fix a value $v$ . At each position, define an indicator that is $1$ when the current value equals $v$ and $0$ otherwise. These indicators move with the cards, so their final expectations are column $v$ of the matrix.

Initially, $b_i=[a_i=v]$ . If $v$ occurs $c_v$ times, the indicator sum remains $c_v$ , giving mean $\mu=c_v n^{-1}$ . Repeated values therefore contribute to the same column automatically. An absent value starts with all zeros and remains zero.

## One-round recurrence

Write $M=998244353$ . Let $x_1,\ldots,x_n$ be the current position expectations. The underlying random variables may be array values or indicators for a particular value. Swaps preserve their total, whose mean is $\mu$ .

Round $i$ swaps position $i$ with an independently and uniformly chosen position. Let

$$\alpha=(n-1)n^{-1}\pmod M$$

For $j\ne i$ , with probability $1/n$ the value at $i$ moves to $j$ ; otherwise $j$ stays unchanged. Thus

$$x'_j=\alpha x_j+n^{-1}x_i\quad(j\ne i),\qquad x'_i=\mu$$

The last identity holds because position $i$ receives a uniformly selected current value. This uses independence of the new random choice from the preceding process. It requires neither independence between position values nor a uniform final permutation.

## Global affine updates

Store one coefficient $b_j$ per position and two global values $s,t$ such that

$$x_j=s b_j+t\pmod M$$

Initially, $s=1,t=0,b_j=x_j$ . In round $i$ , first use the old $s,t,b_i$ to obtain $c=x_i$ , then set

$$s'=\alpha s,\qquad t'=\alpha t+n^{-1}c$$

This applies the shared part of the round to every position simultaneously. Position $i$ alone must become $\mu$ , so set

$$b_i=(\mu-t')(s')^{-1}\pmod M$$

Leave other coefficients unchanged. Maintain $h=s^{-1}$ using $h'=h\alpha^{-1}$ ; no new exponentiation is needed per round. All assignments must use the pre-update value $c$ .

For $n=1$ , return the deterministic result directly. For $2\le n\le300$ , neither $n$ nor $n-1$ is zero modulo $M$ , so $\alpha$ and every scale $s$ are invertible.

## Correctness

The initial affine representation is valid. Assuming it holds before a round, the global update gives $\alpha x_j+n^{-1}c$ at every position whose coefficient is unchanged. Resetting the active coefficient gives $\mu$ at position $i$ . These are precisely the correct recurrence. Induction proves every round, and evaluating $s b_j+t$ yields the final results.

## Building the matrix and complexity

For each $v=1,\ldots,n$ , initialize the $n$ indicators, run $n$ rounds and store the result in column $v$ . Share the two modular inverse calculations between all columns.

Total time is $O(n^2+\log M)$ , including all $n^2$ outputs. The implementation computes by column and outputs by row, storing the full matrix in $O(n^2)$ space. In the fixed-modulus arithmetic model, output alone requires $\Omega(n^2)$ time, so the preferred algorithm matches that order.

Element-by-element propagation takes $O(n^3+\log M)$ time and $O(n^2)$ space. It is a correct backup that illustrates where each original element goes. Its single-element distribution uses rolling storage, while the matrix is retained. The preferred algorithm instead computes the required value columns directly.

## Denominators, invariants and numeric bounds

The $n^n$ possible random-choice sequences are equally likely. Every probability can therefore use denominator $n^n$ , which is invertible when $n<M$ . Use 64-bit products and reduce at every step.

Each row sums to $1$ . Column $v$ sums to the input frequency $c_v$ , which need not equal $1$ . The final row equals $c_v/n$ , because the last round swaps a uniformly chosen position into position $n$ . These identities also support validation.

Weighting each row gives the [expectation version](../shuffle-expectation/statement.en.md): $E_i=\sum_{v=1}^{n}vP_{i,v}$ .

## Verification and Use

Fixed-seed input recipes are in `tests/plan.json` . Compile a program, then run:

```text
python tests/generate.py --out-dir <output-directory> --std <compiled-program>
```

Omit `--std` to generate only inputs; `--case 01` selects one case. See [independent verification](../../../tools/check_r15_followup.py), [five-round timings, memory and hashes](../../../docs/benchmark-R15-followup.json), and the [environment](../../../docs/评测环境与性能.md).

Small checks enumerate every random-choice sequence, execute its swaps and count outcomes, rather than relying only on the probability recurrence. Additional checks cover row sums, column frequencies, the last row and agreement between expectations and weighted matrix rows. Finite tests supplement the proofs.

## Measured Results

Each program ran five times on the same ten formal inputs, using an Intel Core Ultra 9 275HX, Windows 11, GCC 16.2.0 and C++17 `-O2` . Time is the largest per-input median, including process startup and input/output. Memory is the separately measured peak working set, including runtime overhead.

| Program and algorithm | Largest median (seconds) | Peak (MiB) | 0.5-second reference limit |
| --- | ---: | ---: | --- |
| [Indicators with affine updates](std.cpp) | 0.035418 | 5.99 | Measured inputs pass |
| [Element probabilities](alternative-element-probabilities.cpp) | 0.059872 | 6.01 | Measured inputs pass |

The reference limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R15-followup.json) for all runs and input/source hashes. Recalibrate on other judge machines.
