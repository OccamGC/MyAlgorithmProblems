# 剑与暴击：数据与评测 / Tests and evaluation

## 题目包 / Package

十个正式测试点各占 10%。只交付源码、固定种子生成配方和三个样例；正式输入、答案及二进制生成到忽略的 `build/` 目录。双语题面与样例文件逐字一致。

There are ten scored input files worth 10% each. Sources, deterministic recipes, and three samples are delivered; formal inputs, answers, and executables are generated under the ignored `build/` directory. Both statements match the sample files exactly.

| 编号 / IDs | 分值 / Score | 目的 / Purpose |
| --- | --- | --- |
| 01–02 | 20% | Exhaustive checks; zero/certain probabilities, multiplier one, equality and truncation |
| 03–05 | 30% | Large sword counts, thresholds up to $2\cdot10^7$ , quotient boundaries and dense-DP stress |
| 06–07 | 20% | Medium enumeration, signed integer boundaries and conceptual products beyond 64 bits |
| 08 | 10% | Five independent $n=44,q=1$ collections; comparison-sort stress |
| 09 | 10% | One $n=28,q=5600$ collection with distinct prime multipliers; repeated binary-search stress |
| 10 | 10% | Two $n=30,q=1700$ collections plus the maximum small-threshold workload |

第 08 点使用互不相同的整数倍率，不能合并相同倍率的剑。第 09 点使用互不相同的质数，截断前的不同子集乘积也互不相同，避免靠合并相同乘积大幅减少查询规模。第 10 点同时覆盖两种算法的总工作量。

File 08 uses distinct integer multipliers, preventing grouping identical swords. File 09 uses distinct primes, so distinct subsets also have distinct products before pruning; product deduplication cannot substantially collapse its query workload. File 10 combines both algorithm branches.

## 再生成 / Reproduction

从题库根目录执行，需要 C++17 编译器及 Python 3.10 或更新版本的标准库。

Run from the repository root with a C++17 compiler and Python 3.10 or newer:

```text
python3 topics/probability/swords-and-crits/tests/verify.py --cxx g++
python3 topics/probability/swords-and-crits/tests/generate.py --out-dir build/data/swords-and-crits --std build/swords-and-crits/std.exe
python3 topics/probability/swords-and-crits/tests/validate.py build/data/swords-and-crits/08.in --group 4
python3 tools/benchmark_swords.py
python3 topics/probability/swords-and-crits/tests/stress-smoke.py --timeout 5
```

`std.cpp` 可单独编译、直接提交，不依赖自定义头文件。辅助程序定义 `SWORDS_LIBRARY_ONLY` 后复用标程的函数；它们不改变标程的独立编译方式。生成器支持 `--plan` 、可重复的 `--case` 、`--out-dir` 及可选的 `--std` .不传 `--std` 时只生成输入。

The reference is self-contained and uses no custom headers. Auxiliary programs define `SWORDS_LIBRARY_ONLY` to reuse its functions; ordinary standalone compilation is unaffected. The generator accepts `--plan` , repeated `--case` options, `--out-dir` , and optional `--std` . Without `--std` , it generates inputs only.

## 正确性与整数检查 / Correctness and integer checks

- Python oracle 用独立的任意精度整数分布验证小实例，其大整数只用于测试对照，不是题目求解的依赖。
- C++ 暴力直接枚举触发集合，不复用确定性预处理或赔率变换。
- 强制分别执行整除 DP 与折半枚举，交叉核对两条分支。
- 用 Python 精确整数验证乘前截断、乘积不等式、向上整除、整数平方根，以及八项模乘累加的最坏数值。
- 检查非法输入拒绝、总查询数和两类工作量预算、固定种子生成、CLI 输出、双语样例；将标程单独放入隔离目录编译。

