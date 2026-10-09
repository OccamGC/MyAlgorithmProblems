# 测试数据 / Test data

生成器仅依赖Python标准库；固定配方和种子见 [plan.json](plan.json)。
The generator uses only the Python standard library; [plan.json](plan.json) fixes all recipes and seeds.

```text
python tests/generate.py --out-dir build/data
python tests/generate.py --plan tests/plan.json --out-dir build/data --case 01 --case 02 --std ./std
```

在单题目录中运行。`--case` 可以重复；未知编号会报错。`--std` 指定已编译程序并生成对应输出。
Run inside the problem directory. Repeat `--case` to select inputs; unknown IDs are rejected. `--std` runs the compiled program to produce outputs.

小规模独立模型、输入校验、正式数据复现和五轮测量分别见仓库工具 `tools/check_r34.py` 和 `tools/benchmark_r34.py` .公开性能记录见 [benchmark-R34.json](../../../../docs/benchmark-R34.json)。正式生成文件不入库，样例文件入库。
Independent small models and validators are in repository tool `tools/check_r34.py` ; reproduction and five-run measurements are in `tools/benchmark_r34.py` . See [benchmark-R34.json](../../../../docs/benchmark-R34.json). Formal files are regenerated locally; sample files are versioned.

## 本地交互 / Local interaction

```text
g++ -std=c++17 -O2 std.cpp -o std
python judge.py --input tests/samples/02.in --program ./std --transcript trace.json
g++ -std=c++17 -O2 simulate.cpp -o simulate
```

隐藏文件先给n，再给排列。本地交互器读取隐藏文件，提交程序只收到n和逐次回复。`--std` 通过真实交互验证，并把恢复的排列保存为 ` .out` .样例输出也是该排列，不能当作交互协议的完整输出记录。`trace.json` 保存实际询问和回复。
Hidden fixtures contain n followed by the permutation. The judge reads them; the submission receives only n and replies. `--std` validates real interaction and writes the recovered permutation to ` .out` . Sample outputs have this same fixture format, not a complete protocol transcript. `trace.json` records actual queries and replies.

`simulate.cpp` 直接读取隐藏文件，只是算法验证工具，输出恢复的排列及下一行的询问次数。它与提交程序共享 `solver.hpp` .不要将模拟器提交为交互解答。
`simulate.cpp` reads a hidden fixture directly and prints the recovered permutation, then the query count on the next line. It is a testing harness sharing `solver.hpp` , not an interactive submission.

交互器会拒绝非法查询、超过800次询问、错误排列、多余输出、异常退出和超时。默认30秒是本地诊断超时；正式时限见题面及测量。
The judge rejects invalid queries, more than 800 queries, wrong permutations, extra output, unsuccessful exit, and timeout. Its default 30 seconds is a diagnostic timeout; use the statement and measurements for the evaluation limit.
