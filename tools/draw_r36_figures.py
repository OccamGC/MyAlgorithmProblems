"""Rebuild four shared-label SVG illustrations using the Python standard library."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=22,color='#183247'):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="middle">{s}</text>'
def rect(x,y,w,h,fill='#ffffff'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#43677f" stroke-width="2"/>'
def save(topic,slug,w,h,parts):
    p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'+rect(1,1,w-2,h-2,'#f6f9fc')+''.join(parts)+'</svg>','utf-8',newline='\n')
def main():
    parts=[]
    for j,values in enumerate([[2,3],[2,3,5],[3,5]]):
        x=30+j*230;parts.append(text(x+80,45,['n = 3','1 5','2 → 2'][j]))
        for k in range(3):parts.append(rect(x+k*53,75,53,56,'#dceefa' if k<len(values) else '#ffffff'))
        for k,v in enumerate(values):parts.append(text(x+k*53+26,111,str(v)))
        if j<2:parts.append(text(x+195,112,'→',30))
    save('data-structures','bounded-conveyor',700,165,parts)
    parts=[]
    for b in range(5):
        x=25+b*130
        for cell in range(4):
            black=cell==b-1;xx=x+cell%2*43;yy=55+cell//2*43
            parts.append(rect(xx,yy,43,43,'#183247' if black else '#ffffff'));parts.append(text(xx+21,yy+29,'B' if black else 'W',20,'#ffffff' if black else '#183247'))
        parts.append(text(x+43,32,str(b+1),18))
    save('combinatorics','white-cell-board',660,165,parts)
    parts=[text(95,38,'t = 1'),rect(68,65,55,55),text(95,100,'1'),text(205,102,'+',30),text(330,38,'t = 2')]
    for i in range(2):
        for j in range(2):parts.extend([rect(275+j*55,60+i*55,55,55),text(302+j*55,96+i*55,str(2 if i==j==1 else 1))])
    parts.extend([text(475,110,'1 + 5 = 6')]);save('number-theory','box-gcd-prefix-sum',570,205,parts)
    parts=[text(330,30,'n = 3, m = 2')]
    for j,(a,b) in enumerate([(1,1),(2,1),(2,2),(3,1),(3,2),(3,3)]):
        x=20+j*106;parts.extend([rect(x,60,94,60,'#dceefa'),text(x+47,98,f'({a}, {b})'),text(x+47,157,str(__import__('math').gcd(a,b)))])
    parts.append(text(330,202,'1 + 1 + 2 + 1 + 1 + 3 = 9'));save('number-theory','monotone-gcd-sum',660,230,parts)
if __name__=='__main__':main()