The independent Python oracle uses exact arbitrary-precision products only as a test reference; solution programs require no big integers. The C++ brute force omits deterministic preprocessing and odds. Checks force both main branches, exercise signed arithmetic and accumulator boundaries, reject malformed input, verify budgets and deterministic CLI generation, compare bilingual samples, and compile the reference in isolation.

完整计数与源文件哈希见[正确性记录](../../../../docs/verification-swords-and-crits.json)。标程、暴力、流式解法、强制分支、排序见证、二分见证和稠密 DP 见证共七种实现参加小规模验证。

The [verification record](../../../../docs/verification-swords-and-crits.json) contains counts and hashes for seven implementations: reference, brute force, streaming, forced branches, sorting, binary search, and dense DP.

## 时限校准 / Time calibration

参考环境为 Intel Core Ultra 9 275HX、Windows 11、GCC 16.2.0；编译选项为 `-std=c++17 -O2 -DNDEBUG -Wall -Wextra -Wpedantic` .每份正式输入先交叉核对三种程序的输出并测量峰值工作集，再各计时五次，交替运行顺序。取每例中位数及各程序最慢的中位数；计时含启动和输入输出，不含生成数据。全部原始记录见 [SC2](../../../../docs/benchmark-swords-and-crits.json)和[参考环境](../../../../docs/评测环境与性能.md)。

Measurements use an Intel Core Ultra 9 275HX, Windows 11, GCC 16.2.0, and the flags above. Every formal input has cross-checked outputs and a separate peak-memory run, followed by five interleaved timing runs. Per-input medians include startup and I/O but exclude generation. See [SC2](../../../../docs/benchmark-swords-and-crits.json) and the [shared environment](../../../../docs/评测环境与性能.md).

| 程序 / Program | 最慢中位数 / Worst median (s) | 定位 / Role |
| --- | ---: | --- |
| `std.cpp` | 0.898646 | Quotient DP + ordered generation + linear scans |
| `slow-sort.cpp` | 2.932093 | Unsorted enumeration followed by comparison sorting |
| `slow-binary.cpp` | 2.626888 | Ordered generation but a binary search for each left state and query |

参考时限为 **2 秒**，内存限制 **256 MiB**。时限等于标程最慢中位数乘 2，再向上取整至 0.5 秒。两份慢程序也使用 64 位整数、乘前剪枝、概率前缀和、区间结算及八项模乘批量归约，主要差别为建表或查询方式。标程峰值工作集为 **149.54 MiB**。

The reference limit is **2 seconds** with **256 MiB** memory. The limit doubles the reference's worst median and rounds upward to 0.5 seconds. Both slow witnesses also use 64-bit arithmetic, pruning before multiplication, probability prefix sums, block aggregation, and batched modular products; their principal difference is construction or query strategy. The reference's peak working set is **149.54 MiB**.

两份代表性慢程序均超过时限，较接近者的分离倍率为 **1.313×**，同时保留标程两倍的通过余量。有限测试不证明全部同阶实现都必然超时；基数排序等同等有效复杂度的方法不属于应排除范围，目标 OJ 仍须重新测量。

Both representative slow programs exceed the limit. The closer witness has a **1.313×** separation ratio, while the reference retains a factor-of-two passing margin. Finite tests do not prove that every implementation in an asymptotic class must time out. Equivalent effective bounds, such as radix sorting, remain valid; remeasure on the target judge.

## 补充资源检查 / Additional resource checks

优化稠密 DP 会跳过零状态，并复用一个分布回答所有询问；四分流式解法有明确空间优势，但增加时间。正式压力点的限时结果，以及单独标注为 $n=40,q=1$ 的内存比较，见[资源记录](../../../../docs/stress-swords-and-crits.json)。小实例内存对比不代表完整规模峰值。

The dense witness skips zero states and reuses one distribution for all queries. The four-list streaming companion uses less space at the cost of time. See the [resource record](../../../../docs/stress-swords-and-crits.json) for bounded formal stress checks and a separately identified $n=40,q=1$ memory comparison, which is not a full-range peak measurement.
