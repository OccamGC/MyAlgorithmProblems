# Inclusion-Exclusion by Mirror Pairs of Rows

Codex (GPT-6): application of inclusion-exclusion, grouping row sets by mirror relationships, with proof and a [calculator](alternative.cpp). This method passes the full tests and independently regenerates the answer table.

## Diagonals first

Let $A_d$ count boards with $d$ specified long diagonals forced black, while every row and column still contains white, for $d=0,1,2$ . The two single-diagonal cases are symmetric, so the answer is

$$A_0-2A_1+A_2$$

Inclusion-exclusion remains valid when the diagonals coincide for $n=1$ . Return one separately for the empty board.

## Exclude all-black rows

Choose a row set $R$ to force black, with $r=|R|$ . Let $f_j$ be the number of cells in column $j$ covered by neither these rows nor a forced diagonal. The column has $2^{f_j}-1$ colorings containing white. Columns are independent, so the contribution is

$$(-1)^r\prod_{j=1}^{n}(2^{f_j}-1)$$

Summing over all $R$ gives $A_d$ . Inclusion-exclusion cancels every board with an all-black row and retains every other board once.

For $d=0$ , every column has $n-r$ free cells:

$$A_0=\sum_{r=0}^{n}(-1)^r\binom nr(2^{n-r}-1)^n$$

For $d=1$ , the diagonal cell is already covered in $r$ columns. Each remaining column loses one additional free cell:

$$A_1=\sum_{r=0}^{n}(-1)^r\binom nr(2^{n-r}-1)^r(2^{n-r-1}-1)^{n-r}$$

A factor with exponent zero is one without evaluating its base; this avoids evaluating a nonexistent negative free-cell count.

## Force both diagonals black

Pair rows $i,n+1-i$ , giving $h=\lfloor n/2\rfloor$ mirror pairs. Suppose $t,u,v$ pairs have zero, one, or two selected rows, respectively, with $t+u+v=h$ . A one-row selection has two orientations, so the number of row sets in this category is

$$\binom ht\binom{h-t}{u}2^u$$

When a center row exists, let $c\in\{0,1\}$ indicate whether it is selected; for even orders only $c=0$ is allowed. There are $r=u+2v+c$ selected rows. The three pair categories give $2t,2u,2v$ columns with $n-r-2,n-r-1,n-r$ free cells, respectively. The center column has only one distinct diagonal cell: it joins the second category if its row is unselected, and the third otherwise.

Thus a category contributes

$$
(-1)^r\binom ht\binom{h-t}{u}2^u
(2^{n-r-2}-1)^{2t}
(2^{n-r-1}-1)^{2u+(n\bmod2)-c}
(2^{n-r}-1)^{2v+c}
$$

Sum these contributions to obtain $A_2$ . Each row set belongs to exactly one category, and all sets in a category have the same distribution of free-cell counts. Grouping therefore preserves the inclusion-exclusion sum.

## Complexity and boundaries

One order takes $O(n^2\log n)$ time. All orders through $N$ take $O(N^3\log N)$ time and $O(N^2)$ space for binomial coefficients. Use 64-bit products with immediate modular reduction and normalize subtractions. Return one for zero exponents before inspecting a free-cell count; every count actually used as an array index is nonnegative.
