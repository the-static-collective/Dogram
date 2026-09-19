# FACTORIZATION-PATH-001

Status: bounded research specimen. Authority: none. Promotion: none.

## Question

Does an exact composite transport receipt determine the composable arrows that produced it?

## Frozen specimen

Let `G=S3` act by conjugation on its order-2 subgroups and let `H=< (01) >`.
Take `g=(012)` and `k=(021)=g^-1`.

Two length-2 paths begin and end at `H`:

- `H --g--> gHg^-1 --g^-1--> H`
- `H --k--> kHk^-1 --k^-1--> H`

The intermediate subgroups are distinct, the ordered arrow pairs are distinct, and both composites are the identity element.

Therefore:

> **SAME COMPOSITE TRANSPORT != SAME FACTORIZATION HISTORY.**

The composite receipts the net group action. It does not reconstruct a chosen decomposition of that arrow.

## Documented mathematics

This is standard category/groupoid arithmetic, not a new theorem. A groupoid has objects, arrows, source/target maps, composition, identities, and inverses. More generally, an arrow may admit multiple decompositions into composable arrows. See:

- E. Soylu Yilmaz & K. Yilmaz (2022), *On relations among quadratic modules*, DOI 10.1002/mma.8129 — groupoid structure and composition.
- L. Poinsot & S. Caenepeel (2013), *Two Interacting Coordinate Hopf Algebras of Affine Groups of Formal Series on a Category*, DOI 10.1155/2013/370618 — explicit treatment of proper decompositions of an arrow into composable arrows.
- B. Jurco, C. Saemann & M. Wolf (2016), *Higher groupoid bundles, higher spaces, and self-dual tensor field equations*, DOI 10.1002/prop.201600031 — the nerve of a category retains strings of composable morphisms as higher simplices while face maps compose adjacent arrows.

Wolfram group-theory documentation independently supplies finite permutation-group, stabilizer, orbit, and multiplication machinery. The exact specimen here is dependency-free and exhaustively finite.

## Dogram inference

If Dogram needs to preserve *which declared factorization was supplied*, storing only the composite arrow is insufficient. A factorization/path receipt can be retained without claiming that the path occurred in history.

This fits LINEAGE-SPINE/BRAID/WEAVE: endpoint or composite equality is compatible with distinct receipted derivation/factorization structure.

## Refusal boundary

- TRANSPORT ARROW != OCCURRENCE.
- FACTORIZATION PATH != HISTORICAL PATH.
- SAME COMPOSITE != SAME PROVENANCE.
- INTERMEDIATE CONSTITUTION != OBSERVED INTERMEDIATE STATE.
- GROUPOID COMPOSITION != CAUSAL COMPOSITION.
- LONGER RECEIPT != GREATER TRUTH OR AUTHORITY.

No public operator, schema, causal semantics, evidence semantics, or authority path is proposed.

## Reproduce

```bash
pytest -q tests/test_factorization_path_001.py
python - <<'PY'
from pprint import pprint
from research.factorization_path_001 import receipt
pprint(receipt())
PY
```

## Next frontier

The current specimen distinguishes two factorizations by their intermediate objects. A stronger hostile control should hold the full object sequence fixed and find distinct parallel arrow factorizations with the same composite. If that survives, the residual lives in arrow-level path data rather than merely intermediate-object data. Only then consider a 2-cell/homotopy receipt that declares when two such paths may themselves be identified.
