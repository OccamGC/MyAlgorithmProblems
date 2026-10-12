"""Build the documentation site from Git-indexed repository Markdown.

Only build/site-source and build/pages are generated. Source documents are never
rewritten. New documents must be staged with git add before a local preview.
"""
from __future__ import annotations

import hashlib
import html
import json
import logging
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import subprocess
from urllib.parse import quote, unquote, urlsplit
from urllib.request import urlopen

import yaml
from mkdocs.commands.build import build
from mkdocs.config import load_config
from pymdownx.slugs import slugify
from markdown_math import AdjacentDisplayMathExtension

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'build/site-source'
OUTPUT = ROOT / 'build/pages'
SITE = 'https://occamgc.github.io/MyAlgorithmProblems/'
REPO = 'https://github.com/OccamGC/MyAlgorithmProblems'
RAW = 'https://raw.githubusercontent.com/OccamGC/MyAlgorithmProblems/main/'
IMAGE_EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp'}
DOWNLOADS = {'research-index.json', 'CITATION.cff'}
LANGUAGE_NAMES = {'zh': '中文', 'en': 'English'}
LINK = re.compile(r'(!?\[[^\]\n]*\]\()([^\n)]+)(\))')
CODE = re.compile(r'(```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~|`[^`\n]*`|\$\$.*?\$\$|(?<!\\)\$(?!\$)[^\n]*?(?<!\\)\$)', re.S)
STATUS = {
    'current_proof': '已给出证明 · Proof provided',
    'refuted_conjecture': '猜想已否定 · Conjecture refuted',
    'historical_upper_bound': '较早上界 · Earlier bound',
    'historical_experiment': '历史实验 · Historical experiment',
    'conjecture': '待证猜想 · Conjecture',
    'experimental_evidence': '实验支持 · Experimental evidence',
    'open_question': '开放问题 · Open question',
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf8', newline='\n')


def git_files() -> set[str]:
    data = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT)
    return {p for p in data.decode('utf8').split('\0') if p}


def destination(path: str) -> str:
    if path == 'README.md':
        return 'catalog.md'
    if path == 'website/CONTRIBUTING.md':
        return 'contributing.md'
    p = PurePosixPath(path)
    return str(p.with_name('index.md')) if p.name == 'README.md' else path


def page_url(path: str) -> str:
    p = PurePosixPath(destination(path))
    return SITE + quote(str(p.parent) + '/' if p.name == 'index.md' else str(p.with_suffix('')) + '/', safe='/').replace('./', '')


def relative(source: str, target: str) -> str:
    return quote(posixpath.relpath(target, posixpath.dirname(source) or '.'), safe='/')


def reset_generated() -> None:
    # The only recursive deletion is constrained to this exact generated path.
    expected = (ROOT / 'build/site-source').resolve()
    if SOURCE.is_symlink() or SOURCE.resolve() != expected or not expected.is_relative_to(ROOT / 'build'):
        raise ValueError('Unsafe generated-source directory')
    if SOURCE.exists():
        shutil.rmtree(SOURCE)
    SOURCE.mkdir(parents=True)
    if OUTPUT.is_symlink() or not OUTPUT.resolve().is_relative_to(ROOT / 'build'):
        raise ValueError('Unsafe output directory')


def validate_index(index: dict, tracked: set[str]) -> None:
    rows = index['results']
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate research result IDs')
    for row in rows:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', row['id']):
            raise ValueError(f"Unstable result ID: {row['id']}")
        if not all(row['title'].get(lang) for lang in ('zh', 'en')):
            raise ValueError(f"Missing bilingual titles: {row['id']}")
        if row['status'] not in index['status_definitions'] or row['status'] not in STATUS:
            raise ValueError(f"Unknown result status: {row['status']}")
        if not any(row.get(key) for key in ('entry_paths', 'proof_paths', 'documentation_paths')):
            raise ValueError(f"Missing reading entry: {row['id']}")
        for key, value in row.items():
            if key.endswith('_paths'):
                paths = value.values() if isinstance(value, dict) else value
                for path in paths:
                    if path not in tracked or not (ROOT / path).is_file():
                        raise ValueError(f"Unpublished or missing {key}: {path}")
            if key in ('related_results', 'supersedes', 'extends', 'specializes', 'refutes'):
                if not set(value) <= set(ids):
                    raise ValueError(f"Unknown related result in {row['id']}")
        if row.get('superseded_by') and row['superseded_by'] not in ids:
            raise ValueError(f"Unknown successor in {row['id']}")
        if row['status'] == 'current_proof' and not row.get('proof_paths'):
            raise ValueError(f"A current proof needs proof_paths: {row['id']}")


