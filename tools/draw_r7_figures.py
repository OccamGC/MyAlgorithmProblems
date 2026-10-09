"""Draw the R7 explanatory SVGs with the Python standard library."""
from draw_figures import Figure, BLUE, TEAL, ORANGE, INK, GRID, RED, cross

def controlled_path():
    figure=Figure(700,290,'Controlled vertices and their connecting path',
                  'Controlled vertices 1 and 3 on the path 1-2-3-4 are connected through vertex 2. The uncontrolled vertex 2 costs 5; vertex 4 need not be visited.')
    figure.text(350,40,'S = {1, 3}',25)
    positions=[100,265,430,595]
    for index in range(3):
        figure.line(positions[index]+30,127,positions[index+1]-30,127,
                    BLUE if index<2 else GRID,5 if index<2 else 2)
    for index,position in enumerate(positions):
        controlled=index in (0,2)
        color=TEAL if controlled else ORANGE if index==1 else GRID
        figure.circle(position,127,30,'#d8efe9' if controlled else '#fff0d1' if index==1 else 'white',color,3)
        if controlled:
            figure.circle(position,127,25,'none',TEAL,1)
        figure.text(position,135,index+1,24,INK)
        figure.text(position,193,f'v = {[3,5,7,11][index]}',21,color)
    figure.line(70,230,460,230,BLUE,3)
    figure.text(265,268,'5',25,ORANGE,**{'font-weight':'bold'})
    figure.save('topics/trees/psychic-control-tree/assets/controlled-path.svg')

def strict_radius():
    figure=Figure(560,590,'Strict Manhattan radius',
                  'A source S at the center has radius 3. The 13 cells at distance less than 3 receive plus L; cells at distance 3 or greater do not.')
    figure.text(280,39,'R = 3,  d < 3',25)
    origin_x,origin_y,size=75,97,58
    for i in range(7):
        figure.text(origin_x+(i+.5)*size,79,i+1,18)
        figure.text(51,origin_y+(i+.5)*size+6,i+1,18)
    for i in range(7):
        for j in range(7):
            distance=abs(i-3)+abs(j-3)
            x,y=origin_x+j*size,origin_y+i*size
            figure.rect(x,y,size,size,'#d8efe9' if distance<3 else '#f6f8fa',GRID)
            figure.text(x+size/2,y+24,'S' if distance==0 else distance,21,TEAL if distance<3 else '#697888')
            if distance<3:
                figure.text(x+size/2,y+47,'+ L',18,TEAL)
            if distance==3:
                figure.rect(x+3,y+3,size-6,size-6,'none',ORANGE,**{'stroke-dasharray':'5 4','stroke-width':1.5})
    figure.text(278,551,'|x − i| + |y − j| = d',22)
    figure.save('topics/data-structures/torch-light/assets/strict-radius.svg')

def largest_square():
    figure=Figure(602,425,'An empty square of side four',
                  'In a 5 by 7 grid, buildings occupy (1,1), (1,3), and (5,7). Rows 2 through 5 and columns 2 through 5 form a valid square of side 4.')
    x0,y0,size=99,69,58
    figure.text(301,30,'s = 4',25)
    for j in range(7):
        figure.text(x0+(j+.5)*size,56,j+1,18)
    for i in range(5):
        figure.text(77,y0+(i+.5)*size+6,i+1,18)
        for j in range(7):
            building=(i,j) in ((0,0),(0,2),(4,6))
            field=1<=i<=4 and 1<=j<=4
            x,y=x0+j*size,y0+i*size
            figure.rect(x,y,size,size,'#ffe4e8' if building else '#d8efe9' if field else 'white')
            if building:
                cross(figure,x+size/2,y+size/2)
    figure.rect(x0+size+2,y0+size+2,4*size-4,4*size-4,'none',TEAL,**{'stroke-width':4})
    figure.line(x0+size,y0+5*size+22,x0+5*size,y0+5*size+22,TEAL,2)
    figure.text(x0+3*size,y0+5*size+51,'4',23,TEAL)
    figure.save('topics/geometry/wheat-field/assets/largest-square.svg')

if __name__=='__main__':
    controlled_path()
    strict_radius()
    largest_square()
