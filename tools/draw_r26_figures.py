"""Draw language-neutral mathematical diagrams used by both language editions."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
BLUE='#205b99';TEAL='#15766e';RED='#b03c47';INK='#152b43';MUTED='#526579'
def text(x,y,value,size=24,color=INK,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'
def rect(x,y,w,h,fill='#eef5fb',stroke=BLUE,r=10):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def line(x1,y1,x2,y2,color=BLUE,width=3,dash=False):return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 5"' if dash else '')+'/>'
def arrow(x1,y1,x2,y2):return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrow)"/>'
def tile(x,y,value,w=68,h=64,stroke=BLUE):return rect(x,y,w,h,stroke=stroke)+text(x+w/2,y+h/2+9,value,26)
def save(topic,slug,body,height):
    p=ROOT/'topics'/topic/slug/'assets/explanation.svg';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{BLUE}"/></marker></defs><rect width="960" height="{height}" fill="white"/>'+body+'</svg>\n','utf-8')
def main():
    s=text(480,40,'(b, c, ℓ)',22)
    for i in range(5):s+=tile(125+i*92,75,i+1)
    s+=text(740,115,'(1, 1, 5)',26,TEAL)+line(140,156,540,156,TEAL)+text(600,164,'✓',30,TEAL)
    for row in range(2):
        for i in range(3):s+=tile(125+i*92,205+row*100,i+1,stroke=RED)
        s+=text(575,248+row*100,'(1, 1, 3)',26,RED)
    s+=line(720,230,790,355,RED,6)+line(790,230,720,355,RED,6)
    save('dynamic-programming','distinct-tile-runs',s,410)
    s=''
    for r in range(3):
        s+=rect(56,45+r*100,284,82,'#f7fafc',BLUE)
        s+=rect(608,45+r*100,284,82,'#f3faf6',TEAL)
        for c in range(3):s+=tile(70+c*90,54+r*100,c+1)+tile(622+c*90,54+r*100,r+1,stroke=TEAL)
    s+=arrow(379,182,572,182)
    s+=text(480,380,'3 × 3 = 9',26)
    save('dynamic-programming','prefix-tile-groups',s,425)
    s=rect(364,36,232,80)+text(480,86,'f(3)',30)
    s+=arrow(422,118,266,242)+arrow(538,118,694,242)
    s+=text(315,161,'C = 7',23)+text(650,161,'D = 4',23)
    s+=rect(123,245,282,78,stroke=TEAL)+rect(553,245,282,78,stroke=TEAL)
    s+=text(264,294,'f(2) = 1',26)+text(694,294,'f(3 − e) = 1',26)
    s+=text(480,378,'7 × 1 + 4 × 1 = 11',28)
    save('number-theory','old-yd-disjoint-set',s,420)
    s=text(66,66,'i',22,MUTED)+text(66,122,'Aᵢ',24,MUTED)
    for i,v in enumerate([3,4,2,-1,5,7,6],1):
        x=78+i*107;s+=text(x+37,66,i,22,MUTED)+tile(x,82,v,74,60,TEAL if i==3 else BLUE)
    for row,l in enumerate([1,2,3]):
        y=198+row*57;x1=78+l*107+8;x2=78+3*107+66;s+=line(x1,y,x2,y,TEAL,5)+text(695,y+8,f'[{l}, 3] : '+str([9,6,2][row]),24)
    s+=text(480,388,'L₃ = 0, R₃ = 4;   2 × (9 + 6 + 2) = 34',26)
    save('data-structures','minimum-weighted-subarrays',s,430)
    s=text(48,260,'i',24,MUTED)+text(48,328,'Pᵢ',24,MUTED)
    for i,v in enumerate([0,1,0,2,0]):
        x=100+i*176;s+=text(x+34,260,i,24,MUTED)+tile(x,284,v,68,64,TEAL if v==0 else BLUE)
    for a,b,y,label in [(0,2,148,'2'),(2,4,148,'2'),(0,4,34,'4')]:
        x1=134+a*176;x2=134+b*176
        s+=f'<path d="M{x1},236 Q{(x1+x2)/2},{y} {x2},236" fill="none" stroke="{TEAL}" stroke-width="3"/>'
        s+=text((x1+x2)/2,(236+y)/2-12,label,26,TEAL)
    s+=text(480,408,'2 + 2 + 4 = 8',28)
    save('data-structures','clue-generator',s,450)
if __name__=='__main__':main()
