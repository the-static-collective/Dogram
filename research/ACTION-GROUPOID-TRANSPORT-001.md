# ACTION-GROUPOID-TRANSPORT-001

Status: bounded research specimen. Promotion: none.

## Question

Does preserving only the source and target constitution preserve the transport that connected them?

## Exact specimen

Let `G=S3` act by conjugation on its subgroups and let `H=< (01) >={e,(01)}`. The transporter from `H` to itself is

`T_G(H,H)={g in G : gHg^-1=H}=N_G(H)=H`.

Hence there are exactly two distinct action-groupoid arrows `H -> H`: one labelled by `e`, one labelled by `(01)`. They have identical source and target objects but are different arrows.

Seal:

> **SAME SOURCE + SAME TARGET != SAME TRANSPORT ARROW.**

This is the bounded continuation of NON-NORMAL-TYPE-CONSTITUTION-001: endpoint constitution alone does not receipt transport history.

## Documented mathematics

A groupoid is a category whose arrows are invertible, with source, target, identity, inverse, and composition data; arrows are data in addition to objects. See Soylu Yilmaz & Yilmaz (2022), DOI `10.1002/mma.8129`, and Avila et al. (2020), DOI `10.1155/2020/3967368`.

For a group action, the associated translation/action groupoid has action elements as arrows between objects. Under conjugation on subgroups, the endomorphism arrows at `H` are exactly the stabilizer of `H`, i.e. its normalizer. Wolfram's group-theory documentation independently confirms stabilizer/orbit machinery under permutation actions; the exact S3 specimen here is exhaustively enumerated in stdlib Python.

## Dogram inference

If a receipt stores only `(source constitution, target constitution)`, it can collapse distinct lawful transports. If transport identity matters to the calculation, retain the arrow label or an explicitly declared quotient of arrows.

## Refusal boundary

- GROUP ACTION ARROW != OCCURRENCE
- SAME ENDPOINT != SAME HISTORY
- TRANSPORTER ELEMENT != EVIDENCE
- GROUPOID COMPOSITION != CAUSAL COMPOSITION
- LOOP ARROW != HISTORICAL LOOP
- NORMALIZER != AUTHORITY

No public operator, schema, evidence semantics, causal semantics, or authority path is added.

## Reproduce

`pytest -q tests/test_action_groupoid_transport_001.py`

Strongest next frontier: distinct composable arrow paths with the same composite arrow. That would separate `same composite transport` from `same factorization/history` and point toward path/groupoid or 2-dimensional receipts only if a bounded hostile specimen earns them.
