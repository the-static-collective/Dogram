# MINIMAL-SEPARATING-BASES-001

Status: bounded research specimen; no public operator or authority promotion.

## Question

If a declared finite probe family separates all supplied states, is there a unique minimal measurement basis? No.

## Frozen specimen

States are the four binary words `00, 01, 10, 11`. Declared binary probes are:

- `x`: first bit
- `y`: second bit
- `xor`: parity of the two bits

Every two-probe family `{x,y}`, `{x,xor}`, `{y,xor}` gives four distinct joint signatures, hence separates the supplied finite state set. No singleton binary probe can distinguish four states. Therefore all three two-probe families are distinct minimum-cardinality and inclusion-minimal separating families.

The full three-probe family is separating but redundant: remove any one probe and separation survives. Yet inside any chosen two-probe minimum basis, either member is indispensable for that basis.

## Seals

**SAME COMPLETE DISTINGUISHING POWER != SAME MEASUREMENT BASIS.**

**INDISPENSABLE WITHIN ONE MINIMAL BASIS != GLOBALLY INDISPENSABLE.**

**SEPARATING != UNIQUELY MINIMAL.**

## Documented mathematics

This is a finite separating-system / observability specimen. Separating systems assign distinct signatures to distinct objects; minimum separating systems minimize the number of tests/probes. Related graph formulations include resolving sets / metric bases and identifying codes. See Lichev & Sanhueza-Matamala (2026), DOI `10.1002/rsa.70091`, for separating systems and minimum-size questions; Sun et al. (2024), DOI `10.1002/mma.10485`, for minimum measurements making switching Boolean networks observable; Jean & Seo (2024), DOI `10.1002/net.22254`, for minimum identifying-code detector sets.

The particular XOR specimen and Dogram seals are project-local finite deductions, not claims copied from those papers.

## Dogram delta

PROBE-SEPARATION-001 asks whether a supplied probe family separates a finite domain. This slice asks a different combinatorial question after separation succeeds: which subfamilies still separate, which are inclusion-minimal, what is the minimum cardinality, and is the basis unique?

The receipt preserves every separating subset and all minimum/inclusion-minimal families instead of choosing one canonical basis.

## Refusals

- separating family != evidentiary truth
- minimum cardinality != semantic importance
- minimum basis != unique basis
- probe indispensability within a basis != global indispensability
- redundancy != uselessness
- same distinguishing power != same provenance
- finite-domain separation != global separation
- probe output != occurrence
- mathematical minimality != authority to remove a measurement

## Reproduce

`pytest -q tests/test_minimal_separating_bases_001.py`
