"""Usage: python checker.py input.in contestant.out. Exit 0 accepts; exit 1 rejects."""
import argparse
from pathlib import Path

def read_input(text):
    values=list(map(int,text.split()))
    if len(values)<2:raise ValueError('missing N M')
    n,m=values[:2]
    if not 1<=n<=200000 or not 0<=m<=200000 or len(values)!=2+2*m:raise ValueError('invalid input size')
    used=set();soul=list(range(n+3))
    for u,v in zip(values[2::2],values[3::2]):
        pair=tuple(sorted((u,v)))
        if not 1<=u<=n or not 1<=v<=n or u==v or pair in used:raise ValueError('invalid historical pair')
        used.add(pair);soul[u],soul[v]=soul[v],soul[u]
    return n,used,soul

def check(input_text,output_text):
    n,used,soul=read_input(input_text)
    # Reject unexpectedly long output before tokenizing it.
    if len(output_text)>40*(2*n+2):raise ValueError('output too long')
    values=list(map(int,output_text.split()))
    if not values:raise ValueError('missing operation count')
    count=values[0]
    if not 0<=count<=2*n+1 or len(values)!=1+2*count:raise ValueError('operation count or extra tokens')
    for u,v in zip(values[1::2],values[2::2]):
        pair=tuple(sorted((u,v)))
        if not 1<=u<=n+2 or not 1<=v<=n+2 or u==v:raise ValueError('invalid body index')
        if pair in used:raise ValueError('body pair reused')
        used.add(pair);soul[u],soul[v]=soul[v],soul[u]
    if any(soul[i]!=i for i in range(1,n+3)):raise ValueError('a soul was not restored')
    return count

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    try:count=check(args.input.read_text('ascii'),args.output.read_text('ascii'))
    except (ValueError,UnicodeError) as error:print('Rejected:',error);raise SystemExit(1)
    print(f'Accepted: {count} operations')
if __name__=='__main__':main()