def rewrite_links(body: str, source: str, documents: dict[str, str], assets: set[str], tracked: set[str]) -> str:
    def convert(match):
        original = match[2]
        target = original.strip('<>')
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match[0]
        path = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parsed.path)))
        suffix = ('?' + parsed.query if parsed.query else '') + ('#' + parsed.fragment if parsed.fragment else '')
        if path in documents:
            out = relative(documents[source], documents[path])
        elif path in assets or path in DOWNLOADS or path == 'llms.txt':
            out = relative(documents[source], path)
        elif path in tracked:
            out = REPO + '/blob/main/' + quote(path, safe='/')
        else:
            raise ValueError(f'Broken source link in {source}: {target}')
        return match[1] + out + suffix + match[3]
    # Code examples and expressions such as [z^n](1+z) are not Markdown links.
    return ''.join(part if i % 2 else LINK.sub(convert, part) for i, part in enumerate(CODE.split(body)))


def frontmatter(meta: dict, body: str) -> str:
    return '---\n' + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + '---\n\n' + body


def result_paths(row: dict) -> dict:
    return row.get('entry_paths') or row.get('proof_paths') or row['documentation_paths']


def result_row(row: dict, featured: bool = False) -> str:
    paths = result_paths(row)
    state_class = 'status-refuted' if row['status'] == 'refuted_conjecture' else 'status-historical' if row['status'].startswith('historical') else ''
    title = html.escape(row['title']['zh'])
    links = ' · '.join(f'[{LANGUAGE_NAMES.get(lang, lang)}]({destination(path)})' for lang, path in paths.items())
    summary = row.get('summary', {})
    text = f'<section class="result-row" markdown="1">\n\n<span class="result-status {state_class}">{STATUS[row["status"]]}</span>\n\n### {title}\n\n'
    text += f'<p class="english">{html.escape(row["title"]["en"])}</p>\n\n'
    if summary:
        text += summary.get('zh', '') + '\n\n' + f'<p class="english">{html.escape(summary.get("en", ""))}</p>\n\n'
    text += links + '\n\n'
    if not featured:
        text += f'稳定标识 / ID: `{row["id"]}`\n\n'
        relations = []
        for key, label in [('extends', '推广'), ('specializes', '特殊情形'), ('refutes', '否定'), ('related_results', '相关'), ('supersedes', '改进')]:
            for other in row.get(key, []):
                relations.append(f'{label}: [{other}](research.md#{other})')
        if row.get('superseded_by'):
            other = row['superseded_by']
            relations.append(f'后续结果: [{other}](research.md#{other})')
        if relations:
            text += ' · '.join(relations) + '\n\n'
    return text + '</section>\n\n'


