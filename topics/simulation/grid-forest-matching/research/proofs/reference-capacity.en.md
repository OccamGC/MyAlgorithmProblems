# After reference deletion: a disjointness obstruction and a capacity-two draft

Date: 2026-10-12. Following the [ten-round investigation](reference-followup.en.md).

**Subsequent audit update:** the bin argument is valid, and a finite-axis-segment proof now establishes second-axis spacing without infinite physical extension or a high-power assumption. The self-contained [general cubic proof](cubic-bound.en.md) further reduces each label's charge to four intersection budgets. Subsequent work completed independent full-charge verification and synchronized both editorials; see Section 9 of the new proof. The original draft remains below: its conditional claims, five-budget bound, and pending-audit wording are historical.

**Original draft status.** The obstruction has been independently checked against complete histories: direction A's connected-union disjointness conjecture is false. Sections 3–5 give a complete derivation draft that may close the general complexity gap, grouping by a full label length instead of requiring a disjoint union. It depends on the established physical periodic-axis extension and second-axis separation lemmas. The planned follow-up was to audit those dependencies, quantifiers, and constants. Until that audit is complete, the main editorial retains its previously confirmed bound; finite checks are not presented as a general proof.

## 1. Oppositely directed early arms give a genuine obstruction

Choose the label, three query heights, and early horizontal endpoints as

$$
h=(0,6),\qquad (r_1,r_2,r_3)=(10,23,40),\qquad (c_1,c_2,c_3)=(4,-4,2).
$$

Starting at the origin, descend column zero through these heights. At each height visit the early endpoint, then retrace the arm to the trunk. After the third early arm, revisit the heights in reverse order, going right to the late endpoint and returning to the trunk:

$$
e_i=(r_i,c_i),\qquad f_i=e_i+h.
$$

Define the sources and host roads exactly by

$$
a_i=(-r_i,0),\qquad
F=\bigcup_{i=1}^{3}\left((a_i+P_{t(f_i)})\cup(a_i+h+P_{t(e_i)})\right).
$$

This is a union of complete prefixes, not just six prescribed endpoints. It has 171 road vertices and is an induced tree; the query has 65 distinct positions. After translating into a board of side 71, a walk realizing the discovery order has 116 moves. The standard program and two independent answer algorithms agree on 1418 candidate checks. See the [official-format fixture](../examples/inputs/opposite-arms.in).

### Why the host is acyclic and the stars are genuine

There are only two vertical trunks: column zero from row minus forty to thirty, and column six from row minus forty to zero. The horizontal segment in row zero, from column minus four to ten, joins the trunks. All other arms occur at rows minus thirty, minus seventeen, minus thirteen, thirteen, seventeen, and thirty; these rows are mutually nonadjacent.

On negative rows the two arm groups have at least one empty cell between them. On positive rows the column-six trunk has already ended. Thus every arm is a pendant path, apart from the single connection in row zero.

The query first moves down. After the first successful filter, source columns can only be zero or six, since vertical edges occur only there. For a late source in column zero, a fixed target and query row allow an earlier successful point only in the late endpoint's column or six columns to its left. The former is the late point itself, which has not yet been visited; the latter uniquely specifies the stated early endpoint. Its full successful prefix is explicitly included. Thus the prescribed pairs use genuine earliest stars.

### Self-translation overlap survives reference deletion

The maximum early index is 50 and the strict cutoff is 51. The reference is in the third layer, with early and late indices 50 and 56. After deleting its class, the largest resource of the upper source covers the right interval in host row zero, while that of the second source covers the left interval:

$$
S_{a_1,e_1}\cap\{r=0\}=\{(0,c):0\le c\le4\},\qquad
S_{a_2,e_2}\cap\{r=0\}=\{(0,c):-4\le c\le0\}.
$$

The resources share a trunk and the origin, so their union is connected. Its host-axis projection interval is

$$
[-4,4],\qquad \operatorname{diam}\pi_L(U)=8>6=\ell.
$$

Consequently,

$$
U\cap(U+h)\supseteq\{(0,2),(0,3),(0,4)\}.
$$

