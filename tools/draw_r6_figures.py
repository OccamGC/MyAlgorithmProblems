"""Draw the shared R6 statement diagrams with the Python standard library."""
from draw_figures import Figure, BLUE, TEAL, ORANGE, INK, GRID, cross, tick


def shield_timeline():
    figure = Figure(814, 350, 'Shield activation and later construction',
                    'An activation at time 1 protects A through time 3. B is completed at time 2 and is not protected. The device cools down at time 4 and is available again at time 5.')
    x0, size = 286, 82
    figure.text(126, 38, '(X_i, T_i)', 19)
    for i in range(5):
        figure.text(x0+(i+.5)*size, 43, i+1, 21)
    figure.line(x0, 16, x0+5*size, 16, width=1.5, **{'marker-end':'url(#arrow-ink)'})
    figure.text(x0+5*size+20, 23, 't', 20)
    figure.rect(x0, 60, 3*size, 32, '#d9eafa', BLUE)
    figure.text(x0+1.5*size, 83, 'R_s = 3', 19, BLUE)
    figure.rect(x0+3*size, 60, size, 32, '#ffedc4', ORANGE)
    figure.text(x0+3.5*size, 83, 'S = 1', 19, ORANGE)
    figure.text(125, 159, 'A: (0, 1)', 23)
    figure.text(125, 240, 'B: (1, 2)', 23)
    for row in range(2):
        for col in range(5):
            exists = row == 0 or col >= 1
            protected = row == 0 and col < 3
            fill = '#cceae4' if protected else ('#f5f7fa' if exists else '#e4e8ed')
            left, top = x0+col*size, 112+row*82
            figure.rect(left, top, size, 66, fill)
            if protected:
                tick(figure,left+size/2,top+33)
            elif exists:
                cross(figure,left+size/2,top+33)
            else:
                figure.text(left+size/2,top+41,'—',22,'#637587')
    figure.line(x0,284,x0+3*size,284,BLUE,3)
    figure.text(x0+1.5*size,315,'[1, 3]',21,BLUE)
    figure.circle(x0+4.5*size,293,20,'white',ORANGE)
    figure.text(x0+4.5*size,300,'5',21,ORANGE)
    figure.save('topics/optimization/force-shield/assets/shield-timeline.svg')


def transformations():
    figure = Figure(854, 456, 'Reflection and counterclockwise rotation',
                    'Both panels start at P=(2,1). Reflection in x=y gives Q=(1,2), and a 90 degree counterclockwise rotation gives Q=(-1,2).')
    size = 43
    for panel, ox, target in [('A', 211, (1,2)), ('B', 639, (-1,2))]:
        oy = 248
        figure.text(ox, 31, f'({panel})',24,**{'font-weight':'bold'})
        for i in range(-3,4):
            figure.line(ox-3*size,oy+i*size,ox+3*size,oy+i*size,GRID,1)
            figure.line(ox+i*size,oy-3*size,ox+i*size,oy+3*size,GRID,1)
        figure.line(ox-3*size,oy,ox+3*size+15,oy,INK,2,**{'marker-end':'url(#arrow-ink)'})
        figure.line(ox,oy+3*size,ox,oy-3*size-15,INK,2,**{'marker-end':'url(#arrow-ink)'})
        figure.text(ox+3*size+28,oy+6,'x',20)
        figure.text(ox,oy-3*size-28,'y',20)
        for i in (-2,-1,1,2):
            figure.text(ox+i*size,oy+20,i,16)
            figure.text(ox-14,oy-i*size+6,i,16)
        figure.text(ox+14,oy+20,'0',16)
        if panel == 'A':
            figure.line(ox-3*size,oy+3*size,ox+3*size,oy-3*size,ORANGE,2,**{'stroke-dasharray':'6 5'})
            figure.text(ox+72,oy-3*size-10,'x = y',19,ORANGE)
        px,py=ox+2*size,oy-size
        qx,qy=ox+target[0]*size,oy-target[1]*size
        if panel == 'A':
            figure.line(px-9,py-9,qx+10,qy+10,BLUE,2.5,**{'marker-end':'url(#arrow-blue)'})
        else:
            figure.element('path',{'d':f'M {px} {py-10} A {size*2.24} {size*2.24} 0 0 0 {qx+12} {qy-4}',
                                  'stroke':BLUE,'stroke-width':2.5,'fill':'none','marker-end':'url(#arrow-blue)'})
            figure.text(ox+19,oy-105,'90°',18,BLUE)
        figure.circle(px,py,7,BLUE,BLUE)
        figure.rect(qx-7,qy-7,14,14,'#cceae4',TEAL,**{'stroke-width':2})
        figure.text(px+27,py+5,'P',22,BLUE)
        figure.text(qx-23,qy-15,'Q',22,TEAL)
        figure.text(ox,421,'(2,1) → '+str(target).replace(' ',''),21)
    figure.save('topics/data-structures/vacuum-imploder/assets/transformations.svg')


def aligned_halves():
    figure=Figure(778,346,'Aligned DNA halves',
                  'Positions 1,2,3 match positions 5,6,7 respectively, with position 4 in the middle. Changing 0123012 to 0023002 changes positions 2 and 6 only.')
    x0,size=134,76
    for start,count,color,label in [(0,3,TEAL,'A'),(3,1,ORANGE,'c'),(4,3,TEAL,'A')]:
        figure.rect(x0+start*size+3,27,count*size-6,40,'#ffedc4' if start==3 else '#cceae4',color)
        figure.text(x0+(start+count/2)*size,55,label,25,color,**{'font-weight':'bold'})
    for i in range(7):
        figure.text(x0+(i+.5)*size,98,i+1,18)
    for row,text in enumerate(('0123012','0023002')):
        y0=116+row*107
        figure.text(71,y0+39,'s' if row==0 else 't',26)
        for i,value in enumerate(text):
            fill = '#ffedc4' if i==3 else '#e8f4f0'
            figure.rect(x0+i*size,y0,size,64,fill)
            figure.text(x0+(i+.5)*size,y0+43,value,31)
            if row==1 and i in (1,5):
                figure.rect(x0+i*size+3,y0+3,size-6,58,fill='none',stroke=BLUE,**{'stroke-width':3})
    for i in (1,5):
        figure.line(x0+(i+.5)*size,187,x0+(i+.5)*size,213,BLUE,2,**{'marker-end':'url(#arrow-blue)'})
    for x,label in [(262,'1 ↔ 5'),(402,'2 ↔ 6'),(542,'3 ↔ 7')]:
        figure.text(x,326,label,21)
    figure.save('topics/strings/cloning-vat/assets/aligned-halves.svg')


if __name__=='__main__':
    shield_timeline()
    transformations()
    aligned_halves()
