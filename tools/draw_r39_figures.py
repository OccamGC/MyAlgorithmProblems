"""Rebuild the single-member-household example figure."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=20):return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="middle" fill="#183247">{s}</text>'
def circle(x,y,s,color):return f'<circle cx="{x}" cy="{y}" r="29" fill="{color}" stroke="#245d87" stroke-width="2"/>'+text(x,y+7,s,23)
def main():
    parts=[]
    for x,values in [(95,['1','9','13']),(345,['5','5','13']),(595,['9','5','9'])]:
        for i,v in enumerate(values):parts.append(circle(x,65+85*i,v,'#fef3c7' if i==0 else '#ffffff'))
    for left,right,y,label in [(132,305,65,'(1 + 9) / 2'),(382,555,65,'(5 + 13) / 2')]:
        parts.append(f'<path d="M{left} {y} L{right} {y}" fill="none" stroke="#245d87" stroke-width="3" marker-end="url(#arrow)"/>');parts.append(text((left+right)/2,y-33,label,17))
    parts.extend([text(95,295,'a = 1'),text(345,295,'x = 5'),text(595,295,'A = 9'),text(360,341,'14 − 9 = 5     |     9 − 5 = 4',21)])
    p=ROOT/'topics/greedy/single-member-household/assets/example.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 375" width="720" height="375"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 Z" fill="#245d87"/></marker></defs><rect x="1" y="1" width="718" height="373" fill="#f6f9fc" stroke="#8ba6ba"/>'+''.join(parts)+'</svg>','utf-8',newline='\n')
if __name__=='__main__':main()
