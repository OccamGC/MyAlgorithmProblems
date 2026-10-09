"""Shared mathematical SVGs for the final batch."""
from draw_r27_figures import start,text,line,node,save

def main():
    s=start(940,335)
    for y,a,c,label in [(85,[2,2,1,0],[2,2,1,0],'0'),(245,[0,2,1,2],[0,1,0,0],'1')]:
        text(s,70,y,'a('+label+')',23)
        for i,x in enumerate([210,380,550,720]):
            node(s,x,y,a[i],blue=i in [0,2,3]);text(s,x,y+59,'c = '+str(c[i]),20)
        text(s,855,y+8,'Σc = '+str(sum(c)),22)
    for x in [210,550,720]:line(s,x,164,x,204,True,True)
    text(s,385,181,'k = 1',22)
    save('topics/data-structures/selective-suffix-sort/assets/example.svg',s)
    s=start(820,330)
    for shift,t in [(0,'T_1[S]'),(410,'T_2[S]')]:
        text(s,shift+205,35,t,25)
        line(s,shift+205,97,shift+105,223);line(s,shift+205,97,shift+305,223)
        node(s,shift+205,97,'2','−3',True);node(s,shift+105,223,'4','5',True);node(s,shift+305,223,'5','7',True)
        text(s,shift+205,302,'S = {2,4,5},  Σa_i = 9',22)
    save('topics/graphs/common-tree-subset/assets/example.svg',s)
    s=start(900,390)
    rows=[[1,1,1,1,1,1,1],[1,1,1,1,1,2],[1,1,1,2,2],[1,2,2,2],[1,1,1,4],[1,2,4]]
    for i,row in enumerate(rows):
        y=54+i*57;text(s,65,y+5,i+1,20)
        x=145
        for value in row:
            width=72*value
            s.append(f'<rect x="{x}" y="{y-23}" width="{width-5}" height="42" rx="6" fill="{("#e4f4fc" if value<4 else "#cde5f4")}" stroke="#1379ad"/>')
            text(s,x+(width-5)/2,y+5,value,22);x+=width
        text(s,775,y+5,'= 7',24)
    save('topics/combinatorics/binary-power-partitions/assets/example.svg',s)
    s=start(940,285)
    text(s,190,55,'(H_0,D_0,A_0) = (1,1,2)',24)
    text(s,190,106,'(h_1,d_1,a_1) = (1,1,2)',22)
    text(s,190,157,'k_1 = 1',22)
    line(s,390,132,560,75,False,True);line(s,390,150,560,221,True,True)
    text(s,730,68,'C = 1, (H,D,A) = (2,1,2)',22)
    text(s,730,102,'H − F = 1',20)
    text(s,730,212,'C = 1, (H,D,A) = (1,2,2)',22)
    text(s,730,248,'H − F = 1',20)
    save('topics/optimization/battle-upgrades/assets/example.svg',s)
    s=start(940,355)
    for base,t,values in [(0,0,[7,7]),(320,1,[7]),(640,2,[7,8])]:
        text(s,base+150,35,'t = '+str(t),23)
        root=(base+150,103);positions=[(base+77,231),(base+223,231)] if len(values)==2 else [(base+150,231)]
        for pos in positions:line(s,*root,*pos)
        node(s,*root,'0','0')
        for i,(pos,value) in enumerate(zip(positions,values),1):node(s,*pos,str(i),str(value),True)
        text(s,base+150,317,'I(1) = '+('0' if t==0 else '2'),24)
    save('topics/strings/dynamic-path-independence/assets/example.svg',s)
if __name__=='__main__':main()
