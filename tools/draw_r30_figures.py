"""Regenerate the five explanatory SVG figures for R30."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
BLUE='#176c95';INK='#19344a';GRAY='#718096';GREEN='#217553'
def start(w,h):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="{GRAY}"/></marker></defs><rect width="100%" height="100%" fill="#f7fafc"/>']
def text(s,x,y,value,size=22,color=INK):s.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="middle">{escape(str(value))}</text>')
def line(s,x,y,X,Y,arrow=False):s.append(f'<path d="M{x} {y}L{X} {Y}" stroke="{GRAY}" stroke-width="2" fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
def node(s,x,y,value,active=True):
 s.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{BLUE if active else "#ffffff"}" stroke="{INK}" stroke-width="2"/>');text(s,x,y+8,value,23,'#fff' if active else INK)
def save(path,s):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(s)+'</svg>\n','utf-8')
def main():
 s=start(920,260);text(s,460,36,'n = 2, m = 3, k = 2, c = 1',24)
 for i,(a,b,w) in enumerate([(1,1,3),(1,2,3),(1,3,3),(2,2,5),(2,3,5),(3,3,7)]):
  x=85+i*150;s.append(f'<rect x="{x-64}" y="65" width="128" height="112" rx="12" fill="white" stroke="#cbd8e2"/>');text(s,x,105,f'({a}, {b})',23);text(s,x,152,f'2·{a}+1 = {w}',19)
 text(s,460,228,'3 + 3 + 3 + 5 + 5 + 7 = 26',26)
 save('topics/combinatorics/nested-linear-sum/assets/example.svg',s)
 s=start(820,235);text(s,410,35,'n = 3, m = 2',24)
 for j,seq in enumerate([(1,1,1),(1,1,2),(1,2,2),(2,2,2)]):
  for i,v in enumerate(seq):node(s,62+j*202+i*54,105,v,v==1)
  text(s,116+j*202,170,str(j+1),19)
 text(s,410,213,'4',26);save('topics/combinatorics/monotone-sequence-count/assets/example.svg',s)
 s=start(700,325);line(s,350,88,200,211);line(s,350,88,500,211)
 for x,y,i,f in [(350,88,2,10),(200,211,1,2),(500,211,3,2)]:node(s,x,y,i);text(s,x+82,y+7,f'f = {f}',20)
 text(s,89,94,'d = 1',20);text(s,89,217,'d = 2',20);text(s,350,296,'10·1 + 2·2 + 2·2 = 18',25)
 save('topics/dynamic-programming/optimal-search-tree/assets/example.svg',s)
 s=start(780,320)
 for x,y,X,Y in [(118,82,253,82),(307,82,443,82),(307,97,442,200),(552,221,657,221),(657,241,552,241)]:line(s,x,y,X,Y,True)
 for x,y,i in [(90,82,1),(280,82,2),(470,82,3),(470,210,6)]:node(s,x,y,i);text(s,x,y+55,'1',20,GREEN)
 for x,y,i in [(525,230,4),(685,230,5)]:node(s,x,y,i,False);text(s,x,y+55,'0',20)
 text(s,193,169,'1 → 2 → {3, 6}',24);text(s,605,42,'2, 3, 4, 5, 6',19);text(s,605,76,'1, 1, 0, 0, 1',20)
 save('topics/logic/monotone-unlocks/assets/example.svg',s)
 s=start(840,445)
 # Schematic diamonds preserve contact and row order; horizontal ratios compressed.
 for x,y,w,h,i in [(260,90,145,55,1),(550,90,145,55,3),(260,200,55,55,2),(370,200,55,55,5),(550,200,55,55,6),(260,310,28,55,4)]:
  s.append(f'<path d="M{x-w} {y}L{x} {y-h}L{x+w} {y}L{x} {y+h}Z" fill="#e7f2f8" stroke="{BLUE}" stroke-width="2"/>');text(s,x,y+8,i,23)
 for y,h,label in [(90,0,'1  3'),(200,1,'2  5  6'),(310,2,'4')]:text(s,57,y+7,f'h = {h}',19);text(s,752,y+7,label,21)
 text(s,420,413,'1, 3   /   2, 5, 6   /   4',24)
 save('topics/trees/diamond-hangers/assets/example.svg',s)
if __name__=='__main__':main()
