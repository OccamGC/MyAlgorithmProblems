"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(case):
    if 'expression' in case:return case['expression']+'\n'
    length=case['length'];mode=case['mode']
    if mode=='unary':text='~'*(length-1)+'7'
    elif mode=='deep':
        count=(length-1)//2;text='('*count+'7'+')'*count
        if len(text)<length:text='+'+text
    elif mode=='conditional':text='1?0:'*((length-1)//4)+'1'
    elif mode=='middle':
        count=(length-1)//6;text='1?'*count+'7'+':1/0'*count
    elif mode=='short':text='0&&('+'1/0+'*((length-7)//4)+'1)'
    elif mode=='spaces':text=' '*(length-6)+'15<<33'
    else:raise ValueError(mode)
    return text+'\n'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, default=Path(__file__).with_name('plan.json'))
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--std', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    requested = set(args.case)
    unknown = requested - {case['id'] for case in plan['cases']}
    if unknown:
        parser.error('unknown case: ' + ', '.join(sorted(unknown)))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for case in plan['cases']:
        if requested and case['id'] not in requested:
            continue
        target = args.out_dir / (case['id'] + '.in')
        target.write_text(generate(case), encoding='utf-8', newline='\n')
        if args.std:
            with target.open('rb') as source, target.with_suffix('.out').open('wb') as output:
                subprocess.run([str(args.std.resolve())], stdin=source, stdout=output, check=True)
if __name__ == '__main__':
    main()
