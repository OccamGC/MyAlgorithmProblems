# Grox's Sequence II Editorial

**Preferred method: prefix sums by exponent residue, a linear algorithm by Codex (GPT-6) for the three requested totals.** The problem setter’s divide-and-conquer NTT method computes all coefficients; its complete approach and complexity are retained below. Since this task needs only three totals, `std.cpp` uses the linear method.

## 1. Retain the information needed by the output

Let $f_i=(i!)^{-1}\bmod P$ . A nonnegative pair $(i,j)$ contributes exactly when $i+j\le n$ . Its coefficient is $f_if_j$ and its exponent is $i-j$ .

For a fixed $i$ , group the values $f_j$ for $0\le j\le n-i$ by $j\bmod3$ . Define

$$H_t(z)=\sum_{\substack{0\le j\le z\\j\equiv t\pmod3}}f_j$$

Then

$$A_r=\sum_{i=0}^n f_iH_{(i-r)\bmod3}(n-i)\pmod P$$

Normalize all remainders to $0,1,2$ .

## 2. One scan

Compute factorials, obtain $f_n$ by one modular exponentiation, and use $f_{i-1}=if_i$ downwards to obtain every inverse factorial.

Scan $i$ from $n$ down to zero. Insert the newly available $j=n-i$ into its residue-class prefix sum, then add the contribution to each of the three answers. Neither all prefix arrays nor the entire Laurent polynomial need to be stored.

When processing $i$ , the three running sums cover exactly $j=0,\ldots,n-i$ . Every legal pair is therefore counted once in the correct residue class, and no illegal pair enters the sums. This proves correctness. For $n=0$ , the process yields $1,0,0$ .

Time is $O(n+\log P)$ and space is $O(n)$ . With the fixed modulus, exponentiation is constant with respect to $n$ , giving $O(n)$ time.

## 3. Problem setter’s solution: triangular divide and conquer with NTT

To compute every coefficient, process the triangle $i+j\le n$ . Set $t=n-j$ , giving $0\le i\le t\le n$ . The corresponding exponent is $i+t-n$ and the coefficient is $f_i f_{n-t}$ .

Recursively process pairs $l\le i\le t\le r$ . With midpoint $h$ :

1. Recurse on $l\le i\le t\le h$ .
2. Recurse on $h+1\le i\le t\le r$ .
3. Evaluate the cross rectangle $l\le i\le h<t\le r$ by convolution.

For the rectangle, use $A_{i-l}=f_i$ and $B_{t-h-1}=f_{n-t}$ . A convolution term at index $k=(i-l)+(t-h-1)$ contributes to exponent $l+h+1+k-n$ . At a leaf $i=t=l$ , add $f_lf_{n-l}$ to exponent $2l-n$ .

Every legal pair appears once, either at a leaf or in the cross rectangle where its indices first separate. Thus the method computes all coefficients. Use NTT modulo $P$ with primitive root $3$ , padding to a power of two at least the sum of the two array lengths minus one to avoid cyclic aliasing. Finally accumulate the coefficient of exponent $e$ into class $e\bmod3$ .

A node of size $s$ takes $O(s\log s)$ time. Each recursion level has total size $O(n)$ , giving $O(n\log^2(n+2))$ time. Depth-first processing with reusable buffers requires $O(n)$ space. Inverse factorials can use the preprocessing from Section 2.

Divide-and-conquer NTT is useful for variants requesting every coefficient or finer coefficient queries. For these three totals, residue prefix sums have lower asymptotic time and retain all necessary information. This comparison makes no unmeasured claim about program runtimes.

## Data and validation

Samples include $n=0,1,3$ . Generated cases cover power-of-two boundaries and the maximum size. The independent oracle enumerates every legal pair and computes inverse factorials independently. Use `tests/generate.py` ; calibration is documented in [environment and measurements](../../../docs/评测环境与性能.md).
