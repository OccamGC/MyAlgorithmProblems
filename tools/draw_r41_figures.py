"""Draw the four legal moves that attain 98/9 with exactly two slots."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]


def text(x,y,value,size=20,anchor='middle',color='#183247'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>'


def main():
    titles=['0','1: T₁ → B','2: O₁ → A','3: T₂ → B','4: O₂ → A']
    members_a=['T₁  T₂','T₂','T₂  O₁','O₁','O₁  O₂']
    members_b=['O₁  O₂','T₁  O₁  O₂','T₁  O₂','T₁  T₂  O₂','T₁  T₂']
    wealth_a=['2','1','22/3','11/3','82/9']
    wealth_b=['18','19','38/3','49/3','98/9']
    parts=[]
    for i in range(5):
        x=18+225*i
        parts.append(text(x+98,37,titles[i],21))
        for slot,y,members,money in [('A',63,members_a[i],wealth_a[i]),('B',207,members_b[i],wealth_b[i])]:
            final=(i==4 and slot=='B')
            parts.append(f'<rect x="{x}" y="{y}" width="196" height="124" rx="12" fill="{"#fff2bd" if final else "#eaf2f8"}" stroke="{"#b17d00" if final else "#7b9bb5"}" stroke-width="2"/>')
            parts.extend([text(x+17,y+27,slot,20,'start'),text(x+98,y+59,members,23),text(x+98,y+98,'M = '+money,24)])
        if i<4:
            parts.append(f'<path d="M{x+200} 195 H{x+222}" stroke="#376986" stroke-width="2" marker-end="url(#arrow)"/>')
    parts += [text(565,376,'T: target residents     O: other residents     M: household Simoleons',20)]
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="1132" height="402" viewBox="0 0 1132 402"><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#376986"/></marker></defs><rect x="1" y="1" width="1130" height="400" rx="12" fill="#fbfdff" stroke="#a8bece"/>'+''.join(parts)+'</svg>'
    dest=ROOT/'topics/greedy/town-editing-simoleons-3/assets/example.svg'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(svg,encoding='utf-8',newline='\n')


if __name__=='__main__':main()
