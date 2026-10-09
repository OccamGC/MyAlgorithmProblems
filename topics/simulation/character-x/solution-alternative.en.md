# Character X: Substitute into a Fixed Template

Problem setter's solution. Codex (GPT-6): preserve the template approach and verify trailing spaces. [alternative.cpp](alternative.cpp) has the same complexity as [cell testing](solution.en.md) and passes all formal inputs as a supplementary option.

Store eight strings of length ten. Use `#` for filled cells and actual spaces elsewhere. Scan each row, replacing `#` with the input character while keeping spaces, then print a newline.

Every template row matches the union of the two diagonal strips. Substitution changes only the fill character, preserving positions and dimensions, so it works for every allowed letter or digit. The internal `#` marker is never printed unchanged.

Time is $O(T+1)$ and extra space is $O(1)$ , including the fixed $80$ cells. Templates are convenient for a fixed pattern. Cell conditions are easier to adapt if dimensions or strip widths vary. Validation must compare complete lines without trimming their spaces.

See the [test plan](tests/plan.json), [generation instructions](../../../README.md#使用题目文件), and [environment and measurements](../../../docs/评测环境与性能.md).
