"""Regression checks for formulas that previously appeared as literal $$ text."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as etree

import markdown

from markdown_math import AdjacentDisplayMathExtension

ROOT = Path(__file__).resolve().parents[1]
FORMULA = r'S=\{k\}\cup\{j:k<j\le n,\ a_j<a_k\}.'


def render(source):
    html = markdown.markdown(source, extensions=[
        'pymdownx.superfences', 'pymdownx.arithmatex', AdjacentDisplayMathExtension()
    ], extension_configs={'pymdownx.arithmatex': {'generic': True}})
    return etree.fromstring('<main>' + html + '</main>')


class DisplayMathTests(unittest.TestCase):
    def test_reported_statement_in_both_languages(self):
        for language in ('zh', 'en'):
            with self.subTest(language=language):
                path = ROOT / f'topics/data-structures/selective-suffix-sort/statement.{language}.md'
                page = render(path.read_text(encoding='utf8'))
                formulas = page.findall('.//div[@class="arithmatex"]')
                self.assertEqual(len(formulas), 2)
                self.assertIn(FORMULA, formulas[0].text)
                self.assertIn(r'k=((\mathrm{ans}+q)\bmod n)+1,', formulas[1].text)

    def test_adjacent_multiple_blocks_and_inline_math(self):
        page = render('Before $k$.\n$$\n' + FORMULA + '\n$$\nBetween.\n$$\nx<y\n$$\nAfter.')
        self.assertEqual([child.tag for child in page], ['p', 'div', 'p', 'div', 'p'])
        self.assertEqual(len(page.findall('.//span[@class="arithmatex"]')), 1)
        self.assertIn(FORMULA, page[1].text)
        self.assertIn('x<y', page[3].text)

    def test_blank_line_blocks_still_work(self):
        page = render('Before.\n\n$$\n' + FORMULA + '\n$$\n\nAfter.')
        self.assertEqual(len(page.findall('.//div[@class="arithmatex"]')), 1)
        self.assertIn(FORMULA, page[1].text)

    def test_leading_formulas_do_not_merge(self):
        for source in ('$$x<y$$\n$$y<z$$', '$$\nx<y\n$$\nTherefore\n$$\ny<z\n$$'):
            with self.subTest(source=source):
                page = render(source)
                formulas = page.findall('.//div[@class="arithmatex"]')
                self.assertEqual(len(formulas), 2)
                self.assertEqual([f.text.strip() for f in formulas], ['\\[\nx<y\n\\]', '\\[\ny<z\n\\]'])

    def test_list_and_quote_keep_their_containers(self):
        for source, parent in [
            ('1. Before\n   $$\n   x<y\n   $$\n   After', './/li'),
            ('> Before\n> $$\n> x<y\n> $$\n> After', './/blockquote'),
        ]:
            with self.subTest(parent=parent):
                page = render(source)
                self.assertIsNotNone(page.find(parent + '/div[@class="arithmatex"]'))
                self.assertIsNone(page.find('./div[@class="arithmatex"]'))

    def test_code_examples_are_not_typeset(self):
        examples = [
            '```text\n$$\nx<y\n$$\n```',
            '~~~~text\n$$\nx<y\n$$\n~~~~',
            '    $$\n    x<y\n    $$',
            'Use `$$` as a delimiter.',
            '`example\n$$\nx<y\n$$\nexample`',
        ]
        for source in examples:
            with self.subTest(source=source):
                page = render(source)
                self.assertIsNone(page.find('.//div[@class="arithmatex"]'))
                self.assertIsNotNone(page.find('.//code'))


if __name__ == '__main__':
    unittest.main()
