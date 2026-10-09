# Virus Sniper: Solution

## Comparing solutions

The linear expectation transition matrix in the problem setter’s solution models the spread. When exponentiating it, the step count must not simply be reduced modulo $P-1$ : Fermat’s theorem for nonzero field elements does not extend to arbitrary matrices.

For example, over the field modulo prime $P$ , let $H=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ . Then $H^t=\begin{pmatrix}1&t\\0&1\end{pmatrix}$ . At $t=P-1$ this is not the identity, whereas reducing the exponent first gives zero. Such a matrix also represents retaining existing counts while adding them to a following level. The full exponent must therefore be handled correctly.

A direct way to evaluate the matrix model is binary exponentiation using the entire big-integer exponent. For $b$ bits and dimension $d$ , each exponent takes $O(bd^3)$ field operations and $O(d^2+b)$ space. The implementation used by Codex (GPT-6) reduces powers by the characteristic polynomial, making the polynomial stage $O(d^2)$ per bit, with additional preprocessing and matrix reconstruction. Full bounds follow below. It handles the complete exponent correctly and reduces repeated matrix multiplication, at the cost of polynomial preprocessing and a more involved implementation.

## Initial values and expectation transitions

Apply the $Q$ rectangle additions with a two-dimensional difference array, then take two-dimensional prefix sums to recover the initial field. Raw intensities are at most $10^{15}$ ; use 64-bit integers for accumulation.

All following algebra takes place modulo the prime $P=1000000009$ . Since $1\le b<P$ , a probability is represented by $a b^{P-2}\bmod P$ . Let $v_t$ be the row vector of expected intensities in the $d=NM$ cells. Build a transition matrix $H$ : add $1$ to each diagonal entry to retain the old intensity, then add the transmission probability from source $i$ to target $j$ to $H_{ij}$ . Ignore directions outside the rectangle.

Transmission trials are independent of the current intensities. Linearity of expectation gives

$$v_{t+1}=v_tH,\qquad v_T=v_0H^T$$

Reducing a matrix exponent modulo $P-1$ is invalid in general. For example, $H=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ satisfies $H^T=\begin{pmatrix}1&T\\0&1\end{pmatrix}$ , whose off-diagonal entry depends on $T\bmod P$ . Valid inputs can also produce singular matrices.

## Computing the characteristic polynomial

Write

$$f(x)=\det(xI-H)=x^d+c_1x^{d-1}+\cdots+c_d$$

Compute $I,H,\ldots,H^d$ by repeated matrix multiplication, and obtain $s_j=\operatorname{tr}(H^j)$ . Newton's identities, with $c_0=1$ , give

$$c_k=-k^{-1}\sum_{j=1}^{k}c_{k-j}s_j\pmod P\qquad(1\le k\le d)$$

Every $k$ is invertible because $d\le50<P$ . Retaining the matrix powers takes $O(d^4)$ arithmetic work, at most about $6.25\times10^6$ matrix product terms under these constraints.

## Handling the full exponent with polynomials

The Cayley–Hamilton theorem states that $f(H)=0$ . Hence, if

$$x^T\bmod f(x)=r_0+r_1x+\cdots+r_{d-1}x^{d-1}$$

then

$$H^T=\sum_{j=0}^{d-1}r_jH^j$$

To multiply two polynomials of degree less than $d$ , convolve their coefficients, then eliminate high-degree terms in descending order using

$$x^d\equiv-c_1x^{d-1}-\cdots-c_d\pmod {f(x)}$$

Each product costs $O(d^2)$ .

Repeatedly divide the decimal input string by $2$ to obtain its complete binary representation. Precompute $x^{2^j}\bmod f(x)$ and share these powers across queries. Multiply those corresponding to set bits to obtain the remainder. No exponent information is discarded, so the method works for singular matrices and repeated eigenvalues as well. For $T=0$ , the remainder is $1$ . For $d=1$ , reduce $x$ to a constant modulo the degree-one polynomial before starting.

## Processing queries in order

Extract the current rectangle's row vector $v_0$ from the initial field. Use the stored matrix powers to compute

$$v_T=\sum_{j=0}^{d-1}r_j(v_0H^j)$$

Output each entry in $[0,P-1]$ , then sum these residues into a 64-bit integer $S$ . Do not reduce $S$ modulo $P$ . Update the rectangle origin using the stated formulas. The next query again reads from the unchanged initial field.

## Correctness

The difference array restores exactly the field after all rectangle additions. Each transition-matrix entry represents retaining an existing value or adding an expected contribution, so $v_T=v_0H^T$ . Newton's identities compute the characteristic polynomial of $H$ , and Cayley–Hamilton ensures that replacing $H^T$ by the polynomial remainder preserves the answer. Binary exponentiation uses the complete exponent and therefore computes the correct remainder. Updating the origin from the output values and restarting from the initial field then implements every query exactly.

## Complexity

Let $L$ be the maximum number of decimal digits in an input time and $b=O(L)$ its maximum binary length. Matrix powers and the characteristic polynomial take $O(d^4)$ time. Shared polynomial powers take $O(bd^2)$ time. Each query costs $O(L^2+bd^2+d^3)$ , where string division accounts for $O(L^2)$ . Total time is

$$O(Q+AB+d^4+bd^2+K(L^2+bd^2+d^3))$$

Space usage is $O(AB+d^3+bd+L)$ . Every modular product fits in a signed 64-bit integer; so does $7S<7dP$ .
