# DOGWOLF-001 — Operation-preservation counterexample hunt

**Status:** bounded internal research specimen. **Authority:** none. **Public operator:** none. **Mandatory dependencies:** none.

## New seam, not a duplicate

OPERATION-REACHABILITY-QUOTIENT-001 checks whether a declared one-step enabledness predicate is constant on quotient fibers. DOGWOLF-001 asks the same exact factorization question for the typed results of any predeclared finite operation table: q(a)=q(b) must imply f(a)=f(b) for every checked pair. Values have type-sensitive equality; True is not integer 1. Operations are inert tables, never user-supplied callbacks.

A result is preserved only after **every** pair in **every** declared quotient fiber has been checked. One witnessed mismatch proves non-factorization for the declared operation and returns counterexample even if the search has not finished. Exhausting max_pair_checks without a mismatch yields inconclusive, never preservation. possible_pairs counts only unordered within-fiber pairs, and the bound applies per operation. Nothing here establishes preservation of all possible future operations, bisimulation, chronology, or real-world meaning.

## Reproduce

    python -m unittest tests.test_dogwolf_operation_preservation -v
    # Optional independent Wolfram Language finite oracle:
    wolframscript -file research/dogwolf_001.wl

The frozen V4 = Z2 x Z2 specimen contains 16 supplied ordered two-arrow paths, four composite fibers of size four, and 24 unordered distinct path pairs sharing a composite. The composite-only operation factors through the quotient; first-arrow extraction does not. The first counterexample is 0:0 versus 1:1, sharing composite (0,0) but with first arrows (0,0) and (0,1). The Wolfram oracle independently reproduces this exact finite specimen; it is not called by the Dogram runtime, and Wolfram is not a required dependency.

## Call the kernel

    from dogram.dogwolf_operation_preservation import probe_operation_preservation
    receipt = probe_operation_preservation(
        states=("ready", "blocked", "done"),
        projection=("pending", "pending", "done"),
        operations={"advance": (True, False, False), "reset": (False, False, True)},
        max_pair_checks=32,
    )
    assert receipt.probes[0].status == "counterexample"

The input_sha256 identifies the canonical typed declaration and budget, not an external run or historical occurrence. Each counterexample retains separate state IDs, the common quotient result, and the distinct operation results. The module does not register with CLI/public dispatch.

## Boundaries

- Same quotient does not mean same supplied state or path.
- Exact preservation for a declared operation does not imply preservation for every operation.
- An unfinished no-counterexample search does not prove preservation.
- Algebraic quotient is not evidence equivalence, source identity, chronology, causal history, or authority.
- An optional Wolfram oracle is not a mandatory deployment dependency.

**Next frontier:** successor-sensitive transition tables and bisimulation pressure, only as a separate explicitly declared experiment.
