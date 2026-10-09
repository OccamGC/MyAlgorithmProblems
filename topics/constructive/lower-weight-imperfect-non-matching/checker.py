"""Validate a closed spanning walk and print its integer score from 0 to 100.

Usage: python checker.py input.in contestant.out
Exit 0 means a legal route (possibly partial credit); exit 1 means invalid.
The baseline is twice the minimum spanning tree weight, computed by Prim.
"""
import argparse,heapq
from pathlib import Path
def read_input(text):
    z=list(map(int,text.split()))
    if len(z)<2:raise ValueError('missing dimensions')
    n,m=z[:2]
    if not (1<=n<=100000 and n-1<=m<=200000 and len(z)==2+3*m):raise ValueError('invalid dimensions')
    edges=[];adj=[[] for _ in range(n)]
    for i in range(m):
        u,v,w=z[2+3*i:5+3*i]
        if not (1<=u<=n and 1<=v<=n and 0<=w<=10000):raise ValueError('invalid edge')
        edges.append((u-1,v-1,w));adj[u-1].append((w,v-1));adj[v-1].append((w,u-1))
    seen=[False]*n;queue=[(0,0)];weight=0;visited=0
    while queue:
        cost,u=heapq.heappop(queue)
        if seen[u]:continue
        seen[u]=True;visited+=1;weight+=cost
        for cost,v in adj[u]:
            if not seen[v]:heapq.heappush(queue,(cost,v))
    if visited!=n:raise ValueError('graph is disconnected')
    return n,edges,2*weight
def check(input_text,output_text):
    n,edges,baseline=read_input(input_text);tokens=output_text.split()
    if not tokens:raise ValueError('missing edge count')
    count=int(tokens[0])
    if not 0<=count<=5*n or len(tokens)!=count+1:raise ValueError('invalid edge count or extra/missing tokens')
    position=0;visited={0};distance=0
    for token in tokens[1:]:
        edge=int(token)
        if not 1<=edge<=len(edges):raise ValueError('invalid edge ID')
        u,v,w=edges[edge-1]
        if position==u:position=v
        elif position==v:position=u
        else:raise ValueError('discontinuous walk')
        visited.add(position);distance+=w
    if position!=0:raise ValueError('walk does not return to vertex 1')
    if len(visited)!=n:raise ValueError('walk misses a vertex')
    if distance<=2*baseline:score=100
    elif distance<=5*baseline:score=40+(60*(5*baseline-distance)+3*baseline-1)//(3*baseline)
    else:score=40
    return {'score':score,'distance':distance,'baseline':baseline,'edges':count}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    try:result=check(args.input.read_text('utf-8'),args.output.read_text('utf-8'))
    except (ValueError,OSError) as error:print(0);parser.exit(1,str(error)+'\n')
    print(result['score'])
if __name__=='__main__':main()
