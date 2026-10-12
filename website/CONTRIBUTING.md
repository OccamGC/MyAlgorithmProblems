# 新增结论、拓展问题与网站维护

网站从仓库 Markdown 和 [research-index.json](../research-index.json) 自动生成。证明正文只有一份；生成的 HTML 不需要提交。The website is built from repository Markdown and the result index. Edit the source documents, not the generated HTML.

## 添加一项研究成果

1. 在对应题目目录中新增摘要、证明或问题说明，优先提供 `.zh.md` 与 `.en.md`。可以复制 [中文成果模板](templates/result.zh.md)和[英文成果模板](templates/result.en.md)，替换所有占位内容。
2. 在 `research-index.json` 的 `results` 中添加条目。复制[索引条目模板](templates/result-entry.json)，设置唯一、稳定的小写连字符 `id`，填写中英文标题、状态、模型假设、结论和文档路径。
3. 通过 `extends`、`specializes`、`refutes` 或 `related_results` 引用其他结果的 `id`，分别表示推广、特殊情形、否定或相关问题。这些关系会出现在成果目录中。
4. 将新增文件加入 Git 暂存区，运行下面的构建与检查命令。构建器只读取 Git 已跟踪或已暂存的文档，避免发布临时文件。
5. 提交并推送到 `main`。GitHub Actions 构建、检查并发布 Pages；PR 会执行相同检查，但不会发布。

如果还没有证明，可以先记录开放问题或猜想。不要为了进入成果目录把实验支持写成已证明。

To add research, create source notes, register their stable ID and paths in the index, stage the files, and run the build. Pushes to `main` deploy automatically; pull requests are checked without deployment.

## 状态与字段

| `status` | 含义 / Meaning |
| --- | --- |
| `current_proof` | 已给出文字证明；必须提供 `proof_paths` / Written proof provided |
| `conjecture` | 待证明或证否的猜想 / Conjecture |
| `open_question` | 尚未解决的问题 / Open question |
| `experimental_evidence` | 只有有限实验支持 / Finite experimental evidence |
| `refuted_conjecture` | 已找到反例；链接到反例说明 / Refuted conjecture |
| `historical_upper_bound` | 仍有效但已有更强结论的旧上界 / Valid earlier bound |
| `historical_experiment` | 保留的历史实验，不代表一般结论 / Historical experiment |

必需字段为 `id`、`title.zh`、`title.en`、`status`，以及至少一组阅读路径：`entry_paths`、`proof_paths` 或 `documentation_paths`。所有路径都相对仓库根目录。建议同时填写 `keywords`、`assumptions`、`conclusions`、`limitations` 和复核命令。

`featured: true` 将该条目加入首页和研究导航；`summary.zh`、`summary.en` 提供首页摘要。首页的成果数量、研究目录和网站上的 Agent 导航自动更新。新增展示状态时，也需同步 `website/build.py` 的状态名称。

## 更新已有证明与引用

保留稳定 `id` 和文件路径，尽量不修改已有章节标题，从而维持页面和章节链接。修正证明时说明影响范围；若旧猜想被否定，更新其状态并通过关系字段指向反例。较早证明和实验可以继续保留，注明范围与后续结果。

新研究发布后，在 [引用说明](../CITATION.md)中增加独立条目，并使用实际包含该研究的 Git 提交作为固定版本链接。现有索引顶层的 `publication_commit` 只描述 2026-10-12 的原始研究快照；新成果可填写自己的 `publication_commit` 和 `immutable_proof_url`，不要沿用旧提交。

Keep result IDs and paths stable. Add citations using the actual commit containing the new proof. The original publication commit does not automatically apply to later results.

## 本地构建与检查

需要 Git 和 Python 3.12。仓库根目录执行：

```text
python -m venv .venv
```

Windows PowerShell 使用 `.venv/Scripts/python.exe`，Linux/macOS 使用 `.venv/bin/python`。以下命令中的 `python` 均指这个虚拟环境内的解释器：

```text
python -m pip install -r website/requirements.txt
git add <新增或修改的文件>
python website/build.py
python website/check_site.py
```

首次构建需要联网获取固定版本的 MathJax 并校验 SHA-256；文件缓存在已忽略的 `build/vendor/`。网站发布的公式脚本与字体图形自包含，页面本身无需访问公式 CDN。Material 的字体使用系统字体。

独立公式使用各占一行的 `$$` 分隔符。网站也兼容公式紧贴前后文字、未留空行的写法；`website/markdown_math.py` 在 Markdown 解析阶段保留公式原文，再交给 MathJax。代码示例中的分隔符不会被当成公式。整站检查会拦截代码块之外残留的 `$$`，避免漏渲染悄悄发布。公式兼容性回归测试可运行 `python -m unittest discover -s website -p 'test_*.py'`。

输出为 `build/pages/`，可本地预览：

```text
python website/preview.py
```

打开终端显示的本地地址。重新构建后刷新页面即可；修改生成文件会在下次构建时被覆盖。`build/` 和 `.venv/` 已被 Git 忽略。

## 自动发布的范围

`website/` 保存生成器、主题样式和维护模板；`mkdocs.yml` 保存站点设置；`.github/workflows/pages.yml` 执行检查与部署。所有默认分支推送都会触发构建，便于新增其他题目的研究而无需逐项修改触发路径。

网页复制 Git 中的 Markdown 和图示；程序、测试输入和大型证据报告的链接指向 GitHub 源文件。来源按钮保留原文访问方式。网站提供 `sitemap.xml`、`llms.txt` 和结论索引；这些入口帮助检索与阅读，不保证搜索引擎收录。

部署只需要工作流的 `pages: write` 与 `id-token: write` 权限，不需要个人访问令牌。发布目录不包含 `.git`、虚拟环境或本地研究状态文件。
