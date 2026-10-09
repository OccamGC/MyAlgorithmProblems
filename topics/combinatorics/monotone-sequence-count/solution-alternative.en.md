# A Certain Unscientific Count of Monotone Sequences: Alternative solution

## Pascal recurrence: the setter's solution

[alternative.cpp](alternative.cpp) evaluates the coefficient proved in the [main editorial](solution.en.md). Set $a=n+m-1$ , $t=\min(n,m-1)$ , initialize $C_0=1$ and all other entries to zero. For each row $i=1,\ldots,a$ , update in descending order $j=\min(i,t),\ldots,1$ :

$$C_j\leftarrow C_j+C_{j-1}\pmod p$$

Both values on the right then belong to the previous row, exactly implementing Pascal's identity. Descending order prevents overwriting $C_{j-1}$ too early. After the row, $C_j=\binom{i}{j}$ ; consequently the final $C_t$ is correct. If $t=0$ , the value remains one.

Time is $O((n+m)t)$ and auxiliary space $O(t)$ . The method uses addition only, needs neither a prime modulus nor inverses, and passes the complete tests. Products are preferred here for less computation and storage. Codex (GPT-6) replaced the setter's two-dimensional table with rolling storage while retaining its recurrence.
