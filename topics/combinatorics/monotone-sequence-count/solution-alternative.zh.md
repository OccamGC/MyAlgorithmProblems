# 某不科学的单调序列计数: 补充解法

## Pascal 递推：出题人解法

[alternative.cpp](alternative.cpp) 计算[主解证明的组合数](solution.zh.md)。令 $a=n+m-1$ 、$t=\min(n,m-1)$ ，初始 $C_0=1$ ，其余为零。对行号 $i=1,\ldots,a$ ，按 $j=\min(i,t),\ldots,1$ 倒序更新

$$C_j\leftarrow C_j+C_{j-1}\pmod p$$

更新前两个值都来自上一行，正是 Pascal 恒等式。倒序保证 $C_{j-1}$ 尚未被覆盖；每行完成后 $C_j=\binom{i}{j}$ ，因此最后 $C_t$ 为答案。$t=0$ 时始终为一。

时间 $O((n+m)t)$ ，辅助空间 $O(t)$ .此法只做加法，不依赖质数或逆元，支持完整数据；本题首选乘积法减少运算和存储。Codex（GPT-6）把出题人的二维表改为滚动数组，保留同一递推。
