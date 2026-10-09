"""Draw the Day solution's Delaunay tutorial diagrams from explicit coordinates."""

import math

from draw_figures import Figure, BLUE, GRID, INK, ORANGE, RED, TEAL


DESTINATION = 'topics/geometry/nomadism-day/assets/'
EXAMPLE = {'A': (0, 0), 'B': (0, 6), 'C': (3, 3),
           'D': (4, 0), 'E': (4, 6), 'F': (8, 3)}


def point(figure, x, y, label, dx=0, dy=-15):
    figure.circle(x, y, 4.5, INK, 'white', 1)
    figure.text(x + dx, y + dy, label, 18)


def segment(figure, positions, edge, color=BLUE, width=2.5, **attrs):
    figure.line(*positions[edge[0]], *positions[edge[1]], color, width, **attrs)


def polygon(figure, positions, vertices, fill, stroke='none'):
    figure.element('polygon', {'points': ' '.join(f'{positions[v][0]},{positions[v][1]}'
                                                for v in vertices),
                               'fill': fill, 'stroke': stroke})


def basics():
    figure = Figure(900, 370, 'Convex hull and triangulation',
                    'The same six sites appear twice. A B C D E form the convex hull. '
                    'Adding segments from interior site P to each hull vertex gives five triangles.')
    hull = {'A': (75, 280), 'B': (325, 280), 'C': (365, 155),
            'D': (220, 75), 'E': (75, 130), 'P': (210, 180)}
    figure.line(450, 55, 450, 315, GRID, 1)
    for offset in (0, 450):
        pos = {v: (x + offset, y) for v, (x, y) in hull.items()}
        polygon(figure, pos, 'ABCDE', '#eef4fa', BLUE)
        for a, b in zip('ABCDE', 'BCDEA'):
            segment(figure, pos, a + b, BLUE, 3)
        if offset:
            for i, a in enumerate('ABCDE'):
                b = 'BCDEA'[i]
                polygon(figure, pos, 'P' + a + b, ['#e0f1ed', '#edf4fb'][i % 2])
                segment(figure, pos, 'P' + a, TEAL, 2)
        for v, (x, y) in pos.items():
            point(figure, x, y, v, -17 if v in 'AE' else 15 if v in 'BC' else 0,
                  22 if v in 'AB' else -14)
        figure.text(225 + offset, 34, '(A)' if not offset else '(B)', 23)
    figure.text(225, 348, 'A → B → C → D → E → A', 20)
    figure.text(675, 348, '5 △', 22, TEAL)
    figure.save(DESTINATION + 'triangulation-basics.svg')


def empty_circle():
    figure = Figure(900, 420, 'Two diagonals and the empty-circle test',
                    'A=(0,0), B=(6,0), C=(6,4), D=(0,2). The diagonal AC is invalid: '
                    'D is inside the circumcircle of ABC. The diagonal BD gives a Delaunay triangulation; '
                    'C is outside the circumcircle of ABD.')
    figure.line(450, 60, 450, 362, GRID, 1)
    coords = {'A': (0, 0), 'B': (6, 0), 'C': (6, 4), 'D': (0, 2)}
    for offset, diagonal, center, radius, color in (
            (0, 'AC', (3, 2), math.sqrt(13), RED),
            (450, 'BD', (3, 1), math.sqrt(10), TEAL)):
        pos = {v: (100 + offset + 35 * x, 275 - 35 * y) for v, (x, y) in coords.items()}
        figure.circle(100 + offset + 35 * center[0], 275 - 35 * center[1],
                      35 * radius, '#fcfaf6', ORANGE, 1.5)
        for edge in ('AB', 'BC', 'CD', 'DA'):
            segment(figure, pos, edge, INK, 2)
        segment(figure, pos, diagonal, color, 3.5,
                **({'stroke-dasharray': '7 5'} if not offset else {}))
        for v, (x, y) in pos.items():
            point(figure, x, y, v, -16 if v in 'AD' else 16, 20 if v in 'AB' else -12)
        figure.text(225 + offset, 36, f'{diagonal}  ' + ('×' if not offset else '✓'), 25, color)
        figure.text(225 + offset, 390, 'D ∈ disk(ABC)' if not offset else 'C ∉ disk(ABD)', 21, color)
    figure.save(DESTINATION + 'empty-circle.svg')


def mst_disk():
    figure = Figure(750, 360, 'An MST edge has an empty diameter disk',
                    'Suppose P is another site inside or on the diameter disk of AB. '
                    'Both AP and BP are shorter than AB. Removing AB from the tree separates '
                    'A and B; one of AP and BP crosses that cut and gives a cheaper tree.')
    figure.circle(220, 180, 120, '#eef4fa', GRID, 2)
    pos = {'A': (100, 180), 'B': (340, 180), 'P': (220, 120)}
    segment(figure, pos, 'AB', BLUE, 4)
    for edge in ('AP', 'PB'):
        segment(figure, pos, edge, ORANGE, 2.5, **{'stroke-dasharray': '7 4'})
    for v, (x, y) in pos.items():
        point(figure, x, y, v, -18 if v == 'A' else 18 if v == 'B' else 0)
    figure.text(545, 112, '|AP| < |AB|', 24, ORANGE)
    figure.text(545, 157, '|BP| < |AB|', 24, ORANGE)
    figure.text(545, 232, 'T − AB + AP', 24, TEAL)
    figure.text(545, 271, 'T − AB + BP', 24, TEAL)
    figure.text(220, 332, 'AB ∈ MST  ⇒  P cannot exist', 20)
    figure.save(DESTINATION + 'mst-disk.svg')


