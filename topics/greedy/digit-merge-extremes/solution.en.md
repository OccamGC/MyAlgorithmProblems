# Extremes after Merging Two Digits — Solution

## Method and Contributions

The preferred method is the setter's linear greedy selection of the higher digit and then its partner, distinguishing carry and no-carry cases. Codex (GPT-6) supplies the comparison proof, boundary analysis and portable C++17 implementation below. Lexicographic comparison of equal-length digits is the usual positional-notation property.


The diagram shows sample one in base ten. The two arrows give the choices producing the maximum and minimum.

![ Worked example ](assets/example.svg)

## Comparing Results

After removing leading zeros, compare lengths first and digits second. The result stays positive: a no-carry operation preserves the digit sum, while a carry leaves a digit one.

A carry retains all $n$ digits. A no-carry operation leaves at most $n-1$ . Thus, maximize by carrying whenever possible, and minimize without carrying whenever possible. Positions below refer to the original array.

For a fixed left position $i$ , a no-carry merge increases the right digit, so minimization uses the rightmost feasible partner. A carry decreases the right digit, so maximization also uses the rightmost feasible partner. Delaying the change preserves favorable earlier digits. If the added value is zero, choosing a later partner remains no worse.

## Maximum

Scan from right to left with a suffix maximum to find the rightmost position $i$ that can carry with a later digit.

When $a_i\ge2$ , replacing it by one is the first decrease. Among such operations, a later position is better; for that position choose the rightmost feasible partner.

Handle $a_i=1$ separately. It can carry only with $k-1$ , leaves the higher digit unchanged, and changes the lower digit to zero. Use the leftmost one and the rightmost $k-1$ , provided they occur in that order. Let the latter position be $q$ . If $q>i$ , this operation delays the first decrease beyond the ordinary candidate and wins. If $q=i$ , the ordinary candidate leaves one there while this candidate leaves zero, so the ordinary candidate wins. If $q<i$ , it also loses. This comparison includes the situation where the ordinary candidate itself has higher digit one.

If no pair carries, merge the first two digits. Merging the first with a later position puts the original second digit first, which is smaller than the sum of the first two. An operation starting later preserves first digit $a_1$ , whereas merging the first two produces $a_1+a_2\ge a_1$ . Equality requires $a_2=0$ ; deleting that earlier zero is no worse than deleting a later digit, as comparison at the first nonzero difference shows.

## Minimum

First consider extra leading-zero removal. If $a_2=0$ and the first digit can merge without carrying with some $j>2$ , deleting the first digit also removes at least one leading zero. This beats every result retaining $n-1$ digits. Use the rightmost feasible partner.

After excluding that case, feasible no-carry results have $n-1$ digits. A pair satisfying

$$a_i>a_{i+1},\qquad j\ge i+2,\qquad a_i+a_j<k$$

shifts the smaller digit $a_{i+1}$ into position $i$ , postponing the increase caused by addition. Choose the leftmost such descent, then its rightmost feasible partner.

Why check strict descents? Deletion shifts the digits before the partner one position left. An ascent makes the result larger at the first differing position. Equal adjacent digits allow the deletion position to move right without changing either the result or feasibility. If the first favorable change is a descent, that descent itself satisfies the displayed condition. Therefore the earliest feasible descent determines the best prefix.

If no such descent exists, choose the rightmost feasible left position and its rightmost feasible partner. The following exchanges move a candidate to the right without improving on this choice:

- At an ascent, preserving that position and operating later is better.
- At equality, moving the deletion right preserves the result.
- At a descent with no nonadjacent feasible partner, only the adjacent merge is possible. It replaces the digit by a sum and cannot decrease it. Equality means the right digit is zero, equivalent to deleting that zero, again moving the deletion right.

Repeating these exchanges reaches a rightmost feasible left position with an equally good or better result. Finally, if every pair carries, all digits are positive. Merge the first two: lower the highest digit to one and then decrease the second digit as early as possible. If the highest digit was already one, this still gives the earliest possible zero in the second position.

## Implementation and Complexity

Suffix maxima test carry feasibility; suffix minima test no-carry feasibility. The descent test must use a suffix starting at $i+2$ , excluding the adjacent partner. Each branch uses only a constant number of linear scans. Output skips the deleted position and leading zeros directly, without modifying the array.

Time is $O(n)$ and space is $O(n)$ . The sum of two digits is at most $2(k-1)<2\times10^9$ , which fits a signed thirty-two-bit integer. The complete result is never stored as an integer. The [reference program](std.cpp) uses buffered input and output.

Enumerating left positions and querying suitable right partners can also verify answers, but requires more involved result-string comparisons and $O(n\log n)$ time. The linear greedy method is preferred here.
