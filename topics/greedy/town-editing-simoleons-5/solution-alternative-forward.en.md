# Edit Town and Simoleons 5: Forward Batched Averaging

Codex (GPT-6) provides this alternative. It uses the fixed-position construction and optimality proof in the [main solution](solution.en.md), while maintaining each target's wealth directly. The [program](alternative-forward.cpp) shares input and modular utilities in [wealth.hpp](wealth.hpp).

## The Effect of One Group

Process richer external groups in ascending initial mean order. Let the current mean be $v$ , its population $c$ , and the target vector $x$ . After subtracting $v$ , one outsider starts at zero and averages with targets in order, applying

$$B=\frac12(I-L/2)^{-1}$$

to the deviation vector. Here $L$ is the $k\times k$ downward shift matrix. Repeating this $c$ times gives $B^c$ , whose lower-triangular convolution kernel is

$$h_0=2^{-c},\qquad h_d=h_{d-1}\frac{c+d-1}{2d}\quad(1\le d<k).$$

Therefore

$$x_i'=v+\sum_{j=1}^i h_{i-j}(x_j-v).$$

Each group takes $O(k^2)$ operations without expanding its residents. Use separate old and new vectors so the convolution never overwrites an input. Sum the final target vector for the answer.

## Bounds and Complexity

Compute the group mean from one initial representative, whose population is less than $P$ . The total count $c$ may exceed $P$: retain the full 64-bit exponent, reduce $c+d-1$ before multiplication, and invert only $d<P$ .

Grouping takes $O(n(g+1))$ time, calculation takes $O(k+g(k^2+\log P+\log(Q+1)))$ , and space is $O(k+g)$ . Since $k\le20,g\le3$ , this implementation passes every formal file. The main method is the reference because its per-group work is linear; this implementation demonstrates a different batch evaluation of individual averages.

Large inputs are checked against generic matrix exponentiation and small inputs against an exact Fraction grid. See [testing instructions](tests/README.md) and [measurements](../../../docs/benchmark-R42.json).
