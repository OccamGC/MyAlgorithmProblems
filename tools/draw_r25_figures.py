"""Deterministically draw the five R25 examples with standard-library SVG."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=22,color='#18334a'):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{s}</text>'
def line(x1,y1,x2,y2,arrow=False):return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#4777ac" stroke-width="3"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def circle(x,y,s,color='#e7f1ff'):return f'<circle cx="{x}" cy="{y}" r="28" fill="{color}" stroke="#4777ac" stroke-width="2"/>'+text(x,y+8,s)
def save(topic,slug,body,w=1000,h=340):
    p=ROOT/'topics'/topic/slug/'assets/example.svg';p.parent.mkdir(parents=True,exist_ok=True)
    source=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8" fill="#4777ac"/></marker></defs><rect width="{w}" height="{h}" fill="#f6f9fc"/><g font-family="Microsoft YaHei, Arial, sans-serif" text-anchor="middle">'+body+'</g></svg>\n'
    translations={'Five consecutive groups; one station per group':'五个连续组，每组设置一个服务站','cost =':'距离和 =','Station coordinates: 2, 7, 22, 44, 50; total distance = 9':'服务站坐标：2, 7, 22, 44, 50；总距离 = 9','Strictly downhill: count by ending vertex':'严格下坡：按终点统计路线数','ways =':'路线数 =','Energy budget E = 2':'初始体力 E = 2','uphill: cost 2':'上坡：消耗 2','downhill: cost 0':'下坡：消耗 0','height =':'高度 =','Start 1:':'从 1 出发：','Start 2:':'从 2 出发：','Process [5, 3, 3, 4, 2] from left to right':'从左到右处理 [5, 3, 3, 4, 2]','read ':'读入 ','Stacks shown from bottom to top':'栈中元素按从底到顶的顺序展示','Equal values are popped. Final positions: 1, 4, 5.':'相等的旧值也会弹出。最终留下的位置为 1, 4, 5。','x = 2: count each ancestor subtree separately':'x = 2：分别统计每个祖先的子树','Ancestor u':'祖先 u','less / equal / greater':'较浅 / 同深 / 较深','Total':'总计','Nodes in both subtrees contribute twice.':'同时属于两个子树的节点计数两次。'}
    zh=source
    for a,b in translations.items():zh=zh.replace(a,b)
    for lang,content in [('en',source),('zh',zh)]:p.with_name('example.'+lang+'.svg').write_text(content,'utf-8')
    if p.exists():p.unlink()
b=text(500,38,'Five consecutive groups; one station per group',26)
for i,(homes,station,cost) in enumerate([('1, 2, 3',2,2),('6, 7, 9, 11',7,7),('22',22,0),('44',44,0),('50',50,0)]):
    x=100+200*i;b+=f'<rect x="{x-88}" y="76" width="176" height="185" rx="12" fill="white" stroke="#b6c9dd"/>'+text(x,113,homes,20)+circle(x,162,str(station),'#d7f2e6')+text(x,223,f'cost = {cost}',20)
b+=text(500,307,'Station coordinates: 2, 7, 22, 44, 50; total distance = 9',22);save('optimization','postal-facilities',b)
b=text(500,35,'Strictly downhill: count by ending vertex',26)
for i in range(4):b+=line(148+i*180,168,272+i*180,168,True)
b+='<path d="M120 135 Q300 -5 480 135" fill="none" stroke="#4777ac" stroke-width="3" marker-end="url(#arrow)"/>'
for i,count in enumerate([1,2,4,5,6]):
    x=120+180*i;b+=circle(x,168,str(5-i))+text(x,222,f'h = {5-i}',19)+text(x,261,f'ways = {count}',19)
b+=text(500,315,'1 + 2 + 4 + 5 + 6 = 18',24);save('graphs','downhill-routes',b)
b=text(500,38,'Energy budget E = 2',26)+circle(220,150,'1')+circle(780,150,'2')+text(220,203,'height = 0',20)+text(780,203,'height = 1',20)
b+='<path d="M250 138 Q500 45 750 138" fill="none" stroke="#4777ac" stroke-width="3" marker-end="url(#arrow)"/><path d="M750 166 Q500 245 250 166" fill="none" stroke="#4777ac" stroke-width="3" marker-end="url(#arrow)"/>'+text(500,88,'uphill: cost 2',20)+text(500,236,'downhill: cost 0',20)
b+=text(500,281,'Start 1: (1), (1,2), (1,2,1)',21)+text(500,317,'Start 2: (2), (2,1), (2,1,2), (2,1,2,1)',21);save('dynamic-programming','energy-limited-routes',b,h=345)
b=text(500,38,'Process [5, 3, 3, 4, 2] from left to right',26)
for i,(v,s) in enumerate([(5,'5'),(3,'5, 3'),(3,'5, 3'),(4,'5, 4'),(2,'5, 4, 2')]):
    x=100+200*i;b+=text(x,100,f'read {v}',21)+f'<rect x="{x-75}" y="131" width="150" height="65" rx="9" fill="#e7f1ff" stroke="#4777ac"/>'+text(x,173,s,23)
    if i<4:b+=line(x+78,163,x+119,163,True)
b+=text(500,242,'Stacks shown from bottom to top',20)+text(500,285,'Equal values are popped. Final positions: 1, 4, 5.',22);save('data-structures','little-y-segment-tree',b,h=315)
b=text(500,38,'x = 2: count each ancestor subtree separately',26)
coords={1:(225,108),2:(130,212),3:(320,212),4:(70,320),5:(195,320)}
for u,v in [(1,2),(1,3),(2,4),(2,5)]:b+=line(*coords[u],*coords[v])
for u,(x,y) in coords.items():b+=circle(x,y,str(u),'#d7f2e6' if u in [1,2] else '#e7f1ff')
b+=text(530,114,'Ancestor u',21)+text(795,114,'less / equal / greater',21)+text(530,174,'1',24)+text(795,174,'1 / 2 / 2',24)+text(530,234,'2',24)+text(795,234,'0 / 1 / 2',24)+line(445,260,955,260)+text(530,308,'Total',25)+text(795,308,'1 / 3 / 4',25)+text(500,389,'Nodes in both subtrees contribute twice.',22)
save('trees','ancestor-depth-counts',b,h=415)
