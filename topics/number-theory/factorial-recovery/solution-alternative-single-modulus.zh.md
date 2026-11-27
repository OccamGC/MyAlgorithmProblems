# 数据恢复 · 单模数还原

Codex（GPT-6）编写的 [C++17 实现](alternative-single-modulus.cpp)以倍增和模加完成精确乘法，最大加法中间值小于 $2M$。每次乘法至多进行 $O(\log M)$ 次模加。

$M=7\cdot2^{52}+1$ 与十互质，且大于缺失前缀。算得 $(n!-s)10^{-k}\bmod M$ 已唯一确定前缀，后缀原样输出以保留前导零。只保存 $k$ 位后缀及常数个整数。

[题面](statement.zh.md) · [主解与共同推导](solution.zh.md)
