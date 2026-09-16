# CONTRIBUTION-FIELD-001 — Contribution History as a Dogram Field

**Status:** design / future shaper / no runtime promotion

**Date:** 2026-09-16

## Purpose

`CONTRIBUTION-FIELD-001` explores one narrow architectural claim:

> Attributable contribution history can be represented as a typed, time-addressed graph that Dogram may measure without deciding what the graph means, what a contributor is worth, or what any economic reward should be.

The long-horizon intent is to support creative participation across code, music, research, teaching, repair, maintenance, physical places, community infrastructure, and other domains without collapsing them into one universal score.

The first proving ground is deliberately smaller: a finite synthetic contribution field with one immutable Workmark birth record, later attributable history, and neutral Dogram measurements across two cuts.

The design also defines a downstream boundary for **Full Measure — World Layer**:

> Dogram computes the contribution field. Full Measure may turn receipted measurements into playable story, participation openings, quests, chronicles, and character/world texture without manufacturing graph facts or rewriting contribution history.

## Constitutional laws

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
STORY != SOURCE
NARRATION != WITNESS
PLAYABILITY != AUTHORITY
```

Dogram's existing contract remains controlling:

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

## Why Dogram

Dogram already owns deterministic graph calculation and explicit receipts. Its current research floor includes bounded ancestry and information-loss machinery:

- `LINEAGE-SPINE-001` — fixed-shape multi-generation ancestry;
- `LINEAGE-BRAID-001` — attributable multi-parent convergence;
- `LINEAGE-WEAVE-001` — typed composition without erasing relation kind;
- `ANTI-COLLAPSE-REACHABILITY-001` — explicit measurement of distinctions lost under a declared projection;
- public `ablate@1` and `reach@1` operators — finite reachability change under declared graph intervention.

`CONTRIBUTION-FIELD-001` should reuse those laws and patterns rather than create a parallel social/economic graph engine.

It does **not** promote the contribution vocabulary below into a universal ontology and does **not** make Dogram the canonical owner of human identity, reputation, economics, social meaning, or historical truth.

## Core model

At a declared cut `t`, a contribution field is a finite typed graph:

```text
G_t = (V_t, E_t, type, receipts)
```

where every included vertex or edge must be attributable to supplied evidence at that cut.

### Candidate vertex kinds

The first specimen may declare only the kinds it actually needs. The broader vocabulary is a future-facing specimen language, not canon:

```text
PERSON
AGENT
COLLECTIVE
CONTRIBUTION
ARTIFACT
PROJECT
PLACE
IDEA
RESOURCE
WORKMARK
```

### Candidate edge kinds

Likewise, relation names are declared locally by a specimen:

```text
CREATED
REPAIRED
TAUGHT
ENABLED
CARRIED
MAINTAINED
REVIEWED
CHALLENGED
SUPERSEDED
INSPIRED
USED
DEPENDS_ON
WITNESSED_BY
```

A specimen must not infer an edge merely because the relation would make a coherent story.

```text
PLAUSIBLE RELATION != DECLARED EDGE
NARRATIVE COHERENCE != GRAPH EVIDENCE
```

## Event and cut discipline

Contribution history is time-addressed rather than stored as one mutable present-tense object.

Each event admitted to the specimen must carry enough supplied identity to distinguish at minimum:

```text
event_id
relation_kind
source_ref
subject_ref
evidence_ref
available_from
```

Additional owner-local coordinates may be present, but Dogram does not invent missing chronology.

For two cuts `t0 < t1`:

```text
G_t0 = attributable graph visible at t0
G_t1 = attributable graph visible at t1
```

Later events may enlarge, challenge, supersede, or connect the neighborhood around an older contribution without mutating that contribution's birth event.

```text
LATER HISTORY MAY ENRICH THE NEIGHBORHOOD
LATER HISTORY MAY NOT REWRITE THE BIRTH RECEIPT
```

## Workmark

A Workmark is not a score, balance, currency unit, title, or authority token.

Conceptually:

```text
W = {
  workmark_id,
  contribution_root,
  birth_cut,
  birth_receipt_ref,
  graph_address
}
```

Its durable function is to provide a stable address back to one attributable contribution origin.

A Workmark must not contain an issuer-controlled scalar `value` field in the first design.

```text
WORKMARK != SCORE
WORKMARK != MONEY
WORKMARK != AUTHORITY
WORKMARK != OWNERSHIP OF THE UNDERLYING WORK
```

The first specimen should treat the Workmark as immutable birth metadata plus references. Any later description of its state must be derived from later receipts, not written back into the origin.

## Executable Workmark horizon (`xWM`)

`xWM` is a future horizon, not required for the first implementation.

An executable Workmark would be a Workmark plus a bounded, versioned recipe for re-evaluating declared graph measurements against a supplied present cut:

```text
xWM
  -> resolve immutable birth receipt
  -> accept declared present contribution field
  -> verify the birth root is represented lawfully
  -> execute allowlisted Dogram measurements
  -> emit a fresh measurement receipt
