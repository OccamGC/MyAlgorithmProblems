"""Draw R33 SVG explanations; all labels are shared mathematical notation."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=22):return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="#172b4d">{escape(str(s))}</text>'
def edge(x,y,a,b,arrow=False):return f'<path d="M{x},{y} L{a},{b}" fill="none" stroke="#506680" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def box(x,y,w,h,s,green=False):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="'+('#dcf5eb' if green else '#edf2fa')+'" stroke="#8393aa" stroke-width="2"/>'+text(x+w/2,y+h/2+8,s)
def vertex(x,y,v):return f'<circle cx="{x}" cy="{y}" r="24" fill="#edf2fa" stroke="#506680" stroke-width="2"/>'+text(x,y+8,v)
def save(topic,slug,body):
 d=ROOT/'topics'/topic/slug/'assets';d.mkdir(parents=True,exist_ok=True)
 (d/'example.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400" role="img"><defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7" fill="#506680"/></marker></defs><rect width="800" height="400" fill="white"/><g font-family="Arial, sans-serif">'+body+'</g></svg>\n','utf-8')
def main():
 body=text(400,40,'n = 3, k = 1')
 coords=[(100,110),(340,110),(580,110),(580,260),(340,260),(100,260)]
 for (x,y),s in zip(coords,['123','132','213','231','312','321']):body+=box(x,y,120,55,s)
 for i in range(6):
  x,y=coords[i];a,b=coords[(i+1)%6]
  if y==b:body+=edge(x+(137 if a>x else -17),y+27,a+(-17 if a>x else 137),b+27,True)
  else:body+=edge(x+60,y+(72 if b>y else -17),a+60,b+(-17 if b>y else 72),True)
 body+=text(400,368,'321 → 123')
 save('permutations','lexicographic-jump',body)
 for anonymous,slug in [(False,'labeled-leaf-orders'),(True,'anonymous-leaf-orders')]:
  body=text(400,36,'n = 3, m = 2')
  for offset in [0,400]:
   body+=edge(200+offset,105,90+offset,230)+edge(200+offset,105,310+offset,230)
   labels=[3,1] if anonymous and offset else [1,3]
   body+=vertex(200+offset,105,2)+vertex(90+offset,230,labels[0])+vertex(310+offset,230,labels[1])
   steps=[2,1] if not anonymous and offset else [1,2]
   body+=text(120+offset,162,'①' if steps[0]==1 else '②')+text(280+offset,162,'①' if steps[1]==1 else '②')
  body+=text(400,195,'≃' if anonymous else '≠',32)
  body+=text(400,330,'1 ↔ 3, 2 → 2' if anonymous else '3 × 2 = 6')
  save('combinatorics',slug,body)
 body=text(100,38,'t')+text(655,38,'(u, v)')
 for j in range(4):body+=text(235+85*j,38,j+1)
 rows=[[2,1,3,4],[3,1,2,4],[3,4,2,1],[3,2,4,1],[1,2,4,3],[1,2,3,4]]
 for i,row in enumerate(rows):
  y=62+50*i;body+=text(100,y+29,i)+text(655,y+29,['—','(3, 1)','(4, 2)','(3, 2)','(4, 1)','(3, 4)'][i])
  for j,v in enumerate(row):body+=box(205+85*j,y,60,40,v,v==j+1)
 body+=text(400,388,'S = 5 = 2N + 1',20)
 save('constructive','mind-swap-restoration',body)
 body=text(400,35,'a = 2, B(i) = 1 + i')
 for i in range(3):
  y=65+i*83;body+=text(85,y+33,'i = '+str(i+1))+box(165,y,115,52,2**(i+1))+text(319,y+33,'×')+box(355,y,115,52,i+2)+edge(495,y+26,565,y+26,True)+box(600,y,115,52,2**(i+1)*(i+2),True)
 body+=text(400,378,'4 + 12 + 32 = 48')
 save('number-theory','dynamic-polynomial-geometric-sum',body)
if __name__=='__main__':main()
