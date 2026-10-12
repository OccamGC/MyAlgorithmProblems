"""Check current bilingual math, local Markdown links, and unchanged program bytes."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parent
REPO = PROBLEM.parents[2]
BT = chr(96)
MATH = re.compile(BT*3+r"[^\n]*\n.*?"+BT*3+"|"+BT+"[^"+BT+r"\n]*"+BT+
                  r"|\$\$(.*?)\$\$|(?<![\$\\])\$(?!\$)([^\n]*?)(?<!\\)\$(?!\$)", re.S)
LINK = re.compile(r"\]\(([^)\n]+)\)")


def formulas(path):
    text = path.read_text(encoding="utf8")
    return Counter(re.sub(r"\s+", "", m[1] or m[2]).rstrip(".,;")
                   for m in MATH.finditer(text) if m[1] is not None or m[2] is not None)


def main():
    pairs = [PROBLEM / name for name in ["solution", "complexity", "complexity-research"]]
    pairs += [HERE / "proofs" / name for name in [
        "complexity-paths", "complexity-chains", "complexity-branches",
        "complexity-overlaps", "complexity-labels", "reference-followup", "reference-capacity", "cubic-bound"]]
    pairs += [HERE / "examples" / name for name in [
        "comb-scales", "comb-candidates", "tree-extension", "local-obstructions", "reference-components"]]
    pairs += [HERE / "results" / name for name in ["cubic-bound", "tree-extension", "diagonal-only"]]
    counts = {}
    for stem in pairs:
        zh, en = formulas(Path(str(stem)+".zh.md")), formulas(Path(str(stem)+".en.md"))
        assert zh == en, (stem.name, zh-en, en-zh)
        counts[stem.relative_to(PROBLEM).as_posix()] = sum(zh.values())
    broken = []
    links = 0
    documents = list(PROBLEM.glob("*.md")) + list(HERE.rglob("*.md"))
    documents += [REPO / name for name in ["README.md", "CITATION.md", "llms.txt"]]
    for path in documents:
        body = path.read_text(encoding="utf8")
        assert body.count("$$") % 2 == 0, path
        for link in LINK.findall(body):
            if re.match(r"[a-zA-Z]+://", link) or link.startswith("#"):
                continue
            target = (path.parent / unquote(link.split("#", 1)[0].strip("<>"))).resolve()
            links += 1
            if not target.exists():
                broken.append((str(path.relative_to(REPO)), link))
    assert not broken, json.dumps(broken, ensure_ascii=False, indent=2)
    expected = "0aabcd81214279752287d1ca35ff4192fd4dafbca47a74037e36da63b2a546d0"
    assert hashlib.sha256((PROBLEM/"std.cpp").read_bytes()).hexdigest() == expected
    print(json.dumps({"paired_formulas": counts, "documents": len(documents),
                      "local_links": links, "unchanged_std_sha256": expected}, indent=2))


if __name__ == "__main__":
    main()
