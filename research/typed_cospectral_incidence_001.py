from collections import Counter
from itertools import permutations

A=((1,1,0,1),(0,1,1,0),(1,0,0,0),(1,0,0,0))
B=((1,0,1,1),(1,1,0,0),(0,1,0,0),(1,0,0,0))

def margins(m):
    return tuple(sorted(map(sum,m))), tuple(sorted(sum(r[j] for r in m) for j in range(4)))

def typed_isomorphic(a,b):
    # Exact bounded check: row and column permutations only; side roles may not swap.
    for rp in permutations(range(4)):
        for cp in permutations(range(4)):
            if all(a[i][j]==b[rp[i]][cp[j]] for i in range(4) for j in range(4)):
                return True
    return False

def transpose(m):
    return tuple(tuple(m[i][j] for i in range(4)) for j in range(4))

def untyped_isomorphic_via_side_swap(a,b):
    # For connected bipartite graphs, an untyped isomorphism either preserves or swaps the unique bipartition.
    return typed_isomorphic(a,b) or typed_isomorphic(a,transpose(b))

def adjacency(m):
    z=[[0]*8 for _ in range(8)]
    for i in range(4):
        for j in range(4):
            z[i][4+j]=z[4+j][i]=m[i][j]
    return z

def charpoly_coeffs_int(matrix):
    # Faddeev-LeVerrier, exact integer arithmetic.
    n=len(matrix); I=[[int(i==j) for j in range(n)] for i in range(n)]
    B=[row[:] for row in I]; coeff=[1]
    def mul(x,y): return [[sum(x[i][k]*y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    for k in range(1,n+1):
        AB=mul(matrix,B); ck=-sum(AB[i][i] for i in range(n))//k; coeff.append(ck)
        B=[[AB[i][j]+ck*I[i][j] for j in range(n)] for i in range(n)]
    return tuple(coeff)

def receipt():
    return {
      'margins_A':margins(A),'margins_B':margins(B),
      'typed_isomorphic':typed_isomorphic(A,B),
      'untyped_isomorphic':untyped_isomorphic_via_side_swap(A,B),
      'charpoly_A':charpoly_coeffs_int(adjacency(A)),
      'charpoly_B':charpoly_coeffs_int(adjacency(B)),
    }

if __name__=='__main__': print(receipt())
