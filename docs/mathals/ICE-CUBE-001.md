# Ice Cube 001 — bounded mathematical projection receipt

Ice Cube 001 composes four exact structures into one verifiable specimen family:

```text
Mandelbrot quadratic family
  × Lucas-selected period
  × Halley root iteration
  × Fibonacci/Lucas torus monodromy
```

The producer may spend substantial compute rendering a Halley basin for

```text
f_c^(L_n)(z) - z = 0.
```

Dogram does not claim to reproduce the entire render. It verifies a bounded receipt:

1. the Lucas recurrence and selected period;
2. the exact even Fibonacci companion-matrix power used as an SL(2,Z) torus monodromy;
3. trace and determinant invariants;
4. the finite-fiber mapping-torus quotient already provided by `dogram.mapping_torus`;
5. replayed Halley witnesses and their periodic residuals;
6. the returned render content address;
7. deterministic pixel challenges derived from the canonical work spec.

The last step is the useful-work asymmetry: production may be large while the receipt samples a deterministic subset of the projection.

The receipt explicitly says:

```text
claim_scope = bounded-math-and-projection-witness/v0
```

Therefore:

```text
DOGRAM RECEIPT != FULL PROOF OF EVERY PIXEL
RENDER HASH != MATHEMATICAL TRUTH
VERIFIED CHALLENGES != UNIVERSAL VERIFICATION
EXPENSIVE PRODUCTION != EXPENSIVE CHECKING
```

This module is designed to be called by GHoT Ice Cube Experiment 030. reLATTE remains the carrier: the crossing substrate need not understand any of these mathematical semantics.
