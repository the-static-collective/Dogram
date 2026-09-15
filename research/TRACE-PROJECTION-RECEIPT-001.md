# TRACE-PROJECTION-RECEIPT-001

Status: bounded research specimen; no public operator.

## Question

After MAZURKIEWICZ-TRACE-QUOTIENT-001 and FOATA-PROFILE-COLLISION-001, what is a complete but decomposed receipt for a finite trace under a fixed dependence relation?

## Documented mathematics

For a concurrent alphabet, the classical projection lemma says that two words represent the same Mazurkiewicz trace iff their projections onto every dependent letter-pair agree. Equivalently, a trace can be represented by a consistent family of dependent-pair word projections. See Diekert & Muscholl, *Trace Theory* (2011), DOI 10.1007/978-0-387-09766-4_491, and Mikulski, *Projection Representation of Mazurkiewicz Traces* (2008), DOI 10.3233/FUN-2008-851-427.

## Frozen exact specimen

Alphabet `Sigma={a,b,c}`. The only independent distinct pair is `a I c` (symmetrically). Thus the canonical unordered dependent projection family is `aa, ab, bb, bc, cc`.

Compare:

- left word `abac`, exact trace class `{abac, abca}`;
- right word `baac`, exact trace class `{baac, baca, bcaa}`.

The classes are disjoint by exhaustive adjacent-independent-swap closure.

Their complete dependent-pair projection receipts agree everywhere except `ab`:

- `aa`: `aa = aa`
- `ab`: `aba != baa`
- `bb`: `b = b`
- `bc`: `bc = bc`
- `cc`: `c = c`

If the `ab` projection is omitted, the remaining receipts are exactly equal even though the traces remain different.

## Delta

`full dependent-pair receipt equality = false`

`receipt equality after omitting ab = true`

`trace equality = false`

Exactly one required local projection carries the separating order information in this specimen.

## Seals

**A FAMILY OF LOCAL PROJECTIONS CAN BE COLLECTIVELY COMPLETE EVEN WHEN NO SINGLE SUMMARY IS THE CARRIER.**

**OMITTING ONE DECLARED DEPENDENCE PROJECTION CAN COLLAPSE DISTINCT TRACES.**

**RECEIPT WHICH LOCAL VIEWS WERE ACTUALLY RETAINED.**

## Pressure boundary

- TRACE PROJECTION != HISTORICAL OBSERVATION
- DEPENDENT PAIR != CAUSAL DEPENDENCE
- COMPLETE TRACE RECEIPT != COMPLETE REAL-WORLD HISTORY
- LOCAL PROJECTION != EVIDENCE CHANNEL
- TRACE EQUALITY != OCCURRENCE IDENTITY
- OMITTED PROJECTION != HIDDEN CAUSE
- MATHEMATICAL SUFFICIENCY != AUTHORITY

## Inference

For Dogram, the useful structural lesson is not to promote trace projections. It is narrower: when an invariant is assembled from a declared family of local views, the family/index set belongs in the receipt. Completeness of the full family does not transfer to an undeclared subfamily.

## HOLD

`trace_projection@1`, `projection_family@1`, `dependence_receipt@1`, and any occurrence/evidence/causal/authority interpretation remain unpromoted.
