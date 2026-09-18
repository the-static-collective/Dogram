# TYPE-STABILIZER-AUTHORITY-001

## Question
When an untyped structural symmetry exchanges two declared carrier roles, does the symmetry itself authorize quotienting the role boundary?

## Frozen specimen
Use the 4-cycle C4 with alternating declared vertex types `representative` and `successor`. Exact enumeration of all 4! vertex permutations gives 8 graph automorphisms. Four preserve the declared types and four swap the two type classes globally.

With the admissibility declaration restricted to `preserve`, exactly 4 automorphisms are licensed. If and only if `swap` is explicitly added to the allowed type actions, all 8 become licensed.

Thus the structural automorphism group and the admissible symmetry group are different objects:

`Aut(G)` records symmetries of the untyped carrier.

`Aut(G,c)` (the color/type stabilizer) records symmetries preserving the declared typing.

A larger admissible action that includes a type swap requires an additional declaration; it is not inferred from the existence of a side-switching automorphism.

## Documented mathematics
Vertex-colored graph isomorphism requires the isomorphism to preserve colors. Equivalently, a declared coloring/partition restricts the automorphism group to its color-preserving subgroup. This is standard colored-graph/group-action mathematics; see López-Presa, *Novel Techniques to Speed Up the Computation of the Automorphism Group of a Graph*, Journal of Applied Mathematics (2014), DOI 10.1155/2014/934637. Related distinguishing-coloring work likewise studies automorphisms that preserve vertex colors.

## Dogram inference
A type boundary is part of the calculation contract when downstream operations distinguish the roles. An untyped symmetry may demonstrate that the carrier has a role-exchanging shape symmetry, but cannot manufacture permission to forget the role distinction. The quotient constitution must declare which type actions are admissible.

Seal: **SYMMETRY CAN EXHIBIT A ROLE SWAP; IT CANNOT LICENSE THE SWAP.**

Secondary seal: **AUTOMORPHISM GROUP != ADMISSIBLE AUTOMORPHISM GROUP WHEN THE CONTRACT CARRIES TYPES.**

## Boundary
- AUTOMORPHISM != AUTHORITY.
- TYPE SWAP EXISTS != TYPE SWAP DECLARED.
- STRUCTURAL SYMMETRY != SEMANTIC INTERCHANGEABILITY.
- ADMISSIBLE RELABELING != OCCURRENCE.
- COLOR PRESERVATION != EVIDENCE OR TRUTH.

No public Dogram operator, semantic promotion, evidence claim, or authority path is introduced.

## Reproduction
Run `python research/type_stabilizer_authority_001.py` and `pytest -q tests/test_type_stabilizer_authority_001.py`.