def generate_home(index: dict, count: int) -> str:
    current = sum(row['status'] == 'current_proof' for row in index['results'])
    body = '''<div class="site-hero" markdown="1">

<div class="site-eyebrow">ALGORITHMS / PROOFS / COUNTEREXAMPLES</div>

# 从问题出发，走到证明

<p class="lead">探索算法的边界，记录成立的证明，也留下让猜想失败的反例。</p>
<p class="english">Algorithm problems and research notes, with precise assumptions, complete proofs, and reproducible evidence. Read in Chinese or English.</p>

<div class="site-actions" markdown="1">

[阅读研究成果 / Research](research.md)
[浏览题库 / Problems](catalog.md)

</div>
</div>

'''
    body += f'<div class="site-stats"><span><strong>{count}</strong>道算法题 / problems</span><span><strong>{current}</strong>项已证记录 / proof records</span><span><strong>中 / EN</strong>双语阅读</span></div>\n\n'
    body += '## 重点研究 / Featured research\n\n'
    for row in index['results']:
        if row.get('featured'):
            body += result_row(row, True)
    body += '''## 选择你的阅读路径 / Find your starting point

<div class="reading-path" markdown="1">

**想了解结论**：从成果摘要开始，先看模型和适用边界，再进入完整证明。<br>
**想复核推导**：沿证明中的引理与算例阅读，再运行附带的验证程序。<br>
**想继续研究**：在成果目录查看已否定猜想和历史探索，避免重复走过的弯路。

Start with a result summary, follow its proof, then inspect the evidence. The research directory distinguishes current proofs, refuted conjectures, and historical experiments.

</div>

## 继续扩展 / Continue the research

新的结论、推广或开放问题使用同一套文档与索引结构。每项结果保留稳定标识，关联原问题、证明和验证材料。

[新增成果与维护说明](contributing.md) · [引用与固定版本](CITATION.md) · [Agent 阅读导航](llms.txt) · [机器可读索引](research-index.json)
'''
    return frontmatter({'title': '算法问题与可复核的研究 / Algorithms and reproducible research', 'hide': ['navigation', 'toc'], 'search': {'boost': 2}}, body)


def generate_directory(index: dict) -> str:
    body = '# 研究成果与问题 / Research results and questions\n\n'
    body += '按研究状态组织，保留当前结论与探索过程。证明状态表示仓库提供了文字证明；有限实验不替代一般证明。\n\nOrganized by research status. A proof record indicates a written proof in this repository; finite experiments do not establish a general theorem.\n\n'
    for state in STATUS:
        rows = [row for row in index['results'] if row['status'] == state]
        if not rows:
            continue
        body += f'## {STATUS[state]}\n\n'
        for row in rows:
            body += f'<span id="{row["id"]}"></span>\n\n' + result_row(row)
    body += '[添加新结论或拓展问题](contributing.md) · [完整机器索引](research-index.json)\n'
    return frontmatter({'title': '研究成果与问题 / Research directory', 'search': {'boost': 2}}, body)


