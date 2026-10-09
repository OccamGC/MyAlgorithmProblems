"""Draw the string, rail and Hanoi examples with language-neutral labels."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def svg(width,height,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#f8fafc"/>
<g font-family="Arial, sans-serif" font-size="20" fill="#193247" text-anchor="middle">{body}</g></svg>\n'''

def write(topic,slug,name,text):
    path=ROOT/'topics'/topic/slug/'assets'/name
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')

def main():
    body=''
    for row,(label,text,added) in enumerate([('S0','abcde',0),('S1','eabcde',1),('S2','eeeabcde',2)]):
        y=32+row*88
        body+=f'<text x="38" y="{y+26}">{label}</text>'
        for i,char in enumerate(text):
            x=80+i*48
            fill='#cfe7db' if i<added else '#dbeafa'
            body+=f'<rect x="{x}" y="{y}" width="42" height="40" rx="5" fill="{fill}" stroke="#60809a"/><text x="{x+21}" y="{y+27}">{char}</text>'
        if row<2:
            body+=f'<path d="M 274 {y+47} v 28 m -5 -6 l 5 6 5 -6" fill="none" stroke="#426580" stroke-width="2"/><text x="397" y="{y+66}" font-size="16">p={4+row}, D={1+row}</text>'
    write('strings','paper-tiger-sequence','growth.svg',svg(500,300,body))

    body=''
    coords={1:(92,92),2:(92,246),3:(290,170),4:(500,170)}
    edges=[(1,2,-5,64,172,True),(2,3,-4,178,194,True),(1,3,-3,205,115,True),(3,4,7,397,148,True),(2,4,9,310,240,False)]
    for a,b,w,lx,ly,chosen in edges:
        x1,y1=coords[a];x2,y2=coords[b]
        body+=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{"#2f775c" if chosen else "#8998a6"}" stroke-width="{4 if chosen else 2}"'+(' stroke-dasharray="7 5"' if not chosen else '')+'/>'
        body+=f'<rect x="{lx-19}" y="{ly-20}" width="38" height="27" fill="#f8fafc"/><text x="{lx}" y="{ly}">{w}</text>'
    body+='<path d="M 72 78 C 0 14, 157 7, 111 76" fill="none" stroke="#2f775c" stroke-width="4"/><text x="88" y="27">-2</text>'
    body+='<path d="M 480 151 C 431 92, 566 92, 520 151" fill="none" stroke="#8998a6" stroke-width="2" stroke-dasharray="7 5"/><text x="500" y="100">0</text>'
    for v,(x,y) in coords.items():body+=f'<circle cx="{x}" cy="{y}" r="23" fill="#e5eef6" stroke="#426580" stroke-width="2"/><text x="{x}" y="{y+7}">{v}</text>'
    body+='<text x="296" y="318">-5 -4 -3 -2 +7 = -7</text>'
    write('graphs','simple-rail-network','network.svg',svg(580,350,body))

    body=''
    states=[[[1,2],[],[]],[[1],[],[2]],[[],[1],[2]],[[],[1,2],[]]]
    for step,stacks in enumerate(states):
        ox=20+step*190
        body+=f'<text x="{ox+78}" y="30">t={step}</text>'
        for peg,stack in enumerate(stacks):
            x=ox+peg*52+25
            body+=f'<line x1="{x}" y1="75" x2="{x}" y2="164" stroke="#a3adb5" stroke-width="4"/><text x="{x}" y="192">{"ABC"[peg]}</text>'
            for level,disk in enumerate(stack):
                width=45 if disk==1 else 29;y=139-level*26
                body+=f'<rect x="{x-width/2}" y="{y}" width="{width}" height="23" rx="3" fill="{"#cfe7db" if disk==1 else "#dbeafa"}" stroke="#426580"/><text x="{x}" y="{y+18}" font-size="16">{disk}</text>'
        if step<3:body+=f'<path d="M {ox+160} 105 h 20 m -5 -5 l 5 5 -5 5" fill="none" stroke="#426580" stroke-width="2"/>'
    write('recursion','block-tower','moves.svg',svg(780,220,body))
    print('Drew three SVG figures.')

if __name__=='__main__':main()
