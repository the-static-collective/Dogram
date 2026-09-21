from research.typed_cospectral_incidence_001 import A,B,receipt

def test_typed_cospectral_collision():
    r=receipt()
    assert r['margins_A']==r['margins_B']==((1,1,2,3),(1,1,2,3))
    assert r['charpoly_A']==r['charpoly_B']==(1,0,-7,0,13,0,-6,0,0)
    assert r['typed_isomorphic'] is False
    assert r['untyped_isomorphic'] is True

def test_exact_carriers_are_distinct():
    assert A != B
