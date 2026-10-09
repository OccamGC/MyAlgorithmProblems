"""Check bilingual documents, math escapes, samples, score groups and figures."""

import json
from fractions import Fraction
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTE = re.compile(
    r"原题|原版|旧版|暂予保留|original problem|carried over|retained provisionally",
    re.IGNORECASE,
)
MARKDOWN_TOKEN = re.compile(
    r"^```[^\n]*\n.*?^```[^\n]*$|`[^`\n]*`"
    r"|\$\$.*?\$\$|(?<![\\$])\$(?:\\.|[^$\n])*\$(?!\$)",
    re.MULTILINE | re.DOTALL,
)


def math_formulas(text):
    """Extract inline/display formulas, excluding code, with source line numbers."""
    return [
        (match.group().strip("$"), text.count("\n", 0, match.start()) + 1)
        for match in MARKDOWN_TOKEN.finditer(text)
        if match.group().startswith("$")
    ]


def check_math_escapes(directory):
    checked = 0
    kinds = ['statement', *sorted({p.name[:-6] for p in directory.glob('solution*.zh.md')})]
    for kind in kinds:
        documents = [directory / f"{kind}.{language}.md" for language in ("zh", "en")]
        formulas = [math_formulas(path.read_text(encoding="utf-8")) for path in documents]
        checked += sum(map(len, formulas))
        for index, document in enumerate(documents):
            counterparts = {}
            for formula, _ in formulas[1 - index]:
                compact = re.sub(r"\s+", "", formula)
                counterparts.setdefault(compact.replace("\\", ""), set()).add(compact)
            for formula, line in formulas[index]:
                compact = re.sub(r"\s+", "", formula)
                variants = counterparts.get(compact.replace("\\", ""), set())
                if compact in variants:
                    continue
                # Natural-language translations may split or reorder formulas.
                # Only flag counterparts differing by missing backslashes.
                for expected in sorted(variants):
                    assert expected.count("\\") <= compact.count("\\"), (
                        f"{document}:{line}: possible missing math escape: "
                        f"{formula!r}; counterpart {expected!r}"
                    )
    return checked


def sample_blocks(text, heading):
    pattern = rf"(?m)^### {heading}\r?\n\r?\n```text\r?\n(.*?)\r?\n```"
    return [block.replace("\r\n", "\n") for block in re.findall(pattern, text, re.DOTALL)]


def check_problem(directory):
    zh = (directory / "statement.zh.md").read_text(encoding="utf-8")
    en = (directory / "statement.en.md").read_text(encoding="utf-8")
    for name, statement in (("zh", zh), ("en", en)):
        assert not SOURCE_NOTE.search(statement), (directory, name, "source note")

    story_zh = re.search(r"(?s)## 背景故事\n(.*?)\n## 形式化问题描述", zh)
    story_en = re.search(r"(?s)## Story\n(.*?)\n## Formal Problem Statement", en)
    assert story_zh and story_en, directory
    model_zh = re.findall(r"\(本故事由([^()]+)重写\)", story_zh.group(1))
    model_en = re.findall(r"\(This story was rewritten by ([^()]+)\.\)", story_en.group(1))
    assert model_zh == model_en and len(model_zh) <= 1, (directory, "story credit")
    if model_zh:
        assert story_zh.group(1).strip().endswith(f"(本故事由{model_zh[0]}重写)")
        assert story_en.group(1).strip().endswith(
            f"(This story was rewritten by {model_en[0]}.)"
        )

    samples = sorted((directory / "tests" / "samples").glob("*.in"))
    for heading_zh, heading_en, suffix in (
        ("输入", "Input", ".in"),
        ("输出", "Output", ".out"),
    ):
        blocks_zh = sample_blocks(zh, heading_zh)
        blocks_en = sample_blocks(en, heading_en)
        assert len(blocks_zh) == len(blocks_en) == len(samples), directory
        for index, sample in enumerate(samples):
            expected = sample.with_suffix(suffix).read_text(encoding="ascii")
            expected = expected.replace("\r\n", "\n")
            if expected.endswith("\n"):
                expected = expected[:-1]
            assert blocks_zh[index] == blocks_en[index] == expected, (
                directory,
                sample,
                suffix,
            )

    shares_zh = [Fraction(value) for value in re.findall(r"(?m)^\|[ \t]*(\d+(?:/\d+)?)%[ \t]*\|", zh)]
    shares_en = [Fraction(value) for value in re.findall(r"(?m)^\|[ \t]*(\d+(?:/\d+)?)%[ \t]*\|", en)]
    assert shares_zh == shares_en and sum(shares_zh) == 100, directory
    plan = json.loads((directory / "tests" / "plan.json").read_text(encoding="utf-8"))
    actual = [0] * len(shares_zh)
    for case in plan["cases"]:
        actual[case["group"] - 1] += Fraction(str(case["score_percent"]))
    assert actual == shares_zh, (directory, actual, shares_zh)
    return len(samples), len(plan["cases"])


