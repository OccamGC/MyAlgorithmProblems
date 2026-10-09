# Grox's Sequence V B — Editorial

**Problem setter's solution: obtain a row of Stirling numbers of the second kind by convolution, then evaluate a binomial moment.** Codex (GPT-6) organizes NTT, inverse factorials, zero powers and normalized residues, and truncates the convolution to the prefix contributing to the answer. The fixed modulus $P=1005060097$ differs from those of IV and VII.

## Binomial moments

For $k=0$ , the answer is $2^n-1$ . For $k>0$ , use the falling-factorial expansion:

$$\sum_{i=0}^n i^k\binom ni=\sum_{j=1}^{\min(n,k)}S(k,j)(n)_j2^{n-j}$$

Here $S(k,j)$ is a Stirling number of the second kind and $(n)_j=n(n-1)\cdots(n-j+1)$ . The proof follows [Sequence V A](../grox-sequence-5a/solution.en.md): expand $i^k$ by the number of distinct images, then use $\binom ni(i)_j=(n)_j\binom{n-j}{i-j}$ and the binomial theorem.

## One convolution for the needed prefix

Inclusion-exclusion over missing target values gives

$$S(k,j)=\frac1{j!}\sum_{t=0}^j(-1)^{j-t}\binom jt t^k=\sum_{t=0}^j\frac{t^k}{t!}\frac{(-1)^{j-t}}{(j-t)!}$$

Put $m=\min(n,k)$ and construct only

$$U_t=\frac{t^k}{t!},\qquad W_t=\frac{(-1)^t}{t!}\qquad(0\le t\le m)$$

Coefficient $j$ of their ordinary convolution is $S(k,j)$ . For $j\le m$ , both contributing indices are at most $j$ , so truncation loses no needed term. The setter's complete row through $k$ is also correct; when $n<k$ , later columns do not enter the final sum and can be omitted. Convolution is used only for $k>0$ , so the power at $t=0$ is zero. Return zero directly for $n=0$ .

$P=1917\times2^{19}+1$ is prime and $5$ is a primitive root. Factorial indices are at most $m<P$ , so inverses exist. Choose the smallest power-of-two NTT length strictly greater than $2m$ ; its maximum is $2^{18}$ , dividing $P-1$ . Invert $m!$ once, then compute all inverse factorials downward.

Update $(n)_j$ successively. Starting from $2^n$ , multiply by the inverse of $2$ per step to obtain $2^{n-j}$ , considering only $1\le j\le m$ . Normalize all results to $[0,P-1]$ .

## Correctness and complexity

Inclusion-exclusion counts surjections to $j$ targets; division by target permutations gives the Stirling number. NTT computes ordinary convolution, and truncation preserves every coefficient used by the answer. Substitution into the binomial-moment identity proves the result.

Constructing powers takes $O(m\log(k+1))$ time, convolution takes $O(m\log(m+1))$ , and computing $2^n$ takes $O(\log(n+1))$ . Total time is

$$O(m\log(k+1)+m\log(m+1)+\log(n+1))$$

Space is $O(m+1)$ . Worst-case bounds match the setter's full row: $O(k\log(k+1)+\log(n+1))$ time and $O(k+1)$ space. Small $n$ needs a much shorter convolution. Row-by-row Stirling recurrence is also correct but takes $O(k^2)$ time, appropriate for smaller $k$ .

## Supplementary solution

An exponential generating function extracts binomial moments through formal-series log/exp, giving a different algorithm with the same worst-case asymptotic bounds. It uses more polynomial operations; the supplied implementation exceeds the 0.5-second limit and is explicitly a backup, not a full-data reference.

[Complete editorial and measurements](solution-alternative-fps.en.md) · [Program](alternative-fps.cpp)