def merge_steps():
    figure = Figure(1080, 740, 'Six stages of a Delaunay merge',
                    'Coordinates: A=(0,0), B=(0,6), C=(3,3), D=(4,0), E=(4,6), F=(8,3). '
                    'The two initial triangles are ABC and DEF. The cross edges are added '
                    'in the order AD, CD, CF, CE, BE. DE is deleted before adding CF. '
                    'Blue edges were already added, and orange marks the current base.')
    old = ['AB', 'BC', 'CA', 'DE', 'EF', 'FD']
    stages = [(None, [], False), ('AD', ['AD'], False), ('CD', ['AD', 'CD'], False),
              ('CF', ['AD', 'CD', 'CF'], True),
              ('CE', ['AD', 'CD', 'CF', 'CE'], True),
              ('BE', ['AD', 'CD', 'CF', 'CE', 'BE'], True)]
    for i, (base, added, removed) in enumerate(stages):
        x0, y0 = (i % 3) * 360, (i // 3) * 370
        if i % 3:
            figure.line(x0, y0 + 18, x0, y0 + 350, GRID, 1)
        if i >= 3:
            figure.line(x0 + 18, y0, x0 + 342, y0, GRID, 1)
        pos = {v: (x0 + 44 + 33 * x, y0 + 282 - 33 * y)
               for v, (x, y) in EXAMPLE.items()}
        figure.text(x0 + 180, y0 + 35, f'({i + 1})', 23)
        figure.line(x0 + 44 + 33 * 3.5, y0 + 64, x0 + 44 + 33 * 3.5,
                    y0 + 308, GRID, 1, **{'stroke-dasharray': '4 5'})
        for edge in old:
            if removed and edge == 'DE':
                if i == 3:
                    segment(figure, pos, edge, RED, 2, **{'stroke-dasharray': '5 5'})
                continue
            segment(figure, pos, edge, GRID, 2)
        for edge in added:
            segment(figure, pos, edge, ORANGE if edge == base else BLUE, 3.5 if edge == base else 2.7)
        for v, (x, y) in pos.items():
            point(figure, x, y, v, -17 if v in 'ABC' else 17 if v == 'F' else 0,
                  22 if v in 'AD' else -14)
        figure.text(x0 + 180, y0 + 337, '△ABC + △DEF' if base is None else
                    ('− DE, + CF' if i == 3 else '+ ' + base), 22,
                    INK if base is None else ORANGE)
    figure.save(DESTINATION + 'merge-steps.svg')


def merge_pruning():
    figure = Figure(820, 435, 'Why the merge deletes DE',
                    'With current base CD, the first right candidate is E and the next is F. '
                    'The circumcircle of CDE is centered at (8,3), exactly F, and has radius five. '
                    'F is strictly inside, so DE is deleted. The next cross edge will be CF.')
    pos = {v: (55 + 27 * x, 312 - 27 * y) for v, (x, y) in EXAMPLE.items()}
    figure.circle(*pos['F'], 135, '#fcfaf6', ORANGE, 1.8)
    for edge in ('AB', 'BC', 'CA', 'EF', 'FD', 'AD'):
        segment(figure, pos, edge, GRID, 2)
    segment(figure, pos, 'CD', ORANGE, 4)
    segment(figure, pos, 'DE', RED, 3, **{'stroke-dasharray': '7 5'})
    segment(figure, pos, 'CF', BLUE, 3)
    for v, (x, y) in pos.items():
        point(figure, x, y, v, -18 if v in 'ABC' else 14, 21 if v in 'AD' else -13)
    figure.text(620, 103, 'base = CD', 24, ORANGE)
    figure.text(620, 155, 's = E,  t = F', 23)
    figure.text(620, 215, 'F ∈ disk(CDE)', 23, RED)
    figure.text(620, 267, '− DE', 26, RED)
    figure.text(620, 319, '+ CF', 26, BLUE)
    figure.text(235, 407, '(x − 8)² + (y − 3)² = 25', 21)
    figure.save(DESTINATION + 'merge-pruning.svg')


def navigation():
    figure = Figure(790, 355, 'Navigating a directed edge',
                    'In the counterclockwise triangle u v w, e points from u to v. '
                    'Onext(e) points from u to w, LeftNext(e) points from v to w, '
                    'and Reverse(e) points from v to u. Onext stays at the origin; '
                    'LeftNext walks around the left face.')
    pos = {'u': (100, 270), 'v': (365, 270), 'w': (200, 70)}
    polygon(figure, pos, 'uvw', '#eef4fa')
    for edge, color, marker in [('uv', BLUE, 'blue'), ('uw', INK, 'ink'), ('vw', INK, 'ink')]:
        x1, y1 = pos[edge[0]]
        x2, y2 = pos[edge[1]]
        length = math.hypot(x2 - x1, y2 - y1)
        figure.line(x1, y1, x2 - 12 * (x2 - x1) / length, y2 - 12 * (y2 - y1) / length,
                    color, 3, **{'marker-end': f'url(#arrow-{marker})'})
    for v, (x, y) in pos.items():
        point(figure, x, y, v, -17 if v == 'u' else 17 if v == 'v' else 0)
    figure.text(232, 302, 'e = u → v', 23, BLUE)
    figure.text(74, 158, 'Onext', 19)
    figure.text(343, 148, 'LeftNext', 19)
    figure.text(600, 106, 'Onext(e) = u → w', 21)
    figure.text(600, 171, 'LeftNext(e) = v → w', 21)
    figure.text(600, 236, 'Reverse(e) = v → u', 21)
    figure.save(DESTINATION + 'quad-edge-navigation.svg')


def draw():
    basics()
    empty_circle()
    mst_disk()
    merge_steps()
    merge_pruning()
    navigation()


if __name__ == '__main__':
    draw()
