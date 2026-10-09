"""Rebuild explanatory SVG figures for batch R38."""
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=20,color='#183247'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="middle" fill="{color}">{s}</text>'
def line(a,b,color='#334155',arrow=False,width=3):
    x,y=a;u,v=b
    return f'<path d="M{x} {y} L{u} {v}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def node(x,y,label,mark=False):
    return f'<circle cx="{x}" cy="{y}" r="21" fill="'+('#fef3c7' if mark else 'white')+'" stroke="#245d87" stroke-width="2"/>'+text(x,y+7,str(label))
def save(topic,slug,w,h,parts):
    p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(parents=True,exist_ok=True)
    prefix=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 Z" fill="#245d87"/></marker></defs><rect x="1" y="1" width="{w-2}" height="{h-2}" fill="#f6f9fc" stroke="#8ba6ba"/>'
    p.write_text(prefix+''.join(parts)+'</svg>','utf-8',newline='\n')
def main():
    parts=[]
    for i,p in enumerate('BNTWGGBW'):
        x=40+90*(i%4);y=35+80*(i//4);color='#e0f2fe' if abs(i%4-1)<=1 and p!='N' else '#ffffff'
        parts.append(f'<rect x="{x}" y="{y}" width="80" height="70" rx="8" fill="{color}" stroke="#245d87" stroke-width="2"/>');parts.append(text(x+40,y+43,p,26))
    parts.extend([text(545,70,'S = 1.25'),text(545,110,'F = 1.5625'),text(545,151,'1.25 × (1 + 0.2 × 1.25)',16)])
    save('search','garden-click-coefficient',720,220,parts)
    parts=[line((55,190),(635,190),width=1),text(350,30,'K = 5')]
    heights=[5,4,1,1,3,4]
    for i,h in enumerate(heights):
        x=95+i*100;parts.append(line((x,190),(x,190-h*25),color='#94a3b8',width=9));parts.append(text(x,217,str(i+1),17))
    parts.extend([line((95,65),(595,90),'#245d87',True,4),line((195,90),(495,115),'#b45309',True,4),text(355,70,'1 → 6',17),text(355,135,'2 → 5',17)])
    save('combinatorics','bounded-span-pipelines',720,242,parts)
    parts=[text(350,28,'xⱼ = max(tⱼ, xᵢ + cᵢⱼ)'),line((95,95),(580,95),'#245d87',True),node(70,95,'i'),node(610,95,'j'),text(350,78,'T ≥ 0',18),text(350,145,'xᵢ = −100,  cᵢⱼ = 3,  tⱼ = −7  ⇒  xⱼ = −7',18),line((95,210),(580,210),'#245d87',True),node(70,210,'i'),node(610,210,'j'),text(350,193,'T &lt; 0',18),text(350,252,'xⱼ = tⱼ = −7',20)]
    save('graphs','nether-portal',720,280,parts)
    pos={1:(350,150),2:(215,80),3:(80,80),4:(485,80),5:(350,250),6:(220,300),7:(215,190)}
    edges=[(2,1,5),(3,2,5),(4,1,9),(5,1,4),(6,5,10),(7,2,9)];parts=[]
    for u,v,w in edges:
        a=pos[u];b=pos[v];parts.append(line(a,b,width=5));parts.append(text((a[0]+b[0])/2+18,(a[1]+b[1])/2-10,str(w),18))
    for u,(x,y) in pos.items():parts.append(node(x,y,u,u in [6,7]))
    parts.extend([text(190,324,'6*',17),text(177,206,'7*',17),text(580,181,'6 → 3',21,'#245d87'),text(580,216,'7 → 4',21,'#b45309'),text(580,270,'28, 42',22)])
    save('trees','digging-the-subway',720,350,parts)
    parts=[line((120,75),(350,145),arrow=True),line((375,160),(575,230),arrow=True),'<path d="M600 218 Q490 -20 141 49" fill="none" stroke="#245d87" stroke-width="3" marker-end="url(#arrow)"/>',node(100,60,'1'),node(355,150,'2'),node(600,240,'3'),text(100,103,'h = 3',17),text(355,193,'h = 1',17),text(600,280,'h = 0',17),text(465,50,'3 → 1: +3',20)]
    save('graphs','snow-white',720,310,parts)
if __name__=='__main__':main()
