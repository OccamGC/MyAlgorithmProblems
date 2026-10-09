# Elite Combatant Solution

## Comparing solutions

The problem setter’s method compresses positive-attack enemy types into subset states, storing the largest reachable health for each cleared subset. The treatment of nonpositive-attack enemies and grouping consecutive removals of one type are also inherited. With the same cleared set, higher health cannot restrict future choices, so only its maximum matters. Cumulative damage during a removal is quadratic in the attack count; survival requires its intermediate maximum, not merely its final value.

The peak occurs at integer positions near the quadratic vertex. The implementation by Codex (GPT-6) uses a discrete peak test and portable big-integer arithmetic, handling peaks and intermediates beyond 64 bits exactly at the cost of big-integer overhead. With $k$ positive-attack types, the subset DP has $O(2^k)$ states and $O(k2^k)$ transitions; preprocessing and arithmetic costs are detailed below.

## Put combat into a useful order

Each unit of type $i$ needs $t_i=\lceil h_i/A\rceil$ attacks; its actual count is $c_i$ . Ignore types with zero units.

First fix the dog's choice. The number of attacks required by each remaining unit is fixed, so the total number of combat turns does not depend on their order.

Consider an attack against a nonpositive-attack unit immediately followed by the complete processing of one positive-attack type. Swap these two parts: finish the positive-attack type first, then make that single attack. Every positive unit dies no later, while the nonpositive unit dies no earlier, if this attack eliminates it at all. At each corresponding turn, the total enemy attack cannot increase, so Boris's health is never lower than under the original order. Moving a complete type also respects the type lock. Repeating this exchange places every attack against nonpositive-attack units after all positive-attack types.

Within one positive-attack type, finish individual enemies one at a time. Each unit requires $t_i$ attacks, so the $j$-th elimination cannot occur before attack $jt_i$ against that type. Finishing units individually attains every one of these earliest times. This minimizes the number of surviving units at every turn and cannot increase net damage. The type lock requires processing the entire type consecutively, leaving only the order of positive-attack types to decide.

Removing a nonpositive-attack type with the dog cannot improve on the health-boost option: retaining those enemies until the end causes no damage and may provide healing. Only the health boost and removal of one present positive-attack type need consideration.

## Total damage and the dangerous moment

For the type currently being processed, let $c$ be its count, $a>0$ its attack, and $t$ the attacks needed per enemy. Let $B$ be the attack sum of all other surviving units, including negative attacks from healers.

After eliminating $k$ units of this type, cumulative net damage is

$$D(k)=ktB+a\left(\frac{tk(2c-k+1)}2-k\right),\qquad 0\le k\le c$$

The term $-ak$ accounts for each eliminated unit missing its final retaliation. Net damage may be negative.

For $t>1$ , also consider the moment after eliminating $k$ units and reducing the next to one hit from elimination:

$$Q(k)=D(k)+(t-1)\bigl(B+a(c-k)\bigr),\qquad 0\le k<c$$

On the nonlethal turns between consecutive eliminations, net damage per turn is constant. A maximum therefore occurs just after an elimination or just before one. Include the initial damage $0$ as well.

Both sequences are concave quadratics. Their forward differences avoid floating-point vertex calculations:

$$D(k+1)-D(k)=t(B+ac)-a-ta\,k$$

$$Q(k+1)-Q(k)=t\bigl(B+a(c-1)\bigr)-ta\,k$$

For first difference $L$ and a decrease of $s=ta>0$ per step, a maximizing index is $0$ if $L\le0$ , otherwise $\lceil L/s\rceil$ , clamped to the valid index range. Evaluate the sequence there. Health at the start of this type must be **strictly greater** than the maximum cumulative damage.

Checking health only after the entire type is eliminated is insufficient. With $c=2,t=3,a=4,B=-5$ , cumulative net damage after successive turns is $3,6,5,4,3,-2$ . Starting from $5$ health would appear to give a final health of $7$ , but Boris actually fails on the second turn.

## Subset dynamic programming

Let $S$ contain the remaining positive-attack types and let $f[S]$ be the largest reachable health. There are at most $20$ such types.

- The boost initializes $f[\mathrm{All}]=H+\Delta H$ .
- Removing type $i$ initializes $f[\mathrm{All}\setminus\{i\}]=H$ .
- Unreachable states have value $-1$ .

For each state and next type, determine $B$ from $S$ , remembering that all nonpositive-attack units are still alive, and check the damage peak. If current health exceeds it, update the state without that type using $f[S]-D(c)$ . For the same remaining set, greater health is always at least as useful, so only the maximum is needed. Process masks in descending order: every transition clears one bit and therefore reaches a smaller mask. If the empty set remains unreachable, output `leave!` .

## Finish the harmless and healing units

First reduce every remaining unit to one hit from elimination, without eliminating any. If their total healing per turn is $R$ , this stage restores

$$R\sum_i c_i(t_i-1)$$

Then eliminate units in ascending order of individual healing $-a_i$ . Swapping adjacent eliminations shows that keeping the larger healer alive for an extra turn is better. For $c$ identical units with healing $r$ each, with other surviving units healing $R'$ in total, this stage restores

$$cR'+r\frac{c(c-1)}2$$

If a nonlethal attack occurs after an elimination, moving it just before that elimination kills nothing earlier and preserves one more turn of healing from the eliminated unit. Repeating this exchange places all nonlethal attacks first; then use the elimination order above. Health never decreases during this phase, so no further survival check is needed. Its total healing is also independent of the earlier order of positive-attack types.

## Complexity and exact arithmetic

Let $P$ count present positive-attack types, $K$ declared types, and $N$ units. Hash-based name lookup takes expected $O(K+N)$ input work, plus name bytes. The remaining work takes $O(P2^P+K\log K)$ time and $O(2^P+K)$ space, plus name storage.

Signed 64-bit answers are insufficient. With $50000$ enemies each having health $10^5$ and attack $-10^5$ , and Boris's attack equal to $1$ , the nonlethal preparation stage alone restores $24999750000000000000$ health.

There are at most $N\cdot10^5$ turns, each with absolute attack sum at most $N\cdot10^5$ . Values are bounded in magnitude by $2.5\times10^{19}+2\times10^9$ . The reference uses an exact signed representation `High * 1000000000 + Low` with $0\le\mathrm{Low}<10^9$ . Normalize after addition and subtraction. Split a nonnegative multiplier into high and low parts so every machine-integer product fits 64 bits. This requires neither compiler-specific integer types nor third-party libraries. Peak indices use ordinary 64-bit arithmetic; no floating point is needed.

In the code, `InitialHealth` , `BorisAttack` , and `HealthBonus` correspond to $H,A,\Delta H$ ; `PositiveKinds` corresponds to $P$ . Here $P$ counts present positive-attack types, while $K$ counts all declared types.
