"""Draw editable SVG explanations for R14 using only the standard library."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]

def svg(width,height,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#f8fafc"/><g font-family="Arial, sans-serif" fill="#15283e">'+body+'</g></svg>\n'

def text(x,y,value,size=20,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{escape(value)}</text>'

def write(topic,slug,name,content):
    p=ROOT/'topics'/topic/slug/'assets'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8',newline='\n')

def main():
    size=45;x0=88;y0=45;parts=[];blocks=[]
    def split(a,b,s):
        if a+b>6:return
        if a+b+2*s-2<=6:blocks.append((a,b,s));return
        h=s//2
        for da,db in [(0,0),(h,0),(0,h),(h,h)]:split(a+da,b+db,h)
    split(0,0,8)
    colors=['#cbe7f5','#bce5d7','#fde4b5','#dfd3f3']
    for index,(a,b,s) in enumerate(blocks):
        parts.append(f'<rect x="{x0+a*size}" y="{y0+(8-b-s)*size}" width="{s*size}" height="{s*size}" fill="{colors[index%4]}"/>')
    for i in range(9):
        parts.append(f'<path d="M{x0+i*size} {y0}V{y0+8*size} M{x0} {y0+i*size}H{x0+8*size}" stroke="#bcc9d6" fill="none"/>')
    for a,b,s in blocks:parts.append(f'<rect x="{x0+a*size+2}" y="{y0+(8-b-s)*size+2}" width="{s*size-4}" height="{s*size-4}" rx="3" stroke="#294763" stroke-width="2" fill="none"/>')
    for i in range(8):
        parts.append(text(x0+i*size+size/2,y0+8*size+28,str(i),18))
        parts.append(text(x0-23,y0+(7-i)*size+size/2+6,str(i),18))
    parts.append(text(x0+8*size+35,y0+8*size+8,'i',23))
    parts.append(text(x0-25,y0-15,'j',23))
    parts.append(text(265,475,'n = 6;  i + j ≤ 6',23))
    write('combinatorics','grox-sequence-4','triangle-blocks.svg',svg(530,510,''.join(parts)))

    parts=[text(360,39,'N = 4',24)]
    labels=['A₁(x)','A₂(x)','A₃(x)','A₄(x)']
    for i,label in enumerate(labels):parts.append(text(160+i*140,85,label,23))
    for row in range(4):
        parts.append(text(53,143+row*68,'r = '+str(row+1),18))
        for col in range(4):
            value='1' if row==0 else 'A'+str(col+1).translate(str.maketrans('1234','₁₂₃₄'))+'(x)'+('' if row==1 else '²' if row==2 else '³')
            parts.append(text(160+col*140,143+row*68,value,25))
    parts.append('<path d="M115 105H100V370H115 M625 105H640V370H625" stroke="#294763" stroke-width="3" fill="none"/>')
    parts.append(text(360,414,'Mᵣ,ᵢ = Aᵢ(x)ʳ⁻¹',25))
    write('linear-algebra','grox-sequence-7','vandermonde.svg',svg(720,450,''.join(parts)))

    parts=[];states=[([2,3,1],2),([2,1,3],1),([1,2,3],0)]
    for row,(values,position) in enumerate(states):
        y=60+row*130
        for col,value in enumerate(values):
            x=135+col*125
            parts.append(f'<rect x="{x-42}" y="{y-32}" width="84" height="64" rx="7" fill="#dbe9f6" stroke="#7e9ab6"/>')
            parts.append(text(x,y+9,str(value),28))
            if col==position:parts.append(f'<ellipse cx="{x}" cy="{y}" rx="36" ry="26" fill="none" stroke="#bf6039" stroke-width="3"/>')
            parts.append(text(x,y+58,str(col+1),16))
        if row<2:
            parts.append(f'<path d="M475 {y+34}V{y+90}" stroke="#294763" stroke-width="3" fill="none"/>')
            parts.append(f'<path d="M468 {y+81}L475 {y+90}L482 {y+81}" stroke="#294763" stroke-width="3" fill="none"/>')
            parts.append(text(495,y+67,'swap',18,'start'))
    parts.append(text(290,420,'(0) → (1)',24))
    write('sorting','gnome-sort','gnome-swaps.svg',svg(590,460,''.join(parts)))

if __name__=='__main__':main()
