"""Redraw R24 examples as self-contained SVG assets."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def svg(body,w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><rect width="{w}" height="{h}" fill="#f7fafc"/><g font-family="Arial, sans-serif" font-size="22" text-anchor="middle" fill="#18334a">'+body+'</g></svg>\n'
body='<text x="390" y="36" font-size="27" font-weight="bold">N = 4, M = 11</text><text x="44" y="100" font-size="15">TOP</text><path d="M44 120 V282 l-7 -12 m7 12 l7 -12" fill="none" stroke="#516879" stroke-width="2"/>'
for j,values in enumerate([[8,1],[11,5,4],[9,7,2],[10,6,3]]):
    x=140+175*j
    body+=f'<line x1="{x}" y1="86" x2="{x}" y2="300" stroke="#a5b8c8" stroke-width="7"/><line x1="{x-52}" y1="305" x2="{x+52}" y2="305" stroke="#18334a" stroke-width="5"/>'
    for i,v in enumerate(values):
        y=100+82*i
        body+=f'<circle cx="{x}" cy="{y}" r="27" fill="#e5efff" stroke="#2e5eaa" stroke-width="2"/><text x="{x}" y="{y+8}">{v}</text>'
        if i:body+=f'<text x="{x+57}" y="{y-35}" font-size="17" fill="#81531d">Σ={v+values[i-1]}</text>'
    body+=f'<text x="{x}" y="342" font-size="18">{j+1}</text>'
for slug in ['square-sum-stacks','square-sum-capacity']:
    p=ROOT/'topics/combinatorics'/slug/'assets/stacks.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg(body,810,365),'utf-8')
body='<text x="450" y="36" font-size="27" font-weight="bold">n = 3: two orders, one tree</text>'
for base,order in [(40,[1,2]),(470,[2,1])]:
    body+=f'<rect x="{base}" y="62" width="390" height="212" rx="12" fill="white" stroke="#c3d1dc"/>'
    for j in range(2):
        x=base+60+j*135
        body+=f'<line x1="{x}" y1="166" x2="{x+135}" y2="166" stroke="#2e5eaa" stroke-width="4"/><text x="{x+67}" y="127" font-size="20">#{order[j]}</text>'
    for j in range(3):
        x=base+60+j*135
        body+=f'<circle cx="{x}" cy="166" r="26" fill="#e5efff" stroke="#2e5eaa" stroke-width="2"/><text x="{x}" y="174">{j+1}</text>'
    label='(1,2) → (2,3)' if order[0]==1 else '(2,3) → (1,2)'
    body+=f'<text x="{base+195}" y="242" font-size="20">{label}</text>'
p=ROOT/'topics/combinatorics/ordered-tree-building/assets/orders.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg(body,900,298),'utf-8')
