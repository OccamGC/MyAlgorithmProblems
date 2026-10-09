# 数据生成与检验 / Test recipes

仅需 C++17 与 Python 3 标准库。在本题目录执行：
Only C++17 and the Python 3 standard library are needed. Run in this problem directory:

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --out-dir ../../../build/data/single-member-household --std ./std.exe
python tests/validate.py ../../../build/data/single-member-household/01.in
```

[plan.json](plan.json)列出固定种子、用途及10份各占10%的正式文件。`--plan` 可指定其他计划；重复 `--case 01 --case 02` 选择编号；省略 `--std` 只生成输入。输出使用LF换行。提供参考程序时，生成器独立计算预期结果并核验输出。

[plan.json](plan.json) lists fixed seeds, purposes, and ten formal files worth 10% each. Use `--plan` for another plan and repeat `--case` to select files. Omit `--std` to generate inputs only. Text uses LF line endings. When an executable is supplied, the generator derives expected results independently and checks its output.

## 覆盖与独立模型 / Coverage and Independent Models

小例展开每名居民，使用精确 Fraction 平均和直接财富公式；大例按整比例尺人均财富建立直方图，逆序累计各财富档的贡献。大例的大小比较由结构界确定，不复制标准程序的逆向阈值分支。包含百万家庭、最多近2000万人、全等人均财富、贫富混合、单个外部成员、精确相等和指数级接近相等的情况。样例7的真实前三项为31/24、29/12、1/8.

Small cases expand individual residents and use exact Fraction averages. Large cases group equal scaled per-capita values and sum their contributions in reverse order. Structural bounds decide the large-case branches, independently of the reference's backward threshold code. Cases cover one million households, nearly twenty million people, equal means, mixed wealth, one outsider, exact equality, and exponentially small differences. The true first three values in sample 7 are 31/24, 29/12, and 1/8.

## 仓库检验工具 / Repository Checks

先将标准程序编译至仓库 `build/R39/single-member-household-std.exe` . 在仓库根目录执行：
Compile the reference to the repository's `build/R39/single-member-household-std.exe` , then run from the repository root:

```text
python tools/check_r39.py
python tools/benchmark_r39.py
```

[独立检验工具](../../../../tools/check_r39.py)检查39600次任意子集平均不增加势函数，穷举2000组外部家庭分区，并验证600组精确有理数输入、420组阈值网格、5组近相等和1组精确相等输入。还检查非法输入与错误输出的拒绝。

The [independent checker](../../../../tools/check_r39.py) tests 39600 arbitrary subset averages against the potential and exhaustively partitions outsiders in 2000 instances. It also checks 600 exact-rational inputs, 420 threshold-grid cases, five near-equality cases, one equality case, and rejection of invalid inputs and outputs.

[性能工具](../../../../tools/benchmark_r39.py)验证确定性生成、全部正式答案和命令行选项，逐份计时五次并另测整进程峰值。记录见[逐次耗时与哈希](../../../../docs/benchmark-R39.json)。时限为标准程序最慢中位数的两倍，向上取整至0.5秒；其他环境需重新校准。

The [benchmark tool](../../../../tools/benchmark_r39.py) verifies deterministic generation, all formal answers, and command-line options. It records five timings per input and separately measures whole-process peak memory; see [timings and hashes](../../../../docs/benchmark-R39.json). The limit is twice the slowest reference median, rounded up to 0.5 seconds. Recalibrate on another platform.
