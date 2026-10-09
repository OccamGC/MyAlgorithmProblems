"""Reproducible shared mathematical diagrams for R28."""
from pathlib import Path
from draw_r27_figures import start,text,line,node,save
def main():
    s=start(900,370);positions={1:(200,65),2:(100,170),3:(300,170),5:(100,290),4:(300,290)}
    for a,b in [(1,2),(1,3),(2,5),(3,4)]:line(s,*positions[a],*positions[b])
    for v,pos in positions.items():node(s,*pos,v)
    text(s,630,55,'p_i = 0',24);text(s,630,123,'j = 0, 1, 2, 3, 4',20);text(s,630,160,'1 → 2 → 5 → 3 → 4',28)
    line(s,630,183,630,225,True,True);text(s,630,269,'4 → 3 → 5 → 2 → 1',28);text(s,630,311,'k = 1, 2, 3, 4, 5',20)
    save('topics/greedy/tree-demolition/assets/example.svg',s)
    s=start(870,405)
    for y,stage in [(110,1),(305,2)]:
        for x in [120,320,520]:line(s,x+35,y,x+165,y);text(s,x+100,y+24,'1',18)
        for i,x in enumerate([120,320,520,720],1):node(s,x,y,i,blue=i in ([1] if stage==1 else [1,4]))
        text(s,435,y-(86 if stage==1 else 106),'p_1 = 2, F_1 = 1' if stage==1 else 'p_2 = 1, F_2 = 2',22)
        for x,label in [(120,'r_1 = 1'),(320,'r_2 = 0'),(520,'r_3 = 0'),(720,'∞')]:text(s,x,y+62,label,19)
    s.append('<path d="M310 75 Q220 8 130 75" fill="none" stroke="#1379ad" stroke-width="3" marker-end="url(#blue)"/>')
    s.append('<path d="M330 270 Q520 172 710 270" fill="none" stroke="#1379ad" stroke-width="3" marker-end="url(#blue)"/>')
    save('topics/data-structures/line-capacity-transport/assets/example.svg',s)
    s=start(720,380);left=[(135,75),(135,180),(135,285)];right=[(585,75),(585,180),(585,285)]
    for i,j,g,lx,ly in [(0,0,70,360,61),(1,2,69,265,196),(2,1,70,468,193)]:
        line(s,left[i][0]+35,left[i][1],right[j][0]-40,right[j][1],True,True);text(s,lx,ly,g,22)
    for i in range(3):node(s,*left[i],f'i={i+1}');node(s,*right[i],f'j={i+1}')
    text(s,360,356,'c_70 = 2, c_69 = 1',24)
    save('topics/optimization/time-management-and-team-sports/assets/example.svg',s)
    s=start(950,395);node(s,90,204,'∅',blue=True);text(s,90,260,'S',20)
    text(s,480,30,'A_i = B_i = C_i = D_i = E_i = 1',22)
    for y,pair,label in [(78,'(0,0)','{A,B,C,D,E}'),(166,'(0,1)','{A,C}'),(254,'(1,0)','{B,C}'),(342,'(1,1)','{D}')]:
        line(s,125,204,535,y,True,True)
        s.append(f'<rect x="548" y="{y-26}" width="340" height="52" rx="10" fill="#e4f4fc" stroke="#1379ad" stroke-width="2"/>')
        text(s,715,y+7,label,24)
        tx=350;ty=204+(y-204)*.57
        s.append(f'<rect x="{tx-46}" y="{ty-20}" width="92" height="30" rx="4" fill="white"/>');text(s,tx,ty+3,pair,19)
    save('topics/bitwise/dynamic-binary-bounds/assets/example.svg',s)
    s=start(990,280);grid=['1110','0010','1110','0000'];offsets=[(0,0),(0,1),(0,2),(1,2)]
    starts=[(r,c) for r in range(4) for c in range(4) if grid[r][c]=='1']
    for t,(dx,dy) in enumerate(offsets):
        starts=[(r,c) for r,c in starts if 0<=r+dx<4 and 0<=c+dy<4 and grid[r+dx][c+dy]=='1']
        xbase=32+t*245;top=64;text(s,xbase+70,35,f't = {t}',23)
        for r in range(4):
            for c in range(4):
                x=xbase+c*35;y=top+r*35;b=grid[r][c]=='1'
                s.append(f'<rect x="{x}" y="{y}" width="35" height="35" fill="{("#e5edf4" if b else "#f5f5f5")}" stroke="#8b98a7"/>')
                text(s,x+17.5,y+24,grid[r][c],19,'#172b4d' if b else '#8b98a7')
                if (r,c) in starts:s.append(f'<circle cx="{x+17.5}" cy="{y+17.5}" r="14" fill="none" stroke="#1379ad" stroke-width="2.5"/>')
        text(s,xbase+70,242,f'Q_{t} = {len(starts)}',22)
        if t<3:line(s,xbase+157,133,xbase+222,133,True,True);text(s,xbase+190,110,'3' if t<2 else '1',20)
    save('topics/simulation/grid-forest-matching/assets/example.svg',s)
if __name__=='__main__':main()
