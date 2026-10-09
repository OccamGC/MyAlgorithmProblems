"""Rebuild the three explanatory SVGs for batch R12."""
from pathlib import Path
from html import escape
from math import hypot

ROOT=Path(__file__).resolve().parents[1]

def begin(width,height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#2563eb"/></marker></defs>',
            '<rect width="100%" height="100%" fill="white"/>',
            '<g font-family="Arial, sans-serif" font-size="21" fill="#172033">']

def text(out,x,y,label,size=21,anchor='middle'):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(str(label))}</text>')

def line(out,a,b,width=3,arrow=False):
    extra=' marker-end="url(#arrow)"' if arrow else ''
    out.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#2563eb" stroke-width="{width}"{extra}/>')

def save(out,topic,slug,name):
    out.extend(['</g>','</svg>'])
    target=ROOT/'topics'/topic/slug/'assets'/name
    target.parent.mkdir(exist_ok=True)
    target.write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
    print(target.relative_to(ROOT))

def directory():
    out=begin(800,505)
    pos={1:(400,55),2:(400,165),3:(250,275),4:(560,275),5:(130,395),6:(345,395),7:(650,395)}
    for a,b,w,label in [(1,2,2,(435,115)),(2,3,5,(295,205)),(2,4,6,(505,205)),(3,5,1,(165,330)),(3,6,3,(325,330)),(4,7,-5,(630,335))]:
        x,y=pos[a];u,v=pos[b];length=hypot(u-x,v-y)
        line(out,(x+(u-x)*25/length,y+(v-y)*25/length),(u-(u-x)*25/length,v-(v-y)*25/length),7 if (a,b) in {(1,2),(2,3)} else 2)
        text(out,*label,w)
    for v,(x,y) in pos.items():
        out.append(f'<circle cx="{x}" cy="{y}" r="25" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>')
        if v in (5,6):out.append(f'<circle cx="{x}" cy="{y}" r="19" fill="none" stroke="#2563eb" stroke-width="2"/>')
        text(out,x,y+7,v)
    text(out,400,470,'{5, 6}:  1 → 2 → 3,   2 + 5 = 7')
    save(out,'trees','dynamic-directory','common-prefix.svg')

def summoning():
    out=begin(900,440)
    boxes=[(35,65,'0',None,'(2, 3, 5)'),(345,65,'NPC 1','(1, 2, 4)','(4, 2, 2)'),(655,65,'NPC 3','(4, 1, 1)','(5, 2, 3)'),(345,285,'NPC 2','(3, 2, 3)','(3, 4, 3)')]
    for x,y,title,req,attr in boxes:
        dashed=' stroke-dasharray="8 5"' if title=='NPC 2' else ''
        out.append(f'<rect x="{x}" y="{y}" width="210" height="120" rx="12" fill="#f8fafc" stroke="#475569" stroke-width="2"{dashed}/>')
        text(out,x+105,y+28,title,22)
        if req:text(out,x+105,y+64,req,21)
        text(out,x+105,y+99,attr,21)
    line(out,(247,126),(334,126),3,True)
    line(out,(557,126),(644,126),3,True)
    text(out,450,240,'0 → 1 → 3',24)
    save(out,'data-structures','contract-summoning','summoning-chain.svg')

def movement():
    out=begin(800,450)
    def cells(values,y,start=140):
        for i,v in enumerate(values):
            x=start+i*100
            out.append(f'<rect x="{x}" y="{y}" width="76" height="60" rx="8" fill="#eff6ff" stroke="#475569" stroke-width="2"/>')
            text(out,x+38,y+39,v,26)
    def outline(x,y,w):
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="76" rx="10" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="8 5"/>')
    cells([1,2,2,3,1],40);text(out,80,78,'1.')
    outline(232,32,192)
    cells([1,3,1],185);cells([2,2],185,560);text(out,80,223,'2.')
    outline(552,177,192)
    cells([1,3,1,2,2],330);text(out,80,368,'3.')
    outline(432,322,192)
    line(out,(130,118),(130,168),3,True)
    line(out,(130,263),(130,313),3,True)
    text(out,460,145,'l = 2, len = 2',19)
    text(out,460,293,'nl = 4',19)
    text(out,400,430,'3 2 2 4',18)
    save(out,'data-structures','canister-sequence','segment-move.svg')

if __name__=='__main__':
    directory()
    summoning()
    movement()
