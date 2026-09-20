# NON-NORMAL-TYPE-CONSTITUTION-001

Status: bounded research specimen. Authority: none. Promotion: none.

## Question

If a declared admissible type-action subgroup is transported by an exact structural change of frame, when may Dogram identify the transported subgroup with the originally declared constitution?

## Frozen specimen

Let `G=S3`, let `H=< (01) >={e,(01)}`, and let `g=(012)`. Exact finite enumeration gives:

- `|G|=6`, `|H|=2`, `[G:H]=3`;
- `g H g^-1 = {e,(12)} != H` under the tuple convention frozen in the kernel;
- `gH != Hg`;
- therefore `H` is not normal in `G`.

The transported subgroup is structurally conjugate to the declared subgroup, but it is not the same subset of available actions. A frame transport can therefore carry a constitution to a conjugate constitution without rewriting which constitution was declared.

## Documented mathematics

This is standard finite group theory. Conjugation `h -> g h g^-1` is an inner automorphism; subgroups related by it are conjugate. A subgroup is normal exactly when every such conjugate equals itself; equivalently its left and right cosets agree for every group element.

Scholarly provenance: Popplestone, Liu & Weiss (1990), *AI Magazine* 11(1), DOI `10.1609/aimag.v11i1.825`, explicitly defines left/right cosets, conjugate subgroups by inner automorphism, and normality by `g H g^-1 = H`. Bernardini et al. (2011), DOI `10.5402/2011/898254`, likewise states normal-subgroup and quotient-group prerequisites.

## Dogram inference

`TYPE-ACTION-SUBGROUP-001` showed that the structural action group and the declared admissible subgroup need not coincide. This specimen adds that, for a non-normal admissible subgroup, an exact structural change of frame can transport the declaration to a distinct conjugate subgroup.

Seal:

> CONJUGATE CONSTITUTION != DECLARED CONSTITUTION WHEN THE ADMISSIBLE SUBGROUP IS NON-NORMAL.

Secondary:

> A CHANGE OF FRAME MAY TRANSPORT A CONSTITUTION. IT DOES NOT SILENTLY REWRITE WHICH CONSTITUTION WAS DECLARED.

## Refusal boundary

- `CONJUGACY != IDENTITY`
- `CHANGE OF FRAME != CHANGE OF DECLARATION`
- `LEFT COSET != RIGHT COSET WITHOUT NORMALITY`
- `COSET != SEMANTIC CLASS`
- `GROUP ACTION != OCCURRENCE`
- `STRUCTURAL TRANSPORT != AUTHORITY`

No causal, evidential, historical, semantic, or authority interpretation is inferred from the group calculation. No public operator or schema is added.

## Reproduce

```bash
pytest -q tests/test_non_normal_type_constitution_001.py
python research/non_normal_type_constitution_001.py
```

## Next frontier

The strongest next question is not a larger group. It is whether a chain of frame transports should receipt the conjugating element itself, so that `H -> gHg^-1 -> kgHg^-1k^-1` can be distinguished from merely observing the terminal subgroup. This points toward groupoids / transport categories: same endpoint constitution need not mean same transport history.
