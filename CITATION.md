# 引用仓库与网格森林研究成果

## 署名与版本 / Attribution and versions

作者使用公开署名 **OccamGC**。[CITATION.cff](CITATION.cff)描述整个仓库；引用某项数学结论时，请使用下方对应研究笔记的条目，并注明实际使用的版本。四邻接的三次方界与补树障碍引用研究提交 `640ae4ac52a1ce5a3082022162611839f97591fe`；仅对角邻接拓展引用自己的提交 `3fe652bb9f3458ed41071e5f2377141272848dbc`；八邻接拓展引用 `600f5edfc176a6c2265dac1c62e74ac94081bfbd`。这些研究版本均发布于 2026-10-12，链接分别固定到包含该成果的证明版本。

The public author name is **OccamGC**. [CITATION.cff](CITATION.cff) describes the whole repository. For a particular mathematical result, use its separate research-note entry below and identify the version actually used. The orthogonal cubic bound and tree obstructions cite research commit `640ae4ac52a1ce5a3082022162611839f97591fe`; the diagonal-only extension cites `3fe652bb9f3458ed41071e5f2377141272848dbc`; the eight-neighbor extension cites `600f5edfc176a6c2265dac1c62e74ac94081bfbd`. These research versions were published on 2026-10-12, with immutable links to versions that contain the respective results.

入口页及默认分支会继续维护；以下固定链接不会随默认分支变化。条目类型为公开研究笔记，不表示期刊或会议发表。程序复核记录是辅助证据，不替代文字证明。

Entry pages and the default branch may evolve; the versioned links below remain fixed. These are public research notes, not claims of journal or conference publication. Program checks supplement the written proofs.

## 网格森林平移匹配的三次方上界 / Cubic bound

OccamGC. (2026). *A general cubic upper bound for the candidate-list algorithm*. MyAlgorithmProblems, grid-forest-matching research note, commit `640ae4a`.

[当前摘要 / Current summary](topics/simulation/grid-forest-matching/research/results/cubic-bound.en.md) · [固定中文证明](https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/proofs/cubic-bound.zh.md) · [Versioned English proof](https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/proofs/cubic-bound.en.md)

```bibtex
@misc{OccamGC2026GridForestCubic,
  author = {{OccamGC}},
  title = {A general cubic upper bound for the candidate-list algorithm},
  year = {2026},
  month = oct,
  howpublished = {MyAlgorithmProblems research note},
  note = {Published 2026-10-12. Git commit 640ae4ac52a1ce5a3082022162611839f97591fe},
  url = {https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/proofs/cubic-bound.en.md}
}
```

## 诱导网格森林的补树障碍 / Tree-extension obstructions

OccamGC. (2026). *Induced grid forests cannot always be extended to trees*. MyAlgorithmProblems, research note, commit `640ae4a`.

[当前摘要 / Current summary](topics/simulation/grid-forest-matching/research/results/tree-extension.en.md) · [固定中文证明](https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/examples/tree-extension.zh.md) · [Versioned English proof](https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/examples/tree-extension.en.md)

```bibtex
@misc{OccamGC2026GridForestTreeExtension,
  author = {{OccamGC}},
  title = {Induced grid forests cannot always be extended to trees},
  year = {2026},
  month = oct,
  howpublished = {MyAlgorithmProblems research note},
  note = {Published 2026-10-12. Git commit 640ae4ac52a1ce5a3082022162611839f97591fe. Fixed-position induced vertex-addition model},
  url = {https://github.com/OccamGC/MyAlgorithmProblems/blob/640ae4ac52a1ce5a3082022162611839f97591fe/topics/simulation/grid-forest-matching/research/examples/tree-extension.en.md}
}
```

## 仅对角邻接拓展 / Diagonal-only extension

OccamGC. (2026). *Diagonal-only grid forests: parity decomposition and cubic bounds*. MyAlgorithmProblems, research note, commit `3fe652b`.

