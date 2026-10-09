from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def document(width,height,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<defs><marker id="arrow" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="#334155"/></marker></defs>
<g font-family="Arial,sans-serif" font-size="24" fill="#172554" text-anchor="middle" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>\n'''

def text(x,y,value,size=24):return f'<text x="{x}" y="{y}" font-size="{size}">{value}</text>'
def node(x,y,value):return f'<circle cx="{x}" cy="{y}" r="36" fill="#eff6ff" stroke="#1d4ed8" stroke-width="2.5"/>'+text(x,y+8,value)
def arrow(path):return f'<path d="{path}" fill="none" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>'
body=arrow('M164 128 Q230 55 296 128')+arrow('M296 162 Q230 230 164 162')
body+=node(130,145,'AA')+node(330,145,'TT')+text(230,82,'R',20)+text(230,222,'R',20)
body+='<line x1="450" y1="24" x2="450" y2="246" stroke="#94a3b8" stroke-dasharray="6 6"/>'
body+=arrow('M621 115 C685 45 515 45 579 115')+node(600,145,'AT')+text(600,45,'R',20)
for slug in ['paired-strand-count','general-paired-strands']:
    path=ROOT/'topics/combinatorics'/slug/'assets/strands.svg';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(document(750,270,body),'utf-8')
body=text(120,38,'4 + 1')+text(510,38,'2 + 1 + 1 + 1')
for origin,parts in [(30,[4,1]),(465,[2,1,1,1])]:
    for row,length in enumerate(parts):
        for col in range(length):body+=f'<rect x="{origin+44*col}" y="{65+44*row}" width="40" height="40" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>'
body+=arrow('M260 145 L410 145')
path=ROOT/'topics/dynamic-programming/unlabeled-distributions/assets/partitions.svg';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(document(680,275,body),'utf-8')
print('Three R23 SVG resources written.')
