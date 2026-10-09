# Random Analysis: Expectations

## Algorithms and attribution

The preferred algorithm uses global affine updates; see [std.cpp](std.cpp). Codex (GPT-6) expresses the expectation recurrence as a shared transformation plus one point assignment, and supplies a linear-round implementation and proof. Affine representations and modular inverses are established tools; the contribution is their application to this recurrence.

The problem setter's [element-probability method](solution-alternative-element-probabilities.en.md), with [source](alternative-element-probabilities.cpp), and the accompanying editorial's [direct expectation method](solution-alternative-direct-expectation.en.md), with [source](alternative-direct-expectation.cpp), remain available. Both are correct. The preferred method eliminates the per-position work within each round.

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

## Applying the recurrence to values

Initialize $b_j=a_j$ . The invariant mean is

$$\mu=n^{-1}\sum_{j=1}^{n}a_j\pmod M$$

One complete affine pass produces all $E_j$ . Two exponentiations for inverses take $O(\log M)$ modular operations, while processing and output take $O(n)$ . Total time is $O(n+\log M)$ and space is $O(n)$ . With the fixed modulus, growth in $n$ is linear.

## Comparing the three algorithms

| Algorithm | Time | Space | Role |
| --- | --- | --- | --- |
| Global affine updates | $O(n+\log M)$ | $O(n)$ | Preferred; avoids per-position updates |
| Direct expectations | $O(n^2+\log M)$ | $O(n)$ | Backup; follows the round formula directly |
| Element probabilities | $O(n^3+\log M)$ | $O(n)$ | Backup; explains element-location probabilities |

Space bounds describe the supplied rolling-storage implementations. For the current $n\le300$ , all three programs pass the measured formal inputs; timings are reported below.

There are $n^n$ equally likely random-choice sequences. All probabilities and expectations can be expressed with denominator $n^n$ , which is invertible because $n<M$ . Use 64-bit multiplication intermediates and reduce at each step.

For complete value distributions, see the [probability version](../shuffle-distribution/statement.en.md). The answers satisfy $E_i=\sum_{j=1}^{n}jP_{i,j}$ , but expectations alone do not require the matrix.

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
| [Global affine updates](std.cpp) | 0.030652 | 5.31 | Measured inputs pass |
| [Direct expectations](alternative-direct-expectation.cpp) | 0.032607 | 5.33 | Measured inputs pass |
| [Element probabilities](alternative-element-probabilities.cpp) | 0.054410 | 5.32 | Measured inputs pass |

The reference limit is twice the reference program's largest median, rounded up to a multiple of 0.5 seconds. See the [measurement record](../../../docs/benchmark-R15-followup.json) for all runs and input/source hashes. Recalibrate on other judge machines.
