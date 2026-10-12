# Comb constructions: multiple scales and mixed heights

For a connected host, candidates after linearly many scans, exact counts for fixed template-size multiples, and why the construction still has no supercubic cost, see the illustrated [comb-tree questions](comb-candidates.en.md).

## The single-prefix product bound is tight at many scales

A uniform threshold cannot force the candidate count down to linear size early: no absolute constant $C$ makes $|P|>Cn\Rightarrow|A(P)|\le Cn$ hold for every forest.

Take an integer $s\ge2$ and set $n=4s^2$. Stack $2s$ combs. Each backbone occupies an entire row, with teeth extending down by $2s-2$ cells in every even column; leave an empty row between layers. Their induced graph is a forest. The template is a comb of width $2s^2$ with the same tooth positions and height. A translation is valid exactly when its backbone aligns with a host backbone and its starting column is even. Thus

$$
N=8s^4,\qquad |P|=2s^3,\qquad |A(P)|=2s^3+2s.
$$

Both $|P|/n$ and $|A(P)|/n$ tend to infinity, while $|P|\,|A(P)|=\Theta(nN)$. The host can also be made into a single induced tree: remove the tooth in the rightmost even column of each layer, then fill the rightmost column to connect all backbones. This gives $N=8s^4+2s$ and $|P|=|A(P)|=2s^3$, so the counterexample remains valid.

More generally, use $g=\lfloor(n+1)/(h+2)\rfloor$ layers of tooth height $1\le h\le n-1$, and template width $\lfloor n/2\rfloor$. The same construction gives

$$
N=\Theta(n^2),\qquad
|P|=\Theta(n(h+1)),\qquad
|A(P)|=\Theta\!\left(\frac{n^2}{h+2}\right).
$$

Thus the single-prefix product bound is tight at template sizes ranging from linear to quadratic. Each height here uses a different host; their costs cannot simply be added to obtain a logarithmic lower bound for one input.

## Mixed-height combs: count how long each candidate survives

The same board can contain layers of different heights. Let their positive tooth heights be $h_1,\ldots,h_g$, still separated by empty rows, with $\sum_i h_i+2g-1\le n$. Write

$$
S=\sum_i h_i,\quad H=\max_i h_i,\quad
K=|\{i:h_i=H\}|,\quad N=gn+\lceil n/2\rceil S.
$$

The query first completes its backbone from left to right, of width $2\le w\le n$. It then grows every tooth in an even column to height $H$, in any interleaving order. Let

$$
t=\lceil w/2\rceil,\qquad a=\left\lfloor\frac{n-w}{2}\right\rfloor+1.
$$

**For this restricted family, the rigorous bound is**

$$
W\le N+g\sum_{j=1}^{w-1}(n-j)+a(tS-K)\le(2n+1)N.
$$

To prove it, first note that $g(n-w+1)$ candidates remain after the backbone. All starts in odd columns fail at the first vertical filter, leaving $a$ even-column starts in each layer. In a layer of height $h_i$, each such start can successfully check at most $th_i$ new tooth cells. If $h_i<H$, it incurs one further failed check at the first excessive depth; if $h_i=H$, it survives to the end. The total after completing the backbone is therefore at most

$$
g(n-w+1)+a(tS-K).
$$

Adding the horizontal phase proves the first inequality. The second follows from $g\sum_{j=1}^{w-1}(n-j)\le nN$ and $atS\le nN$. Growing all teeth one depth level at a time attains equality in the first inequality.

The costs of the different heights therefore share the total tooth-height budget $S$ of one board. This proof does not cover arbitrary queries or arbitrary branching forests.
