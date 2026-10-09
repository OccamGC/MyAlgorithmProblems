"""Draw language-neutral diagrams used by both statements."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]


def text(x,y,value,size=19):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="#182b43">{escape(str(value))}</text>'


def line(x1,y1,x2,y2,color='#496078',width=3,dash=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def circle(x,y,value,apple=False):
    return f'<circle cx="{x}" cy="{y}" r="23" fill="{"#d8f1e4" if apple else "white"}" stroke="#234b64" stroke-width="2"/>'+text(x,y+7,value)+(text(x,y-33,'*',26) if apple else '')


def save(topic,slug,name,body,width=760,height=280):
    path = ROOT/'topics'/topic/slug/'assets'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"><rect width="{width}" height="{height}" fill="#f7f9fc"/><g font-family="Arial, sans-serif">{body}</g></svg>\n'
    path.write_text(svg,encoding='utf-8',newline='\n')


def main():
    body = text(380,34,'[1, 3, 5]')
    for i,value in enumerate((1,3,5)):
        x = 230+150*i
        body += f'<rect x="{x-42}" y="65" width="84" height="60" rx="8" fill="white" stroke="#234b64" stroke-width="2"/>'
        body += text(x,104,value,26)+text(x,150,f'i = {i+1}',16)
    body += line(230,187,380,187)+line(380,187,530,187)
    body += text(305,180,'2')+text(455,180,'2')+text(380,243,'d(1, 3) = 2; length = 3')
    save('data-structures','catalyst-sequence','minimum-gap.svg',body)

    body = text(380,32,'Sample 1: S1 before S2; capacity(M1) = capacity(M2) = 1',17)
    coords = {'S1':(160,95),'S2':(160,200),'M1':(595,95),'M2':(595,200)}
    body += line(183,95,572,95,'#8396aa',2,'6 5')+text(380,82,'tier 2',16)
    body += line(183,200,572,200,'#8396aa',2,'6 5')+text(380,222,'tier 2',16)
    body += line(183,95,572,200,'#15825a',4)
    body += line(183,200,572,95,'#245cad',4)
    for x,label in [(433,'S1: tier 2'),(310,'S2: tier 1')]:
        body += f'<rect x="{x-51}" y="161" width="102" height="27" rx="4" fill="#f7f9fc"/>'+text(x,181,label,16)
    for name,(x,y) in coords.items():
        body += circle(x,y,name)
    body += text(380,257,'solid = chosen assignment; dashed = another listed choice',16)
    save('graphs','spode-seminary','same-tier.svg',body)

    body = text(190,28,'Sample 1; apples = {2, 3}',18)+text(570,28,'Sample 2; apples = {1, 3}',18)
    body += line(190,83,115,178)+line(190,83,265,178)
    body += text(130,119,'1',16)+text(250,119,'1',16)
    body += circle(190,83,1)+circle(115,178,2,True)+circle(265,178,3,True)
    body += line(500,83,570,133)+line(570,133,640,183)
    body += text(546,86,'1',16)+text(621,136,'1',16)
    body += circle(500,83,1,True)+circle(570,133,2)+circle(640,183,3,True)
    body += text(190,235,'2 → 1 → 3 → 1 → 2; distance = 4',16)
    body += text(570,235,'1 → 2 → 3 → 2 → 1; distance = 4',16)
    body += text(380,272,'* = apple; edge labels = lengths',15)
    save('trees','hagen-farm','apple-walks.svg',body,height=295)


if __name__ == '__main__':
    main()