本项通过奇偶类格点同构，将已有四邻接三次方界、算法最坏下界和补树障碍迁移到仅对角邻接模型；它依赖上面两项结果。新版本包含完整中英文归约、验证脚本和有限验证报告。

This result transfers the orthogonal cubic bound, algorithm-specific worst-case lower bound, and tree-extension obstructions through parity-class lattice isomorphisms. It depends on the two results above. Its version contains the complete bilingual reduction, verifier, and finite evidence report.

[当前中文证明](topics/simulation/grid-forest-matching/research/results/diagonal-only.zh.md) · [Current English proof](topics/simulation/grid-forest-matching/research/results/diagonal-only.en.md) · [固定中文证明](https://github.com/OccamGC/MyAlgorithmProblems/blob/3fe652bb9f3458ed41071e5f2377141272848dbc/topics/simulation/grid-forest-matching/research/results/diagonal-only.zh.md) · [Versioned English proof](https://github.com/OccamGC/MyAlgorithmProblems/blob/3fe652bb9f3458ed41071e5f2377141272848dbc/topics/simulation/grid-forest-matching/research/results/diagonal-only.en.md)

```bibtex
@misc{OccamGC2026DiagonalGridForest,
  author = {{OccamGC}},
  title = {Diagonal-only grid forests: parity decomposition and cubic bounds},
  year = {2026},
  month = oct,
  howpublished = {MyAlgorithmProblems research note},
  note = {Published 2026-10-12. Git commit 3fe652bb9f3458ed41071e5f2377141272848dbc. Corollary of the orthogonal cubic bound and tree-extension obstructions},
  url = {https://github.com/OccamGC/MyAlgorithmProblems/blob/3fe652bb9f3458ed41071e5f2377141272848dbc/topics/simulation/grid-forest-matching/research/results/diagonal-only.en.md}
}
```

## 八邻接拓展 / Eight-neighbor extension

OccamGC. (2026). *Eight-neighbor induced forests retain the cubic bound*. MyAlgorithmProblems, research note, commit `600f5ed`.

本项沿用原完整历史收费证明，将方向词从两对扩为四对互逆符号，保留有限第二轴引理、相同检查次数上界和条带最坏下界。其固定版本包含中英文证明、八邻接验证器及 881 个完整收费实例的报告；它不建立八邻接的补树障碍。

This result extends the original complete-history charge from two to four inverse direction pairs, preserving the finite second-axis lemma, exact check bound, and stripe worst-case lower bound. Its snapshot includes bilingual proofs, the eight-neighbor verifier, and a report with 881 complete-charge cases. It does not establish eight-neighbor tree-extension obstructions.

[当前中文证明](topics/simulation/grid-forest-matching/research/results/eight-neighbor.zh.md) · [Current English proof](topics/simulation/grid-forest-matching/research/results/eight-neighbor.en.md) · [固定中文证明](https://github.com/OccamGC/MyAlgorithmProblems/blob/600f5edfc176a6c2265dac1c62e74ac94081bfbd/topics/simulation/grid-forest-matching/research/results/eight-neighbor.zh.md) · [Versioned English proof](https://github.com/OccamGC/MyAlgorithmProblems/blob/600f5edfc176a6c2265dac1c62e74ac94081bfbd/topics/simulation/grid-forest-matching/research/results/eight-neighbor.en.md)

```bibtex
@misc{OccamGC2026EightNeighborGridForest,
  author = {{OccamGC}},
  title = {Eight-neighbor induced forests retain the cubic bound},
  year = {2026},
  month = oct,
  howpublished = {MyAlgorithmProblems research note},
  note = {Published 2026-10-12. Git commit 600f5edfc176a6c2265dac1c62e74ac94081bfbd. Extension of the complete-history cubic charging proof},
  url = {https://github.com/OccamGC/MyAlgorithmProblems/blob/600f5edfc176a6c2265dac1c62e74ac94081bfbd/topics/simulation/grid-forest-matching/research/results/eight-neighbor.en.md}
}
```
