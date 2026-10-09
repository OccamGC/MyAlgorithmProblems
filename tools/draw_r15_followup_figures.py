"""Numerator matrix for all 27 histories of the three-element example."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]

def text(x,y,value,size=22):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">{escape(value)}</text>'

def main():
 counts=[[9,10,8],[9,8,10],[9,9,9]]
 parts=[text(275,35,'a = (1, 2, 3)',23)]
 for j in range(3):parts.append(text(205+j*110,80,f'j = {j+1}',18))
 for i in range(3):
  parts.append(text(85,135+i*65,f'i = {i+1}',18))
  for j in range(3):
   x,y=160+j*110,100+i*65
   parts.append(f'<rect x="{x}" y="{y}" width="90" height="50" rx="5" fill="{"#dcebe3" if i==2 else "#e0ecf6"}" stroke="#56798e" stroke-width="1.5"/>')
   parts.append(text(x+45,y+34,str(counts[i][j]),26))
 parts.append(text(285,315,'Pᵢⱼ = count / 27',22))
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 350"><rect width="560" height="350" fill="#f8fafc"/><g fill="#173147" font-family="Arial, sans-serif">'+''.join(parts)+'</g></svg>\n'
 for slug in ['shuffle-expectation','shuffle-distribution']:
  path=ROOT/'topics/probability'/slug/'assets/probabilities.svg'
  path.parent.mkdir(parents=True,exist_ok=True)
  path.write_text(svg,encoding='utf-8',newline='\n')

if __name__=='__main__':main()
