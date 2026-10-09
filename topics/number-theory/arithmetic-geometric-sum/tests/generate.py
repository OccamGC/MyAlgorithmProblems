"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);count=recipe['queries'];mode=recipe['mode'];lines=[str(count)]
    for i in range(count):
        a,b,c,d=[rng.randint(1,1000000000) for _ in range(4)]
        l=rng.randint(1,1000000000);r=rng.randint(l,1000000000)
        if mode=='small':l=rng.randint(1,12);r=rng.randint(l,24);a,b,c,d=[rng.randint(1,12) for _ in range(4)]
        elif mode=='unit_base':c=1
        elif mode=='unit_ratio':c=rng.randint(2,31622)**2;b=500000003
        elif mode=='singleton':r=l
        elif mode=='full_interval':l=1;r=1000000000
        elif mode=='short_interval':r=min(l+rng.randint(0,8),1000000000)
        elif mode=='maximum':l=1;r=1000000000;a=b=c=d=1000000000
        elif mode=='boundaries':
            a,b,c,d=[rng.choice([1,2,999999999,1000000000]) for _ in range(4)]
            l=rng.choice([1,999999999,1000000000]);r=rng.randint(l,1000000000)
        elif mode=='mixed':
            if i%4==0:c=1
            elif i%4==1:c=4;b=500000003
            elif i%4==2:r=l
        lines.append(' '.join(map(str,(l,r,a,b,c,d))))
    return '\n'.join(lines)+'\n'


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
