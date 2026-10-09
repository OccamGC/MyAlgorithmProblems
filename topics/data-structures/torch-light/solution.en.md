# Torch Lighting — Solution

## Comparing solutions

The problem setter’s solution transforms Manhattan diamonds into axis-aligned squares with $u=x+y$ and $v=x-y$ . It splits valid lattice points into the two shared parities, compresses each group, and uses rectangle differences and prefix sums. Only $u,v$ with equal parity map back to integer grid points, so the split preserves coverage without counting invalid points. The full explanation below describes this same algorithm.

Compressed bounds can be computed by endpoint-parity cases or uniformly with ceiling and floor operations. The implementation by Codex (GPT-6) uses the latter. For grid dimensions $n,m$ , both have $O((n+m)^2)$ time and space bounds, besides reading and outputting the grid.

## Transform diamonds into rectangles

Use coordinates $u=x+y$ and $v=x-y$ . The identity

$$|x-i|+|y-j|=\max\{|u-(i+j)|,|v-(i-j)|\}$$

turns the strict radius condition into a rectangle with inclusive bounds:

$$i+j-R+1\le u\le i+j+R-1$$
$$i-j-R+1\le v\le i-j+R-1$$

Apply rectangle updates with a two-dimensional difference array, then recover brightness using two-dimensional prefix sums.

## Compress by parity

Original integer grid points satisfy $u\equiv v\pmod2$ . About half the positions in a full transformed rectangle would not represent integer grid points. Build separate grids for even and odd coordinates, compressing each step of two into one index.

For each source, intersect its rectangle with each parity grid's global coordinate range, then round both bounds inward to the required parity. Skip empty rectangles and use four difference updates for every nonempty one. A radius-zero source is skipped entirely.

Some transformed integer positions still lie outside the farm. Keeping them as auxiliary positions is harmless because only actual farm cells are queried at the end.

## Correctness

The coordinate identity preserves the source region exactly, including its strict boundary. Parity splitting assigns every actual cell to exactly one compressed grid. Difference updates followed by prefix sums give each cell precisely the sum of the sources covering it. Testing whether that brightness is at most its own threshold therefore gives the required count.

## Complexity and implementation

Let $H=n+m$ . The compressed grids contain $O(H^2)$ positions in total. Time is $O(nm+H^2)$ and space is $O(H^2)$ . At maximum size, the difference arrays occupy about $74$ MiB, within the $128$ MB limit.

Apply updates as sources are read, then stream thresholds after recovering brightness; there is no need to store the full input. Use 64-bit integers for brightness and differences. The reference uses buffered input for large files.
