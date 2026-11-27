# Grox的序列五B · 逐行 Stirling 递推

Codex（GPT-6）编写的 [C++17 实现](alternative-stirling-dp.cpp)由 $S(i,j)=S(i-1,j-1)+jS(i-1,j)$ 倒序更新一行，两项分别对应新元素单独成组或加入已有组。只需 $j\le t=\min(n,k)$ 的列。时间 $O(k(t+1)+\log(n+1))$，空间 $O(t+1)$，适用于 $k$ 小或所需列数少的输入。

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
