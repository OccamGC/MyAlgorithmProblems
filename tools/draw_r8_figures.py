"""Draw both nomadism tour illustrations and the Day Delaunay tutorial figures."""

from draw_figures import Figure, BLUE, GRID, INK, ORANGE
from draw_delaunay_figures import draw as draw_delaunay


def draw():
    figure = Figure(960,420,'A tree and its first-visit tour',
                    'Four farms form a square of side ten. Three sides form an MST of weight thirty. '
                    'The doubled tree walk visits 1 2 3 4 3 2 1 and costs sixty. '
                    'Its first-visit tour 1 2 3 4 1 uses the fourth side and costs forty.')
    figure.text(245,42,'M = 30',26)
    figure.text(720,42,'C = 40',26)
    figure.line(480,65,480,375,GRID,1)
    for offset,closed in ((0,False),(475,True)):
        positions = [(145+offset,290),(345+offset,290),(345+offset,90),(145+offset,90)]
        for a,b in ((0,1),(1,2),(2,3)):
            x1,y1 = positions[a]
            x2,y2 = positions[b]
            figure.line(x1,y1,x2,y2,BLUE,4)
        if closed:
            figure.line(positions[3][0],positions[3][1],positions[0][0],positions[0][1],
                        ORANGE,4,**{'stroke-dasharray':'9 6'})
            figure.text(positions[0][0]-35,196,'10',20,ORANGE)
        figure.text(245+offset,76,'10',20)
        figure.text(380+offset,196,'10',20)
        figure.text(245+offset,323,'10',20)
        for i,(x,y) in enumerate(positions,1):
            figure.circle(x,y,20,'white',INK,2)
            figure.text(x,y+7,i,21)
        figure.text(245+offset,351,'1 → 2 → 3 → 4 → 1' if closed else '1 → 2 → 3 → 4 → 3 → 2 → 1',20)
        figure.text(245+offset,393,'C = 40 ≤ 2M' if closed else '2M = 60',23)
    for slug in ('nomadism-day','nomadism-night'):
        figure.save(f'topics/geometry/{slug}/assets/tree-tour.svg')


if __name__ == '__main__':
    draw()
    draw_delaunay()
