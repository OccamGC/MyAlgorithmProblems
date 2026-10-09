# A Certain Unscientific Arithmetic-Geometric Sum: Alternative Solution

## Division-free block concatenation

Codex (GPT-6) supplied this method and [alternative.cpp](alternative.cpp). The [main solution](solution.en.md) gives the reference based on differentiating a geometric series. With $q=c^b\bmod p$ , store for a block of length $L$

$$P=q^L,\qquad S=\sum_{j=0}^{L-1}q^j,\qquad W=\sum_{j=0}^{L-1}jq^j$$

When appending block $B$ after $A$ , every power in $B$ is multiplied by $P_A$ , and its indices increase by $L_A$ . Thus

$$P=P_AP_B,\quad S=S_A+P_AS_B,\quad W=W_A+P_A(W_B+L_AS_B)$$

Add the lengths and reduce values modulo $p$ . The empty block is $(L,P,S,W)=(0,1,0,0)$ and a one-term block is $(1,q,1,0)$ . As in binary exponentiation, repeatedly double the current block and append it to the result for set bits of the required length $L=r-l+1$ .

Substituting $i=l+j$ gives the answer

$$c^dq^l\bigl((a+bl)S+bW\bigr)\pmod p$$

The concatenation identities account for every term in both segments and preserve the four definitions. Binary concatenation produces the required length, and the substitution gives the desired range sum. Ratio $q=1$ works directly.

Time is $O(\log(b+1)+\log(d+1)+\log(l+1)+\log(r-l+2))$ with $O(1)$ auxiliary space. The method avoids inverses and a special ratio case while maintaining more products per level. Both it and the reference support the full input range.
