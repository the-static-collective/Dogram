# MAPPING-TORUS-RECEIPT-001 Design

## Status

Approved architectural slice against `Dogram/main@a499853b728fa72a58b82e8666c3b06678ac4e86`.

This design promotes only the exact calculational residue already earned by the merged co-phase walk-braid + spring research. It does not promote the surrounding metaphors or add a general braid ontology.

## Goal

Add one deterministic Dogram calculation surface for finite-fiber mapping-torus return structure:

```text
fiber count N
shift m
optional winding / comparison parameters
    ->
components
orbit length
normalized shift
winding decomposition
relative realignment
exact twisted-mode fraction
```

The result is a calculation receipt only.

## Existing executable ancestry

Current `dogram/transverse.py` already proves neighboring arithmetic:

- quotient sheet coordinates;
- quotient return periods;
- exact carrier return periods;
- return debt;
- generated sheets;
- bounded-history sheet traces and reach counts.

The new slice should reuse the same validation style and exact integer arithmetic rather than duplicating transverse analysis.

## Mathematical contract

For integer `N > 0` and integer shift `m`, define the finite-fiber return map

```text
j -> j + m (mod N)
```

The v0 exact quantities are:

```text
normalized_shift = m mod N
components       = gcd(N, m)
orbit_length     = N / gcd(N, m)
```

Each orbit is a component of the finite fiber under repeated return shift.

### Winding decomposition

For integer traversal count `k`, use Euclidean division:

```text
k = N*w + r
0 <= r < N
```

Return exact integers `w` and `r`. The runtime does not assign symbolic meaning to either.

### Relative realignment

For two integer shifts `m_a`, `m_b`, define the relative delta

```text
delta = (m_a - m_b) mod N
```

The first positive round count at which their fiber positions re-align is:

```text
realignment_period = N / gcd(N, m_a - m_b)
```

This must recover the already-researched `N=72`, `m_a=5`, `m_b=7` result:

```text
relative delta magnitude/residue = 2 mod 72
realignment period = 36
```

### Twisted-mode fraction

The research expression

```text
n + k*m/N
```

is represented exactly as a reduced rational pair rather than a floating point approximation.

For integer `n`, mode index `k`, shift `m`, fiber count `N`:

```text
numerator   = n*N + k*m
denominator = N
```

Reduce by `gcd(abs(numerator), denominator)` and return signed numerator + positive denominator.

The runtime does not multiply by `2π/L`, evaluate transcendental functions, infer physical resonance, or claim that a formal mode corresponds to a real material system.

## Proposed API

Create a focused module rather than widening `transverse.py`:

```python
@dataclass(frozen=True)
class MappingTorusAnalysis:
    fiber_count: int
    shift: int
    normalized_shift: int
    components: int
    orbit_length: int


def analyze_mapping_torus(fiber_count: int, shift: int) -> MappingTorusAnalysis: ...

def decompose_winding(fiber_count: int, traversal_count: int) -> WindingDecomposition: ...

def relative_realignment(fiber_count: int, shift_a: int, shift_b: int) -> RelativeRealignment: ...

def twisted_mode_fraction(fiber_count: int, shift: int, longitudinal_index: int, fiber_mode: int) -> RationalValue: ...
```

Dataclasses expose deterministic `to_data()` methods using only JSON-safe integers and lists.

## Dogram operator boundary

This design does **not** require a new public `dogram.specimen/v0` operator on the first commit.

Preferred implementation sequence:

1. pure module + focused tests;
2. research example/fixture proving the 72/5/7 case and a small hostile set;
3. only if the pure module is stable and the existing dispatch architecture has a clean calculation-shaped slot, expose one narrowly named public operator such as `mapping_torus@1` in a separate reviewed task.

If public dispatch would require semantic special-casing or schema widening disproportionate to the calculation, stop at the executable module. Executability does not require premature stdlib promotion.

## Receipt shape

If exposed through Dogram's public engine, the operative result must remain calculation-only:

```json
{
  "calculation": "mapping_torus@1",
  "consumed_inputs": {
    "fiber_count": 72,
    "shift": 5
  },
  "result": {
    "normalized_shift": 5,
    "components": 1,
    "orbit_length": 72
  }
}
```

Optional winding/comparison requests must name their consumed inputs explicitly. No hidden default values may influence the result.

## Hostile controls

Minimum exact controls:

1. `N=72,m=5` -> one component, orbit 72;
2. `N=72,m=6` -> six components, orbit 12;
3. negative shift normalizes correctly;
4. shifts differing by a multiple of N have the same coarse return structure;
5. same coarse return structure does **not** collapse input shift identity in the receipt;
6. `72,5,7` relative realignment -> 36;
7. winding decomposition reconstructs `k` exactly for positive, zero, and negative traversal counts using Python's Euclidean `divmod` convention;
8. twisted-mode fraction reduces exactly and never emits float drift;
9. invalid `N <= 0` refuses with a typed input error;
10. bools are not accepted as integers, matching current transverse validation discipline.

## Same surface / different history boundary

The runtime may observe that distinct shifts or traversal counts produce the same coarse quantity. It must preserve the exact consumed inputs in the receipt.

```text
same coarse observable != same calculation history
```

Dogram records the arithmetic distinction. It does not decide whether that distinction matters to ALEX, 3rdi, physics, music, theology, or narrative.

## Error handling

Use typed calculation errors with stable reason codes. Invalid dimensions or indices refuse; there is no coercion from strings/floats/bools.

Arithmetic functions must be total over valid integers and must not depend on platform time, randomness, network state, or external libraries.

## Dependencies

Python standard library only. Reuse `math.gcd` and existing Dogram canonical receipt/digest machinery if public dispatch is added.

## Boundaries

No new claim is made about:

- physical springs or tubes;
- time travel;
- co-creation semantics;
- calendar or symbolic correspondences;
- phi as a privileged runtime constant;
- causal mechanism;
- evidence/support/authority.

No `braid@1`, `spring@1`, `humanentropy@1`, or metaphor-named universal operator is introduced.

## Acceptance

The slice is complete when the pure calculations are deterministic and exact, hostile controls pass, the 72/5/7 research case is reproduced from executable code, and any public Dogram exposure preserves the standard consumed-input / calculation-only receipt boundary.

> **PROMOTE THE ARITHMETIC, NOT THE METAPHOR.**
