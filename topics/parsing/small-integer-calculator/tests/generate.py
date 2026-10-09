"""Deterministic test recipes; Python 3 standard library only."""
import argparse,json,random,subprocess
from pathlib import Path

def generate(case):
    if 'expression' in case:return case['expression']+'\n'
    mode=case['mode'];n=case['length']
    if mode=='unary':text='-~'*((n-1)//2)+'7'
    elif mode=='deep':text='('*((n-1)//2)+'6'+')'*((n-1)//2)
    elif mode=='sum':text='+'.join(['9']*((n+1)//2))
    elif mode=='nested':
        count=(n-1)//4;text='1+('*count+'2'+')'*count
    else:
        count=(n-7)//2;text='*'.join(['9']*count)+'/(-0)'
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
