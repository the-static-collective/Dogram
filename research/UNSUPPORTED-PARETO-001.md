# UNSUPPORTED-PARETO-001 — nondominated does not imply linearly selectable

Status: bounded research slice; no public operator/runtime/authority promotion.

## Frozen specimen

For biobjective minimization, declare three feasible cost vectors:

- `A=(0,4)`
- `B=(2,3)`
- `C=(4,0)`

No point dominates another, so all three are Pareto-minimal.

For a separately declared nonnegative normalized linear scalarization `(w,1-w)`:

- `C_w(A)=4-4w`
- `C_w(B)=3-w`
- `C_w(C)=4w`

For B to weakly beat A requires `w <= 1/3`. For B to weakly beat C requires `w >= 3/5`. These exact requirements are disjoint. Therefore B is Pareto-valid but is never a minimizer of any such weighted sum.

## Seal

**PARETO-VALID OPTION != OPTION SELECTABLE BY A LINEAR WEIGHTED SUM.**

Secondary: **NEVER SELECTED BY THIS SCALARIZATION FAMILY != DOMINATED OR IRRELEVANT.**

## Documented mathematics

This is the standard supported/unsupported nondominated-point distinction in discrete/nonconvex multiobjective optimization. Könen & Stiglmayr (2025), DOI `10.1002/mcda.70024`, explicitly distinguish efficient solutions obtainable by positive weighted-sum scalarization from unsupported efficient solutions. Sayın (2024), DOI `10.1002/mcda.1829`, studies supported nondominated points as only a representation of a larger nondominated set. Ding et al. (2017), DOI `10.1002/etep.2324`, notes that weighted-sum methods fail to capture nonconvex portions of Pareto surfaces.

Scholar Gateway pass: 10 passages / 7 articles / 2007–2025. Wolfram semantic search did not return a direct unsupported-point specimen; its ParetoListMinima documentation independently confirms Pareto minima as minimal elements of the componentwise partial order. Exact inequalities above are reproduced directly in the kernel/tests.

## Dogram inference

A scalarizer is a lossy selection lens over a vector-valued feasible set. Failure to be selected by that lens does not erase Pareto status. Therefore any later Dogram scalarization receipt should preserve both the pre-scalar Pareto relation and the declared scalarization family/parameters rather than treating scalar nonselection as structural inferiority.

## Refusals

- Pareto optimal != semantically preferred.
- Unsupported != dominated.
- Unsupported != irrelevant.
- Never selected by weighted sum != impossible.
- Weight != evidence, human worth, or authority.
- Scalarization family != complete decision procedure.
- Objective vector != ontology.
- Mathematical selection != permission to act.

No claim is made that linear scalarization is generally defective; it is an exact declared calculation with a known information boundary.
