# ROBUST-SEPARATING-DISTANCE-001

Status: research-only; no public operator promotion.

## Question

Given a declared finite family of binary views, separation answers whether signatures are distinct. What extra receipt records how fragile that distinction is to missing or corrupted views?

## Frozen specimen

Four states use signatures

- x0 = 000
- x1 = 011
- x2 = 101
- x3 = 110

Every unordered pair has Hamming distance exactly 2. Therefore the minimum separation multiplicity is 2.

Exact enumeration shows that deletion of any one coordinate preserves four distinct projected signatures. Deletion of two coordinates is not guaranteed safe. Under standard coding semantics, minimum distance 2 detects an arbitrary one-bit change but does not uniquely correct one arbitrary bit flip.

## Delta

A merely separating family has minimum pair distance >= 1. This specimen has minimum pair distance 2, so every state-pair has two independent coordinate distinctions in the declared signature representation.

The resulting finite receipt separates two failure models:

- erasure/missing-view tolerance: d-1 arbitrary erased coordinates;
- adversarial flip correction: floor((d-1)/2) arbitrary corrupted coordinates.

For d=2 these are 1 and 0 respectively.

## Durable seal

**SUFFICIENT != ROBUST. RECEIPT THE MINIMUM PAIRWISE SEPARATION MULTIPLICITY AND THE FAILURE MODEL.**

**MISSING VIEW != CORRUPTED VIEW. THE SAME DISTANCE BUDGET PAYS DIFFERENTLY FOR ERASURES AND ERRORS.**

## Refusals

- HAMMING DISTANCE != EVIDENCE STRENGTH
- VIEW ERASURE != HISTORICAL ABSENCE
- BIT FLIP != FALSE TESTIMONY
- ROBUST IDENTIFICATION != TRUTH
- ERROR CORRECTION != AUTHORITY
- SEPARATION MULTIPLICITY != INDEPENDENT REAL-WORLD WITNESSES

## Provenance

This is standard finite coding/separating-system mathematics applied as a bounded Dogram research specimen. Separating systems encode objects by binary signatures; minimum Hamming distance measures coordinate disagreement. Error-correcting-code theory distinguishes erasure tolerance from arbitrary-error correction. Recent fault-tolerant identifying-code work similarly studies identification under detector failures.

Literature consulted: Lichev & Sanhueza-Matamala (2026), DOI 10.1002/rsa.70091; Jean & Seo (2024), DOI 10.1002/net.22254; Junnila, Laihonen & Parreau (2012), DOI 10.1002/net.21472.

Wolfram was queried for direct verification. It exposed HammingDistance/error-correcting-code documentation but returned no direct result for this exact specimen, so no independent Wolfram calculation is claimed.
