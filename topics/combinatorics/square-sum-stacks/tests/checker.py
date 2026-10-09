"""Check any optimal arrangement: python checker.py input.in contestant.out."""
import argparse
import math
from pathlib import Path

def check(input_text, output_text):
    tokens=input_text.split()
    if len(tokens)!=1:
        raise ValueError('expected one stack count')
    n=int(tokens[0])
    if not 1<=n<=1000:
        raise ValueError('stack count outside constraints')
    lines=output_text.strip().splitlines()
    if len(lines)!=n:
        raise ValueError('wrong number of stack lines')
    maximum=(n+1)**2//2-1
    seen=bytearray(maximum+1)
    count=0
    for line in lines:
        labels=list(map(int,line.split()))
        if not labels:
            raise ValueError('an optimal arrangement has no empty stack')
        for label in labels:
            if not 1<=label<=maximum or seen[label]:
                raise ValueError('label outside optimal range or repeated')
            seen[label]=1
            count+=1
        for top,bottom in zip(labels,labels[1:]):
            if top<=bottom or math.isqrt(top+bottom)**2!=top+bottom:
                raise ValueError('labels must decrease, with square adjacent sums')
    if count!=maximum:
        raise ValueError('some labels of the optimal prefix are missing')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    try:
        check(args.input.read_text(encoding='ascii'),args.output.read_text(encoding='ascii'))
    except (ValueError,OSError,UnicodeError) as error:
        print('Rejected:',error)
        return 1
    print('Accepted')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
