# 简单统计：整除分块

出题人解法；Codex（GPT-6）整理实现、边界与说明。程序：[alternative-quotient-blocks.cpp](alternative-quotient-blocks.cpp)。首选方案及比较见[主解](solution.zh.md)。

## 思路与正确性

初始保存 $F(0)=0,F(1)=1$ .读到正查询 $x$ 时，按递增顺序补齐尚未计算的值。计算 $F(n)$ 所需的 $F(\lfloor n/i\rfloor)$ 均满足 $\lfloor n/i\rfloor<n$ ，所以已经可用。

若当前分母从 $l\ge2$ 开始，设

$$q=\lfloor n/l\rfloor,\qquad r=\lfloor n/q\rfloor$$

则 $[l,r]$ 内的分母具有同一商 $q$ ，这一整段贡献 $(r-l+1)F(q)$ .累加后令 $l=r+1$ ，直到超出 $n$ .区间连续、不重不漏，恰好计算定义中的所有求和项；再对参数递增归纳，即得正确性。

## 复杂度与实现

商的不同取值有 $O(\sqrt n)$ 个：分母不超过 $\sqrt n$ 的部分至多有 $\sqrt n$ 项，其余商不超过 $\sqrt n$ .设最大正查询为 $N$ ，总时间 $O(N\sqrt N+Q+1)$ ，空间 $O(N+1)$ .无正查询时仅处理输入输出。

乘积使用 64 位整数，每块立即取模。负数和零直接返回；重复或递减查询直接查表。该方案适合需要流式读取查询的场景，代价是更高的预处理时间阶。当前时限适用性见[主解的测量](solution.zh.md#验证与运行)。
