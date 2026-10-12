"""Check rendered links, publication boundaries, metadata, and search output."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'build/pages'
BASE = 'https://occamgc.github.io/MyAlgorithmProblems/'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.math = 0
        self.display_math = 0
        self.literal_depth = 0
        self.readable_text = []
        self.canonical = None
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag in ('code', 'pre', 'script', 'style'):
            self.literal_depth += 1
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if 'arithmatex' in attrs.get('class', '').split():
            self.math += 1
            self.display_math += tag == 'div'
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag in ('a', 'link', 'script', 'img'):
            href = attrs.get('href') or attrs.get('src')
            if href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag in ('code', 'pre', 'script', 'style'):
            self.literal_depth -= 1

    def handle_data(self, data):
        if not self.literal_depth:
            self.readable_text.append(data)


def main():
    pages = {p.relative_to(SITE).as_posix(): Page(p.read_text(encoding='utf8')) for p in SITE.rglob('*.html')}
    broken = []
    count = 0
    for path, page in pages.items():
        if '$$' in '\n'.join(page.readable_text):
            broken.append((path, '$$', 'unprocessed display-math delimiter outside code'))
        for link in page.links:
            url = urlsplit(urljoin(BASE + path, link))
            if url.netloc != urlsplit(BASE).netloc:
                continue
            prefix = urlsplit(BASE).path
            if not url.path.startswith(prefix):
                broken.append((path, link, 'outside project prefix'))
                continue
            target = unquote(url.path[len(prefix):])
            target = target + 'index.html' if target.endswith('/') or not target else target
            count += 1
            if not (SITE / target).is_file():
                broken.append((path, link, 'missing file'))
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                broken.append((path, link, 'missing anchor'))
        if path != '404.html' and (not page.canonical or not page.canonical.startswith(BASE)):
            broken.append((path, '', 'missing canonical URL'))
    assert not broken, json.dumps(broken[:60], ensure_ascii=False, indent=2)
    for required in ['sitemap.xml', 'llms.txt', 'research-index.json', 'CITATION.cff', 'search/search_index.json', 'assets/site/mathjax/tex-svg.js', 'assets/site/mathjax/MathJax-LICENSE']:
        assert (SITE / required).is_file(), required
    for forbidden in ['.git', '.venv', 'continuation-state.json', '.env']:
        assert not list(SITE.rglob(forbidden)), forbidden
    index = json.loads((SITE / 'research-index.json').read_text(encoding='utf8'))
    directory = (SITE / 'research/index.html').read_text(encoding='utf8')
    for row in index['results']:
        assert f'id="{row["id"]}"' in directory, row['id']
    for language in ['zh', 'en']:
        path = f'topics/simulation/grid-forest-matching/research/proofs/cubic-bound.{language}/index.html'
        assert pages[path].math >= 50, (language, pages[path].math)
        regression = f'topics/data-structures/selective-suffix-sort/statement.{language}/index.html'
        assert pages[regression].display_math == 2, (regression, pages[regression].display_math)
        extension = f'topics/simulation/grid-forest-matching/research/results/eight-neighbor.{language}/index.html'
        assert pages[extension].display_math >= 10, (extension, pages[extension].display_math)
        assert pages[extension].math == 89, (extension, pages[extension].math)
        edges = f'topics/simulation/grid-forest-matching/research/results/edge-obstacles.{language}/index.html'
        assert pages[edges].display_math == 9, (edges, pages[edges].display_math)
        assert pages[edges].math == 70, (edges, pages[edges].math)
    search = json.loads((SITE / 'search/search_index.json').read_text(encoding='utf8'))
    assert any('cubic-bound.zh' in row['location'] for row in search['docs'])
    assert any('tree-extension.en' in row['location'] for row in search['docs'])
    for language in ['zh', 'en']:
        assert any(f'eight-neighbor.{language}' in row['location'] for row in search['docs'])
        assert any(f'edge-obstacles.{language}' in row['location'] for row in search['docs'])
    sitemap = ET.parse(SITE / 'sitemap.xml')
    assert len(sitemap.getroot()) >= len(pages) - 1
    print(json.dumps({'html_pages': len(pages), 'checked_internal_links': count,
                      'search_entries': len(search['docs']), 'indexed_results': len(index['results'])}, indent=2))


if __name__ == '__main__':
    main()
