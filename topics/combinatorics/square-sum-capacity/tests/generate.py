"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    mode=recipe['mode'];rng=random.Random(recipe['seed'])
    if mode=='literal':return recipe['input']
    if mode=='grox':
        a=recipe['a'];n=recipe['n']
        if a=='maximum':a='1'+'0'*1000
        if n=='maximum':n='1'+'0'*1000
        return f"{a}\n{recipe['b']}\n{recipe['c']}\n{n}\n"
    if mode=='capacity':
        count=recipe['queries'];digits=recipe['digits'];values=[]
        for i in range(count):
            if recipe['shape']=='maximum':value='2'+'0'*100000
            elif recipe['shape']=='nines':value='9'*digits
            elif recipe['shape']=='power':value='1'+'0'*(digits-1)
            elif recipe['shape']=='alternating':value=('19'*((digits+1)//2))[:digits]
            elif recipe['shape']=='small':value=str(i+1)
            else:value=str(rng.randrange(1,10))+''.join(str(rng.randrange(10)) for _ in range(digits-1))
            if recipe['shape']=='leading_zero':value='0'*(599990-digits)+value
            values.append(value)
        return str(count)+'\n'+'\n'.join(values)+'\n'
    raise ValueError(mode)


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
