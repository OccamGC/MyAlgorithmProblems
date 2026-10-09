"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);count=recipe['queries'];mode=recipe['mode'];values=[]
    for i in range(count):
        n=rng.randint(1,1000000000)
        if mode=='small':n=i+1
        elif mode=='one':n=1
        elif mode=='odd':n=2*rng.randrange(500000000)+1
        elif mode=='even':n=2*rng.randint(1,500000000)
        elif mode=='maximum':n=1000000000
        elif mode=='descending':n=1000000000-i
        elif mode=='table_edges':n=max(1,min(1000000000,rng.randrange(30518)*32768+rng.choice([-1,0,1])))
        elif mode=='paired' and i%2:n=values[-1]
        values.append(n)
    return str(count)+'\n'+'\n'.join(map(str,values))+'\n'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir',type=Path,required=True)
    parser.add_argument('--case')
    parser.add_argument('--std',type=Path)
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text(encoding='utf-8'))
    recipes=[item for item in plan['cases'] if args.case is None or item['id']==args.case]
    if not recipes:parser.error('unknown case: '+str(args.case))
    args.out_dir.mkdir(parents=True,exist_ok=True)
    for recipe in recipes:
        path=args.out_dir/(recipe['id']+'.in')
        path.write_text(generate(recipe),encoding='ascii',newline='\n')
        if args.std:
            with path.open('rb') as inp,path.with_suffix('.out').open('wb') as out:
                subprocess.run([str(args.std.resolve())],stdin=inp,stdout=out,check=True)
    print('Generated',len(recipes),'input(s)')

if __name__=='__main__':main()