One interval goes four steps left from zero and the other four steps right. Each is shorter than the label, but their connected union crosses a full label length. The [axis-span equivalence](reference-followup.en.md) remains valid; the hoped-for strict span bound is what fails.

The six remaining marks still have distinct early endpoints, hence admit a unit allocation in their full resources. This is neither an algorithmic complexity counterexample nor a refutation of constant capacity after reference deletion.

## 2. Paying four long-axis classes does not repair disjointness

Use seven layers with

$$
r_i=3\cdot2^{i-1}\ (1\le i\le7),\qquad
h=(0,8),\qquad c_i=6(-1)^{i+1}.
$$

Early visits run from top to bottom and late visits from bottom to top. Extend a negative early arm to column eight on its late visit, and a positive arm to column fourteen. Each source matches its full late prefix, and its shifted source matches its largest early prefix.

All nonzero layer differences are distinct multiples of three, so arms on different levels create no extra adjacency. As in the small case, the two trunks connect only in row zero, giving an induced tree. The actual marks yield seven long-early-axis classes, each with five marks. Breaking payment ties toward later classes, paying four classes and then reselecting the reference leaves the first two layers: ten marks, two sources, and a connected axis interval from minus six to six, longer than the label length eight.

Thus the obstruction survives paying four long-axis classes and deleting the new reference. However, each source has only five marks against its nine-point block; the final excess is zero. It is not a counterexample to the final excess term of Section 38.

## 3. The replacement: equal-early copies are farther apart than a label length

The following is the derivation awaiting audit. Fix a host label component and a subfamily of its high-power strict marks. Use the notation from [Sections 23 and 25–30](complexity-labels.en.md): host left translation, axis, primitive period, and label-axis length are

$$
g,\qquad L,\qquad p,\qquad \ell=qp,\qquad q\ge4,\qquad \delta=h/q.
$$

For each mark its query translation and axis are

$$
g_e=w_f w_e^{-1}=a^{-1}ga,\qquad I_e=a^{-1}L.
$$

Within the selected subfamily of this component, choose the mark with latest early index as reference, with axis

$$
J=I_{e_*}.
$$

Delete the reference-axis class. Different query axes belong to different query-intersection components, so genuine time reversal implies that every remaining source matches the complete reference late prefix. That prefix contains a reference-axis segment

$$
A\subseteq J,\qquad |E(A)|\ge\ell.
$$

Now consider two different remaining sources with **the same query early endpoint**. Their late endpoint is also the same, hence so is their query axis. Moreover,

$$
aI_e=bI_e=L,\qquad I_e\ne J,
\qquad aA\subseteq F,\quad bA\subseteq F.
$$

Both axis segments lie in the same host tree because the sources belong to the fixed host label component. The second-axis lemma of Section 30 makes them disjoint. The relative source translation preserves the host axis and moves by a nonzero integer multiple of its primitive period. The reference axis has the same period and horizontal displacement. Therefore

$$
\boxed{|\Delta_{\rm axis}(a,b)|>|E(A)|\ge\ell.}
$$

The crucial choice fixes the image of the **original query axis of an equal early endpoint**, using the reference axis as the second axis. It does not fix the reference-axis image. This reverses the roles used in Section 37.

### Expanding the second-axis argument

The relative left translation preserves the first axis, so its grid displacement is a nonzero integer multiple of the common horizontal period. The two infinite physical images of the reference axis therefore coincide. If their actual finite segments meet, unique continuation along the periodic directions from that host vertex forces the two abstract reference-axis images to coincide as well.

A nonidentity free-group left translation would then preserve two distinct axes. In the free action on the Cayley tree, a nonidentity element has a unique translation axis, which is impossible. The finite segments must consequently be separated along their common physical axis by more than their edge length.

This uses the established infinite physical periodic-axis property. Conjugacy in an abstract free tree alone does not establish the distance bound. Both full reference late prefixes, the identical physical period, and the common host tree are essential.

## 4. Binning by one label length gives capacity two

Each mark still uses its own complete early resource; define its projection's left endpoint by

