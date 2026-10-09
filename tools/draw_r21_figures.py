"""Draw neutral-symbol figures for the R21 statements."""
from pathlib import Path
from html import escape
import math
ROOT=Path(__file__).resolve().parents[1]
def start(w,h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">','<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#264c66"/></marker></defs>',f'<rect width="{w}" height="{h}" rx="10" fill="#f5f8fc"/>']
def text(p,x,y,s,size=22):p.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{size}" fill="#17364c">{escape(str(s))}</text>')
def line(p,x,y,u,v,arrow=False,color='#264c66',width=3,both=False):p.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' marker-start="url(#arrow)"' if both else '')+'/>')
def circle(p,x,y,r=25,fill='white'):p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#264c66" stroke-width="2"/>')
def save(p,path):
    dest=ROOT/'topics'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(p+['</svg>'])+'\n','utf-8')
def draw_candy():
    p=start(700,385)
    examples=[
        (['●','●'],['-10','100'],'S = 90','B = 100'),
        (['(',')'],['-4','7'],'S = 3','B = 3'),
        (['(','●',')'],['-8','10','-9'],'S = -7','B = 10'),
    ]
    for row,(symbols,values,total,best) in enumerate(examples):
        y=55+row*120
        for i,(symbol,value) in enumerate(zip(symbols,values)):
            x=90+i*85;text(p,x,y,symbol,34);text(p,x,y+32,value,18)
        line(p,340,y-8,460,y-8,True)
        text(p,565,y,'●',34)
        text(p,565,y+30,total,20)
        text(p,565,y+56,best,20)
    save(p,'strings/candy-brackets/assets/reductions.svg')

def main():
    draw_candy()
    p=start(670,330)
    coords={1:(95,150),2:(240,150),3:(485,70),4:(385,245),5:(585,245)}
    p.append('<path d="M116 131Q168 85 217 131" fill="none" stroke="#264c66" stroke-width="3" marker-end="url(#arrow)"/>')
    p.append('<path d="M219 169Q169 219 117 169" fill="none" stroke="#264c66" stroke-width="3" marker-end="url(#arrow)"/>')
    for a,b in [(3,4),(4,5),(5,3)]:
        x,y=coords[a];u,v=coords[b];d=math.hypot(u-x,v-y);line(p,x+29*(u-x)/d,y+29*(v-y)/d,u-29*(u-x)/d,v-29*(v-y)/d,True)
    for i,(x,y) in coords.items():circle(p,x,y);text(p,x,y+8,i)
    text(p,167,292,'2');text(p,485,310,'3')
    save(p,'number-theory/permutation-order/assets/cycles.svg')
    p=start(500,380)
    for i in range(2):
        for j in range(2):
            road=(i,j)!=(0,1);x=90+j*160;y=35+i*160
            p.append(f'<rect x="{x}" y="{y}" width="150" height="150" fill="'+('#ffffff' if road else '#d4dce6')+'" stroke="#264c66" stroke-width="2"/>')
            if not road:
                for offset in range(20,130,25):line(p,x+offset,y+12,x+offset+20,y+35,color='#a5b3c1',width=2)
            text(p,x+75,y+86,1 if road else 0,28)
    line(p,165,139,165,236,True,both=True);line(p,197,270,293,270,True,both=True)
    save(p,'probability/grid-survival/assets/grid.svg')
    p=start(750,365);coords={1:(100,70),2:(365,105),3:(650,70),4:(365,285),5:(100,285)}
    for u,v,c,lx,ly in [(1,2,5,227,70),(2,3,2,510,70),(4,2,1,392,205),(4,5,9,230,310),(1,5,20,66,180)]:
        x,y=coords[u];a,b=coords[v];line(p,x,y,a,b,color='#157862' if (u,v) in [(2,3),(4,2)] else '#7f92a4',width=5 if (u,v) in [(2,3),(4,2)] else 2);text(p,lx,ly,c,21)
    for i,(x,y) in coords.items():
        circle(p,x,y,32);text(p,x,y+6,i,22)
        if i in [1,4]:text(p,x+48,y-18,'S',18)
        if i in [3,5]:text(p,x+48,y-18,'T',18)
    save(p,'graphs/nearest-terminal-sets/assets/network.svg')

if __name__=='__main__':main()
