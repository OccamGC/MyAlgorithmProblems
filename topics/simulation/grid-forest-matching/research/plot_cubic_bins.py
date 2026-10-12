"""Draw the axis-interval diagram; requires Pillow and a TrueType/OpenType font."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'assets' / 'cubic-axis-bins.png'


def load_font(size, font_path=None):
    if font_path is not None:
        return ImageFont.truetype(str(font_path), size)
    # Pillow searches platform font directories for these common font names.
    for name in ('arial.ttf', 'DejaVuSans.ttf', 'LiberationSans-Regular.ttf', 'Arial.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    raise RuntimeError('No supported font found. Pass --font PATH to a .ttf or .otf file.')


def draw(output=OUT, font_path=None):
    image = Image.new('RGB', (1600, 1040), '#ffffff')
    pen = ImageDraw.Draw(image)
    fonts = {size: load_font(size, font_path) for size in (24, 27, 30, 34, 42)}
    ink, blue, green, red = '#203044', '#2563a6', '#16806c', '#bb3f42'

    def text(x, y, value, size=27, fill=ink, anchor=None):
        pen.text((x, y), value, font=fonts[size], fill=fill, anchor=anchor)

    def axis_x(t):
        return 240 + 72 * t

    text(70, 45, 'Why one road vertex needs at most two bin budgets', 42)
    text(70, 107, 'Axis projection schematic: label length = 6; each resource spans at most 5 edges.', 27)
    pen.rounded_rectangle((55, 165, 1545, 660), radius=18, fill='#f7f9fc')
    text(85, 185, '1. A resource containing z must have its left endpoint between 4 and 9.', 30)
    for y in range(268, 610, 18):
        pen.line((axis_x(9), y, axis_x(9), y + 8), fill=red, width=3)
    text(axis_x(9), 260, 'projection of z: x = 9', 24, red, 'mb')
    intervals = [('A', 4, 9), ('B', 5, 10), ('C', 6, 11), ('D', 8, 13), ('E', 9, 14)]
    for index, (name, left, right) in enumerate(intervals):
        y = 285 + 59 * index
        color = blue if left < 6 else green
        text(90, y, f'Resource {name}', 27, anchor='lm')
        pen.line((axis_x(left), y, axis_x(right), y), fill=color, width=8)
        for value in range(left, right + 1):
            radius = 7 if value == left else 4
            pen.ellipse((axis_x(value)-radius, y-radius, axis_x(value)+radius, y+radius), fill=color)
        text(axis_x(right) + 18, y, f'left = {left}', 24, color, 'lm')
    pen.line((axis_x(0), 596, axis_x(16), 596), fill=ink, width=2)
    for value in range(17):
        pen.line((axis_x(value), 590, axis_x(value), 603), fill=ink, width=2)
        text(axis_x(value), 612, str(value), 24, anchor='mt')

    text(85, 700, '2. Possible left endpoints meet only two bins of width 6.', 30)
    for left, right, fill, color, label in [
        (0, 6, '#e8f1ff', blue, 'Bin 0: [0, 6)'),
        (6, 12, '#e4f5ee', green, 'Bin 1: [6, 12)'),
        (12, 17, '#f0f1f4', ink, 'Bin 2'),
    ]:
        pen.rectangle((axis_x(left), 761, axis_x(right), 870), fill=fill)
        text((axis_x(left)+axis_x(right))/2, 844, label, 24, color, 'mm')
    pen.line((axis_x(4), 792, axis_x(9), 792), fill=red, width=5)
    for value in range(4, 10):
        x = axis_x(value)
        pen.ellipse((x-8, 784, x+8, 800), fill=red)
        text(x, 807, str(value), 24, red, 'mt')
    text(85, 910, 'Distinct early endpoints within each bin allow an injective resource assignment.', 27)
    text(85, 956, 'At most 1 charge from Bin 0 + at most 1 from Bin 1 = at most 2 charges at z.', 30)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUT, help='Output PNG path')
    parser.add_argument('--font', type=Path, help='Optional .ttf or .otf font path')
    args = parser.parse_args()
    draw(args.output, args.font)
