# CONTRIBUTION-FIELD-001

**Status:** bounded internal research specimen  
**Authority:** none  
**Public operator:** none

## Question

Can one attributable contribution retain an immutable birth address while later supplied history changes the typed graph around it, with Dogram calculating the structural delta without pricing the contributor, ranking people, inferring causation, or manufacturing source evidence?

This specimen answers that question only for one finite synthetic field.

> **THE GRAPH PRESERVES CONTRIBUTION HISTORY. IT DOES NOT PRICE THE CONTRIBUTOR.**

## Boundary

The specimen is deliberately narrower than an economy, reputation system, or universal contribution ontology.

```text
GRAPH != ECONOMY
MEASUREMENT != VALUE
VALUE != PRICE
PRICE != HUMAN WORTH
CONTRIBUTION != HUMAN WORTH
CENTRALITY != VALUE
EDGE COUNT != CONTRIBUTION
DESCENDANT COUNT != MERIT
LONGEVITY != GOODNESS
DEPENDENCE != AUTHORITY
GRAPH PATH != CAUSAL PATH
GRAPH REACHABILITY != HISTORICAL OCCURRENCE
```

Dogram receives a caller-declared relation vocabulary and caller-supplied evidence status. It calculates only over the finite supplied specimen.

## Event floor

Each v0 event has exactly:

```text
event_id
relation_kind
source_ref
subject_ref
evidence_ref
evidence_status
available_from
```

The first status vocabulary is:

```text
complete
incomplete
invalid
```

Those statuses are supplied by the owning source. Dogram does not establish whether that source disposition is historically true.

Only `complete` events enter the graph. `incomplete` and `invalid` remain explicit residue in the cut and measurement receipt.

```text
SUPPLIED COMPLETE != DOGRAM-CERTIFIED TRUTH
INCOMPLETE != FALSE
INVALID != NEVER-HAPPENED
MISSING GRAPH EDGE != PROVEN NON-OCCURRENCE
```

Unknown relation kinds, duplicate event ids, malformed event shapes, and undeclared semantic fields fail closed.

## Incidence lowering

A typed event is lowered through its own event node:

```text
entity:<source>
    ↓
event:<event_id>
    ↓
entity:<subject>
```

The relation kind remains attached to the event record rather than being collapsed into an untyped direct edge.

That choice permits multiple distinct declared relations between the same endpoint entities and permits `ablate@1` to remove one specific event node.

```text
SAME ENDPOINTS != SAME RELATION
HEAD ADDRESS != RELATION TYPE
```

The hostile anti-collapse control verifies that collapsing:

```text
(A, X, CREATED)
(A, X, REVIEWED)
```

to only:

```text
(A, X)
(A, X)
```

loses one previously available distinction.

## Frozen history

The declared specimen is:

```text
t0
A CREATED X

t1 additions
B REPAIRED X
X ENABLED Y
C CHALLENGED X
Y CARRIED Z
```

All five events are `complete` in the frozen fixture.

At `t0`, the contribution field contains only `A CREATED X`.

At `t1`, the same immutable birth is surrounded by the later four supplied events.

The two field digests are:

```text
t0 = sha256:4ea238843b993df30c1e6d80329065c995a4ead0fc209168feb76e1770e9d306
t1 = sha256:c620ca16f1f3cc363e70c3c84d663459f76a2b3009fc069cc5c7975c7610b46c
```

Different field digests mean the declared finite cuts differ. They do not establish that the later field is better, more valuable, or more true.

## Workmark birth

The frozen Workmark points at the birth event `e-create-x` and contribution root `X`.

```text
birth event digest
sha256:e2d4ea5d051c3983aeb84886c2dc6c26a3c842c8633de216ba28fb39031f065a

workmark id
sha256:5ae02620badca78daa720284814f2303a6fde107c58c05ca1299152a19024e66
```

The Workmark is identical in the `t0` and `t1` measurement receipts.

If later supplied history rewrites the birth event while keeping its event id, measurement refuses with:

```text
BIRTH_EVENT_DIGEST_MISMATCH
```

Thus:

> **LATER HISTORY MAY ENRICH THE NEIGHBORHOOD. LATER HISTORY MAY NOT REWRITE THE BIRTH RECEIPT.**

The Workmark is an address into contribution history, not an issuer-controlled scalar value.

```text
WORKMARK != SCORE
WORKMARK != MONEY
WORKMARK != AUTHORITY
WORKMARK != OWNERSHIP OF THE UNDERLYING WORK
```

## Neutral measurement

The first measurement family is intentionally small:

```text
descendant_count
relation_kind_counts
reachable_descendant_set
```

At `t0`:

```text
descendant_count = 0
reachable_descendant_set = []
relation_kind_counts = {
  CREATED: 1
}
```

At `t1`:

```text
descendant_count = 2
reachable_descendant_set = [Y, Z]
relation_kind_counts = {
  CARRIED: 1,
  CHALLENGED: 1,
  CREATED: 1,
  ENABLED: 1,
  REPAIRED: 1
}
```

The measurement receipts are:

```text
t0 receipt
sha256:e202074fd05441b1c64153b12964047d046d1fa4c255762ecf7ca50aebfd0338

t1 receipt
sha256:81e29f390778ff783e625c5c92d1c87d370863059e23deea68ff2373e608c642
```

The delta receipt reports only the declared change:

```text
descendant_count_delta = +2
added_reachable_descendants = [Y, Z]
removed_reachable_descendants = []
```

Delta digest:

