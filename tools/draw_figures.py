"""Redraw explanatory SVG figures using only the Python standard library.

Run from any directory: python tools/draw_figures.py
SVG files use shared symbols; captions and alternative text live in each language's Markdown.
"""

import math
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
INK = '#20354b'
GRID = '#acb9c6'
BLUE = '#1268b3'
TEAL = '#086d61'
ORANGE = '#a85a04'
RED = '#ad3845'


class Figure:
    def __init__(self, width, height, title, description):
        self.root = ET.Element(f'{{{NS}}}svg', {
            'width': str(width), 'height': str(height),
            'viewBox': f'0 0 {width} {height}', 'role': 'img',
            'aria-labelledby': 'title description',
        })
        self.element('title', {'id': 'title'}, title)
        self.element('desc', {'id': 'description'}, description)
        defs = self.element('defs')
        for name, color in [('blue', BLUE), ('ink', INK)]:
            marker = self.element('marker', {
                'id': f'arrow-{name}', 'markerWidth': '8', 'markerHeight': '8',
                'refX': '7', 'refY': '4', 'orient': 'auto', 'markerUnits': 'userSpaceOnUse',
            }, parent=defs)
            self.element('path', {'d': 'M 0 0 L 8 4 L 0 8 Z', 'fill': color}, parent=marker)
        pattern = self.element('pattern', {
            'id': 'removed', 'width': '10', 'height': '10', 'patternUnits': 'userSpaceOnUse',
        }, parent=defs)
        self.element('rect', {'width': '10', 'height': '10', 'fill': '#fff5dd'}, parent=pattern)
        self.element('path', {'d': 'M -2 2 L 2 -2 M 0 10 L 10 0 M 8 12 L 12 8',
                              'stroke': '#dba963', 'stroke-width': '1.2'}, parent=pattern)
        self.rect(0, 0, width, height, fill='white', stroke='none')

    def element(self, tag, attrs=None, text=None, parent=None):
        node = ET.SubElement(self.root if parent is None else parent, f'{{{NS}}}{tag}',
                             {key: str(value) for key, value in (attrs or {}).items()})
        node.text = text
        return node

    def rect(self, x, y, width, height, fill='white', stroke=GRID, **attrs):
        return self.element('rect', dict(x=x, y=y, width=width, height=height,
                                        fill=fill, stroke=stroke, **attrs))

    def line(self, x1, y1, x2, y2, color=INK, width=2, **attrs):
        return self.element('line', {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                                    'stroke': color, 'stroke-width': width,
                                    'stroke-linecap': 'round', **attrs})

    def text(self, x, y, text, size=20, color=INK, **attrs):
        return self.element('text', {'x': x, 'y': y, 'fill': color, 'font-size': size,
                                    'font-family': 'Arial, Helvetica, sans-serif',
                                    'text-anchor': 'middle', **attrs}, str(text))

    def circle(self, x, y, radius, fill='white', stroke=BLUE, width=2):
        return self.element('circle', {'cx': x, 'cy': y, 'r': radius, 'fill': fill,
                                       'stroke': stroke, 'stroke-width': width})

    def save(self, relative):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.root, space='  ')
        path.write_text(ET.tostring(self.root, encoding='unicode') + '\n',
                        encoding='utf-8', newline='\n')
        print(path.relative_to(ROOT))


def axes(figure, x, y, size, columns, rows, horizontal='x', vertical='y'):
    for j, label in enumerate(columns):
        figure.text(x + (j+.5)*size, y-14, label, 18)
    for i, label in enumerate(rows):
        figure.text(x-20, y+(i+.5)*size+6, label, 18)
    figure.line(x, y-48, x+len(columns)*size, y-48, width=1.7, **{'marker-end': 'url(#arrow-ink)'})
    figure.text(x+len(columns)*size+22, y-42, horizontal, 19)
    figure.line(x-53, y, x-53, y+len(rows)*size, width=1.7, **{'marker-end': 'url(#arrow-ink)'})
    figure.text(x-53, y+len(rows)*size+25, vertical, 19)


def coordinates():
    figure = Figure(484, 444, 'Integer cell coordinates',
                    'Every cell is labeled (x,y). x increases to the right and y downward. The origin is outlined.')
    x0, y0, size = 98, 84, 64
    axes(figure, x0, y0, size, range(-2, 3), range(-2, 3))
    for y in range(-2, 3):
        for x in range(-2, 3):
            left, top = x0+(x+2)*size, y0+(y+2)*size
            figure.rect(left, top, size, size, '#e0f1ed' if x == y == 0 else 'white')
            figure.text(left+size/2, top+size/2+6, f'({x},{y})', 17)
    figure.rect(x0+2*size+2, y0+2*size+2, size-4, size-4,
                fill='none', stroke=TEAL, **{'stroke-width': '3'})
    figure.save('topics/data-structures/psychic-commando/assets/coordinates.svg')


