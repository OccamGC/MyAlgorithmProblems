"""Draw the five R34 explanatory SVG figures with shared mathematical labels."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,label,size=23,anchor='middle',color='#17324d'):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(str(label))}</text>'
def line(x,y,xx,yy,arrow=False,dashed=False):
    return f'<path d="M{x},{y} L{xx},{yy}" stroke="#526a80" stroke-width="2.5" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 5"' if dashed else '')+'/>'
def box(x,y,label,fill='#eaf3fa',width=86,height=58):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="{fill}" stroke="#244961" stroke-width="2"/>'+text(x+width/2,y+height/2+8,label)
def save(topic,slug,body,height=340):
    p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(exist_ok=True)
    p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {height}" role="img"><rect width="800" height="{height}" fill="white"/><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10" fill="#526a80"/></marker></defs>'+body+'</svg>','utf-8')
body=text(65,102,'a')
for i,v in enumerate([5,3,3,4,2]):
    x=150+110*i;body+=box(x,65,v)+text(x+43,49,i+1,17)
    if i in [1,2]:body+=line(x+20,72,x+65,116)+line(x+65,72,x+20,116)
body+=line(405,145,405,195,True)+text(65,250,'S')
for i,v in enumerate([5,4,2]):body+=box(240+110*i,214,v,'#dff2e8')
body+=text(405,312,'5 > 4 > 2',21);save('data-structures','dynamic-decreasing-stack',body)
body=text(400,35,'a = 1, b = 2, X = 3')
for i,v in enumerate([1,2,3,1]):body+=box(60+i*200,154,v,'#eaf3fa',78)
for i in range(3):
    x=138+200*i;body+=line(x,183,x+117,183,True)+text(x+61,130,f't = {i}',20)+text(x+61,237,'+3 − 2' if i<2 else '−2',22)
body+=text(240,302,'E → E + X − b',22)+text(580,302,'E → E − b',22);save('scheduling','shared-charger',body)
body=''
for i in range(3):body+=line(113+190*i,145,237+190*i,145)+text(170+190*i,112,['{0, 2}','{1}','{2, 3}'][i],23)
for i in range(4):
    x=80+190*i;body+=f'<circle cx="{x}" cy="145" r="33" fill="#eaf3fa" stroke="#244961" stroke-width="2"/>'+text(x,153,i+1)+text(x,215,'[1, 1]' if i==2 else '[0, 0]',22)
body+=text(400,282,'p ∈ {0, 2},  w = 1,  w − p ∉ [0, 0]',23);save('trees','tolerance-paths',body)
body=text(55,93,'p')+text(55,246,'q')
for i,v in enumerate([2,1,4,3]):body+=box(200+110*i,56,v,'#dff2e8' if i<3 else '#eaf3fa')
for i,v in enumerate([1,2,1,4,1]):body+=box(90+110*i,209,v,'#dff2e8' if 1<=i<=3 else '#eaf3fa')
for i in range(3):body+=line(243+110*i,123,243+110*i,200,False,True)
body+=text(400,314,'LCS(p, q) = 3',23);save('interactive','substring-permutation',body)
body=text(65,147,'a')
for i,v in enumerate([-1,-1,-1,2]):body+=box(180+125*i,110,v)+text(223+125*i,99,i+1,18)
body+=line(183,65,511,65)+line(183,65,183,80)+line(511,65,511,80)+text(347,43,'I = [1, 3]',23)
body+=line(307,195,636,195)+line(307,180,307,195)+line(636,180,636,195)+text(472,230,'J = [2, 4]',23)+text(400,302,'3 × 2 + 0 × 1 = 6',25)
save('data-structures','you-wrote-this-problem',body)
print('Drew five mathematical-label SVGs.')
