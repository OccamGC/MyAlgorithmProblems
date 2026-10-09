"""Check editorial identities by exact fractions and explicit coefficient enumeration."""
from fractions import Fraction
from math import comb


def main():
    identities = 0
    for s in range(1,81):
        for t in range(s):
            total = sum((Fraction(comb(t,k),comb(s,k)) for k in range(1,t+1)),Fraction(0))
            assert total == Fraction(t,s-t+1)
            identities += 1
    modulus = 1004535809
    for n in range(101):
        inverse = [1]*(n+1)
        for i in range(1,n+1):
            inverse[i] = inverse[i-1]*pow(i,-1,modulus)%modulus
        actual = [0]*(2*n+1)

        def triangle(l,r):
            if l == r:
                actual[2*l] = (actual[2*l]+inverse[l]*inverse[n-l])%modulus
                return
            h = (l+r)//2
            triangle(l,h)
            triangle(h+1,r)
            left = inverse[l:h+1]
            right = [inverse[n-t] for t in range(h+1,r+1)]
            for x,a in enumerate(left):
                for y,b in enumerate(right):
                    at = l+h+1+x+y
                    actual[at] = (actual[at]+a*b)%modulus

        triangle(0,n)
        expected = [0]*(2*n+1)
        for i in range(n+1):
            for j in range(n-i+1):
                expected[n+i-j] = (expected[n+i-j]+inverse[i]*inverse[j])%modulus
        assert actual == expected,n
    print(f'{identities} exact binomial identities; 101 complete coefficient comparisons passed')


if __name__ == '__main__':
    main()