def radiation(radius):
    figure = Figure(494, 470, f'Radiation increments for r={radius}',
                    'The outlined cell is the bombardment center. Every cell shows its increment p, q, or 0; q is ceil(p/4).')
    x0, y0, size = 105, 104, 58
    figure.text(250, 30, f'r = {radius}', 24, **{'font-weight': 'bold'})
    axes(figure, x0, y0, size, range(-2, 3), range(-2, 3), 'u-x', 'v-y')
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if radius == 1:
                value = 'p' if dx == dy == 0 else '0'
            elif abs(dx) < radius and abs(dy) < radius:
                value = 'p'
            elif ((abs(dx) == radius and abs(dy) < radius-1) or
                  (abs(dy) == radius and abs(dx) < radius-1)):
                value = 'q'
            else:
                value = '0'
            fill = {'p': '#cceae4', 'q': '#ffedc4', '0': '#f5f7fa'}[value]
            left, top = x0+(dx+2)*size, y0+(dy+2)*size
            figure.rect(left, top, size, size, fill)
            figure.text(left+size/2, top+size/2+8, value, 25,
                        {'p': TEAL, 'q': ORANGE, '0': '#637587'}[value])
    figure.rect(x0+2*size+2, y0+2*size+2, size-4, size-4,
                fill='none', stroke=INK, **{'stroke-width': '3'})
    figure.text(250, 442, '(u-x, v-y) = (0, 0)  →  (x, y)', 18)
    figure.save(f'topics/data-structures/psychic-commando/assets/radiation-r{radius}.svg')


def cleanup():
    figure = Figure(842, 458, 'Closed rectangle cleanup and clipping',
                    'Panel A subtracts p in [0,2] by [0,1], including the boundary. Panel B clips the same operation to the recorded region [-1,1] by [-1,1].')
    size, y0 = 54, 92
    for panel, x0 in [('A', 80), ('B', 476)]:
        figure.text(x0+135, 30, f'({panel})', 24, **{'font-weight': 'bold'})
        axes(figure, x0, y0, size, range(-1, 4), range(-1, 4))
        for y in range(-1, 4):
            for x in range(-1, 4):
                requested = 0 <= x <= 2 and 0 <= y <= 1
                recorded = panel == 'A' or (-1 <= x <= 1 and -1 <= y <= 1)
                affected = requested and recorded
                fill = '#cceae4' if affected else ('#f5f7fa' if recorded else '#e4e8ed')
                figure.rect(x0+(x+1)*size, y0+(y+1)*size, size, size, fill)
                label = '-p' if affected else ('0' if recorded else '×')
                figure.text(x0+(x+1.5)*size, y0+(y+1.5)*size+7, label, 23,
                            TEAL if affected else '#637587')
        # The operation's inclusive boundary follows the outside of the selected cells.
        figure.rect(x0+size+2, y0+size+2, 3*size-4, 2*size-4,
                    fill='none', stroke=ORANGE, **{'stroke-width': '3'})
        if panel == 'B':
            figure.rect(x0-3, y0-3, 3*size+6, 3*size+6,
                        fill='none', stroke=BLUE, **{'stroke-width': '3', 'stroke-dasharray': '8 5'})
        figure.text(x0+135, 421, '[0,2] × [0,1]', 21)
    figure.save('topics/data-structures/psychic-commando/assets/cleanup.svg')


def cross(figure, x, y, radius=9):
    figure.line(x-radius, y-radius, x+radius, y+radius, RED, 3)
    figure.line(x-radius, y+radius, x+radius, y-radius, RED, 3)


def tick(figure, x, y):
    figure.element('path', {'d': f'M {x-10} {y} l 7 7 l 14 -16',
                            'fill': 'none', 'stroke': TEAL, 'stroke-width': '3.2',
                            'stroke-linecap': 'round', 'stroke-linejoin': 'round'})


