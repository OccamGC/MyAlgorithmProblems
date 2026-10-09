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
