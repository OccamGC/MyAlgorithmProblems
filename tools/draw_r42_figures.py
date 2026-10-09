"""Draw fixed-position wealth examples as reproducible, bilingual-neutral SVGs."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]


def draw(number, stages, caption):
    width, height = 1120, 740
    margin, gap = 28, 22
    card_width = (width-2*margin-gap*(len(stages)-1))/len(stages)
    pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">Edit Town and Simoleons {number}: fixed household positions</title>',
            f'<desc id="desc">{escape(caption)}</desc>',
            '<rect width="1120" height="740" rx="20" fill="#f3f6fc"/>',
            '<g font-family="Segoe UI, Arial, sans-serif" fill="#17243d">',
            f'<text x="28" y="44" font-size="25" font-weight="700">Edit Town and Simoleons {number}</text>',
            '<text x="28" y="73" font-size="17" fill="#506079">Four fixed positions: A, B, C, D</text>']
    for col,(heading,subtitle,rows) in enumerate(stages):
        x=margin+col*(card_width+gap)
        pieces += [f'<text x="{x+card_width/2}" y="117" text-anchor="middle" font-size="20" font-weight="700">{escape(heading)}</text>',
                   f'<text x="{x+card_width/2}" y="143" text-anchor="middle" font-size="15" fill="#506079">{escape(subtitle)}</text>']
        for row,(members,money) in enumerate(rows):
            y=163+row*119
            target='T' in members; final=col==len(stages)-1 and target
            fill='#dff6eb' if final else '#e6eefc' if target else '#ffffff'
            stroke='#1f9470' if final else '#bfcee4'
            pieces += [f'<rect x="{x}" y="{y}" width="{card_width}" height="101" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
                       f'<text x="{x+14}" y="{y+27}" font-size="18" font-weight="700">{chr(65+row)}</text>',
                       f'<text x="{x+card_width/2}" y="{y+40}" text-anchor="middle" font-size="20">{escape(members)}</text>',
                       f'<text x="{x+card_width/2}" y="{y+78}" text-anchor="middle" font-size="24" font-weight="700">M = {escape(money)}</text>']
        if col+1<len(stages):
            ax=x+card_width+gap/2
            pieces.append(f'<path d="M {ax-6} 397 H {ax+6} l -5 -5 m 5 5 l -5 5" fill="none" stroke="#6c809e" stroke-width="2"/>')
    pieces += [f'<text x="28" y="675" font-size="18">{escape(caption)}</text>',
               '<text x="28" y="711" font-size="16" fill="#506079">T = target resident   O = other resident   M = household wealth</text>', '</g></svg>']
    directory=ROOT/f'topics/greedy/town-editing-simoleons-{number}/assets'
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'example.svg').write_text('\n'.join(pieces)+'\n',encoding='utf-8',newline='\n')


def main():
    draw(4,[('Initial','Reserve D for targets',[('T1, T2','2'),('O1','9'),('O2','9'),('empty','0')]),
            ('After T1','T1 visits B, C, D',[('T2','1'),('O1','5'),('O2','7'),('T1','7')]),
            ('After T2','T2 visits B, C, D',[('empty','0'),('O1','3'),('O2','5'),('T1, T2','12')])],
         'Both targets finish in D. Total town wealth stays 20; the targets own 12.')
    draw(5,[('Initial','All positions occupied',[('T × 2','2'),('O × 2','18'),('O','9'),('O','9')]),
            ('Merge outsiders','Equal mean: 9',[('T × 2','2'),('O × 4','36'),('empty','0'),('empty','0')]),
            ('Separate targets','Reserve D for outsiders',[('T1','1'),('O × 4','36'),('T2','1'),('empty','0')]),
            ('Final','Process, then reunite',[('T1, T2','16'),('empty','0'),('empty','0'),('O × 4','22')])],
         'Each outsider visits A, C, D. Then T2 joins T1 in A. Total town wealth stays 38.')


if __name__=='__main__':
    main()