```text
sha256:6dca2f97fb26b9ff8d1407f1efbdc152dd1100329019e541ae90ddc6bc604705
```

No `value`, `merit`, `price`, `score`, `rank`, or human-worth field is emitted.

## Structural counterfactual

`CONTRIBUTION-FIELD-001` reuses existing public `ablate@1` rather than creating a second graph-intervention engine.

The contribution layer targets one event node and projects the underlying reachability receipt back to the Workmark root.

### Remove `X ENABLED Y`

Ablating `event:e-enable-y` removes root reachability to:

```text
Y
Z
```

Frozen contribution-layer receipt:

```text
sha256:178bea0744d813b8ab150397de8b53163e49de9ccdf6e9e125956ce637c605b3
```

This is a structural result in the supplied finite graph.

```text
ABLATION DELTA != ECONOMIC ENTITLEMENT
ABLATION DELTA != HISTORICAL NECESSITY
ABLATION DELTA != MORAL CREDIT
```

### Remove `B REPAIRED X`

Ablating `event:e-repair-x` changes graph reachability involving `B` and the removed event, but loses no reachability from the Workmark root `X` to `Y` or `Z`.

Frozen contribution-layer receipt:

```text
sha256:29ba0deb7cbcdfa092817a275fc1cbfa6c9cc1247c56e677a48ca9ef32d5b7e6
```

The zero root-reachability delta is deliberately not interpreted as zero contribution, zero importance, or zero merit.

```text
ZERO DECLARED MEASURE != ZERO CONTRIBUTION
```

## Hostile controls

The landed tests preserve these boundaries:

1. **Birth rewrite** — changing the original birth evidence while retaining the event id is rejected.
2. **Undeclared relation** — a relation such as `VALUED_AT_9000` cannot enter unless explicitly declared, and this specimen declares no valuation relation.
3. **Semantic field smuggling** — adding an undeclared event field such as `value` fails exact-shape validation.
4. **Incomplete evidence promotion** — an `incomplete` event remains residue and does not become a graph edge.
5. **Invalid evidence promotion** — an `invalid` event remains residue and does not become a graph edge.
6. **Relation-kind collapse** — erasing `CREATED` versus `REVIEWED` exposes a lost distinction through `ANTI-COLLAPSE-REACHABILITY-001`.
7. **Reachability laundering** — graph reachability is never promoted to historical causation.
8. **Ablation laundering** — a large or zero ablation delta receives no merit/value semantics.
9. **Person scoring** — the module exposes no person-ranking, contribution-pricing, or reputation-award surface.
10. **Narrative laundering** — downstream story text has no route to write source history by narration alone.

## Full Measure handoff

The frozen fixture includes one inert downstream packet for a future **Full Measure — World Layer** adapter.

It contains only references to the frozen Dogram Workmark/measurement/delta receipts plus an explicit authority boundary:

```text
source = Dogram
authority = none

allowed use:
  read-only story proposal input
  read-only quest proposal input
  read-only participation-opening input

forbidden promotion:
  source fact by narration
  economic value
  human worth
  sheet-changing authority
```

This repository does not implement that Full Measure adapter.

```text
DOGRAM RECEIPT -> FULL MEASURE STORY PROPOSAL
FULL MEASURE STORY PROPOSAL -X-> SOURCE FACT
```

If a Full Measure story later helps cause a real human action, that action must pass through the relevant owner-local witness/authority path. Only a resulting attributable source receipt may enter a later contribution-field cut.

## Economic-lens horizon

The specimen intentionally leaves economics downstream:

```text
CONTRIBUTION FIELD
        ↓
DOGRAM MEASUREMENT RECEIPTS
        ↓
DECLARED LENS A -> optional dividend proposal
DECLARED LENS B -> optional bounty proposal
DECLARED LENS C -> optional stewardship view
DECLARED LENS D -> no economic interpretation
```

A future lens may choose to consume Dogram measurements, but the lens must declare its assumptions and remain attributable as a separate object.

```text
SAME HISTORY != SAME VALUATION
VALUATION POLICY != HISTORY
VALUATION OUTPUT != DOGRAM RECEIPT
```

No global social-credit score is introduced here.

## Frozen fixture

The complete machine-readable specimen is:

```text
tests/fixtures/contribution_field_001.json
```

The fixture freezes:

- immutable Workmark birth;
- `t0` and `t1` measurement receipts;
- the cross-cut delta;
- `e-enable-y` ablation;
- `e-repair-x` ablation;
- inert Full Measure handoff references.

Exact regeneration is required by `tests/test_contribution_field_fixture.py`.

## Non-goals

This specimen does not provide:

- a new public Dogram operator;
- cryptocurrency or blockchain integration;
- NFT ownership semantics;
- exchange rates or token prices;
- universal reputation;
- a person score or ranking;
- automated compensation or royalties;
- causal inference;
- historical truth adjudication;
- legal ownership or intellectual-property adjudication;
- a universal ontology of human activity;
- Full Measure runtime integration;
- narrative authority.

## Result

Within the frozen finite specimen, one Workmark preserves the same immutable birth while later attributable supplied events change the typed graph around it. Dogram receipts that change, preserves typed distinctions and source-status residue, and calculates an event-node ablation counterfactual without emitting a valuation or person judgment.

That is enough to establish the first executable floor for the larger contribution-history idea without turning Dogram into the economy that may someday consume it.

## Working seal

> **WORK MINES THE MARKER. TIME ASSAYS THE ORE.**

> **DOGRAM MEASURES THE FIELD. FULL MEASURE TELLS THE PLAYABLE STORY.**
