# TYPE-ACTION-SUBGROUP-001

Status: bounded research specimen. Promotion: none.

## Question

When a carrier has structural symmetries that permute declared role-types, which of those symmetries may a calculation quotient away?

## Frozen specimen

Use the complete graph `K3`. Its three vertices carry distinct declared role-types `R`, `S`, and `W`. Because every permutation of the three vertices preserves `K3`, the structural automorphism group realizes all six elements of `S3` on the role set.

Declare only the even role permutations admissible:

`H = A3 <= S3`.

Exact enumeration gives:

- structural automorphisms: 6;
- induced role permutations: all 6 elements of `S3`;
- admissible role actions in `A3`: 3;
- structurally available but refused transpositions: 3;
- subgroup index `[S3:A3] = 2`.

Thus a transposition such as swapping `R` and `S` while fixing `W` is an exact structural symmetry of the carrier but is outside the declared admissible action.

## Delta

`STRUCTURAL TYPE ACTION EXISTS != TYPE ACTION IS ADMISSIBLE`.

The carrier's automorphism group describes available symmetries. The declared subgroup describes which symmetries this calculation is permitted to forget. Those are separate receipts.

## Documented mathematics

This is elementary finite group-action mathematics. `S3` is the full permutation group on three symbols; `A3` is its order-3 subgroup of even permutations, hence has index 2. Graph automorphisms are vertex permutations preserving adjacency. Wolfram Language documentation exposes `GraphAutomorphismGroup`, `GroupElements`, `GroupOrder`, and named `SymmetricGroup` / `AlternatingGroup` machinery for these exact objects.

## Dogram inference

A quotient constitution can be represented by a declared admissible subgroup of structurally realized type actions. This is not yet proposed as a public operator. The research value is the refusal receipt: symmetries outside the subgroup remain visible rather than being silently normalized away.

## Refusal boundary

- AUTOMORPHISM != AUTHORITY
- STRUCTURAL TYPE ACTION != DECLARED TYPE ACTION
- SAME ORBIT UNDER S3 != SAME ORBIT UNDER A3
- COSET != SEMANTIC CLASS
- ADMISSIBLE RELABELING != OCCURRENCE
- GROUP ACTION != EVIDENCE, CAUSATION, TRUTH, OR AUTHORITY

## Reproduce

`pytest -q tests/test_type_action_subgroup_001.py`

or

`python research/type_action_subgroup_001.py`

## Next frontier

Use a non-normal admissible subgroup `H < G` so left/right cosets and conjugated constitutions can diverge. Ask whether changing the declaration by conjugation is merely a frame change or a genuinely different quotient constitution. Keep that question on HOLD until an exact hostile specimen earns it.
