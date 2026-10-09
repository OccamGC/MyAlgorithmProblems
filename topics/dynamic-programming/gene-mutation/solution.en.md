# Gene Mutation — Solution

## Comparing solutions

The problem setter’s solution processes the difference between the two interpretations digit by digit. For prefixes strictly below the bound, it retains only small absolute differences. A sufficiently positive difference makes the result irreversible, so every remaining suffix is counted at once; a sufficiently negative difference is discarded. The prefix still equal to the bound is handled separately. The recurrence and irreversible-threshold proof below also justify this compression.

The implementation by Codex (GPT-6) includes tightness in a unified state and uses proved positive and negative saturation thresholds. With $L$ digits and base parameter $n$ , bounded-difference DP takes $O(Ln^2)$ time and $O(L+n)$ space including input.

## Track both comparisons

Let $L=\max(L_A,L_B)$ , pad the shorter number with leading zeros, and process digits from most to least significant. A tight flag $t$ records whether the chosen prefix still equals the prefix of $B$ . Also track the difference between the abilities of the processed prefixes, $d=F(x_{\mathrm{prefix}})-F(A_{\mathrm{prefix}})$ .

If the standard digit is $a_i$ and the chosen digit is $c$ , the new difference is

$$d'=md+c-a_i$$

When tight, choose $0\le c\le b_i$ ; otherwise choose $0\le c<n$ . The new flag is $t\land(c=b_i)$ .

## Bound the difference state

Set $T=n-1$ . If $d\ge T$ , then $m\ge2$ and $c-a_i\ge-T$ imply $d'\ge2T-T=T$ . The difference will remain positive forever, so store only $T$ . Similarly, a difference at most $-T$ stays negative and can be stored as $-T$ .

Clamp each updated difference to $[-T,T]$ . Interior states retain exact values; the endpoints represent permanently positive or negative differences. No full large integer is needed.

Let $\mathrm{dp}[d][t]$ count prefixes in a state. Start with $\mathrm{dp}[0][1]=1$ , apply the transitions using two rolling layers, and reduce counts modulo the modulus. After the last digit, sum states with $d>0$ .

## Correctness

The tight flag enumerates exactly the fixed-length digit strings at most $B$ . Leading-zero padding gives each candidate integer one representation. The difference recurrence follows the positional-weight formula. Clamping preserves the final strict comparison because the sign of an endpoint state can never change. Induction therefore shows that the DP counts every state correctly, and the positive states contain exactly the valid candidates.

## Complexity

There are $O(n)$ difference states and at most $n$ digit choices per state. Time is $O(Ln^2)$ . Storing the input and two DP layers takes $O(L+n)$ space.
