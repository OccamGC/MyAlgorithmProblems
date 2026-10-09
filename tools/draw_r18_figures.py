"""Draw rectangle, matrix-operation and overlapping-substring illustrations."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def svg(width,height,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#f8fafc"/><g font-family="Arial,sans-serif" text-anchor="middle" fill="#193247">'+body+'</g></svg>\n'

def write(topic,slug,name,text):
    path=ROOT/'topics'/topic/slug/'assets'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def main():
    body=''
    rectangles=[((0,0,3,3),(1,1,4,4)),((0,0,4,4),(2,1,2,3)),((0,2,4,2),(2,0,2,4)),((0,0,1,1),(2,2,4,4))]
    for panel,(A,B) in enumerate(rectangles):
        ox=35+panel*220;oy=190;scale=32
        body+=f'<text x="{ox+64}" y="28" font-size="20">{panel+1}</text>'
        for box,color,dash,label in [(A,'#277ca4','','A'),(B,'#b06b16',' stroke-dasharray="6 3"','B')]:
            l,b,r,t=box;x=ox+l*scale;y=oy-t*scale
            if l==r or b==t:
                body+=f'<line x1="{x}" y1="{y}" x2="{ox+r*scale}" y2="{oy-b*scale}" stroke="{color}" stroke-width="6"{dash}/>'
            else:
                body+=f'<rect x="{x}" y="{y}" width="{(r-l)*scale}" height="{(t-b)*scale}" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-width="2.5"{dash}/>'
            label_x=ox+l*scale+10 if b==t else ox+(l+r)*scale/2
            body+=f'<text x="{label_x}" y="{oy-t*scale-9}" font-size="17" fill="{color}">{label}</text>'
        if panel==0:
            body+=f'<rect x="{ox+32}" y="{oy-96}" width="64" height="64" fill="#875fb8" fill-opacity="0.24" stroke="#6b4696" stroke-width="2"/>'
        elif panel==1:
            body+=f'<line x1="{ox+64}" y1="{oy-32}" x2="{ox+64}" y2="{oy-96}" stroke="#6b4696" stroke-width="3"/>'
        elif panel==2:
            body+=f'<circle cx="{ox+64}" cy="{oy-64}" r="7" fill="#6b4696" stroke="white" stroke-width="2"/>'
    text=svg(900,225,body)
    for slug in ['rectangle-intersection','rectangle-intersection-type']:
        write('geometry',slug,'intersections.svg',text)

    body=''
    states=[[[1,2,3],[4,5,6]],[[4,5,6],[1,2,3]],[[4,6,5],[1,3,2]],[[1,4],[3,6],[2,5]]]
    for panel,grid in enumerate(states):
        ox=22+panel*215
        body+=f'<text x="{ox+78}" y="29" font-size="20">'+['t = 0','1 1 2','2 2 3','3'][panel]+'</text>'
        for i,row in enumerate(grid):
            for j,value in enumerate(row):
                x=ox+j*44;y=65+i*44
                body+=f'<rect x="{x}" y="{y}" width="42" height="42" rx="4" fill="#dfeefa" stroke="#426580"/><text x="{x+21}" y="{y+28}" font-size="21">{value}</text>'
        if panel<3:
            body+=f'<path d="M {ox+154} 113 h 28 m -7 -6 l 7 6 -7 6" fill="none" stroke="#426580" stroke-width="2.5"/>'
    write('simulation','matrix-mixer','operations.svg',svg(870,215,body))

    body=''
    for i,c in enumerate('aaababa'):
        x=110+i*58
        body+=f'<text x="{x+25}" y="27" font-size="17">{i+1}</text><rect x="{x}" y="43" width="50" height="45" rx="4" fill="#dfeefa" stroke="#426580"/><text x="{x+25}" y="74" font-size="25">{c}</text>'
    body+='<text x="48" y="72" font-size="21">S</text>'
    for row,(l,r) in enumerate([(3,5),(5,7)]):
        y=113+row*48;x=110+(l-1)*58;right=110+(r-1)*58+50
        body+=f'<path d="M {x} {y-9} v 9 H {right} v -9" fill="none" stroke="#356a56" stroke-width="2.5"/><text x="{(x+right)/2}" y="{y+23}" font-size="19">aba [{l},{r}]</text>'
    write('strings','skewer-substrings','overlaps.svg',svg(555,200,body))
    print('Wrote four SVG files (three illustrations).')

if __name__=='__main__':
    main()
