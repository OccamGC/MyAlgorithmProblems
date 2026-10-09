"""Rebuild the five explanatory SVGs used by batch R11."""
from pathlib import Path
from math import cos, sin, pi, hypot
from html import escape

ROOT=Path(__file__).resolve().parents[1]


def begin(width,height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#2563eb"/></marker></defs>',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            '<g font-family="Arial, sans-serif" font-size="20" fill="#172033">']


def text(out,x,y,label,size=20,color='#172033',anchor='middle'):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(label))}</text>')


def edge(out,a,b,color='#8190a6',width=3,arrow=False,dashed=False,radius=25):
    dx=b[0]-a[0];dy=b[1]-a[1];length=hypot(dx,dy)
    x1=a[0]+dx*radius/length;y1=a[1]+dy*radius/length
    x2=b[0]-dx*radius/length;y2=b[1]-dy*radius/length
    extra=(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="9 7"' if dashed else '')
    out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"{extra}/>')


def node(out,x,y,label,double=False):
    out.append(f'<circle cx="{x}" cy="{y}" r="25" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>')
    if double:out.append(f'<circle cx="{x}" cy="{y}" r="19" fill="none" stroke="#2563eb" stroke-width="2"/>')
    text(out,x,y+7,label)


def save(out,topic,slug,name):
    out.extend(['</g>','</svg>'])
    path=ROOT/'topics'/topic/slug/'assets'/name
    path.parent.mkdir(exist_ok=True)
    path.write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
    print(path.relative_to(ROOT))


def trees():
    positions={1:(400,65),2:(220,205),3:(580,205),5:(140,345),4:(660,345)}
    weights={1:-338,2:971,3:-35,4:-221,5:458}
    for slug,downward,name in [('festival-plan',True,'downward-paths.svg'),('grinder',False,'cleanup-paths.svg')]:
        out=begin(820,455)
        for u,v in [(1,2),(1,3),(2,5),(3,4)]:
            edge(out,positions[u],positions[v],color='#2563eb' if downward or v!=4 else '#7c3aed',width=4,arrow=downward,dashed=not downward and v==4)
        for u,(x,y) in positions.items():
            node(out,x,y,u)
            text(out,x+36,y+7,f'{weights[u]:+d}',18,anchor='start')
        if downward:
            text(out,410,407,'1 → 2 → 5: 1091  |  2 → 5: 1429  |  3 → 4: −256',19)
            text(out,410,438,'L = 2, R = 5',17,'#475569')
        else:
            text(out,410,405,'3 — 1 — 2 — 5: 1056',20)
            text(out,410,435,'4 — 3 — 1 — 2 — 5: 835',17,'#475569')
        save(out,'trees',slug,name)


def bread():
    out=begin(790,460)
    positions={i+1:(round(260+155*cos(-pi/2+i*2*pi/5)),round(215+155*sin(-pi/2+i*2*pi/5))) for i in range(5)}
    for i in range(1,6):edge(out,positions[i],positions[i%5+1])
    edge(out,positions[1],positions[5],color='#2563eb',width=5,arrow=True)
    for i,(x,y) in positions.items():
        node(out,x,y,i)
        out.append(f'<rect x="{x-15}" y="{y+31}" width="30" height="26" rx="4" fill="#f1f5f9" stroke="#94a3b8"/>')
        text(out,x,y+51,'10101'[i-1],17)
    text(out,610,155,'s = 10101',23)
    text(out,610,210,'i = 1,  j = 2',21)
    text(out,610,251,'1 → 5',25,'#2563eb')
    text(out,610,293,'"11"',21)
    out.append('<text x="610" y="334" text-anchor="middle" font-size="21">a<tspan baseline-shift="sub" font-size="14">1,2</tspan><tspan baseline-shift="baseline"> = 2</tspan></text>')
    text(out,395,434,'n = 5, K = 5',17,'#475569')
    save(out,'strings','magic-bread','wheat-ring.svg')


def wiring():
    out=begin(700,430)
    positions={1:(180,115),3:(180,230),6:(180,345),2:(510,115),4:(510,230),5:(510,345)}
    text(out,180,48,'a = 0',22)
    text(out,510,48,'a = 1',22)
    for u,v in [(1,2),(3,2),(3,4),(6,4),(6,5)]:edge(out,positions[u],positions[v],width=3)
    for i,(x,y) in positions.items():node(out,x,y,i,double=i in (1,3,6))
    text(out,350,411,'S = {1, 3, 6}    |    |S| = 3',20)
    save(out,'graphs','auto-wiring','connector-cover.svg')


def metro():
    out=begin(850,325)
    points=[(120,135),(425,135),(730,135)]
    for a,b in zip(points,points[1:]): edge(out,a,b,color='#2563eb',width=4,arrow=True)
    for i,(x,y) in enumerate(points,1): node(out,x,y,i)
    text(out,272,95,'2 → 1',25,'#2563eb')
    text(out,578,95,'1 → 0',25,'#2563eb')
    text(out,272,177,'D₁ = 1',19)
    text(out,578,177,'D₂ = 0',19)
    text(out,120,221,'T₁ = 1',20)
    text(out,425,221,'A₂ = T₂ = 2',20)
    text(out,730,221,'A₃ = 2',20)
    text(out,425,284,'2 × (2 − 1) + 2 × (2 − 1) + 3 × (2 − 2) = 4',20)
    save(out,'optimization','metro-delivery','delivery-route.svg')


if __name__=='__main__':
    trees()
    bread()
    wiring()
    metro()
