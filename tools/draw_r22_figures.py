from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]

def svg(width, height, elements):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0 0 L8 3.5 L0 7" fill="#334155"/></marker></defs>
<g font-family="Arial, sans-serif" font-size="20" text-anchor="middle" fill="#172554" stroke-linecap="round" stroke-linejoin="round">
{''.join(elements)}
</g></svg>'''

def text(x,y,value,size=20):
    return f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(str(value))}</text>'

def line(x,y,a,b,arrow=False,dashed=False):
    return f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#334155" stroke-width="2.5"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 5"' if dashed else '')+'/>'

def node(x,y,label,selected=False):
    return f'<circle cx="{x}" cy="{y}" r="23" fill="'+('#dbeafe' if selected else '#ffffff')+'" stroke="#1e40af" stroke-width="2.5"/>'+ (f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="#1e40af" stroke-width="1.5"/>' if selected else '')+text(x,y+7,label)

def save(path,w,h,elements):
    dest=ROOT/'topics'/path;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(svg(w,h,elements)+'\n','utf-8')

e=[line(65,310,570,310,True),line(65,310,65,35,True),text(588,317,'A'),text(64,24,'D')]
for a in range(7):
    x=65+75*a;e.extend([line(x,310,x,315),text(x,341,a,16)])
for d in range(1,4):
    y=310-75*d;e.extend([line(60,y,65,y),text(42,y+5,d,16)])
points=[(1,1),(2,2),(3,3),(4,2),(5,1),(6,0)]
for i,(a,d) in enumerate(points,1):
    x=65+75*a;y=310-75*d
    e.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#1e40af"/>')
    if i>=3:e.append(f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#1e40af" stroke-width="2"/>')
    e.append(text(x+21,y-15,i,18))
save('optimization/queen-of-hearts-card-soldiers/assets/lineup.svg',625,375,e)

e=[text(175,45,'Y',30),text(515,45,'N',30),line(330,25,330,295,dashed=True)]
e += ['<path d="M119 159 Q175 102 231 159" fill="none" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>',
      '<path d="M231 181 Q175 238 119 181" fill="none" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>',node(100,170,1),node(250,170,2)]
e += [line(518,114,577,216,True),line(560,238,454,238,True),line(438,216,496,114,True),node(507,94,1),node(590,238,2),node(424,238,3)]
save('graphs/lattice-completion/assets/completion.svg',680,320,e)

e=[]
pos={'0':(250,370),'a':(130,270),'b':(370,270),'u':(130,140),'v':(370,140),'1':(250,40)}
for p,q in [('0','a'),('0','b'),('a','u'),('a','v'),('b','u'),('b','v'),('u','1'),('v','1')]:e.append(line(*pos[p],*pos[q]))
for label,(x,y) in pos.items():e.append(node(x,y,label,label in ('a','b')))
save('logic/lattice-recognition/assets/bounds.svg',500,415,e)

e=[line(330,35,330,340,dashed=True),text(170,42,'{1, 2, 4}'),text(490,42,'{2, 3}')]
for offset,chosen in [(0,{1,2,4}),(320,{2,3})]:
    pos={1:(170+offset,290),2:(90+offset,180),3:(250+offset,180),4:(170+offset,80)}
    for p,q in [(1,2),(1,3),(2,4),(3,4)]:e.append(line(*pos[p],*pos[q]))
    for label,(x,y) in pos.items():e.append(node(x,y,label,label in chosen))
save('combinatorics/sublattice-count/assets/subsets.svg',660,345,e)
print('Four R22 SVG figures written.')
