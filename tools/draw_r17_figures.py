"""Draw a language-neutral insertion/deletion example for the roboport ring."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    body=['<rect width="760" height="430" fill="#f8fafc"/>',
          '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#3c647e"/></marker></defs>']
    for row,(label,items,current) in enumerate([('t = 0',[1,2,3],1),('op = 1',[1,4,2,3],1),('op = 0',[4,2,3],4)]):
        y=65+row*135
        body.append(f'<text x="72" y="{y+7}" font-size="20">{label}</text>')
        positions=[200+135*i for i in range(len(items))]
        for i in range(len(items)-1):
            body.append(f'<path d="M {positions[i]+29} {y} H {positions[i+1]-31}" fill="none" stroke="#3c647e" stroke-width="2.5" marker-end="url(#arrow)"/>')
        body.append(f'<path d="M {positions[-1]+29} {y} H {positions[-1]+50} V {y+55} H {positions[0]-50} V {y} H {positions[0]-31}" fill="none" stroke="#3c647e" stroke-width="2.5" marker-end="url(#arrow)"/>')
        for x,value in zip(positions,items):
            body.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{"#d6eee3" if value==current else "#e0ebf6"}" stroke="#3c647e" stroke-width="2"/>')
            if value==current:
                body.append(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="#3c647e" stroke-width="1.5"/>')
            body.append(f'<text x="{x}" y="{y+7}" font-size="21">{value}</text>')
    text='<svg xmlns="http://www.w3.org/2000/svg" width="760" height="430" viewBox="0 0 760 430"><g font-family="Arial, sans-serif" fill="#193247" text-anchor="middle">'+''.join(body)+'</g></svg>\n'
    path=ROOT/'topics/data-structures/robot-platforms/assets/ring.svg'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

if __name__=='__main__':
    main()