def movement():
    figure = Figure(746, 372, 'Safe turns for the Terror Drone',
                    'F is the fortress and D the drone. Checks mark safe destinations, crosses mark collinear moves. The fortress moves from F to D in either case. Staying at D destroys the drone.')
    size, top = 82, 68
    for x0, fortress, tag in [(65, (0,1), 'A'), (429, (0,0), 'B')]:
        figure.text(x0+size*1.5, 32, f'({tag})', 24, **{'font-weight': 'bold'})
        fr, fc = fortress
        for row in range(3):
            for col in range(3):
                collinear = (1-fr)*(col-1) == (1-fc)*(row-1)
                fill = '#fce8e9' if collinear else '#e0f1ed'
                figure.rect(x0+col*size, top+row*size, size, size, fill)
                cx, cy = x0+(col+.5)*size, top+(row+.5)*size
                if (row,col) not in [(1,1), fortress]:
                    (cross if collinear else tick)(figure, cx, cy)
        fx, fy = x0+(fc+.5)*size, top+(fr+.5)*size
        dx, dy = x0+1.5*size, top+1.5*size
        figure.line(fx, fy, 2*dx-fx, 2*dy-fy, RED, 1.5, **{'stroke-dasharray': '5 5'})
        length = math.hypot(dx-fx, dy-fy)
        ux, uy = (dx-fx)/length, (dy-fy)/length
        figure.line(fx+ux*26, fy+uy*26, dx-ux*27, dy-uy*27, BLUE, 3,
                    **{'marker-end': 'url(#arrow-blue)'})
        figure.rect(fx-22, fy-22, 44, 44, '#d9eafa', BLUE, **{'stroke-width': '2', 'rx': '5'})
        figure.text(fx, fy+8, 'F', 25, BLUE, **{'font-weight': 'bold'})
        cross(figure, fx+29, fy-28, 5)
        figure.circle(dx, dy, 24, '#fff0d7', ORANGE, 2)
        figure.text(dx, dy+8, 'D', 25, ORANGE, **{'font-weight': 'bold'})
        cross(figure, dx+29, dy-28, 5)
    figure.save('topics/graphs/terror-drone/assets/movement.svg')


def route(figure, points):
    for (x1,y1), (x2,y2) in zip(points, points[1:]):
        distance = math.hypot(x2-x1,y2-y1)
        ux,uy = (x2-x1)/distance,(y2-y1)/distance
        figure.line(x1+16*ux,y1+16*uy,x2-17*ux,y2-17*uy,'white',7)
        figure.line(x1+16*ux,y1+16*uy,x2-17*ux,y2-17*uy,BLUE,3.5,
                    **{'marker-end': 'url(#arrow-blue)'})
    for index,(x,y) in enumerate(points):
        figure.circle(x,y,14,'white',BLUE,2)
        figure.text(x,y+5,index,16,BLUE,**{'font-weight': 'bold'})


def grid_route(name, rows, path, description, removed=None):
    size, x0, y0 = 62, 72, 70
    n,m = len(rows),len(rows[0])
    figure = Figure(x0+m*size+44,y0+n*size+44,name,description)
    for col in range(m):
        figure.text(x0+(col+.5)*size,y0-18,col+1,18)
    for row in range(n):
        figure.text(x0-24,y0+(row+.5)*size+6,row+1,18)
    fills = {'a':'#eee2fa','b':'#ffedc4','c':'#dfe7f1','d':'#f5dce4'}
    for row in range(n):
        for col in range(m):
            value = rows[row][col]
            fill = fills.get(value,'white')
            if value == removed:
                fill = 'url(#removed)'
            figure.rect(x0+col*size,y0+row*size,size,size,fill)
            if value in fills:
                if value == removed:
                    figure.text(x0+col*size+11,y0+row*size+size-9,value,16,ORANGE)
                else:
                    figure.text(x0+(col+.5)*size,y0+(row+.5)*size+8,value,25)
            if value in 'ST':
                figure.text(x0+(col+1)*size-12,y0+(row+1)*size-8,value,17,INK,
                            **{'font-weight':'bold'})
    if removed:
        # In the sample, the removed component consists of two adjacent cells.
        figure.rect(x0+size+3,y0+3,2*size-6,size-6,fill='none',stroke=ORANGE,
                    **{'stroke-width':'2.5','stroke-dasharray':'6 4'})
    points = [(x0+(col-.5)*size,y0+(row-.5)*size) for row,col in path]
    route(figure,points)
    figure.save(f'topics/graphs/terror-drone/assets/{name}.svg')


def main():
    coordinates()
    radiation(1)
    radiation(2)
    cleanup()
    movement()
    grid_route('diagonal-passages', ['......','...bb.','.a..b.','c..bb.','ccc...','......'],
               [(3,1),(2,2),(2,3),(3,4),(4,3),(5,4),(6,4),(6,5)],
               'Three four-connected obstacle components a, b, c and a legal turning route through diagonal gaps. Numbers mark successive fortress positions.')
    grid_route('sample-route', ['Saa..','b....','.cc..','...dT','.....'],
               [(1,1),(1,2),(2,3),(2,4),(3,5),(4,5)],
               'Sample 1: remove the hatched obstacle a. The fortress takes five moves from S through numbered cells 0 to 5 and reaches trap T.', removed='a')


if __name__ == '__main__':
    main()
