# Grox's Sequence V B — Rolling Stirling DP

[The C++17 implementation](alternative-stirling-dp.cpp) by Codex (GPT-6) updates one row in descending order using $S(i,j)=S(i-1,j-1)+jS(i-1,j)$. A new element forms its own group or joins one of the existing groups. Retain only columns through $t=\min(n,k)$. Time is $O(k(t+1)+\log(n+1))$, with $O(t+1)$ space. This simpler implementation suits small $k$ or few required columns.

[Statement](statement.en.md) · [Main editorial and shared derivation](solution.en.md)
