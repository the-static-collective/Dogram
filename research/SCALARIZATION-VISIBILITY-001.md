# SCALARIZATION-VISIBILITY-001

Research-only finite specimen. No public operator or semantic/decision authority is proposed.

## Question

Does failure of one declared scalarization family to select a Pareto point establish that the point is absent, dominated, or irrelevant?

No.

## Frozen exact specimen

For biobjective minimization, declare

- `A=(0,4)`
- `B=(2,3)`
- `C=(4,0)`.

All three are Pareto-minimal.

For every normalized nonnegative weighted sum `(w,1-w)`, B can tie-or-beat A only if `w <= 1/3`, while B can tie-or-beat C only if `w >= 3/5`. These requirements are disjoint. Thus B is unsupported by the entire weighted-sum family.

Now change the *method*, not the feasible points. Under the epsilon-constraint problem

`minimize f1 subject to f2 <= 3`,

A is infeasible, while B and C are feasible; B has smaller f1, so B is the unique optimizer.

Therefore:

**INVISIBLE TO ONE DECLARED SCALARIZATION FAMILY != ABSENT FROM THE PARETO SET.**

And more narrowly:

**METHOD-RELATIVE NONSELECTION != DOMINANCE.**

## Documented mathematics

The epsilon-constraint method optimizes one objective while turning the others into parameterized constraints. Mavrotas (2009), *Applied Mathematics and Computation* 213(2):455-465, DOI `10.1016/j.amc.2009.03.037`, develops AUGMECON and explicitly contrasts generation of Pareto solutions with weighting approaches. Bérubé, Gendreau & Potvin (2009), *European Journal of Operational Research* 194(1):39-50, DOI `10.1016/j.ejor.2007.12.014`, gives an exact epsilon-constraint method for biobjective combinatorial optimization. Recent review/application literature continues to note that weighted sums can miss nonconvex regions while epsilon-constraint methods can expose them.

Consensus search was quota-blocked during this pass; no Consensus result is claimed.

## Dogram inference

A query/measurement/selection procedure has an aperture. Nonselection can receipt a relation between a specimen and that aperture; it does not by itself receipt nonexistence of the specimen. Dogram should therefore retain at least: feasible set/objective declaration, scalarization family, scalarization parameters, and selected result separately.

## Refusals

- Pareto-minimal != semantically preferred.
- Invisible to method M != absent.
- Never selected by weighted sums != dominated or irrelevant.
- Epsilon threshold != evidence, human worth, or authority.
- Selected under epsilon-constraint != intrinsically best.
- Mathematical selection != permission to act.
- Structure/reachability/feasibility != occurrence.

## Reproduce

`pytest -q tests/test_scalarization_visibility_001.py`
