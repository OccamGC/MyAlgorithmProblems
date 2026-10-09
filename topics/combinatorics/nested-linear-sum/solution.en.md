# A Certain Unscientific Weighted Sum of First Values of Monotone Sequences: Solution

## Methods and contributions

The problem setter supplied the binomial formula and an implementation sharing the numerator product between its two terms. Codex (GPT-6) completed the counting proof and applied binomial symmetry to shorten products for small value domains. The reference is [std.cpp](std.cpp). The shared-product method remains in [alternative.cpp](alternative.cpp) with a [separate editorial](solution-alternative.en.md). Both support the full constraints.

## Counting sequences and first values

Let $A$ count the valid sequences. The multiplicities of the $m$ labels are nonnegative integers summing to $n$ . Stars and bars gives

$$A=\binom{n+m-1}{n}$$

Let $B$ sum all first values. A sequence with first value $x_1$ contributes one for each choice $y\in[1,x_1]$ . Each sequence-choice pair corresponds bijectively to a nondecreasing sequence $(y,x_1,\ldots,x_n)$ of length $n+1$ . Hence

$$B=\binom{n+m}{n+1},\qquad \mathrm{Answer}=kB+cA\pmod p$$

The bijection accounts for the first-value and constant contributions, including length one. If $m=0$ , output zero before using the multiplicity model.

## Reference: symmetric products

To compute $\binom{a}{b}$ , set $t=\min(b,a-b)$ and evaluate

$$\binom{a}{b}=\frac{(a-t+1)(a-t+2)\cdots a}{t!}$$

Multiply numerator and denominator modulo $p$ , then use binary exponentiation to obtain the inverse $(t!)^{p-2}$ . Both calls have $t\le n+1\le10000001<p$ , so the denominator is invertible. The upper argument $a$ may reach or exceed $p$ : a numerator factor divisible by $p$ correctly makes the result zero. Computing and inverting $a!$ , or dividing by a possibly zero neighbouring binomial coefficient, is unsafe.

Use signed 64-bit products. Two reduced factors multiply to less than $p^2$ ; the final sum of weighted terms is below $2\times10^9p<2^{63}$ .

## Correctness, complexity and choice

Stars and bars and the bijection compute $A,B$ . Invertible denominators give their exact residues, and their linear combination is the requested sum.

For $m\ge1$ , let $t=\min(n+1,m-1)$ . The reference takes $O(t+\log p)$ time and $O(1)$ auxiliary space. The shared-product method takes $O(n+\log p)$ time and $O(1)$ space. The reference uses fewer iterations on small domains; for large domains, sharing the product avoids repeated multiplication and is a useful coequal option. Asymptotic bounds alone do not determine which implementation is faster on a particular input.

## Data generation and validation

Run the Python 3 standard-library script `tests/generate.py --out-dir <directory>` to generate inputs from [plan.json](tests/plan.json). Repeat `--case` to select identifiers; pass `--std <executable>` to generate outputs as well. Compile the desired source as C++17 first. Fixed recipes and seeds reproduce the inputs. Store large generated data outside the problem directory.

[Measurements](../../../docs/benchmark-R30.json) record input and source hashes, five timings per case, and peak working set. All delivered variants pass the full test set. 312 small inputs agree with independent sequence enumeration or exact integer binomial coefficients. Full-range tests compare both programs and separately check empty domains, single labels and modulus boundaries.
