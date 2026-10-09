"""Deterministic test recipes; Python 3 standard library only."""
from pathlib import Path
import argparse,json,random,subprocess

def generate(c):return f"{c['n']} {c['parameter']}\n"
def validate(text):
    z=list(map(int,text.split()));assert len(z)==2 and 1<=z[0]<=1000000000 and 1<=z[1]<=100000

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case',action='append')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args();plan=json.loads(args.plan.read_text('utf-8'))
    ids={c['id'] for c in plan['cases']}
    if args.case and not set(args.case)<=ids:parser.error('unknown case ID')
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for c in plan['cases']:
        if args.case and c['id'] not in args.case:continue
        text=generate(c);validate(text)
        p=args.out_dir/(c['id']+'.in');p.write_text(text,'utf-8',newline='\n')
        if args.std:
            answer=subprocess.run([str(args.std.resolve())],input=text.encode(),capture_output=True,check=True).stdout
            p.with_suffix('.out').write_bytes(answer.replace(b'\r\n',b'\n'))
if __name__=='__main__':main()
