# 测试与复现 / Tests and Reproduction

在本题目录编译，示例使用 Windows 可执行文件名。GCC 16.2.0，实际测量选项为 `-std=c++17 -O2 -Wall -Wextra` .Python 生成器仅依赖标准库。

Compile from this problem directory; the examples use Windows executable names. Measurements use GCC 16.2.0 with `-std=c++17 -O2 -Wall -Wextra` . The Python generator uses only the standard library.

```text
g++ -std=c++17 -O2 -Wall -Wextra std.cpp -o std.exe
python tests/generate.py --plan tests/plan.json --out-dir data --std std.exe
python tests/generate.py --out-dir selected --case 01 --case 02 --std std.exe
```

`--case` 可重复指定；未指定则生成全部配方。未知编号会报错。省略 `--std` 只生成输入，提供它则运行指定程序生成 ` .out` .同一配方和种子生成相同输入。正式大数据和平台二进制不随包提交；样例已包含。

Repeat `--case` to select several recipes, or omit it for all recipes. Unknown IDs are rejected. Omit `--std` for inputs only, or supply it to generate ` .out` files by running the named executable. A fixed recipe and seed reproduce the same input. Large generated data and platform binaries are not distributed; samples are included.

## 配方 / Recipes

| ID | 分组 / Group | 分值 / Score | 目的 / Purpose |
| --- | --- | --- | --- |
| 01 | 1 | 10% | chain / literal |
| 02 | 1 | 10% | random / literal |
| 03 | 2 | 10% | chain / literal |
| 04 | 2 | 10% | star / literal |
| 05 | 2 | 10% | random / literal |
| 06 | 3 | 10% | chain / sparse |
| 07 | 3 | 10% | star / sparse |
| 08 | 3 | 10% | binary / zero |
| 09 | 3 | 10% | random / sparse |
| 10 | 3 | 10% | chain / accumulate |

## 独立验证 / Independent Validation

小规模逐点集合模型覆盖全部12操作。正式数据的小中规模使用任意更新；大规模使用全局基值加稀疏点差，并独立用距离判定路径和邻域成员，或保持全零测试任意大范围更新。包含长链、星形、二叉树、随机树、赋零、负值和接近10^18的总和。另有长标记下传回归反例。

Small literal vertex sets cover all 12 operations. Small and medium formal cases use arbitrary updates. Large cases use a global base plus sparse point differences, with independent distance-based membership, or arbitrary broad zero updates. Cases include chains, stars, binary and random trees, zero assignment, negative values, and sums near 10^18. A separate regression checks propagation of large accumulated tags.

独立小输入共 350 组，10份正式配方均重复生成并核对输入限制及分组；另检查6类非法输入。每份程序每个正式输入测时5次，并单独测峰值。

There are 350 independent small inputs. All 10 formal recipes were regenerated and checked against input and group constraints; six invalid-input classes were rejected. Each program has five timing runs per formal input and a separate peak-memory run.

## 工具和证据 / Tools and Evidence

仓库根目录的 [check_r35.py](../../../../tools/check_r35.py) 包含独立小模型和输入校验；[benchmark_r35.py](../../../../tools/benchmark_r35.py) 重新生成正式数据、交叉检查并测量。先将编译产物放在 `build/R35/<slug>-std.exe`（有补充程序时也放 `<slug>-alternative.exe`）。基准支持 `--only <slug>` ，当前峰值测量依赖 Windows。校验工具的开发断言需正常 Python 模式运行；独立公开评分器不依赖断言。

From the repository root, [check_r35.py](../../../../tools/check_r35.py) supplies independent small models and input validation. [benchmark_r35.py](../../../../tools/benchmark_r35.py) regenerates, verifies, and measures formal inputs. First place compiled programs at `build/R35/<slug>-std.exe` and, if applicable, `<slug>-alternative.exe` . The benchmark accepts `--only <slug>` ; peak-memory measurement currently requires Windows. Run development validators with normal Python assertions enabled; the standalone public checker does not rely on assertions.

[逐次测量与哈希 / Timings and hashes](../../../../docs/benchmark-R35.json) · [环境与时限校准 / Environment and calibration](../../../../docs/评测环境与性能.md)
