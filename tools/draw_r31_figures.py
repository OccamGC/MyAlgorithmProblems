"""Draw editable SVG explanations using only the Python standard library."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,value,size=22,color='#172b4d'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="middle">{escape(str(value))}</text>'
def line(x1,y1,x2,y2,dash=False,arrow=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#506680" stroke-width="2"'+(' stroke-dasharray="6 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def box(x,y,w,h,label,selected=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="'+('#dcf5eb' if selected else '#edf2fa')+'" stroke="'+('#16775b' if selected else '#8393aa')+'" stroke-width="2"/>'+text(x+w/2,y+h/2+8,label)
def save(topic,slug,name,body,height=300):
    d=ROOT/'topics'/topic/slug/'assets';d.mkdir(parents=True,exist_ok=True)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{height}" viewBox="0 0 800 {height}" role="img"><defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7" fill="#506680"/></marker></defs><rect width="800" height="{height}" fill="white"/><g font-family="Arial, sans-serif">'+body+'</g></svg>\n'
    (d/name).write_text(svg,'utf-8')
def main():
    body=text(400,34,'copy: (0, 0) → (1, 0)')
    for i,v in enumerate([1,1,0,1,0,0]):
        body+=text(150+i*100,66,i,16)+box(108+i*100,82,84,48,v,i<3)+box(108+i*100,193,84,48,[1,1,0,1,1,0][i],i>=3)
    body+=line(400,53,400,256,True)+line(250,145,550,179,arrow=True)+text(250,281,'array 0',18)+text(550,281,'array 1',18)
    save('simulation','memory-functions','memory.svg',body)
    body=text(400,40,'3 < 2 < 1')+box(80,93,260,64,'(3 < 2) < 1')+line(360,125,440,125,arrow=True)+box(460,93,260,64,'0 < 1')+line(590,176,590,220,arrow=True)+box(530,232,120,48,'1',True)
    save('parsing','small-integer-calculator','expression.svg',body)
    body=text(400,38,'m = 3,  k = 3')+line(90,132,730,132)
    for x,value,distance in zip([110,168,226,632,690],[1,2,3,10,11],[2,1,0,7,8]):
        body+=f'<circle cx="{x}" cy="132" r="24" fill="'+('#dcf5eb' if value<=3 else '#edf2fa')+'" stroke="#506680" stroke-width="2"/>'+text(x,140,value)+text(x,203,distance,20)
        if value<=3:body+=f'<circle cx="{x}" cy="132" r="28" fill="none" stroke="#16775b" stroke-width="2"/>'
    body+=text(400,252,'distance = |value − m|',20)+text(400,283,'1 + 2 + 3 = 6',20)
    save('selection','nearest-median','median.svg',body)
    body=text(400,37,'K = 1,  t = 2')+box(60,90,130,70,'AA')+box(280,90,130,70,'TT')+line(208,111,262,111,arrow=True)+line(262,143,208,143,arrow=True)+box(480,90,110,70,'AT',True)+box(645,90,110,70,'TA',True)
    body+=text(235,211,'{AA, TT}',20)+text(535,211,'{AT}',20)+text(700,211,'{TA}',20)+text(400,270,'3 classes',22)
    save('combinatorics','strand-length-range','strands.svg',body)
    body=text(400,39,'L = 20')
    for i,v in enumerate([3,12,16,17,17]):body+=box(93+i*128,88,102,60,v,i<2)
    body+=line(94,179,322,179)+text(208,212,'3 + 12 = 15 ≤ 20',20)+line(94,240,450,240)+text(272,273,'3 + 12 + 16 = 31 > 20',20)
    save('selection','generated-budget-selection','budget.svg',body)
if __name__=='__main__':main()
