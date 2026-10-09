"""Editable SVG explanations for interval statistics, dependencies and traversals."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]

def text(x,y,value,size=20):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle">{escape(value)}</text>'

def svg(width,height,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#426887"/></marker></defs><rect width="100%" height="100%" fill="#f8fafc"/><g fill="#15283e" font-family="Arial, sans-serif">{body}</g></svg>\n'

def write(topic,slug,name,body):
    path=ROOT/'topics'/topic/slug/'assets'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(body,encoding='utf-8',newline='\n')

def main():
    parts=[]
    parts.append('<rect x="255" y="23" width="311" height="102" rx="12" fill="#dbf0e8" stroke="#397861" stroke-width="2" stroke-dasharray="8 5"/>')
    for i,value in enumerate([1,2,3,9,9]):
        x=90+i*105
        parts.append(text(x,48,'b'+str(i+1).translate(str.maketrans('12345','₁₂₃₄₅')),17))
        parts.append(f'<rect x="{x-32}" y="61" width="64" height="49" rx="5" fill="white" stroke="#567990" stroke-width="2"/>')
        parts.append(text(x,94,str(value),26))
    parts.append('<path d="M275 133V144H325V133 M300 144V167" fill="none" stroke="#bc6038" stroke-width="2"/>')
    parts.extend([text(300,194,'2 × b₃ = 6',23),text(415,240,'b₃ + b₄ + b₅ = 21',23),text(98,239,'L = 5',22)])
    for slug in ['interval-top-half','interval-median']:
        write('data-structures',slug,'partition.svg',svg(610,270,''.join(parts)))

    parts=[]
    coordinates={3:(70,150),1:(225,150),2:(395,65),4:(395,240),5:(565,150)}
    for a,b in [(3,1),(1,2),(1,4),(2,5),(4,5)]:
        x,y=coordinates[a];xx,yy=coordinates[b]
        dx,dy=xx-x,yy-y;length=(dx*dx+dy*dy)**0.5
        parts.append(f'<path d="M{x+dx*28/length} {y+dy*28/length}L{xx-dx*31/length} {yy-dy*31/length}" fill="none" stroke="#426887" stroke-width="2.5" marker-end="url(#arrow)"/>')
    for u,duration,finish in [(3,-1,0),(1,3,3),(2,5,8),(4,2,5),(5,4,12)]:
        x,y=coordinates[u]
        parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{"#e6edf3" if u==3 else "#d9eee5"}" stroke="#426887" stroke-width="2"'+(' stroke-dasharray="5 3"' if u==3 else '')+'/>')
        parts.append(text(x,y+8,str(u),24))
        parts.append(text(x,y+51,f't{str(u).translate(str.maketrans("12345","₁₂₃₄₅"))} = {duration}',17))
        parts.append(text(x,y+74,f'T{str(u).translate(str.maketrans("12345","₁₂₃₄₅"))} = {finish}',17))
    write('graphs','technology-tree','research.svg',svg(650,340,''.join(parts)))

    parts=['<path d="M284 67L196 128 M316 67L404 128" stroke="#426887" stroke-width="3" fill="none"/>']
    for value,x,y in [(2,300,52),(1,180,147),(3,420,147)]:
        parts.append(f'<circle cx="{x}" cy="{y}" r="27" fill="#dcebf7" stroke="#426887" stroke-width="2"/>')
        parts.append(text(x,y+9,str(value),26))
    parts.extend([text(300,224,'pre = (2, 1, 3)',23),text(300,266,'in = (1, 2, 3)',23),text(300,308,'post = (1, 3, 2)',23)])
    write('trees','binary-traversals','traversals.svg',svg(600,345,''.join(parts)))

if __name__=='__main__':
    main()