$$
S_{a,e}=a+P_{t(e)},\qquad
\lambda_{a,e}=\min\pi_L(S_{a,e}).
$$

The strict cut makes each individual resource disjoint from its label translate, so

$$
\operatorname{diam}\pi_L(S_{a,e})\le\ell-1.
$$

Resources with the same early endpoint are images under a left translation preserving the host axis. Their projection-left-endpoint difference equals the axis displacement established above:

$$
e=e',\quad a\ne b\quad\Longrightarrow\quad
|\lambda_{a,e}-\lambda_{b,e}|>\ell.
$$

Group resources into the half-open bins

$$
\lambda_{a,e}\in[j\ell,(j+1)\ell),\qquad j\in\mathbb Z.
$$

**Early endpoints are distinct within each bin.** The [full-prefix Hall argument in Section 13](complexity-labels.en.md) gives a unit allocation per bin. Equivalently, assign greedily in increasing early-index order: the current complete prefix contains all earlier distinct early endpoints and the root, so an unused resource vertex always remains.

**A road vertex participates in at most two bins.** If its axis projection is

$$
x=\pi_L(z),
$$

every resource containing it has left endpoint in

$$
\lambda_{a,e}\in[x-\ell+1,x].
$$

This integer interval meets at most two bins of one label-axis length. Superposing the unit allocations therefore gives

$$
\boxed{C_{\rm nonref}\le2.}
$$

No bound on the whole connected union's span is required, and the entire road budget is not charged separately for different reference-axis images. Opposite early arms can cross a bin boundary without making a road vertex participate in unboundedly many bins.

## 5. Combining the draft into a general upper bound

The reference-axis class has unit capacity. Within one such class and host component, source differences follow the common horizontal period, so sources have the same row. If two marks have the same resource early-endpoint image, their late targets are also equal and their query early endpoints have the same row. Uniqueness of the genuine earliest star makes the marks identical. Assign this class to its resource early-endpoint images.

The strict part of a high-power component consequently has capacity at most three. For low-power components retain the established Section 27 bound:

$$
q\le3\quad\Longrightarrow\quad C\le q+1\le4.
$$

Choose references separately within host label components and sum over the disjoint components. No repeated budget across conjugacy types is needed. The part already paid at the common cut uses one additional intersection budget, giving the proposed inequality

$$
\widetilde M_h\le5|G_h|.
$$

There are at most board-side times road-count row stars, and each candidate fails at most once. Using the ordered same-row-pair identity across labels yields

$$
\begin{aligned}
W&\le(n+1)N+\sum_h\widetilde M_h\\
&\le(n+1)N+5(n-1)N=(6n-4)N.
\end{aligned}
$$

The draft thus concludes

$$
T=O(n^2+m+nN)\subseteq O(n^3+m).
$$

This does not use direction A's false disjointness conjecture, nor does it require paying four long-axis classes, source blocks, or straight-axis excess separately. The entire dependency chain requires audit; correct algebra in the last step cannot substitute for Section 3.

## 6. Completed checks and next audit

The [verifier](../verify_reference_capacity.py) and [results](../reference-capacity-results.json) record 16 inputs and 72 reference scenarios, including 10 with curved axes. They check 5667 consecutive equal-early source pairs and construct bin allocations for 10988 marks counted with scenario multiplicity. Maximum vertex use is two.

All stars in the small obstruction were also independently enumerated from complete-prefix definitions. Every answer agrees among the bitset algorithm, literal prefix enumeration, and original standard program. The seven-layer case rebuilds actual marks before filtering long spans, paying four classes, and reselecting the reference. Reused scenarios are not independent random samples.

The next turn should audit Section 3 from first principles: whether equal-early sources really share the original axis image, whether the reference late segment is completely matched, whether physical displacement and abstract axis length correspond, and whether component-local reference selection preserves reversal. Then check bin capacity and the global constant. Any gap must be recorded and the affected conclusion withdrawn; these finite checks cannot replace that work.

```text
python topics/simulation/grid-forest-matching/research/verify_reference_capacity.py --output topics/simulation/grid-forest-matching/research/reference-capacity-results.json --program build/grid-forest-matching.exe
```
