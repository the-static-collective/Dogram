# Sparse Ice Probe 001

This implementation composes Dogram's adaptive probe-cost distinction with
GHoT exact sparse Ice Cube region claims.

The verifier first checks the complete **structure** of the claimed region set:
every declared region must be present exactly once and retain its exact
work/index/x/y identity.

It then performs a deterministic bounded root probe over pixel values.

If every root probe agrees with the Ice Cube work specification, the receipt
stops with:

```text
status = OK
claim_scope = bounded-adaptive-region-witness/v0
branch_triggered = false
```

If any root probe disagrees, the verifier expands to the full region set. Any
mismatch produces REFUSED.

An optional declared prior over:

```text
clean
dirty
```

changes only the reported expected verification cost. It cannot change probe
selection, branching, status, evidence, or authority.

Preserve:

```text
PRIOR != EVIDENCE
LOWER EXPECTED COST != MORE TRUE
POLICY != AUTHORITY
COST ORDER != EVIDENCE ORDER
STRUCTURAL COVERAGE != FULL VALUE VERIFICATION
BOUNDED PROBES != UNIVERSAL PROOF
```
