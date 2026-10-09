"""Draw editable diagrams for character patterns, trees, lists and bit rotations."""
from html import escape
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]

def start(width,height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#536779"/></marker></defs>', f'<rect width="{width}" height="{height}" fill="#f8fafc"/>']

def text(parts,x,y,value,size=22,color='#1b354b',anchor='middle'):
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{escape(str(value))}</text>')

def line(parts,x1,y1,x2,y2,arrow=False,color='#536779',width=3):
    parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')

def save(parts,path):
    dest=ROOT/'topics'/path;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('\n'.join(parts+['</svg>'])+'\n',encoding='utf-8',newline='\n')

def main():
    p=start(670,525);text(p,340,32,'8 × 10')
    for j in range(10):text(p,106+j*48,69,j+1,17)
    for i in range(8):
        text(p,51,107+i*48,i+1,17)
        for j in range(10):
            filled=i<=j<=i+2 or 7-i<=j<=9-i
            x=82+j*48;y=82+i*48
            p.append(f'<rect x="{x}" y="{y}" width="48" height="48" fill="'+('#287ea0' if filled else '#ffffff')+'" stroke="#b9c7d3"/>')
            text(p,x+24,y+32,'c' if filled else '·',24,'#ffffff' if filled else '#8094a4')
    text(p,336,501,'c = character     · = space',19)
    save(p,'simulation/character-x/assets/pattern.svg')

    p=start(1100,420);positions={}
    for depth in range(4):
        for k in range(2**depth):positions[2**depth+k]=(55+(k+.5)*990/(2**depth),45+depth*100)
    path={(1,2),(2,5),(5,10)}
    for v in range(2,16):
        a=positions[v//2];b=positions[v]
        line(p,*a,*b,color='#be6419' if (v//2,v) in path else '#9dacb8',width=5 if (v//2,v) in path else 2)
    for v,(x,y) in positions.items():
        p.append(f'<circle cx="{x}" cy="{y}" r="23" fill="white" stroke="'+('#be6419' if v in (1,2,5,10) else '#287ea0')+'" stroke-width="3"/>')
        text(p,x,y+8,v)
    text(p,550,402,'1 → 2 → 5 → 10 : 3 edges',20)
    save(p,'trees/heap-tree-distance/assets/tree.svg')

    p=start(1000,410)
    text(p,500,34,'id : value',22)
    def row(label,items,y):
        text(p,85,y+36,label,22)
        for i,item in enumerate(items):
            x=180+i*225
            p.append(f'<rect x="{x}" y="{y}" width="155" height="60" rx="9" fill="white" stroke="#287ea0" stroke-width="3"/>')
            text(p,x+77,y+38,item,24)
            if i+1<len(items):
                line(p,x+160,y+23,x+219,y+23,True)
                line(p,x+219,y+42,x+160,y+42,True)
        text(p,180+len(items)*225,y+37,'NULL',20)
    row('L1',['1 : 1','2 : 2'],60)
    row('L2',['3 : 3'],145)
    line(p,790,115,790,235,True);text(p,865,186,'3–8',20)
    row('L1',['4 : 4','2 : −7'],245)
    row('L2',['3 : 3','5 : 5'],325)
    save(p,'data-structures/variable-lists/assets/lists.svg')

    p=start(970,435);pos={1:(100,200),2:(430,100),3:(590,200),4:(430,320),5:(750,200),6:(900,200),7:(290,100),8:(285,320)}
    targets={2:3,3:4,4:2,5:3,6:5,7:2,8:4}
    for a,b in targets.items():
        x,y=pos[a];u,v=pos[b];dx=u-x;dy=v-y;length=math.hypot(dx,dy)
        line(p,x+dx*29/length,y+dy*29/length,u-dx*31/length,v-dy*31/length,True)
    p.append('<path d="M78 180C15 105 185 105 122 180" fill="none" stroke="#536779" stroke-width="3" marker-end="url(#arrow)"/>')
    for v,(x,y) in pos.items():
        p.append(f'<circle cx="{x}" cy="{y}" r="27" fill="'+('#e6f4fa' if v<=4 else 'white')+'" stroke="#287ea0" stroke-width="3"/>')
        if v<=4:p.append(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="#287ea0"/>')
        text(p,x,y+8,v)
    text(p,485,408,'Cycles: (1), (2 → 3 → 4 → 2)     Answer: 4',23)
    save(p,'graphs/didu-hia-signifier-cycles/assets/cycles.svg')

    p=start(830,305);text(p,415,30,'8-bit illustration / rotate right by 3',22)
    for row,bits in enumerate(['00011101','10100011']):
        for j,bit in enumerate(bits):
            x=95+j*80;y=55+row*160
            p.append(f'<rect x="{x}" y="{y}" width="70" height="55" rx="5" fill="'+('#e6f4fa' if (j>=5 if row==0 else j<3) else 'white')+'" stroke="#287ea0" stroke-width="2"/>')
            text(p,x+35,y+36,bit,28)
        text(p,60,90+row*160,'7',16);text(p,770,90+row*160,'0',16)
    line(p,610,119,210,200,True,color='#be6419')
    text(p,605,170,'wrap',18)
    save(p,'bitwise/signal-network/assets/rotation.svg')
    print('Wrote five SVG diagrams.')

if __name__=='__main__':main()