```

The executable recipe may calculate. It may not mint value, authority, reputation, payment, or narrative canon.

```text
EXECUTABLE QUERY != EXECUTABLE CLAIM
```

## Dogram measurement layer

For one Workmark `W` at cut `t`, Dogram may calculate a declared measurement vector:

```text
M_t(W) = {
  lineage_depth,
  descendant_count,
  independent_reuse_count,
  branch_diversity,
  maintenance_events,
  repair_events,
  challenge_events,
  supersession_events,
  surviving_paths,
  rooted_dependencies,
  counterfactual_reachability_delta
}
```

The first executable specimen should implement only the smallest subset necessary to prove the architecture. The complete list above is a horizon, not a v0 requirement.

Every measure must declare:

1. the exact finite graph it consumed;
2. the exact Workmark/root it measured;
3. the cut at which it was evaluated;
4. the algorithm/operator version;
5. the result;
6. any incomplete or invalid lineage encountered.

No Dogram measurement may emit `good`, `valuable`, `deserving`, `trusted`, `important`, or equivalent semantic grades.

## Counterfactual structural contribution

Existing Dogram ablation gives a useful neutral question:

> Under this finite declared model, what reachability changes if this one declared contribution node or edge is removed?

This produces a structural delta only.

```text
ABLATION DELTA != ECONOMIC ENTITLEMENT
ABLATION DELTA != HISTORICAL NECESSITY
ABLATION DELTA != MORAL CREDIT
```

A large delta may be consumed by a later declared valuation policy, but Dogram does not perform that policy step.

## Economic-lens boundary

The contribution field is intended to permit many optional economic or reputation interpretations without embedding one into history.

Conceptually:

```text
CONTRIBUTION FIELD
        ↓
DOGRAM MEASUREMENT RECEIPTS
        ↓
DECLARED LENS A -> optional dividend proposal
DECLARED LENS B -> optional bounty eligibility proposal
DECLARED LENS C -> optional stewardship/reputation view
DECLARED LENS D -> no economic interpretation
```

A lens must remain attributable and explicit about which Dogram measurements it consumes and what additional assumptions it introduces.

The same field may lawfully support conflicting lenses.

```text
SAME HISTORY != SAME VALUATION
VALUATION POLICY != HISTORY
VALUATION OUTPUT != DOGRAM RECEIPT
```

No universal scalar social-credit score is part of this design.

## Full Measure story-layer handoff

Full Measure is the playable world layer. It already distinguishes attributable events from narrative garments: models may propose quests or narrate chronicles, but they may not manufacture witness, Deeds, truth, or memory.

`CONTRIBUTION-FIELD-001` should enter Full Measure through a read-only adapter/reference seam, not by merging runtimes.

### Handoff direction

```text
source-domain receipts
        ↓
contribution-field specimen
        ↓
Dogram measurements + delta receipt
        ↓
Full Measure adapter
        ↓
playable projection / chronicle / quest proposal / participation opening
        ↓
