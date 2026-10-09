# 数据生成与检验 / Test Generation and Verification

使用 C++17 与 Python 3 标准库。在本题目录运行：
Use C++17 and the Python 3 standard library. Run in this problem directory:

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
g++ -std=c++17 -O2 -Wall -Wextra alternative-forward.cpp -o alternative-forward.exe
python tests/generate.py --out-dir ../../../build/data/town-editing-simoleons-2 --std ./std.exe
python tests/validate.py ../../../build/data/town-editing-simoleons-2/01.in
```

[plan.json](plan.json)记录10份正式文件，每份10%，包含种子、用途及验证方法。`--plan` 可指定其他计划；重复 `--case 01 --case 02` 选择文件；省略 `--std` 只生成输入。使用LF换行，未知编号被拒绝。提供程序时，生成器核对输出后才写入答案。

[plan.json](plan.json) specifies ten files worth 10% each, with seeds, purposes, and verification methods. Use `--plan` for another plan and repeat `--case` to select files. Omit `--std` to generate inputs only. Files use LF endings, and unknown IDs are rejected. With an executable, its answer is checked before an output file is written.

## 预期答案的依据 / Expected Answers

- 01～03：展开居民，使用精确 Fraction 网格递推。
- 04：没有更富的外部居民，最优值就是初始财富。
- 05、06、09、10：按相同初始均值分组，从逐人操作构造下三角矩阵，再用通用矩阵快速幂处理总人数；不用标准程序的系数尾和公式。
- 07、08：两份一般百万家庭输入的固定预期值，已由逆序系数法和前向卷积法交叉核对；依赖题解证明，不声称这两份使用独立全量暴力验证。

- 01–03: expand residents and use an exact Fraction grid recurrence.
- 04: no outsider is richer, so initial target wealth is optimal.
- 05, 06, 09, 10: group equal initial means, build the one-person matrix directly, and use generic matrix exponentiation on total populations. This does not use the reference’s coefficient-tail formula.
- 07, 08: fixed expectations for two general million-household inputs, cross-checked between backward coefficients and forward convolution. These rely on the solution proof and are not independently brute-forced at full size.

覆盖目标人数1与20、多人目标必须拆开的反例、精确分数、全贫或等富、不同均值排序、近万亿总人口，以及较富人口数恰为模数前后值的情况。输入合法性检查在 Python 的 `-O` 模式下仍然有效。

Coverage includes 1 and 20 targets, cases where targets must split temporarily, exact fractions, no richer outsiders, equal means, sorting distinct ratios, population near one trillion, and rich population counts immediately around the modulus. Validation remains effective under Python’s `-O` mode.

## 仓库级复现 / Repository Checks

将两份程序分别编译至仓库中的以下位置：
Compile both programs to these repository paths:

```text
build/R40/town-editing-simoleons-2-std.exe
build/R40/town-editing-simoleons-2-alternative-forward.exe
```

随后在仓库根目录运行：
Then run from the repository root:

```text
python tools/check_r40.py
python tools/benchmark_r40.py
python tools/draw_r40_figures.py
```

[独立检验](../../../../tools/check_r40.py)比较720组精确分数与矩阵输入、26816次任意子集平均、15组大人数矩阵检验，并测试非法输入及错误输出的拒绝。

The [checker](../../../../tools/check_r40.py) covers 720 exact-fraction and matrix inputs, 26816 arbitrary subset averages, 15 large-population matrix checks, and rejection of invalid inputs and outputs.

[性能工具](../../../../tools/benchmark_r40.py)重新生成并检验全部正式数据，每份程序计时五次并单独测峰值内存，检查样例和命令行行为。[原始测量与哈希](../../../../docs/benchmark-R40.json)列出两种程序的逐次结果。参考时限由标准程序最慢中位数乘2，再向上取整至0.5秒；换平台须重新校准。

The [benchmark tool](../../../../tools/benchmark_r40.py) regenerates and validates every formal input, records five timings and a separate peak-memory run per program, and checks samples and CLI behavior. [Measurements and hashes](../../../../docs/benchmark-R40.json) provide individual results for both methods. The limit is twice the slowest reference median, rounded up to 0.5 seconds; recalibrate on another platform.
