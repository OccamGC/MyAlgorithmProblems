# {{English Problem Title}}

<!-- Typography: write variables in inline math. Insert one actual U+00A0 nonbreaking space character before prose punctuation following inline math or code; use the ASCII period . for a following full stop in both languages. Do not write HTML entities. Omit sentence commas and periods at the end of display equations. Preserve mathematical punctuation inside formulas, fenced code, and sample data. -->

- Indicative time limit: {{estimated seconds measured in the reference environment}} s (reference environment: {{environment ID}}; for guidance only)
- Actual time limit: {{multiplier, 2 by default}} times the reference solution's baseline runtime on its slowest official test file in the target judging environment, rounded up in 0.5 s increments; if the judge supports only coarser increments, round up again to a supported value.
- Memory limit: {{value and unit}}

## Story

{{Introduce the task through a short fictional setting. You may retain the original plot or create a new story. Do not place rules that affect the answer only in this section.}}

{{If Codex rewrote the story without retaining its main original plot, add a final line such as “(This story was rewritten by GPT-6 Sol.)”, using the actual model. Otherwise delete this line.}}

## Formal Problem Statement

{{Define all objects, variables, indices, and operations. State which inputs are valid, what must be computed, and what the answer means. This section must stand on its own.}}

{{You may replace variable letters or notation with clearer choices. Define abbreviations alongside full names when helpful, or add a compact notation table. If a key formula is hard to interpret, add a strictly equivalent version using full names or an explanation in words. Keep notation aligned with the Chinese statement, solution, and code. Delete this guidance after drafting.}}

{{Redraw source figures that explain the problem, save them in assets/, and embed them with Markdown image syntax next to the relevant rules or samples. Prefer SVG. Provide descriptive alternative text and captions, and use more than color to distinguish elements. Both languages may share figures with common symbols and provide their own captions. Do not replace explanatory figures with prose, tables, or ASCII art. Keep the formal definitions complete. Delete this guidance after drafting.}}

## Input Format

{{Describe every line or test case in input order, including types and meanings.}}

## Output Format

{{Describe the number, order, and format of output lines. State any multiple-answer or precision rules.}}

## Sample 1

### Input

```text
{{Exactly matches tests/samples/01.in}}
```

### Output

```text
{{Exactly matches tests/samples/01.out}}
```

### Explanation

{{Explain why the sample has this answer without introducing new rules.}}

## Constraints and Guarantees

{{First list variable ranges and global guarantees applying to 100% of tests.}}

{{Keep the table only when the official test data follows these groups; otherwise delete it. Every group also follows the general bounds above. Write absolute values as `\lvert T\rvert` inside Markdown tables so the bars do not create columns.}}

### Test Groups

| Score share | Additional conditions |
| --- | --- |
| {{portion}} | {{additional conditions}} |
| {{portion}} | No additional conditions |
