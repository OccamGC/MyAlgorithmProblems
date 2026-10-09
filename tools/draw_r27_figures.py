"""Draw mathematical-label SVGs shared by the two language editions."""
from pathlib import Path
import math,html
ROOT=Path(__file__).resolve().parents[1]
def start(w,h):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#718096"/></marker><marker id="blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#1379ad"/></marker></defs><rect width="100%" height="100%" fill="#fff"/>']
def text(s,x,y,t,size=22,color='#172b4d'):s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{size}" fill="{color}">{html.escape(str(t))}</text>')
def line(s,x1,y1,x2,y2,blue=False,arrow=False):s.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{("#1379ad" if blue else "#718096")}" stroke-width="{3 if blue else 2}"'+(f' marker-end="url(#{"blue" if blue else "arrow"})"' if arrow else '')+'/>')
def node(s,x,y,label,sub=None,blue=False):
    s.append(f'<circle cx="{x}" cy="{y}" r="33" fill="{("#e4f4fc" if blue else "#f4f6f9")}" stroke="{("#1379ad" if blue else "#718096")}" stroke-width="2"/>');text(s,x,y+(7 if sub is None else -3),label,21)
    if sub is not None:text(s,x,y+19,sub,17)
def save(rel,s):p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(s+['</svg>'])+'\n','utf-8')
def main():
    s=start(850,210)
    for x,label in [(80,'1 8 9 9'),(365,'1 8 9 0'),(710,'9 9 9')]:text(s,x if x!=80 else 110,112,label,31)
    line(s,200,100,270,100,True,True);text(s,235,75,'1 + 9',18);line(s,470,100,565,100,False,True);text(s,675,48,'1 + 8',18)
    # Each answer is obtained from the same input; separate branches are explicit.
    s=start(870,240);text(s,125,132,'1 8 9 9',31);line(s,235,115,485,65,True,True);line(s,235,125,485,185,False,True);text(s,380,59,'i = 1, j = 4',18);text(s,380,200,'i = 1, j = 2',18);text(s,665,76,'1 8 9 0',31);text(s,665,196,'9 9 9',31)
    save('topics/greedy/digit-merge-extremes/assets/example.svg',s)
    s=start(900,300)
    for shift,title,stacks in [(0,'000',[[1],[2,3]]),(310,'00011',[[3],[]]),(620,'000111',[[],[]])]:
        text(s,shift+140,42,title,23)
        for j,stack in enumerate(stacks):
            x=shift+65+j*90;line(s,x-31,75,x-31,241);line(s,x-31,241,x+31,241);line(s,x+31,241,x+31,75)
            for i,v in enumerate(stack):s.append(f'<rect x="{x-25}" y="{193-i*50}" width="50" height="43" fill="#e4f4fc" stroke="#1379ad"/>');text(s,x,223-i*50,v)
        if shift<620:line(s,shift+230,146,shift+291,146,True,True)
    save('topics/data-structures/queue-with-stacks/assets/example.svg',s)
    s=start(960,410)
    for shift,labels in [(0,[(4,'1'),(2,'1'),(7,'1'),(5,'2'),(6,'1')]),(520,[(5,'2'),(2,'1'),(7,'1'),(6,'1')])]:
        positions=[(220+shift,70),(100+shift,190),(330+shift,190),(265+shift,300),(335+shift,365)]
        pairs=[(0,1),(0,2),(2,3)]+([(3,4)] if shift==0 else [])
        for a,b in pairs:line(s,*positions[a],*positions[b])
        for (v,c),(x,y) in zip(labels,positions):node(s,x,y,f'{v} × {c}')
    line(s,425,160,525,160,True,True);text(s,475,135,'−4',22)
    save('topics/data-structures/exact-search-tree/assets/example.svg',s)
    s=start(610,380);pos={1:(305,60),2:(305,160),3:(175,270),4:(90,345),5:(435,270)}
    for u,v in [(1,2),(2,3),(2,5),(3,4)]:line(s,*pos[u],*pos[v])
    for u,a in enumerate([1,2,4,5,3],1):node(s,*pos[u],f'{u}: {a}',blue=u==3)
    save('topics/trees/lexicographic-heap-labels/assets/example.svg',s)
    s=start(1400,460);pos={11:(70,105),12:(70,345),8:(245,225),9:(420,105),10:(420,345),5:(595,225),6:(770,105),7:(770,345),4:(945,225),2:(1120,105),3:(1120,345),1:(1310,225)}
    labels={1:'00',2:'1',3:'0',4:'1',5:'1',6:'1',7:'0',8:'0',9:'0',10:'1',11:'101',12:'101'}
    edges=[(3,1,'00000'),(2,1,'1111'),(4,3,'0'),(4,2,'1'),(6,4,'0'),(7,4,'1'),(5,6,'1'),(5,7,'1'),(9,5,'1'),(10,5,'1'),(8,9,'1'),(8,10,'1'),(12,8,'1'),(11,8,'1'),(4,2,'1')]
    route={(11,8),(8,9),(9,5),(5,7),(7,4),(4,2),(2,1)}
    for i,(u,v,label) in enumerate(edges):
        x,y=pos[u];xx,yy=pos[v];d=math.hypot(xx-x,yy-y);dx=(xx-x)/d;dy=(yy-y)/d;x1=x+35*dx;y1=y+35*dy;x2=xx-40*dx;y2=yy-40*dy;blue=(u,v) in route and i!=14
        if (u,v)==(4,2):
            bend=-30 if i==3 else 28;cx=(x+xx)/2-dy*bend;cy=(y+yy)/2+dx*bend
            s.append(f'<path d="M{x1} {y1}Q{cx} {cy} {x2} {y2}" fill="none" stroke="{("#1379ad" if blue else "#718096")}" stroke-width="{3 if blue else 2}" marker-end="url(#{"blue" if blue else "arrow"})"/>');lx=(x+xx)/2-dy*bend*.9;ly=(y+yy)/2+dx*bend*.9
        else:line(s,x1,y1,x2,y2,blue,True);lx=(x+xx)/2-dy*12;ly=(y+yy)/2+dx*12
        s.append(f'<rect x="{lx-9*len(label)}" y="{ly-15}" width="{18*len(label)}" height="25" rx="5" fill="white"/>');text(s,lx,ly+4,label,19,'#1379ad' if blue else '#334155')
    for u,(x,y) in pos.items():node(s,x,y,u,labels[u],u in [11,8,9,5,7,4,2,1])
    save('topics/graphs/rotating-bytes/assets/sample.svg',s)
if __name__=='__main__':main()
