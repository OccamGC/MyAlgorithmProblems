"""Reproducible standard-library test generator; use --help for its interface."""
import argparse,json,random,subprocess
from pathlib import Path


def generate(recipe):
    rng=random.Random(recipe['seed']);count=recipe['queries'];mode=recipe['mode'];values=[]
    for i in range(count):
        n,k,p=[rng.randint(1,1000000000) for _ in range(3)]
        if mode=='small':n=rng.randint(1,12);k=rng.randint(1,6);p=rng.randint(1,31)
        elif mode=='even_modulus':p=2*rng.randint(1,500000000)
        elif mode=='unit_modulus':p=1
        elif mode=='maximum_alphabet':k=1000000000
        elif mode=='odd_length':n=2*rng.randrange(500000000)+1
        elif mode=='even_length':n=2*rng.randint(1,500000000)
        elif mode=='boundaries':n,k,p=[rng.choice([1,2,999999999,1000000000]) for _ in range(3)]
        elif mode=='paired' and i%2:n,k,p=values[-1]
        values.append((n,k,p))
    return str(count)+'\n'+''.join(' '.join(map(str,row))+'\n' for row in values)


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
