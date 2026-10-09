"""Redraw the R9 explanatory figures with standard-library SVG generation."""
from draw_figures import Figure, INK, GRID, BLUE, TEAL, ORANGE

def harvest():
    f=Figure(840,305,'Two terminal harvests','Three melons on the left; two on the right. Arrows connect vines to their melons.')
    for offset,title,rows,arrows in [(30,'tp = 0: 3',['xlMlx','xMlMx'],[((1,0),(1,1)),((3,0),(3,1)),((2,1),(2,0))]),(445,'tp = 1: 2',['xlMlx','xolMx'],[((1,0),(2,0)),((2,1),(3,1))])]:
        f.text(offset+175,35,title,23)
        for y,row in enumerate(rows):
            for x,value in enumerate(row):
                cx=offset+x*70;cy=65+y*70
                f.rect(cx,cy,70,70,fill='#e8edf2' if value=='x' else '#e5f3ea' if value=='l' else 'white')
                if value=='M':f.circle(cx+35,cy+35,20,fill='#fff3cf',stroke=ORANGE)
                f.text(cx+35,cy+42,value,23)
        for (x,y),(u,v) in arrows:
            ax=offset+x*70+35;ay=100+y*70;bx=offset+u*70+35;by=100+v*70
            dx=(bx-ax)/70;dy=(by-ay)/70
            f.line(ax+23*dx,ay+23*dy,bx-24*dx,by-24*dy,color=BLUE,width=3,**{'marker-end':'url(#arrow-blue)'})
    f.text(420,260,'l → M     |     o     |     x',22)
    f.save('topics/graphs/melon-planting/assets/harvest.svg')

def wool():
    f=Figure(880,365,'Deposit route','Four route legs in sample three. Slow wool is deposited at the left chest; all remaining wool at the right chest.')
    values=['S','C','E','0','E','E','E','1','E','C']
    for i,value in enumerate(values):
        f.rect(45+i*78,35,78,60,fill='#e5f3ea' if value.isdigit() else '#fff3cf' if value=='C' else 'white')
        f.text(84+i*78,73,value,24)
        f.text(84+i*78,118,i+1,16,color=GRID)
    for j,(a,b,label) in enumerate([(0,3,'1: 3 × 1 = 3'),(3,1,'2: 2 × 9 = 18'),(1,7,'3: 6 × 1 = 6'),(7,9,'4: 2 × 7 = 14')]):
        y=162+j*49;x1=84+78*a;x2=84+78*b
        f.line(x1,y,x2,y,color=BLUE,width=3,**{'marker-end':'url(#arrow-blue)'})
        f.circle(x1,y,4,fill=BLUE)
        f.text((x1+x2)/2,y-12,label,18)
    f.save('topics/dynamic-programming/potion-wool/assets/deposit-route.svg')

def timber():
    f=Figure(730,450,'Root paths in a forest','Select nodes 5, 11, and 7. Their new path contributions have sizes 5, 4, and 2.')
    xy={1:(225,50),2:(225,130),3:(225,210),4:(135,290),5:(135,370),6:(325,290),7:(325,370),8:(550,50),9:(550,155),10:(550,260),11:(550,370)}
    edges=[(1,2,1),(2,3,1),(3,4,1),(4,5,1),(3,6,3),(6,7,3),(8,9,2),(9,10,2),(10,11,2)]
    for u,v,part in edges:
        x,y=xy[u];a,b=xy[v];f.line(x,y,a,b,color=BLUE if part==1 else TEAL if part==2 else ORANGE,width=4)
        f.text((x+a)/2+20,(y+b)/2,part,17)
    for u,(x,y) in xy.items():
        f.circle(x,y,21,stroke=INK)
        if u in (5,7,11):f.circle(x,y,27,fill='none',stroke=INK,width=1.5)
        f.text(x,y+7,u,20)
    f.text(225,425,'5 + 2 = 7',21);f.text(550,425,'4',21)
    f.save('topics/trees/timber/assets/forest-paths.svg')

def spice():
    f=Figure(680,350,'Spice routes','Squares 1 and 3 are buyers. Circles 4 and 5 are sellers. Edges to sellers fail independently with probability one half.')
    xy={1:(95,80),2:(340,80),3:(585,80),4:(210,255),5:(470,255)}
    for u,v,label in [(1,2,'0'),(2,3,'0'),(2,4,'1/2'),(2,5,'1/2')]:
        x,y=xy[u];a,b=xy[v]
        f.line(x,y,a,b,color=BLUE,width=3,**({'stroke-dasharray':'9 6'} if label=='1/2' else {}))
        f.text((x+a)/2+(20 if v==5 else -20 if v==4 else 0),(y+b)/2-15,label,20)
    for u,(x,y) in xy.items():
        if u in (1,3):f.rect(x-24,y-24,48,48,fill='#e5edf9',stroke=BLUE,**{'stroke-width':2})
        elif u in (4,5):f.circle(x,y,26,fill='#e5f3ea',stroke=TEAL)
        else:f.circle(x,y,22,stroke=GRID)
        f.text(x,y+7,u,22)
        if u != 2:f.text(x,y+46,'H' if u in (1,3) else 'L',17)
    f.text(340,327,'1 − (1/2) × (1/2) = 3/4',23)
    f.save('topics/trees/spice-routes/assets/routes.svg')

if __name__=='__main__':
    harvest();wool();timber();spice()
