"""Accept display-math fences adjacent to prose without editing source Markdown."""
import re
import xml.etree.ElementTree as etree

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import AtomicString


class AdjacentDisplayMathProcessor(BlockProcessor):
    # Up to three spaces also covers continuation lines in compact list items.
    FENCE = re.compile(r'(?m)^ {0,3}\$\$(?P<tex>[\s\S]*?)\$\$[ \t]*(?=\n|$)')

    def find(self, block):
        if '$$' not in block:
            return None
        code_spans = []
        backticks = self.parser.md.inlinePatterns['backtick']
        cursor = 0
        while match := backticks.getCompiledRegExp().search(block, cursor):
            element, start, end = backticks.handleMatch(match, block)
            if isinstance(element, etree.Element) and element.tag == 'code':
                code_spans.append((start, end))
            cursor = end if end is not None else match.end()
        for match in self.FENCE.finditer(block):
            if not any(start <= match.start() < end for start, end in code_spans):
                return match
        return None

    def test(self, parent, block):
        return self.find(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.find(block)
        before, after = block[:match.start()], block[match.end():]
        if before.strip():
            self.parser.parseBlocks(parent, [before.rstrip('\n')])
        element = etree.SubElement(parent, 'div', {'class': 'arithmatex'})
        # Preserve TeX escapes and operators before Markdown's inline processing.
        element.text = AtomicString('\\[\n' + match['tex'].strip('\n') + '\n\\]')
        if after.strip():
            blocks.insert(0, after.lstrip('\n'))
        return True


class LeadingDisplayMathProcessor(AdjacentDisplayMathProcessor):
    def test(self, parent, block):
        match = self.find(block)
        return match is not None and match.start() == 0


class AdjacentDisplayMathExtension(Extension):
    def extendMarkdown(self, md):
        # Split leading dollar blocks before Arithmatex can absorb two formulas
        # into one. Code runs first; other Arithmatex syntaxes keep their handler.
        md.parser.blockprocessors.register(LeadingDisplayMathProcessor(md.parser), 'leading-display-math', 79.95)
        # Handle prose-adjacent formulas after lists and quotes have established
        # their containers, but before ordinary paragraphs consume TeX escapes.
        md.parser.blockprocessors.register(AdjacentDisplayMathProcessor(md.parser), 'adjacent-display-math', 10.1)
