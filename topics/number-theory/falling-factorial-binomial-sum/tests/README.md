# 数据生成与检验 / Test recipes

在本题目录编译标准程序，再生成数据。只需要 C++17 与 Python 3 标准库。
Compile the reference program in this directory, then generate data. Only C++17 and the Python 3 standard library are required.

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --out-dir ../../../build/data/falling-factorial-binomial-sum --std ./std.exe
python tests/validate.py ../../../build/data/falling-factorial-binomial-sum/01.in
```

`--plan` 可指定计划文件，默认 `tests/plan.json`；`--case 01 --case 02` 可重复选择测试编号。省略 `--std` 时只生成输入。程序路径通过参数传入，不依赖平台专用可执行文件。输入输出使用 LF 换行；同一配方与种子生成相同输入。

Use `--plan` for another plan (default: `tests/plan.json`), and repeat `--case` to select cases. Omit `--std` to generate inputs only. The executable is supplied by the user. Input and output files use LF line endings; recipes and seeds are deterministic.

## 覆盖范围 / Coverage

原式逐项求和、k>n、k=n、百万块边界、随机短下降乘积与十亿上界。两种完整程序比较所有正式答案。

Literal summation, k>n, k=n, million-factor boundaries, random short falling products, and the billion limit. Both programs agree on every formal answer.

正式文件、评分比例、固定种子与用途见 [plan.json](plan.json)。完整范围均为一组；棋盘只有一个空输入文件，其余题各十个文件。样例同步收录在双语题面和 `samples/` 中。

See [plan.json](plan.json) for cases, scores, seeds, and purposes. There is one unrestricted scoring group. The board problem has one empty input; other problems have ten inputs. Samples match the bilingual statements.

## 复核 / Verification

仓库工具 [check_r36.py](../../../../tools/check_r36.py)提供独立小规模模型与非法输入检查；[benchmark_r36.py](../../../../tools/benchmark_r36.py)重复生成正式输入，每份计时五次并另测整进程峰值。工具使用仓库 `build/R36/` 中用户编译的程序，数学前缀题还使用阈值80（小参数）和1000000的检查构建；改动的阈值不属于另一种算法。

[check_r36.py](../../../../tools/check_r36.py) supplies independent small models and invalid-input checks. [benchmark_r36.py](../../../../tools/benchmark_r36.py) reproduces formal inputs, times each five times, and separately measures whole-process peak memory. These repository tools expect user-compiled programs in `build/R36/`; summatory problems also use checking builds with thresholds 80 for small parameters and 1000000. Changing the threshold is a consistency check, not an independent algorithm.

公开的 [测量与哈希](../../../../docs/benchmark-R36.json)逐项说明验证方法；大规模共享公式的不同阈值构建不能替代独立枚举与数学证明。
The [measurements and hashes](../../../../docs/benchmark-R36.json) identify each verification method. Large runs sharing a formula do not replace independent enumeration and proof.

另可编译 `alternative.cpp`，实现取舍见对应双语题解。
Compile `alternative.cpp` for the additional method; its tradeoffs are documented in both languages.

## 阶乘表 / Factorial table

```text
g++ -std=c++17 -O2 tests/generate-table.cpp -o generate-table.exe
./generate-table.exe > factorial-table.hpp
g++ -std=c++17 -O2 tests/verify-table.cpp -o verify-table.exe
./verify-table.exe
```

生成器执行约十亿次模乘，属于一次性离线工作；不要在每个输入上重建。校验器逐区间倒序相乘，使用运行时整数除法，逐项对比1001个检查点，最后验证Wilson剩余因子。程序非零退出表示失败。首次生成后重新编译使用头文件的程序。

Generation performs about one billion modular products as one-time offline work. Do not repeat it per input. The verifier multiplies each interval in reverse order using runtime division, compares all 1001 checkpoints, and checks the remaining Wilson factors. A nonzero exit status indicates failure. Recompile programs using the header after regeneration.
