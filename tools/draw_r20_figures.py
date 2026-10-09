"""Draw the student arrangement example for the retained R20 packages."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]

def start(w,h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#294c67"/></marker></defs>',f'<rect width="{w}" height="{h}" fill="#f6f9fc"/>']

def text(p,x,y,s,size=22):
    p.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{size}" fill="#17364c">{escape(str(s))}</text>')

def line(p,x,y,u,v,arrow=False):
    p.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="#294c67" stroke-width="3"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')

def save(p,path):
    dest=ROOT/'topics'/path;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('\n'.join(p+['</svg>'])+'\n','utf-8')

def main():
    p=start(1000,375);text(p,500,31,'N = 5',22)
    for i,(d,c) in enumerate(zip([0,1,0,1,1],'ABCDE')):
        x=110+i*195
        p.append(f'<rect x="{x-60}" y="61" width="120" height="124" rx="10" fill="white" stroke="#8ca6bb" stroke-width="2"/>')
        text(p,x,93,f'{i+1} : {c}')
        if d==0:line(p,x,143,x,110,True)
        else:line(p,x,109,x,143,True)
        text(p,x,170,f'f = {d}',18)
    p.append('<path d="M35 119L15 119L15 215L985 215L985 119L965 119" fill="none" stroke="#738da0" stroke-width="2" stroke-dasharray="6 4"/>')
    p.append('<circle cx="500" cy="237" r="8" fill="none" stroke="#294c67" stroke-width="2"/>')
    p.append('<path d="M483 257Q500 240 517 257" fill="none" stroke="#294c67" stroke-width="2"/>')
    holders=[1,1,2,1,5,3]
    operations=['(1, 0)','(1, 6)','(1, 6)','(0, 6)','(1, 2)']
    for i,v in enumerate(holders):
        x=78+i*169;text(p,x,340,v,26)
        if i<5:
            line(p,x+24,331,x+145,331,True);text(p,x+85,309,operations[i],18)
    text(p,500,280,'(d, p)',17)
    save(p,'simulation/side-scrolling-field-theory/assets/passing.svg')

if __name__=='__main__':main()
