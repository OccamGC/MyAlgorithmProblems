"""Draw five bilingual, mathematical SVG examples without external packages."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def canvas():return ['<svg xmlns="http://www.w3.org/2000/svg" width="880" height="400" viewBox="0 0 880 400"><rect width="880" height="400" rx="16" fill="#f8fafc"/><g font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="#172554">']
def label(a,x,y,s,size=24):a.append(f'<text x="{x}" y="{y}" font-size="{size}">{escape(str(s))}</text>')
def edge(a,x,y,u,v,color='#94a3b8',width=5):a.append(f'<path d="M{x},{y} L{u},{v}" stroke="{color}" stroke-width="{width}" fill="none"/>')
def vertex(a,x,y,s,color='#dbeafe'):
 a.append(f'<circle cx="{x}" cy="{y}" r="29" fill="{color}" stroke="#334155" stroke-width="2"/>');label(a,x,y+8,s)
def save(topic,slug,a):
 p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(exist_ok=True);p.write_text(''.join(a)+'</g></svg>','utf-8')
def main():
 a=canvas();edge(a,180,270,440,110,'#2563eb',7);edge(a,440,110,700,270,'#2563eb',7);edge(a,180,270,700,270)
 label(a,268,157,'e₁ : 1');label(a,602,157,'e₂ : 2');label(a,440,310,'e₃ : 5')
 for x,y,s in [(180,270,1),(440,110,2),(700,270,3)]:vertex(a,x,y,s)
 label(a,440,365,'1 → 2 → 3 → 2 → 1;   Y = B = 6');save('constructive','lower-weight-imperfect-non-matching',a)
 a=canvas()
 for origin,values in [(80,[[1,-2,3],[4,5,-6]]),(525,[[1,5,10],[-6,2,1]])]:
  for i,row in enumerate(values):
   for j,value in enumerate(row):
    x=origin+80*j;y=120+80*i;a.append(f'<rect x="{x}" y="{y}" width="80" height="80" fill="{("#dbeafe" if value!=10 else "#fed7aa")}" stroke="#475569"/>');label(a,x+40,y+49,value)
 label(a,440,210,'→',44);label(a,200,330,'max = 5');label(a,645,330,'max = 10');save('data-structures','batched-rectangle-maximum',a)
 a=canvas();label(a,440,47,'S = ababa;   D = 9;   U = 4')
 for i,s in enumerate(['a','b','ab','ba','aba','bab','abab','baba','ababa']):
  x=160+(i%3)*280;y=105+(i//3)*100;unique=i>=5;a.append(f'<rect x="{x-95}" y="{y-30}" width="190" height="65" rx="9" fill="{("#fed7aa" if unique else "#e2e8f0")}" stroke="{("#c2410c" if unique else "#cbd5e1")}" stroke-width="{3 if unique else 1}"/>');label(a,x,y+12,s)
 save('probability','unique-substring-hits',a)
 a=canvas();edge(a,150,200,380,200,'#2563eb',7);edge(a,380,200,610,200,'#2563eb',7);edge(a,380,200,380,85,'#ea580c',5)
 for x,y,s in [(150,200,1),(380,200,2),(610,200,3)]:vertex(a,x,y,s)
 vertex(a,380,85,4,'#fed7aa');label(a,440,310,'P(1,3) = {1,2,3}');label(a,440,355,'H(1,3) = {4}');save('trees','path-neighborhood-updates',a)
 a=canvas()
 for x,y,u,v in [(250,90,630,90),(630,90,630,270),(630,270,250,270),(250,270,250,90)]:edge(a,x,y,u,v,'#2563eb')
 edge(a,250,90,630,270,'#ea580c',7)
 for x,y,s in [(440,70,2),(670,190,2),(440,310,2),(210,190,2),(455,165,1)]:label(a,x,y,s)
 for x,y,s in [(250,90,1),(630,90,2),(630,270,3),(250,270,4)]:vertex(a,x,y,s,'#fed7aa' if s in [1,3] else '#dbeafe')
 label(a,440,365,'2 + 2 + 2 + 2 + 1 + 1 = 10');save('graphs','closed-edge-survey',a)
if __name__=='__main__':main()
