"""Draw the statements and frontier explanation for the two melon sequels."""
from draw_figures import Figure, INK, GRID, BLUE, ORANGE


def guides():
    f = Figure(560, 310, 'Guide frames and a terminal harvest',
               'L1 can reach R1 or R2; L2 can only reach R2. L1 grows into R2, stopping both vines.')
    for a, b in ((85,85), (85,205), (205,205)):
        f.line(130, a, 425, b, color=GRID, width=2, **{'stroke-dasharray':'7 6'})
    f.line(158, 96, 392, 192, color=BLUE, width=4, **{'marker-end':'url(#arrow-blue)'})
    for y, label in ((85,'L1'), (205,'L2')):
        f.circle(130, y, 28, fill='#e5f3ea', stroke=INK)
        f.text(130, y+7, label, 21)
    f.rect(395, 55, 60, 60, stroke=INK)
    f.text(425, 93, 'R1', 21)
    f.rect(395, 175, 60, 60, stroke=INK)
    f.circle(425, 205, 23, fill='#fff3cf', stroke=ORANGE)
    f.text(425, 213, 'M', 23)
    f.text(425, 263, 'R2', 20)
    f.save('topics/graphs/melon-planting-2/assets/guide-frames.svg')


def terminal():
    f = Figure(440, 235, 'A terminal harvest with two melons',
               'Arrows select two growth edges; the remaining vine has no empty neighbor.')
    for y, row in enumerate(('xlMlx', 'xolMx')):
        for x, value in enumerate(row):
            left, top = 45+x*70, 35+y*70
            f.rect(left, top, 70, 70, fill='#e8edf2' if value=='x' else '#e5f3ea' if value=='l' else 'white')
            if value=='M':
                f.circle(left+35, top+35, 21, fill='#fff3cf', stroke=ORANGE)
            f.text(left+35, top+43, value, 24)
    for x, y in ((1,0), (2,1)):
        f.line(45+x*70+57, 70+y*70, 45+(x+1)*70+12, 70+y*70,
               color=BLUE, width=3, **{'marker-end':'url(#arrow-blue)'})
    f.text(220, 212, '2', 23)
    f.save('topics/dynamic-programming/melon-planting-3/assets/terminal-field.svg')


def frontier():
    f = Figure(800, 335, 'A frontier update',
               'Before and after processing c: forget u above c; retain v on the left and the other frontier cells.')
    for offset, step, count in ((35,'t',2), (445,'t + 1',3)):
        f.text(offset+144, 33, step, 24)
        for y in range(3):
            for x in range(4):
                processed = y==0 or (y==1 and x<count)
                left, top = offset+x*72, 60+y*72
                f.rect(left, top, 72, 72, fill='#e8edf2' if processed else 'white')
                if (y==1 and x<count) or (y==0 and x>=count):
                    f.rect(left+3, top+3, 66, 66, fill='none', stroke=BLUE, **{'stroke-width':3})
                label = {(0,2):'u', (1,1):'v', (1,2):'c'}.get((y,x),'')
                if label:
                    f.text(left+36, top+44, label, 24)
                if (y,x)==(1,2):
                    f.rect(left+8, top+8, 56, 56, fill='none', stroke=ORANGE, **{'stroke-width':2,'stroke-dasharray':'5 4'})
    f.line(350, 164, 414, 164, color=BLUE, width=3, **{'marker-end':'url(#arrow-blue)'})
    f.text(400, 313, 'u → c', 23)
    f.save('topics/dynamic-programming/melon-planting-3/assets/frontier.svg')


if __name__ == '__main__':
    guides()
    terminal()
    frontier()
