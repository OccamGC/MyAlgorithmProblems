"""Regenerate the five R32 explanatory SVGs with Python's standard library."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,value,size=22,color='#172b4d'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="middle">{escape(str(value))}</text>'
def line(x1,y1,x2,y2,dash=False,arrow=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#506680" stroke-width="3"'+(' stroke-dasharray="6 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def box(x,y,w,h,label,selected=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="'+('#dcf5eb' if selected else '#edf2fa')+'" stroke="#8393aa" stroke-width="2"/>'+text(x+w/2,y+h/2+8,label)
def save(topic,slug,body):
    d=ROOT/'topics'/topic/slug/'assets';d.mkdir(parents=True,exist_ok=True)
    (d/'example.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="320" viewBox="0 0 800 320" role="img"><defs><marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7" fill="#506680"/></marker></defs><rect width="800" height="320" fill="white"/><g font-family="Arial, sans-serif">'+body+'</g></svg>\n','utf-8')
    translated=(d/'example.svg').read_text('utf-8')
    labels={'prefix totals':'前缀和','0 is defined separately; 1 contributes 1.':'0 单独定义为 0；参数 1 的贡献为 1。','cut path 2 → 3; longest remaining length = 1':'关闭路径 2 → 3；剩余最长亮边路径长度为 1','solid: on':'实线：亮','dashed: off':'虚线：暗','error flag':'错误标志','ignored':'忽略','the right error is unobserved':'右侧错误不影响结果','values: 5, 2, 2, 4, 1':'数值：5、2、2、4、1','surviving positions: 1 → 4 → 5':'保留位置：1 → 4 → 5','L = 4, capacity = 4':'L = 4，容量 = 4','price 5':'单价 5','price 1':'单价 1','finish':'终点','minimum cost: 2 × 5 + 2 × 1 = 12':'最低费用：2 × 5 + 2 × 1 = 12','minimum stops: buy all 4 units at position 0':'最少次数：在位置 0 一次买 4 单位'}
    for english,chinese in labels.items():translated=translated.replace(escape(english),escape(chinese))
    (d/'example.zh.svg').write_text(translated,'utf-8')
def main():
    body=text(400,35,'G = 0, k = 1, b = 0')
    for i in range(10):
        body+=text(66+74*i,80,i)+box(34+74*i,98,64,48,int(i in [1,2,3,5,7]),i in [1,2,3,5,7])+text(66+74*i,220,[0,1,2,3,3,4,4,5,5,5][i])
    body+=text(400,184,'prefix totals',18)+text(400,287,'0 is defined separately; 1 contributes 1.',20)
    save('number-theory','apostle-luke-password',body)
    body=text(400,35,'cut path 2 → 3; longest remaining length = 1')
    for a,b in [(150,310),(470,630)]:body+=line(a,130,b,130)
    body+=line(310,130,470,130,True)+line(470,130,470,250,True)
    for x,y,v in [(150,130,1),(310,130,2),(470,130,3),(630,130,4),(470,250,5)]:body+=f'<circle cx="{x}" cy="{y}" r="25" fill="#edf2fa" stroke="#506680" stroke-width="2"/>'+text(x,y+8,v)
    body+=text(200,286,'solid: on',18)+text(645,286,'dashed: off',18)
    save('trees','giant-christmas-tree',body)
    body=text(400,38,'0 && (1 / 0)')+box(100,90,120,65,'0',True)+box(440,90,240,65,'error flag')+text(560,191,'ignored',20)+line(240,123,420,123,True)+line(160,178,160,244,arrow=True)+box(100,256,120,48,'0',True)+text(445,284,'the right error is unobserved',20)
    save('parsing','short-circuit-calculator',body)
    body=text(400,36,'values: 5, 2, 2, 4, 1')
    for i,v in enumerate([5,2,2,4,1]):body+=box(83+130*i,83,114,60,v,i in [0,3,4])+text(140+130*i,178,i+1,18)
    body+=text(400,226,'surviving positions: 1 → 4 → 5',22)+text(400,279,'prev[5] = 4, prev[4] = 1, prev[1] = 0',20)
    save('data-structures','old-y-segment-tree',body)
    body=text(400,35,'L = 4, capacity = 4')+line(130,120,670,120)
    for x,v in [(130,0),(400,2),(670,4)]:body+=f'<circle cx="{x}" cy="120" r="24" fill="#edf2fa" stroke="#506680" stroke-width="2"/>'+text(x,128,v)
    body+=text(130,183,'price 5',20)+text(400,183,'price 1',20)+text(670,183,'finish',20)+text(400,242,'minimum cost: 2 × 5 + 2 × 1 = 12',22)+text(400,288,'minimum stops: buy all 4 units at position 0',20)
    save('dynamic-programming','limited-refueling',body)
if __name__=='__main__':main()