def fetch_vendor() -> None:
    files = {
        'tex-svg.js': ('es5/tex-svg.js', 'd4295dc33744836935c1399feece5159577b34c5c8ffb9f1c6324cd82e03a882'),
        'MathJax-LICENSE': ('LICENSE', 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'),
    }
    for filename, (remote, expected) in files.items():
        cached = ROOT / 'build/vendor' / filename
        if not cached.exists():
            cached.parent.mkdir(parents=True, exist_ok=True)
            with urlopen('https://cdn.jsdelivr.net/npm/mathjax@3.2.2/' + remote, timeout=60) as response:
                cached.write_bytes(response.read())
        if hashlib.sha256(cached.read_bytes()).hexdigest() != expected:
            raise ValueError(f'MathJax checksum mismatch: {filename}')
        out = SOURCE / 'assets/site/mathjax' / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, out)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    tracked = git_files()
    index = json.loads((ROOT / 'research-index.json').read_text(encoding='utf8'))
    validate_index(index, tracked)
    documents = {p: destination(p) for p in sorted(tracked)
                 if p.endswith('.md') and (p.startswith(('topics/', 'docs/')) or p in {'README.md', 'CITATION.md', 'website/CONTRIBUTING.md'})}
    if len(documents.values()) != len(set(documents.values())):
        raise ValueError('Two sources map to the same site page')
    assets = {p for p in tracked if PurePosixPath(p).suffix.lower() in IMAGE_EXTENSIONS and p.startswith(('topics/', 'docs/'))}
    for row in index['results']:
        for key in ('entry_paths', 'proof_paths', 'documentation_paths'):
            for path in row.get(key, {}).values():
                if path not in documents:
                    raise ValueError(f'Result document outside publishable roots: {path}')
    reset_generated()
    result_for_path = {path: row for row in index['results'] for key in ('entry_paths', 'proof_paths', 'documentation_paths') for path in row.get(key, {}).values()}
    for path, dest in documents.items():
        body = (ROOT / path).read_text(encoding='utf8')
        meta = {'github_url': REPO + '/blob/main/' + quote(path, safe='/'), 'source_url': RAW + quote(path, safe='/')}
        heading = re.search(r'^#\s+(.+)$', body, re.M)
        if heading:
            meta['title'] = heading[1].strip()
        if path.endswith(('.zh.md', '.en.md')):
            lang = 'zh' if path.endswith('.zh.md') else 'en'
            other = 'en' if lang == 'zh' else 'zh'
            alternate = path[:-6] + '.' + other + '.md'
            meta['language'] = 'zh-CN' if lang == 'zh' else 'en'
            if alternate in documents:
                meta['translations'] = {meta['language']: page_url(path), 'en' if other == 'en' else 'zh-CN': page_url(alternate)}
                meta['other_language_url'] = urlsplit(page_url(alternate)).path
                meta['other_language_label'] = 'English' if other == 'en' else '中文'
        row = result_for_path.get(path)
        if row:
            meta['description'] = row.get('summary', {}).get('zh' if path.endswith('.zh.md') else 'en', row['title']['zh' if path.endswith('.zh.md') else 'en'])
            meta['search'] = {'boost': 2 if row['status'] == 'current_proof' else 0.5}
        body = rewrite_links(body, path, documents, assets, tracked)
        write(SOURCE / dest, frontmatter(meta, body))
    for path in assets | DOWNLOADS:
        target = SOURCE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    for path in (ROOT / 'website/assets').iterdir():
        target = SOURCE / 'assets/site' / path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    fetch_vendor()
    problem_count = sum(p.endswith('/statement.zh.md') for p in documents)
    write(SOURCE / 'index.md', generate_home(index, problem_count))
    write(SOURCE / 'research.md', generate_directory(index))
    llms = (ROOT / 'llms.txt').read_text(encoding='utf8')
    llms += '\n## Website and current result catalog\n\n'
    llms += f'- [Website]({SITE}): Human-readable pages with mathematics and bilingual navigation.\n'
    llms += f'- [Research directory]({SITE}research/): Current and historical statuses.\n'
    for row in index['results']:
        for lang, path in result_paths(row).items():
            llms += f'- [{row["title"][lang]}]({RAW}{quote(path, safe="/")}): {row["status"]}; ID {row["id"]}.\n'
    write(SOURCE / 'llms.txt', llms)
    write(SOURCE / '.nojekyll', '')
    config = load_config(config_file=str(ROOT / 'mkdocs.yml'), strict=True)
    config['markdown_extensions'].append(AdjacentDisplayMathExtension())
    for extension in config['mdx_configs']:
        if extension == 'toc':
            config['mdx_configs'][extension]['slugify'] = slugify(case='lower')
    research_nav = [{'成果与问题目录': 'research.md'}]
    for row in index['results']:
        if row.get('featured'):
            research_nav.append({row['title']['zh']: [{LANGUAGE_NAMES.get(lang, lang): destination(path)} for lang, path in result_paths(row).items()]})
    config['nav'] = [
        {'首页 / Home': 'index.md'},
        {'研究 / Research': research_nav},
        {'题库 / Problems': 'catalog.md'},
        {'引用 / Cite': 'CITATION.md'},
        {'扩展 / Contribute': 'contributing.md'},
    ]
    build(config)
    manifest = {'documents': len(documents), 'problems': problem_count, 'results': len(index['results']),
                'site_url': SITE, 'source_mapping': documents}
    write(ROOT / 'build/site-manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'source_mapping'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
