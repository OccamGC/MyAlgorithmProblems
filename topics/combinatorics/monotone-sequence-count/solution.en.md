# A Certain Unscientific Count of Monotone Sequences: Solution

## Methods and contributions

The problem setter used stars and bars and Pascal's recurrence. Codex (GPT-6) evaluates the binomial coefficient with products and one inverse to reduce time and space; [std.cpp](std.cpp) is the reference. The setter's recurrence is retained with rolling storage in [alternative.cpp](alternative.cpp) and its [editorial](solution-alternative.en.md). It requires no division and passes all constraints.

## Stars and bars

Let $a_j$ be the multiplicity of label $j$ . Nondecreasing order makes these multiplicities uniquely determine the sequence. Thus we count

$$a_1+\cdots+a_m=n,\qquad a_j\ge0$$

Arrange $n$ identical marks and $m-1$ separators. The counts before, between and after separators give the multiplicities. Adjacent separators and separators at either end allow zero multiplicities. The number of arrangements is

$$\binom{n+m-1}{n}=\binom{n+m-1}{m-1}$$

Both conversions are unique, proving the formula.

## Evaluating the coefficient

Set $a=n+m-1$ and $t=\min(n,m-1)$ . Multiply the numerator factors from $a-t+1$ through $a$ , and denominator factors from one through $t$ , modulo the prime $p$ . Multiply by the denominator raised to $p-2$ . All factors are smaller than $p$ , so the denominator is invertible. When $m=1$ , $t=0$ and both empty products are one.

Use 64-bit multiplication, whose operands produce a value below $p^2$ . There is no need to store a table of coefficients.

## Correctness and complexity

The bijection proves that the required count is the chosen binomial coefficient. The product formula and Fermat's little theorem calculate its residue. Time is $O(t+\log p)$ and auxiliary space is $O(1)$ . Rolling Pascal evaluation uses $O((n+m)t)$ time and $O(t)$ space, and remains valid for composite moduli. The prime modulus makes product evaluation the preferred method here.

## Data generation and validation

Run the Python 3 standard-library script `tests/generate.py --out-dir <directory>` to generate inputs from [plan.json](tests/plan.json). Repeat `--case` to select identifiers; pass `--std <executable>` to generate outputs as well. Compile the desired source as C++17 first. Fixed recipes and seeds reproduce the inputs. Store large generated data outside the problem directory.

[Measurements](../../../docs/benchmark-R30.json) record input and source hashes, five timings per case, and peak working set. All delivered variants pass the full test set. 214 small inputs agree with layered prefix counting or exact integer binomial coefficients. Every official input is also checked with exact integer binomial evaluation.
