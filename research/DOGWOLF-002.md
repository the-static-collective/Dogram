# DOGWOLF-002 — Phantom quotient-path lift

**Status:** bounded internal research specimen, stacked on DOGWOLF-001. **Authority:** none. **Public operators:** none. **Mandatory dependencies:** none.

## Distinct frontier

Dogram already studies one-step successor-class factorization (`SUCCESSOR-CLASS-QUOTIENT-001`), MAY/MUST aggregates (`MAY-UNION-QUOTIENT-001`), and representative-successor incidence (`SUCCESSOR-INCIDENCE-001`). DOGWOLF-002 does not reimplement these. It asks whether a **whole route in the existential/may quotient** can be lifted to a **single composable concrete state path** matching *every intermediate quotient class*.

Given declared finite states S, a quotient map q:S->Q, and a finite labeled transition relation E, a quotient edge (A,a,B) is present if some supplied concrete edge (s,a,t) has q(s)=A and q(t)=B. A quotient route may concatenate different representatives of an intermediate class. We call such a route **phantom** if no concrete path obeys all its classes and actions simultaneously. This is a bounded, structural non-liftability claim, **not** a statement that the abstract action-label word cannot be realized elsewhere.

## Frozen specimen

    p --enter--> q_in       q_out --exit--> r
    q(p)=P; q(q_in)=q(q_out)=Q; q(r)=R

The quotient has P --enter--> Q --exit--> R. The first edge requires arriving at q_in, whereas the second edge requires starting at q_out. No concrete two-step path realizes that exact quotient-class route. The receipt retains: the quotient class route; both distinct concrete edge witnesses; the actual concrete prefix (p,q_in); reachable-at-join set {q_in}; next-edge source set {q_out}; and the class Q where those sets do not intersect.

Adding q_in --exit--> r repairs this frozen route; an independent Wolfram calculation confirmed no concrete two-step lift before the repair and a lift afterward. Optional oracle: `wolframscript -file research/dogwolf_002.wl`.

## Implementation and replay

    python -m unittest tests.test_dogwolf_path_lift -v

    from dogram.dogwolf_path_lift import hunt_phantom_path
    r = hunt_phantom_path(
        states=("p", "q_in", "q_out", "r"),
        quotient=("P", "Q", "Q", "R"),
        transitions=(("p", "enter", "q_in"), ("q_out", "exit", "r")),
        max_depth=2,
        max_paths=4096,
    )
    assert r.status == "phantom_found"

Breadth-first search explores quotient-class/action routes from every quotient class in increasing route length; for each route, the kernel maintains the set of actually reachable concrete endpoints plus one prefix witness per endpoint. It checks each quotient-edge expansion against that constrained frontier. A failed expansion produces the first (shortest under the declared finite traversal ordering) phantom route. Every candidate expansion consumes one unit of the explicit budget. Exhaustive no-phantom is only claimed **within max_depth**; budget exhaustion is `inconclusive`, never `preserved`. Inputs are finite, explicitly declared, strictly validated, and canonically ordered for replay.

DOGWOLF-001 is composed as a separate first-order instrument: each declared action's exact one-step successor-class set (including empty/disabled) is compared across every quotient fiber via `probe_operation_preservation`. The resulting statuses and original DOGWOLF-001 input digest are retained alongside the multi-step lift receipt. This does **not** silently convert a one-step result into a stronger multi-step certification.

## Boundaries

- Every abstract edge witnessed != every abstract **path** liftable.
- Same quotient class != same concrete representative or transferable transition witness.
- A phantom quotient-class route != a proof that its action-label word is unrealizable in every other route.
- Structural non-liftability != historical impossibility, observation, evidence, causation, or authority.
- Finite depth/no-phantom != unbounded bisimulation, behavioral equivalence, or correctness of the chosen quotient.
- A declaration of possible transitions != actual executed transitions.

**Next frontier:** bounded executable return traces, with explicit start-state and destination constraints, still without inference of real-world occurrence or automatic quotient-promotion.
