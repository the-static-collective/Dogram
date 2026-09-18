# Residual Topology — Route / Field Pressure

**Date:** 2026-08-28  
**Status:** RESEARCH SLICE / FUTURE OPERATOR CANDIDATE / NO RUNTIME CHANGE  
**Repository:** `the-static-collective/Dogram`  
**Companion frontier:** Far-Side Simplicity mathal harvest (Dogram PR #2)  

> **THE PATH YOU TAKE IS NOT THE TOPOLOGY YOU HAD.**

> **SELECTED ROUTE != AVAILABLE FIELD.**

---

## 0. Scope decision

This slice extracts a general graph-theoretic primitive from the eight-verb / cube H0 without requiring that H0 to be true.

The H0 may fail completely and this primitive may still survive.

The core distinction is:

```text
HOST / AVAILABLE TOPOLOGY
!=
SELECTED ROUTE
!=
TRAVERSED HISTORY
!=
RESIDUAL TOPOLOGY
```

Dogram's role is only to calculate declared graph differences and preserve a receipt.

This document does **not**:

```text
add a fifth Dogram operator
change dogram.specimen/v0
change dogram.receipt/v0
change directed-graph v0 semantics
change ALEX
change 3rdi / HEARTSEE
change eCODE
claim counterfactual truth
claim every untraversed edge was visible to an observer
claim every graph edge was historically available
```

The graph supplied to Dogram is a declared calculation specimen. Another owner must establish what that graph represents.

---

# 1. The primitive

Let:

```math
G = (V,E_G)
```

be a declared host graph and:

```math
H = (V,E_H)
```

be a declared spanning route/subgraph with:

```math
E_H \subseteq E_G.
```

Define the residual edge field:

```math
R_G(H) = (V, E_G \setminus E_H).
```

For short:

```text
R = G \ H
```

where subtraction means **edge-set subtraction over the same declared vertex set**, not deletion of route vertices.

## EXACT

The edge sets partition the host:

```math
E_G = E_H \sqcup E_R.
```

Therefore:

```math
|E_G| = |E_H| + |E_R|.
```

and the pair:

```text
ROUTE + RESIDUAL
```

is sufficient to reconstruct the host edge set when both are receipted against the same vertex identities.

## KEEPER

```text
HISTORY-SHAPED ROUTE
+
UNCONSUMED DECLARED STRUCTURE
=
HOST TOPOLOGY
```

This is a graph identity only. It does not establish that every residual edge was visible, actionable, causal, permitted, or historically contemplated.

---

# 2. Regular-host residual law

Assume now that `G` is a finite simple undirected `k`-regular graph:

```math
\deg_G(v)=k
```

for every vertex `v`.

Assume `H` is a spanning `r`-regular subgraph:

```math
\deg_H(v)=r
```

for every vertex `v`.

Because route and residual edge sets are disjoint and partition the incident host edges:

```math
\deg_G(v)=\deg_H(v)+\deg_R(v).
```

Therefore:

```math
\deg_R(v)=k-r.
```

for every vertex.

## THEOREM

```text
k-REGULAR HOST
-
r-REGULAR SPANNING ROUTE
=
(k-r)-REGULAR RESIDUAL.
```

This is the general mathematical lesson extracted from the cube H0.

It does not depend on:

- eight verbs;
- a cube;
- cups;
- HEARTSEE;
- ternary arithmetic;
- any particular semantic labels.

---

# 3. Cubic host + Hamiltonian cycle

A Hamiltonian cycle on a finite graph visits every vertex exactly once and returns to its starting vertex.

As a spanning subgraph, a Hamiltonian cycle is 2-regular:

```math
\deg_H(v)=2.
```

If the host is cubic / 3-regular:

```math
\deg_G(v)=3,
```

then the residual law gives:

```math
\deg_R(v)=3-2=1.
```

So the residual is 1-regular.

A finite 1-regular graph is a disjoint union of edges covering every vertex exactly once: a **perfect matching / 1-factor**.

## EXACT

```text
CUBIC HOST
-
HAMILTONIAN CYCLE
=
PERFECT MATCHING.
```

If the host has `n` vertices, then the matching contains:

```math
n/2
```

edges.

For an eight-vertex cubic host:

```math
|E_G| = 3*8/2 = 12
```

while a Hamiltonian cycle uses:

```math
|E_H| = 8.
```

Therefore:

```math
|E_R| = 12-8=4.
```

So the exact receipt is:

```text
8 stations
12 host edges
8 route edges
4 residual edges
1 residual edge incident to each station.
```

## IMPORTANT

This result holds for **any cubic graph with a Hamiltonian cycle**.

It is not a special property of `Q3`.

That generalization is precisely why the primitive is more durable than the original eight-verb cube H0.

---

# 4. Path versus round

A Hamiltonian path also visits every vertex once, but it does not close.

Its two endpoints have route degree one:

```math
\deg_H(v_{start})=\deg_H(v_{end})=1,
```

while every internal vertex has route degree two:

```math
\deg_H(v)=2.
```

For a cubic host:

```text
internal residual degree = 3 - 2 = 1
endpoint residual degree = 3 - 1 = 2.
```

So the residual aperture profile of a Hamiltonian path in a cubic host is:

```text
2, 1, 1, ..., 1, 2
```

up to vertex ordering.

If an unused host edge joins the two endpoints and is declared as the closure edge, adding it to the route produces a Hamiltonian cycle.

That closure consumes one residual incident edge at each endpoint:

```text
endpoint residual: 2 -> 1
endpoint residual: 2 -> 1
internal residuals: remain 1.
```

The resulting residual field becomes uniformly 1-regular.

## KEEPER

Under the stated conditions:

> **CLOSING THE SPANNING PATH INTO A ROUND EQUALIZES THE RESIDUAL DEGREE BUDGET.**

## REFUSAL

Do not generalize this sentence without its conditions.

It depends on:

```text
cubic host
spanning Hamiltonian path
an available host edge joining the path endpoints
closure by exactly that edge.
```

A generic path, generic host, or generic closure need not produce uniform residual degree.

---

# 5. Route totalization and counterfactual reification

The graph mathematics suggests two symmetric downstream epistemic failures.

They are **not Dogram predicates**.

They are recorded here because the calculation can supply pressure specimens for another owner.

## Failure A — route totalization

```text
Observed / selected route:
A -> B

invalid promotion:
therefore A -> B was the only available route.
```

Graphically:

```text
E_H
mistaken for
E_G.
```

Non-collapse:

```text
SELECTED ROUTE != AVAILABLE FIELD.
```

## Failure B — untraversed-as-history

```text
Declared residual edge:
A -- C

invalid promotion:
therefore A -> C occurred.
```

Graphically:

```text
E_R
mistaken for
historical E_H.
```

Non-collapse:

```text
UNTRAVERSED OPENING != HISTORICAL EVENT.
```

## Downstream ALEX candidate vocabulary

ALEX may eventually choose to pressure claims like:

```text
ROUTE-TOTALIZATION-001
UNTRAVERSED-AS-HISTORY-001
```

but this Dogram slice does not add those Crucibles or assert that the names are final.

Dogram can calculate the route/residual distinction. ALEX or another provenance owner decides what claims are supportable.

---

# 6. Availability requires an owner

The word `available` is dangerous if left untyped.

A host edge may be:

```text
present in the supplied graph
visible to an observer
known at a cut
legally permitted
physically traversable
selected
traversed
historically realized
```

These are not equivalent.

Therefore Dogram should treat the host graph as:

```text
DECLARED HOST GRAPH
```

not automatically as:

```text
THE TRUE POSSIBILITY SPACE.
```

A future receipt should say what it calculated:

```text
residual relative to supplied host
```

and not:

```text
all paths that really could have happened.
```

3rdi may be a natural upstream owner for observer-local visible openings. ALEX may be a natural owner for attributable formation/support claims. eCODE or another world may own actual constituted transitions.

Dogram owns none of those semantics.

---

# 7. The residual is structured, not merely "everything else"

The residual field may have graph structure worth calculating independently of its interpretation.

Useful structural questions include:

```text
How many residual edges remain?
What is the residual degree sequence?
Is the residual regular?
How many connected components does it have?
Is it a matching?
Is it a perfect matching?
Does it contain cycles?
What is its component-size multiset?
Does removing the route disconnect the residual?
Does route replacement change residual structure?
```

None of these questions require Dogram to decide what the residual means.

This is the key reason a future operator may be justified.

---

# 8. Future Dogram operator candidate — `residual`

This section is a design candidate only.

Provisional conceptual signature:

```text
RESIDUAL(host_graph, route_subgraph)
    -> residual_graph + structural receipt
```

or:

```math
RESIDUAL(G,H) -> (R, receipt).
```

## Candidate calculation outputs

A minimal future receipt could calculate:

```text
host_vertex_count
host_edge_count
route_edge_count
residual_edge_count

host_degree_signature
route_degree_signature
residual_degree_signature

route_is_spanning
route_is_cycle
route_is_path
residual_is_regular
residual_regular_degree
residual_component_sizes
residual_is_matching
residual_is_perfect_matching
```

Optional later additions should require separate earning:

```text
cycle basis
cut sets
matching enumeration
spectral values
weighted residuals
hypergraph residuals
probabilities
semantic edge classes
```

The first operator should remain small.

## Candidate refusal conditions

```text
ROUTE_EDGE_NOT_IN_HOST
VERTEX_SET_MISMATCH
DUPLICATE_EDGE
GRAPH_KIND_UNDECLARED
DIRECTEDNESS_MISMATCH
MALFORMED_ROUTE
UNSUPPORTED_MULTI_EDGE
```

No silent correction.

---

# 9. Important v0 compatibility issue: Dogram graphs are directed

Current Dogram v0 graph specimens are deliberately directed.

The clean regular-host theorem above was stated for finite simple undirected graphs.

That mismatch must not be silently erased.

There are at least three possible future approaches.

## Approach A — paired arcs

Represent each undirected edge `{u,v}` as:

```text
u -> v
v -> u.
```

Then undirected degree corresponds to both in-degree and out-degree under a symmetric-arc invariant.

Advantage:

```text
no new graph kind required immediately.
```

Cost:

```text
receipts become less natural and must verify symmetry.
```

## Approach B — admit explicit graph kind

A future schema/operator revision could distinguish:

```text
directed
undirected
```

Advantage:

```text
clean semantics.
```

Cost:

```text
public schema change; requires independent design approval.
```

## Approach C — research-only precomputation

Keep runtime untouched and express residual examples as externally calculated fixtures / boundary traces for existing Dogram `delta` pressure.

Advantage:

```text
no runtime change.
```

Cost:

```text
Dogram does not itself verify the graph theorem.
```

## Current decision

This slice chooses none of these yet.

The directed/undirected mismatch is a **promotion gate**, not an implementation detail to hide.

---

# 10. Directed generalization

For completeness, there is a simple directed analogue if host and route share the same vertex set and route arcs are a subset of host arcs.

For every vertex:

```math
\deg_R^+(v)=\deg_G^+(v)-\deg_H^+(v)
```

and:

```math
\deg_R^-(v)=\deg_G^-(v)-\deg_H^-(v).
```

Thus a directed host with uniform in/out degree and a spanning route with uniform in/out degree has a residual with the coordinate-wise degree differences.

This does **not** make the undirected perfect-matching theorem automatically applicable.

Matching language should remain tied to an explicitly undirected or symmetrically interpreted specimen.

---

# 11. Smallest positive Dogram specimen

The smallest useful pressure specimen should remove all metaphor.

Use an eight-vertex cubic host with a declared Hamiltonian cycle.

For example, the 3-cube may be supplied simply because it is compact, not because the eight procedural verbs are assumed to map onto it.

Declared host:

```text
V = {000,001,010,011,100,101,110,111}
```

with edges joining bitstrings at Hamming distance one.

This gives:

```text
8 vertices
12 undirected edges
3 host edges per vertex.
```

Choose one declared Hamiltonian cycle, for example:

```text
000
001
011
010
110
111
101
100
000
```

Each adjacent pair differs in one bit, including the final closure `100 -> 000`.

Expected structural receipt:

```text
host edges:      12
route edges:      8
residual edges:   4
residual degrees: [1,1,1,1,1,1,1,1]
perfect matching: true
```

The labels may then be randomized.

The same receipt should remain invariant under vertex renaming.

---

# 12. Path sibling

Remove the final closure edge from the same cycle.

The route becomes a Hamiltonian path with seven route edges.

Expected residual count:

```math
12-7=5.
```

Expected residual degree multiset in the cubic host:

```text
{2,2,1,1,1,1,1,1}
```

because the two path endpoints each retain two unused host edges while every internal vertex retains one.

Then re-add the closure edge.

Expected delta:

```text
route edge count:       +1
residual edge count:    -1
endpoint residual deg:  2 -> 1
endpoint residual deg:  2 -> 1
regularity:             false -> true
perfect matching:       false -> true
```

This is the clean calculational witness for the round/closure distinction.

---

# 13. Host-degree sibling

Use a 4-regular host with a spanning Hamiltonian cycle.

Then:

```math
\deg_R(v)=4-2=2.
```

The residual is 2-regular, hence a disjoint union of cycles.

Expected pressure result:

```text
ONE RESIDUAL OPENING PER STATION
```

fails.

But the general law:

```text
residual degree = host degree - route degree
```

survives.

This is a crucial hostile control because it separates the cubic-specific consequence from the general primitive.

---

# 14. Nonspanning-route sibling

Supply a route that does not visit every host vertex.

Even if the host is cubic and the visited portion locally uses two route edges at some vertices, unvisited vertices retain all three host edges.

The residual degree field will not be uniformly one.

Expected conclusion:

```text
spanning condition matters.
```

Dogram should report the structural failure, not repair the route or infer a missing traversal.

---

# 15. Label-shuffle control

The original H0 used meaningful procedural names:

```text
PEEL
SLICE
SMASH
JAR
EAT
PLANT
HARVEST
REPEAT
```

For a pure graph receipt, those names must be non-operative.

Rename vertices arbitrarily:

```text
BANANA
CLOUD
SEVEN
DOG
WINDOW
Q
RIVER
SPORK
```

while preserving graph incidence and route correspondence.

Expected result:

```text
same unlabeled structural receipt.
```

If the calculation changes merely because semantic labels change, Dogram has accidentally imported meaning into a topology operator.

## KEEPER

```text
STRUCTURE SURVIVES LABEL REMOVAL.
```

---

# 16. Route-swap control

A single host may contain multiple Hamiltonian cycles.

For each cycle `H_i`, calculate:

```math
R_i = G \ H_i.
```

In a cubic host every `R_i` must still be a perfect matching.

But the identity of the matched pairs may differ.

This exposes a useful two-level distinction:

```text
INVARIANT:
residual is a perfect matching

VARIANT:
which vertices are paired.
```

That is exactly the kind of distinction Dogram should make visible without interpreting.

A downstream owner may then ask whether the pairing identity matters.

---

# 17. Residual as a complement of commitment

There is a useful structural symmetry with the recent SMASH work.

SMASH-like construction asks:

```text
Given carriers and declared relations,
what whole is generated?
```

Residual pressure asks:

```text
Given a declared host and consumed route,
what structure remains unconsumed?
```

Conceptually:

```text
CONSTRUCTION:
relations -> whole

SUBTRACTION:
host - route -> residual.
```

Do not promote these into inverse operators.

They answer different questions.

A route may not contain enough information to reconstruct the host without the residual receipt.

A residual may not contain enough information to reconstruct the route without the host or route receipt.

But when all are properly identified:

```math
E_H \sqcup E_R = E_G.
```

That partition is exact.

---

# 18. Decision topology candidate

A downstream research owner may find the following bundle useful:

```text
HOST FIELD
SELECTED ROUTE
RESIDUAL FIELD
```

The combination can preserve more decision context than route history alone.

But Dogram must not rename this automatically as:

```text
DECISION TOPOLOGY
```

unless the owning domain has established that the host graph genuinely represented available options at the relevant cut.

Safe Dogram language:

```text
host graph
route subgraph
residual graph
```

Potential downstream language:

```text
available field
selected path
unselected openings
```

The second vocabulary requires provenance beyond graph arithmetic.

---

# 19. Observer-local pressure

Suppose two observers receive different lawful host projections:

```text
G_A
G_B.
```

The same historical route `H` may have different apparent residuals:

```math
R_A = G_A \ H
R_B = G_B \ H.
```

This is potentially useful for 3rdi / HEARTSEE research.

But Dogram should only calculate it when both host projections are supplied explicitly.

It must not infer visibility.

Potential pressure question:

> Does changing only observer-visible host edges change the residual receipt while leaving the route receipt fixed?

That would preserve:

```text
HISTORY FIXED
PROJECTION OF AVAILABLE FIELD CHANGED.
```

Again:

```text
projection difference != causal history difference.
```

---

# 20. Temporal pressure

A host field may also change with time.

Let:

```text
G_t0
G_t1
```

be declared topology snapshots and let the route prefix at each cut be:

```text
H_t0
H_t1.
```

Then:

```math
R_t = G_t \ H_t.
```

Dogram can compare residual structure across cuts if the snapshots are explicitly provided.

It must not treat later edges as historically available earlier.

This supplies a topology analogue of hindsight control:

```text
EDGE EXISTS LATER
!=
EDGE AVAILABLE AT EARLIER CUT.
```

That distinction belongs upstream in the specimen; Dogram merely preserves the calculation.

---

# 21. Candidate receipt shape — explicitly non-normative

If a future `residual` operator earns implementation, a local receipt might resemble:

```text
RESIDUAL_RECEIPT {
    host_ref
    route_ref
    graph_kind

    host_vertex_count
    host_edge_count
    route_edge_count
    residual_edge_count

    host_degree_signature
    route_degree_signature
    residual_degree_signature

    route_spanning
    route_shape

    residual_regular
    residual_regular_degree
    residual_component_sizes
    residual_matching
    residual_perfect_matching

    residual_edge_refs[]

    warnings[]
    residuals[]
}
```

No fields in this sketch are admitted into `dogram.receipt/v0` by this document.

The receipt should contain only calculational claims supported by the declared graph representation.

---

# 22. Potential implementation economy

Before adding `residual`, test whether existing Dogram operators can answer the bounded research questions cheaply enough.

Current tools include:

```text
delta
rectangle
ablate
reach
```

Possible lowering:

```text
ablate each route edge from a copy of host
then inspect remaining reachability / edge set
```

But v0 `ablate` removes one declared component at a time.

A route containing many edges would require repeated sequential specimens and external orchestration.

That creates three costs:

```text
batch identity is external
intermediate receipts are noisy
final residual structure is not a first-class calculated result.
```

So a future `residual` operator may earn itself if repeated experiments demonstrate that **edge-set complement itself** is the stable discriminator.

Until then:

```text
RESEARCH SLICE FIRST.
```

---

# 23. Hostile controls

A future implementation proposal should survive at least the following.

## 23.1 Route edge outside host

Input:

```text
H contains edge e not in G.
```

Expected:

```text
REFUSE / ROUTE_EDGE_NOT_IN_HOST.
```

No silent union.

## 23.2 Vertex mismatch

Route references a missing or extra vertex.

Expected:

```text
REFUSE / VERTEX_SET_MISMATCH
```

unless a future operator explicitly supports nonspanning routes with a declared common host vertex set.

The schema must distinguish:

```text
nonspanning route over same V
```

from:

```text
route defined over incompatible V.
```

## 23.3 Duplicate edges

Expected:

```text
canonicalize only if graph contract declares set semantics;
otherwise refuse malformed representation.
```

## 23.4 Directedness swap

Supply the same visual topology once as undirected edges and once as asymmetric directed arcs.

Expected:

```text
receipts differ or unsupported mode refuses.
```

Never silently pretend directed and undirected graphs are identical.

## 23.5 4-regular host

Expected:

```text
residual degree 2,
not perfect matching.
```

## 23.6 Hamiltonian path

Expected:

```text
endpoint residual degree k-1
internal residual degree k-2.
```

For cubic:

```text
2,2,1,1,...
```

## 23.7 Nonspanning route

Expected:

```text
unvisited vertices retain full host degree.
```

## 23.8 Vertex label permutation

Expected:

```text
structural invariants unchanged.
```

## 23.9 Route permutation

Reorder the same cycle starting point / orientation without changing its edge set.

Expected:

```text
same residual graph.
```

If route occurrence order is separately receipted for another purpose, edge residual must still depend on the route edge set, not presentation order.

## 23.10 Metaphor removal

Remove:

```text
cups
heart
eight verbs
Y
sacred-number language
```

Expected:

```text
all graph theorems remain unchanged.
```

---

# 24. What a failed eight-verb H0 would leave behind

Suppose no non-arbitrary mapping can ever be found between:

```text
PEEL -> SLICE -> SMASH -> JAR -> EAT -> PLANT -> HARVEST -> REPEAT
```

and any Hamiltonian cycle of `Q3`.

Then discard that mapping.

The following still survive independently:

```text
route != host
residual = host - route
regular host - regular spanning route = regular residual
cubic host - Hamiltonian cycle = perfect matching
path closure can equalize residual degree under stated conditions
route + residual reconstructs host edge set
```

This is the desired research behavior:

> **H0 MAY DIE WHILE ITS PRESSURE HARVEST SURVIVES.**

That is why this slice belongs in Dogram even before the original H0 is settled.

---

# 25. Possible ALEX harvest — downstream only

If the graph work survives and an ALEX owner later wants a research slice, the strongest non-collapse laws are probably:

```text
SELECTED ROUTE != AVAILABLE FIELD
UNTRAVERSED OPENING != HISTORICAL EVENT
OBSERVED HISTORY != EXHAUSTIVE POSSIBILITY CLAIM
```

Possible hostile questions:

```text
Did the claimant infer exclusivity from the path merely because only one path was traversed?

Did the claimant promote a residual edge into history merely because it existed in the declared field?

Was the host field actually attributable at the relevant historical cut?

Was the residual visible to the observer or only to a later custodian?
```

Dogram does not answer these semantic questions.

It can supply a stable calculation receipt for the graph distinction they depend on.

---

# 26. Possible HEARTSEE harvest — downstream only

If an observer-local host field has been independently established, a HEARTSEE-like projection might distinguish:

```text
incident residual edge exists
incident residual edge visible
incident residual edge selected as interesting
incident residual edge traversed
```

The residual operator itself should stop at the first line.

This preserves:

```text
EXISTS != VISIBLE != SELECTED != TRAVERSED.
```

Any ranking, interest, salience, or opening semantics remain outside Dogram.

---

# 27. Promotion gates for `residual`

Do not implement a new operator until all of the following are true:

```text
1. Repeated research specimens need edge-set residual directly.
2. Existing ablate/reach lowering is materially awkward or obscures the invariant.
3. Directed versus undirected graph semantics are explicitly resolved.
4. Host and route identity rules are precise.
5. Refusal behavior is specified for incompatible graphs.
6. At least one positive and four hostile fixtures are frozen.
7. Output remains purely calculational.
8. No availability / support / interest / authority semantics leak into Dogram.
```

If those are not earned, leave `RESIDUAL` as a research vocabulary term.

---

# 28. Minimal future TDD target

If the operator is later approved, the first executable target should be much smaller than the whole philosophical thread.

Positive fixture:

```text
cubic undirected host G
Hamiltonian cycle H
```

Expected:

```text
RESIDUAL(G,H)
-> 1-regular residual
-> perfect matching
```

Negative siblings:

```text
route edge outside host -> refuse
Hamiltonian path -> nonuniform residual degree in cubic host
4-regular host + Hamiltonian cycle -> 2-regular residual
label permutation -> same structural invariants
```

Nothing about PEEL, HEARTSEE, or eCODE is required for this first test.

---

# 29. Far-side compression

The whole insight can be compressed to four lines:

```text
FIELD
  = what the supplied graph contains

ROUTE
  = what the supplied traversal consumes

RESIDUAL
  = FIELD - ROUTE

RECEIPT
  = enough structure to keep those three from collapsing.
```

For the cubic-round specimen:

```text
3 openings per station
- 2 consumed by the round
= 1 residual opening per station.
```

That remaining opening is not automatically:

```text
visible
interesting
permitted
causal
historical
```

It is only present in the supplied residual graph until another owner earns more.

---

# Seal

```text
THE PATH TAKEN IS NOT THE TOPOLOGY SUPPLIED.
THE TOPOLOGY SUPPLIED IS NOT AUTOMATICALLY THE TRUE POSSIBILITY FIELD.
THE RESIDUAL IS STRUCTURE, NOT COUNTERFACTUAL HISTORY.
A CUBIC HOST MINUS A HAMILTONIAN ROUND LEAVES A PERFECT MATCHING.
A PATH LEAVES EXTRA APERTURE AT ITS ENDS; A LAWFUL CLOSURE CAN EQUALIZE THAT BUDGET.
ROUTE + RESIDUAL RECONSTRUCTS THE DECLARED HOST.
```

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

> **THE PATH YOU TAKE IS NOT THE TOPOLOGY YOU HAD.**
