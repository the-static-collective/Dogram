# PROBE-SEPARATION-001

Status: bounded research specimen. Authority: none. Public operator: none.

## Question

After SCALARIZATION-VISIBILITY-001, generalize method-relative visibility without promoting non-observation into nonexistence: when may a declared family of probes identify distinct states?

## Exact finite specimen

Three supplied states carry two declared coordinates:

- `x = (parity=0, high_bit=0)`
- `y = (parity=0, high_bit=1)`
- `z = (parity=1, high_bit=1)`

Under the one-probe family `F={parity}`, signatures are `x->(0)`, `y->(0)`, `z->(1)`. Thus distinct supplied states `x != y` are observationally indistinguishable relative to F.

Extend only the declared family to `G={parity, high_bit}`. Signatures become `(0,0)`, `(0,1)`, `(1,1)` and all three unordered state pairs are separated.

The kernel checks every finite pair. A constant-probe hostile control leaves every pair indistinguishable.

## Delta / seal

**INDISTINGUISHABLE UNDER DECLARED PROBES != IDENTICAL UNLESS SEPARATION IS ESTABLISHED.**

Secondary: **FAILURE OF A PROBE FAMILY TO DISTINGUISH A PAIR IS A RECEIPT ABOUT THAT FAMILY-PAIR RELATION, NOT A RECEIPT OF STATE IDENTITY.**

## Documented mathematics

Observability theory formalizes whether distinct states can be reconstructed/distinguished from outputs. Gerbet & Roebenack (2025), DOI `10.1002/pamm.202400138`, explicitly computes indistinguishable pairs/states for output maps in nonlinear hypergraph systems. Wolfram `ObservableModelQ` documentation independently exhibits distinct initial states producing indistinguishable outputs in an unobservable system and observability changing with the output map.

Goriac (2013), DOI `10.1002/int.21589`, distinguishes observational/extrospective equivalence from stronger state notions and discusses bounded finite observability.

These sources support the mathematical substrate only; Dogram's receipt/refusal interpretation is project-local inference.

## Dogram inference

A probe family induces a signature map `sigma_F : X -> product(outputs)`. For finite X, the family separates supplied states exactly when this map is injective. If injectivity fails, retain a concrete collision pair. If it succeeds after a complete finite pair check, report separation for this supplied finite domain only.

Do not infer global separation from a bounded sample or unfinished search.

## Refusals

- PROBE OUTPUT != OCCURRENCE.
- INDISTINGUISHABILITY != IDENTITY.
- SEPARATION != EVIDENTIARY TRUTH.
- OBSERVABILITY != CAUSAL EXPLANATION.
- ADDING A PROBE != AUTHORITY TO INTERPRET IT.
- FINITE-DOMAIN SEPARATION != GLOBAL SEPARATION.
- FAILURE TO DISTINGUISH != ABSENCE.

## Reproduce

`pytest -q tests/test_probe_separation_001.py`

No public operator, schema, runtime action, evidence promotion, causal semantics, or authority path is introduced.