def check_links():
    checked = 0
    for markdown in ROOT.rglob("*.md"):
        if any(part in {"build", "review", ".git"} for part in markdown.parts):
            continue
        content = markdown.read_text(encoding="utf-8")
        # Formula terms such as dp[b](1-z) are not Markdown links.
        content = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', content)
        content = re.sub(r'`[^`\n]*`|\$\$.*?\$\$|(?<!\$)\$[^$\n]*\$(?!\$)', '', content, flags=re.DOTALL)
        # Angle-bracket destinations may include spaces and parentheses.
        for angled, plain in re.findall(r"(?<!!)\[[^]]+\]\((?:<([^>\n]+)>|([^)\n]+))\)", content):
            target = angled or plain
            if target.startswith(("https://", "http://", "#")):
                continue
            path = target.split("#", 1)[0]
            assert (markdown.parent / path).exists(), (markdown, target)
            checked += 1
    return checked


def figure_references(markdown):
    text = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', markdown)
    text = re.sub(r'`[^`\n]*`', '', text)
    return re.findall(r'!\[([^\]\n]*)\]\(([^)\n]+)\)', text)


def check_figures():
    checked = 0
    resources = set()
    for directory in sorted((ROOT / 'topics').glob('*/*')):
        kinds = ['statement', *sorted({p.name[:-6] for p in directory.glob('solution*.zh.md')})]
        for kind in kinds:
            counts = []
            for language in ('zh', 'en'):
                document = directory / f'{kind}.{language}.md'
                if not document.exists():
                    continue
                references = figure_references(document.read_text(encoding='utf-8'))
                counts.append(len(references))
                for alternative, target in references:
                    assert alternative.strip(), (document, 'missing alternative text')
                    image = (document.parent / target).resolve()
                    assert image.is_file(), (document, target, 'missing image')
                    assert image.is_relative_to(directory.resolve() / 'assets'), (document, target)
                    if image.suffix.lower() == '.svg':
                        root = ET.parse(image).getroot()
                        assert root.tag == '{http://www.w3.org/2000/svg}svg', image
                        box = list(map(float, root.attrib['viewBox'].split()))
                        assert len(box) == 4 and box[2] > 0 and box[3] > 0, image
                    else:
                        assert image.suffix.lower() == '.png', image
                    resources.add(image)
                    checked += 1
            assert len(set(counts)) <= 1, (directory, kind, 'bilingual figure count')
    return checked, len(resources)


def main():
    total_samples = 0
    total_cases = 0
    total_formulas = 0
    for statement in sorted((ROOT / "topics").glob("*/*/statement.zh.md")):
        total_formulas += check_math_escapes(statement.parent)
        samples, cases = check_problem(statement.parent)
        total_samples += samples
        total_cases += cases
        print(f"{statement.parent.name}: {samples} samples, {cases} planned cases")
    links = check_links()
    figures, resources = check_figures()
    print(f"Checked {total_samples} bilingual samples, {total_cases} scored cases, {links} local links")
    print(f"Checked {figures} bilingual image references to {resources} figure files")
    print(f"Compared math escapes across {total_formulas} bilingual inline/display formulas")


if __name__ == "__main__":
    main()
