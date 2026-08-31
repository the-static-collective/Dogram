# PHASELIFT-FLOW-GAP-RECEIPTS-001

**Date:** 2026-08-30  
**Companion:** `research/PHASELIFT-FLOW-GAP-MATHAL-LEDGER-001.md`  
**Status:** EXECUTABLE RECEIPT INDEX · NO NEW OPERATOR

This file records the exact bounded verification path for the PHASELIFT flow-gap mathal suite.

## TDD provenance

### RED

```text
commit: c5f2c063079ad6504b49352e44221c4d199cdc2b
CI run: 33353711585
conclusion: failure
suite result: 10 FileNotFoundError errors
reason: all ten tests named frozen phaselift_flow fixtures that did not yet exist
```

This was the intended RED state.

### GREEN

```text
head: 5289fbb0120bd248267c6446847fc3bd9e873708
push CI run: 33353901828
job: 99372296925
conclusion: success
unit tests: 142 passed
compile: success
constitutional floor: success
Omega scope scan: success
```

The ten new tests all passed in the full suite.

## Executable receipt summaries

### `TERNARY-TO-QUATERNARY-001` / `delta@1`

```text
member_count       SAME
first_difference   affine_rank
affine_rank delta  +1
tetra_volume delta +1/6
```

### `AUTHORITY-TRANSFER-RECTANGLE-001` / `rectangle@1`

Lawful receiver-local authorization matrix:

```text
mixed_delta = 0
interaction_detected = false
```

Hostile silent-transfer control:

```text
mixed_delta = -1
interaction_detected = true
```

### `THRESHOLD-BIRTH-REACH-001` / `reach@1`

```text
H -> W_PRIME
  before false
  after  true
  path   H -> THETA -> W_PRIME

H -> WORK
  before false
  after  true
  path   H -> THETA -> W_PRIME -> WORK
```

### `HOME-ABLATION-001` / `ablate@1`

```text
H -> W_PRIME  true -> false
H -> NEXT     true -> false
```

### `SAME-FOURTH-DIFFERENT-DECODER-001` / `rectangle@1`

```text
rank table = [[3,3],[3,4]]
mixed_delta = 1
interaction_detected = true
```

### `ONE-POINT-TWO-HISTORIES-001` / `delta@1`

```text
endpoint             SAME
first_difference     approach_orientation
+e4 != -e4
```

### `FLOW-HAS-NEXT-001` / `ablate@1`

```text
SELF -> NEXT    true -> true
SELF -> RESIST  true -> false
gained_reachability = []
```

### `ALIGNMENT-WITHOUT-CONTACT-001` / `reach@1`

```text
A_TOUCH -> SYNC     false -> true
A_TOUCH -> B_TOUCH  false -> false
B_TOUCH -> A_TOUCH  false -> false
```

### `SYNCHRONY-BRIDGE-RECTANGLE-001` / `rectangle@1`

```text
crossability table = [[0,1],[0,1]]
mixed_delta = 0
interaction_detected = false
```

### `BRIDGE-BIRTH-001` / `reach@1`

```text
A_PRE -> B_NEXT
  before false
  after  true
  path   A_PRE -> A_TOUCH -> B_TOUCH -> B_NEXT
```

## Existing Omega receipt reused by the ledger

The packet does not duplicate the landed Ω proof. Existing `test_omega.py` verification remains the receipt for:

```text
selected result SAME
execution digest DIFFERENT
step trace DIFFERENT
fuel DIFFERENT
consumed-input provenance DIFFERENT
```

Therefore the packet reuses, rather than remints:

```text
RESULT EQUIVALENCE != EXECUTION EQUIVALENCE
PRESENCE IS NOT CONSUMPTION
```

## Runtime boundary

No production file under `dogram/` was changed by this slice.

No new public operator was added.

The executable witnesses lower entirely through:

```text
delta@1
rectangle@1
ablate@1
reach@1
```

with the existing Ω receipt referenced where execution-history semantics are required.
