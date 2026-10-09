# 数据生成与检验 / Test recipes

在本题目录编译标准程序，再生成数据。只需要 C++17 与 Python 3 标准库。
Compile the reference program in this directory, then generate data. Only C++17 and the Python 3 standard library are required.

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --out-dir ../../../build/data/white-cell-board --std ./std.exe
python tests/validate.py ../../../build/data/white-cell-board/01.in
```

`--plan` 可指定计划文件，默认 `tests/plan.json`；`--case 01 --case 02` 可重复选择测试编号。省略 `--std` 时只生成输入。程序路径通过参数传入，不依赖平台专用可执行文件。输入输出使用 LF 换行；同一配方与种子生成相同输入。

Use `--plan` for another plan (default: `tests/plan.json`), and repeat `--case` to select cases. Omit `--std` to generate inputs only. The executable is supplied by the user. Input and output files use LF line endings; recipes and seeds are deterministic.

## 覆盖范围 / Coverage

唯一正式空输入检验全部21行。独立遍历所有n≤4棋盘，并与镜像行对容斥程序全表核对。

The single empty input checks all 21 lines. Exhaustive boards through n=4 and a complete-table comparison with inclusion-exclusion verify the answers.

正式文件、评分比例、固定种子与用途见 [plan.json](plan.json)。完整范围均为一组；棋盘只有一个空输入文件，其余题各十个文件。样例同步收录在双语题面和 `samples/` 中。

See [plan.json](plan.json) for cases, scores, seeds, and purposes. There is one unrestricted scoring group. The board problem has one empty input; other problems have ten inputs. Samples match the bilingual statements.

## 复核 / Verification

仓库工具 [check_r36.py](../../../../tools/check_r36.py)提供独立小规模模型与非法输入检查；[benchmark_r36.py](../../../../tools/benchmark_r36.py)重复生成正式输入，每份计时五次并另测整进程峰值。工具使用仓库 `build/R36/` 中用户编译的程序，数学前缀题还使用阈值80（小参数）和1000000的检查构建；改动的阈值不属于另一种算法。

[check_r36.py](../../../../tools/check_r36.py) supplies independent small models and invalid-input checks. [benchmark_r36.py](../../../../tools/benchmark_r36.py) reproduces formal inputs, times each five times, and separately measures whole-process peak memory. These repository tools expect user-compiled programs in `build/R36/`; summatory problems also use checking builds with thresholds 80 for small parameters and 1000000. Changing the threshold is a consistency check, not an independent algorithm.

公开的 [测量与哈希](../../../../docs/benchmark-R36.json)逐项说明验证方法；大规模共享公式的不同阈值构建不能替代独立枚举与数学证明。
The [measurements and hashes](../../../../docs/benchmark-R36.json) identify each verification method. Large runs sharing a formula do not replace independent enumeration and proof.

另可编译 `alternative.cpp`，实现取舍见对应双语题解。
Compile `alternative.cpp` for the additional method; its tradeoffs are documented in both languages.
