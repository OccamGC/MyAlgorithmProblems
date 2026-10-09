"""Rebuild the two-target household averaging example."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def text(x,y,value,size=20,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="{anchor}" fill="#183247">{value}</text>'


def main():
    parts=[]
    for i,label in enumerate(['T₁','T₂','O₁','O₂']):
        parts.append(text(53,104+77*i,label,23))
    for x,values in [(170,[1,1,9,9]),(435,[5,3,3,9]),(700,[7,5,3,5])]:
        for i,value in enumerate(values):
            y=96+77*i
            color='#fff0b5' if i<2 else '#e4f1fb'
            parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{color}" stroke="#245d87" stroke-width="2"/>')
            parts.append(text(x,y+8,str(value),24))
    for left,right,labels in [(211,391,['O₁ ↔ T₁','O₁ ↔ T₂']),(476,656,['O₂ ↔ T₁','O₂ ↔ T₂'])]:
        parts.append(f'<path d="M{left} 216 H{right}" stroke="#245d87" stroke-width="3" marker-end="url(#arrow)"/>')
        parts.append(text((left+right)/2,191,labels[0],18))
        parts.append(text((left+right)/2,247,labels[1],18))
    parts += [text(170,40,'0'),text(435,40,'1'),text(700,40,'2'),
              text(170,391,'1 + 1 = 2',22),text(435,391,'5 + 3 = 8',22),text(700,391,'7 + 5 = 12',22)]
    parts.append('<rect x="655" y="54" width="90" height="158" rx="12" fill="none" stroke="#9c6e06" stroke-width="2" stroke-dasharray="5 4"/>')
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="850" height="425" viewBox="0 0 850 425"><defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L9 4 L0 8 Z" fill="#245d87"/></marker></defs><rect x="1" y="1" width="848" height="423" rx="12" fill="#f8fbfe" stroke="#8ba6ba"/>'+''.join(parts)+'</svg>'
    p=ROOT/'topics/greedy/town-editing-simoleons-2/assets/example.svg'
    p.write_text(svg,encoding='utf-8',newline='\n')


if __name__=='__main__':main()
