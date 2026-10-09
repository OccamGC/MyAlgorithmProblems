# Rhino Tank — Solution

## Comparing solutions

The problem setter’s row DP records, for each column, either a color $c$ that has remained constant or an non-monochromatic state. When adding a row, it enumerates which still-constant columns change: unchanged columns use the prescribed-color probability, changed ones use the sum of other colors, and mixed columns are unrestricted. It subtracts compatible monochromatic rows and clears the colors of changed columns. Once mixed, a column cannot become monochromatic again. These transitions are disjoint and exhaustive; the answer ends with every column mixed.

For side length $n$ and $m$ colors, there are $(m+1)^n$ abstract states, at most $2^n$ transitions per state, and $O(n+m)$ work per transition. The DP time bound is $O(n(n+m)2^n(m+1)^n)$ . The problem setter’s code uses three bits per column, additionally scanning $8^n$ encodings per row and storing them: $O(n8^n)$ extra scan time and $O(8^n+n^2m)$ space. The implementation used by Codex (GPT-6) applies inclusion–exclusion to monochromatic columns, with $O(n^2(m+1)^n)$ enumeration time and $O(n^2m)$ space. Both share probability-normalization preprocessing. It removes subset transitions and exponential DP arrays, using signed inclusion–exclusion instead.

## Inclusion-exclusion over constant columns

Call a row or column monochromatic when all its entries are equal. Require every row to be non-monochromatic, then use inclusion-exclusion to eliminate monochromatic columns. For each column choose either no restriction or a forced color $c$ , giving $(m+1)^n$ states.

Let $S$ be the restricted columns and $c_j$ the forced color of column $j$ . The state's sign is $(-1)^{\lvert S\rvert}$ . With these restrictions fixed, rows involve disjoint independent positions, so multiply their probabilities of satisfying the restrictions while remaining non-monochromatic.

## The probability for one row

Precompute $R_{i,c}=\prod_{j=1}^{n}p_{i,j,c}$ , the probability that row $i$ is entirely color $c$ . Define

$$Q_i=\prod_{j\in S}p_{i,j,c_j}$$

with empty product $1$ . The required row probability $G_i$ is:

- If $S$ is empty, $G_i=1-\sum_c R_{i,c}$ .
- If all restricted columns specify one color $c$ , $G_i=Q_i-R_{i,c}$ .
- If at least two colors are specified, the row cannot be monochromatic, so $G_i=Q_i$ .

The answer is

$$\sum_{S,\,(c_j)_{j\in S}}(-1)^{\lvert S\rvert}\prod_{i=1}^{n}G_i$$

## Correctness

Apply inclusion-exclusion to the event that each column is monochromatic. Distinct forced colors for one column are disjoint events, so their probabilities can be summed when that column is selected. The enumeration lists all these intersections. For each row, the formulas remove exactly the monochromatic cases compatible with the column restrictions. Independence allows multiplication over rows. Inclusion-exclusion therefore leaves precisely the matrices with no monochromatic row or column.

## Complexity and implementation

Each column state takes $O(n^2)$ time, for $O(n^2(m+1)^n)$ enumeration time. Binary exponentiation computes one denominator inverse per position; preprocessing takes $O(n^2(m+\log P))$ time. Space is $O(n^2m)$ . All arithmetic is modulo $P$ , with subtraction normalized to a nonnegative residue.