existing Full Measure authority + witness boundaries
```

The handoff is one-way with respect to graph fact creation:

```text
FULL MEASURE STORY MAY READ DOGRAM RECEIPTS
FULL MEASURE STORY MAY NOT WRITE DOGRAM HISTORY BY NARRATION ALONE
```

A Full Measure action may later become a new source event only if the relevant owner produces an attributable event/receipt through its existing authority path. That new receipt may then enter a later contribution-field cut like any other supplied evidence.

### Full Measure import declaration

To satisfy Full Measure's existing Project Weave rule, the eventual adapter must declare:

1. **source project + source version** — exact Dogram version/SHA and contribution-field receipt version;
2. **objects read** — Workmark birth refs, declared contribution-field receipt, declared Dogram measurement receipts;
3. **objects proposed** — Full Measure-local chronicle entries, quest hooks, participation openings, or other explicitly proposed story projections;
4. **authority required to accept** — existing Full Measure/Jubilee human witness and world authority for any sheet-changing Deed, Harvest, Capacity, constituted position, or equivalent state;
5. **receipts emitted** — Full Measure-local story/proposal receipt referencing the exact Dogram inputs it used;
6. **forbidden reads** — hidden graph nodes, private/held material not present in the supplied receipts, unrelated repository state, and any source data outside the declared adapter scope.

### Story-law boundary

Full Measure may say:

> This contribution has acquired seven later carried descendants in the declared field, and here is a quest opening around one unresolved branch.

It may not say merely from Dogram structure:

> This contributor is seven times more valuable.

Nor may a generated campaign recap turn an inferred relation into a historical edge.

```text
MEASUREMENT -> STORY PROPOSAL
STORY PROPOSAL -X-> SOURCE FACT
```

## Creative-participation horizon

The architecture should remain capable of receiving future evidence adapters for domains beyond Git/code, including:

```text
music and arrangement lineage
writing and visual art
research and falsification
review and documentation
maintenance and repair
teaching and mentorship
volunteer and community work
physical tools and infrastructure
gardens, venues, workshops, and other places
```

These domains must not be forced into fake precision.

Each adapter owns its evidence profile. Examples may include exact diffs, before/after measurements, human witness, instrument readings, source citations, declared reuse, or owner-specific receipts.

```text
COMMON GRAPH GRAMMAR != COMMON EVIDENCE STRENGTH
```

## Privacy and participation boundary

The future system must permit contribution evidence to remain local, private, held, pseudonymous, or unpublished according to the owning domain's rules.

A Workmark is not required to be public merely because it exists.

No downstream graph calculation receives hidden material unless an owning authority explicitly supplies it to the bounded occurrence.

```text
EXISTS != DISCLOSED
DISCLOSED != PUBLIC
PUBLIC != AGGREGATION CONSENT
```

## Hostile matrix

Any implementation plan derived from this design must preserve at least the following hostile cases.

### 1. Centrality laundering

A highly connected node is supplied.

Expected: Dogram may calculate centrality-like structure if explicitly requested, but no `value`, `merit`, or reward conclusion is emitted.

### 2. Edge-count gaming

One contribution is surrounded by many low-substance declared edges while another has one deep dependency relation.

Expected: the graph remains as supplied; no edge-count-to-value shortcut exists.

### 3. Birth rewrite

A later event attempts to alter the original Workmark birth contribution or birth cut.

Expected: refuse or classify invalid. Later history must be appended/related, not rewritten into origin.

### 4. Narrative laundering

A Full Measure chronicle proposes a relation absent from Dogram/source receipts, then attempts to feed the prose back as established graph history.

Expected: narration alone is insufficient evidence; no new graph edge is admitted.

### 5. Missing witness lineage

A descendant path references missing parent evidence.

Expected: preserve `incomplete`, not `complete` and not proven severance.

### 6. Relation-kind collapse

`REPAIRED`, `INSPIRED`, and `DEPENDS_ON` are projected into one generic `RELATED_TO` edge before a measure that depends on relation type.

Expected: anti-collapse receipt exposes lost distinctions; no silent equivalence.

### 7. Historical reachability laundering

A graph path exists between contribution A and artifact Z.

Expected: Dogram reports graph reachability only; it does not assert historical causation or occurrence.

### 8. Human-worth collapse

A caller requests one scalar ranking of people from contribution measurements.

Expected: out of scope for Dogram. No person-score operator is introduced by this design.

### 9. Private-material leakage

A downstream Full Measure story request attempts to traverse source material not included in the declared Dogram handoff.

Expected: unavailable/forbidden remains unavailable; story generation cannot widen the read boundary.

### 10. Self-minted value

A contributor supplies their own contribution and a claimed value/importance field.

Expected: contribution evidence and claimed interpretation remain separate. Dogram may receipt supplied structure but cannot promote the self-valuation into measurement fact.

## First falsifiable specimen

The first executable follow-up should remain synthetic and finite.

Declared history:

```text
A CREATED X
B REPAIRED X
X ENABLED Y
C CHALLENGED part_of_X
Y CARRIED part_of_X forward
```

At birth cut `t0`:

```text
A CREATED X
W_X minted as immutable address to X's contribution birth
```

At later cut `t1`:

```text
B REPAIRED X
X ENABLED Y
C CHALLENGED part_of_X
Y CARRIED part_of_X forward
```

The specimen must prove:

1. `W_X` has identical birth identity at `t0` and `t1`;
2. the attributable neighborhood around `W_X` differs between cuts;
3. a declared measurement vector changes accordingly;
4. Dogram emits the delta and retains both cut receipts;
5. removing or changing one declared relation produces an explicit structural difference;
6. no result contains value, merit, price, authority, human-worth, or historical-causation semantics;
7. one Full Measure fixture adapter can consume the neutral receipt and produce only a proposed story/quest projection, with no sheet-changing authority.

## Minimal first measurement set

To prevent scope explosion, the first implementation should likely prove only:

```text
descendant_count
relation_kind_counts
reachable_descendant_set
ablation_reachability_delta
```

These are sufficient to demonstrate historical enrichment, typed relation preservation, and counterfactual structure without inventing a generalized reputation engine.

## Receipt shape — design intent only

The first implementation may define an internal experimental receipt resembling:

```text
{
  "schema": "dogram.contribution-field-receipt/v0-experimental",
  "authority": "none",
  "workmark_ref": "...",
  "cut": "t1",
  "field_digest": "...",
  "measurement_version": "...",
  "measurements": {...},
  "incomplete": [...],
  "source_receipts": [...]
}
```

This is a design sketch, not a promoted schema. Exact field names belong to implementation review.

## Non-goals

`CONTRIBUTION-FIELD-001` does not initially provide:

- cryptocurrency, blockchain, NFT, or smart-contract integration;
- exchange rates or token prices;
- universal reputation;
- a global social-credit score;
- contributor ranking;
- automated compensation;
- automatic royalty allocation;
- legal ownership determination;
- intellectual-property adjudication;
- taxation or securities treatment;
- identity verification;
- public-by-default contribution history;
- automatic causal inference;
- semantic equivalence between contribution domains;
- automatic Full Measure canon promotion;
- a universal ontology of human activity.

## Owner boundaries

### Dogram owns

- deterministic graph calculations over supplied finite contribution specimens;
- typed relation preservation within the declared specimen;
- measurement and delta receipts;
- incomplete/invalid lineage signaling;
- neutral ablation/reachability calculations.

### Dogram does not own

- whether the supplied event is historically true;
- who deserves credit;
- economic valuation;
- social reputation;
- compensation;
- human worth;
- narrative canon;
- Full Measure world authority.

### Full Measure owns

- playable projection of accepted inputs;
- local story/quest/participation proposals;
- existing world-layer authority and witness membranes;
- human-facing chronicles and campaign texture.

### Full Measure does not gain

- authority to rewrite Dogram receipts;
- authority to mint source evidence through narration;
- hidden access to contribution fields;
- economic valuation authority merely because a measurement became playable.

## Success criteria for the future shaper

The design has succeeded if a later implementation can show all of the following without widening authority:

1. one contribution has a stable immutable Workmark birth;
2. later attributable events enlarge or modify its measured neighborhood;
3. Dogram can compare two cuts and show the delta;
4. typed relation distinctions survive unless an explicit projection collapses them;
5. missing evidence remains incomplete rather than invented;
6. ablation produces a neutral structural difference only;
7. Full Measure can consume the receipt as story input without converting it into source truth;
8. no scalar person score or implicit economic policy appears anywhere in the Dogram output.

## Future horizons after the first proof

Only after the first specimen survives hostile pressure should follow-on work consider:

- executable Workmarks (`xWM`);
- additional measurement families;
- multiple independent contribution domains;
- declared valuation-lens protocols outside Dogram;
- retroactive reward experiments;
- commons-dividend allocation experiments;
- sponsorship/bounty attachment to unresolved Workmarks;
- place-centered contribution fields;
- privacy-preserving/pseudonymous Workmark views;
- Full Measure campaign surfaces that reveal contribution ancestry as living world history.

Each horizon requires its own owner-local design gate.

## Compression

> **THE GRAPH PRESERVES CONTRIBUTION HISTORY. IT DOES NOT PRICE THE CONTRIBUTOR.**

> **WORK MINES THE MARKER. TIME ASSAYS THE ORE.**

> **DOGRAM MEASURES THE FIELD. FULL MEASURE TELLS THE PLAYABLE STORY.**
