"""Rebuild the five shared-label SVG figures for the R37 problems."""
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=20):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="middle" fill="#183247">{s}</text>'
def node(x,y,s,blocked=False):
    shape=f'<rect x="{x-23}" y="{y-23}" width="46" height="46" fill="#d7dde4" stroke="#183247" stroke-width="2"/>' if blocked else f'<circle cx="{x}" cy="{y}" r="23" fill="white" stroke="#245d87" stroke-width="2"/>'
    return shape+text(x,y+7,str(s))
def line(x,y,a,b,label=None,arrow=True,dashed=False):
    dx=a-x;dy=b-y;length=math.hypot(dx,dy);x+=dx/length*24;y+=dy/length*24;a-=dx/length*27;b-=dy/length*27
    result=f'<path d="M {x} {y} L {a} {b}" fill="none" stroke="#245d87" stroke-width="2.5"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 5"' if dashed else '')+'/>'
    if label is not None:result+=text((x+a)/2,(y+b)/2-12,label,18)
    return result
def save(topic,slug,w,h,parts):
    p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(parents=True,exist_ok=True)
    prefix=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 Z" fill="#245d87"/></marker></defs><rect x="1" y="1" width="{w-2}" height="{h-2}" fill="#f6f9fc" stroke="#8ba6ba"/>'
    p.write_text(prefix+''.join(parts)+'</svg>','utf-8',newline='\n')
def main():
    parts=[text(270,30,'k = 1')]
    for i in range(3):parts.append(line(60+i*140,90,200+i*140,90,'1'))
    for i,v in enumerate([1,2,3,0]):parts.append(node(60+i*140,90,v,v==0))
    save('automata','dungeon-room-equivalence',540,150,parts)
    positions=[(45,110),(145,48),(145,170),(245,110)];parts=[]
    parts.extend([line(*positions[0],*positions[1],'3'),line(*positions[1],*positions[3],'2'),line(285,110,390,110),text(340,76,'T = 5')])
    for shift in [0,420]:
        for i,(x,y) in enumerate(positions,1):parts.append(node(x+shift,y,i))
    save('graphs','encrypted-reset-network',720,218,parts)
    parts=[text(360,32,'n = 4, K₂ = 3')]
    for i in [0,1,3,4]:parts.append(line(50+i*120,142,170+i*120,142,'1'))
    parts.append('<path d="M 305 121 Q 470 -5 635 121" fill="none" stroke="#245d87" stroke-width="3" marker-end="url(#arrow)"/>');parts.append(text(470,87,'3'))
    for i in range(6):parts.append(node(50+i*120,142,i,i==5))
    parts.extend([text(50,202,'C = 0',17),text(650,202,'5 > n',17)]);save('data-structures','lazy-forward-jumps',720,230,parts)
    parts=[]
    for panel in range(2):
        offset=panel*350;parts.append(text(offset+177,33,'×' if panel==0 else '✓',28))
        pairs=[(0,2,95,'A'),(1,3,95,'B')] if panel==0 else [(0,3,100,'A'),(1,2,52,'B')]
        for a,b,h,label in pairs:
            x=offset+50+a*75;y=offset+50+b*75;parts.append(f'<path d="M{x} 165 Q{(x+y)/2} {165-2*h} {y} 165" fill="none" stroke="#245d87" stroke-width="2.5"/>');parts.append(text((x+y)/2,165-h-7,label,17))
        for i,v in enumerate([1,1,2,2]):parts.append(text(offset+50+i*75,190,str(v),23))
    save('strings','noncrossing-1212-packing',700,220,parts)
    p=[(80,190),(80,65),(300,65),(300,190)];parts=[]
    for i in range(4):parts.append(line(*p[i],*p[(i+1)%4],arrow=False,dashed=i==3))
    for (x,y),s in zip(p,['s','1','2','3']):parts.append(node(x,y,s))
    parts.extend([text(37,132,'e₁=2',16),text(190,38,'e₂=5',18),text(349,132,'e₃=3',16),text(190,237,'e₄=0',18)])
    save('games','dynamic-cycle-edge-game',400,260,parts)
if __name__=='__main__':main()
