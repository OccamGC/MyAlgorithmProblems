"""Exhaust the nonincreasing prime-exponent patterns for values <= 10**9."""
from pathlib import Path
import json

def maximum_divisor_count(limit):
    # The product of these ten primes already exceeds the limit.
    primes=[2,3,5,7,11,13,17,19,23,29]
    best=(1,1)
    visited=0
    def visit(index,max_exponent,value,count):
        nonlocal best,visited
        visited+=1
        if count>best[0] or count==best[0] and value<best[1]:
            best=(count,value)
        if index==len(primes):
            return
        for exponent in range(1,max_exponent+1):
            value*=primes[index]
            if value>limit:
                break
            visit(index+1,exponent,value,count*(exponent+1))
    visit(0,limit.bit_length(),1,1)
    return dict(limit=limit,maximum_divisor_count=best[0],smallest_witness=best[1],enumerated_patterns=visited)

if __name__=='__main__':
    result=maximum_divisor_count(10**9)
    assert result['maximum_divisor_count']==1344
    assert result['smallest_witness']==735134400
    path=Path(__file__).resolve().parents[1]/'build/R17/divisor-bound.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result)
