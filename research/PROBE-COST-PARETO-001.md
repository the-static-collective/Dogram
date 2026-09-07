# PROBE-COST-PARETO-001

Status: bounded research specimen; no public operator promotion.

## Question

Does information refinement determine probe cost, or can the two orders cross even on a four-state deterministic specimen?

## Frozen carrier and probes

Let `X = {a,b,c,d}` and freeze target pair `(a,d)`.

Declared deterministic probes:

- `coarse = (all, all, all, all)`;
- `vertical = (L, L, R, R)`;
- `diagonal = (U, D, U, D)`;
- `joint = (LU, LD, RU, RD)`.

Refinement means exact deterministic factorization: `q` refines `p` when there exists a finite map `h` with `p = h o q` on the frozen carrier.

Declared costs are a separate coordinate:

- `cost(coarse)=0`;
- `cost(vertical)=4`;
- `cost(diagonal)=2`;
- `cost(joint)=3`.

No cost is inferred from partition size, refinement depth, computational complexity, evidence quality, or semantics.

## Exact result

The separating probes for `(a,d)` are:

`{vertical, diagonal, joint}`.

Under information refinement alone, the minimal separators are:

`{vertical, diagonal}`.

Under cost alone, the unique cheapest separator is:

`{diagonal}`.

Define information-cost Pareto dominance by:

`q dominates p` iff

1. `q` refines `p`;
2. `cost(q) <= cost(p)`;
3. at least one of those comparisons is strict.

Then `joint` strictly dominates `vertical`: `joint` is strictly more informative and costs `3 < 4`.

Therefore an information-minimal separator can be Pareto-dominated after an independently declared cost coordinate is added.

Neither `joint` nor `diagonal` dominates the other:

- `joint` is more informative than `diagonal` but costs more (`3 > 2`);
- `diagonal` is cheaper but does not refine `joint`.

The Pareto-minimal separating set is therefore exactly:

`{diagonal, joint}`.

## Earned distinctions

`INFORMATION MINIMAL != PARETO MINIMAL.`

`MORE INFORMATIVE CAN BE CHEAPER.`

`DO NOT DERIVE COST FROM REFINEMENT.`

`A PARETO FRONTIER IS A RECEIPT OF NONDOMINANCE, NOT A DECISION.`

The last seal matters: choosing between `diagonal` and `joint` would require an additional preference, utility, budget, capability, or policy declaration. The mathematics here refuses to manufacture one.

## Documented mathematics

Blackwell-style comparison orders experiments by informativeness / garbling rather than by a generic scalar value. Goel & Ginebra (2003), DOI `10.1046/j.1467-9884.2003.00376.x`, review the finite-experiment partial orders and randomization/garbling characterization. Mu, Pomatto, Strack & Tamuz (2021), DOI `10.3982/ECTA17548`, likewise describe Blackwell comparison as a partial order on informativeness.

Experimental-design literature separately treats cost and information/design performance as distinct criteria. Lu & Anderson-Cook (2012), DOI `10.1002/qre.1476`, explicitly keep cost as a separate Pareto criterion rather than folding it into one information score. Forte et al. (2017), DOI `10.1002/cite.201600104`, use multiobjective/Pareto optimization for conflicting experimental-design objectives and emphasize that the frontier exposes trade-offs rather than selecting a unique design by itself.

No claim is made that these papers contain this exact four-state fixture or Dogram interpretation.

## Inference boundary

For this declared finite family only, information refinement and cost are independent coordinates. Their product order can have dominated information-minimal probes and multiple nondominated separators.

This does **not** establish a universal real-world cost model, a utility function, or a rule for choosing among nondominated probes.

## Explicit refusals

- `MORE INFORMATIVE != MORE EXPENSIVE`;
- `CHEAPER != LESS INFORMATIVE`;
- `PARETO OPTIMAL != TRUE`;
- `PARETO OPTIMAL != PREFERRED`;
- `COST != EVIDENCE QUALITY`;
- `COST != COMPUTATIONAL COMPLEXITY` unless explicitly declared that way;
- `INFORMATION DOMINANCE != AUTHORITY`;
- `PROBE SEPARATION != OCCURRENCE`;
- `NONDOMINATED != CANONICAL`.

## Verification

The frozen finite arithmetic was independently enumerated during the research pass. Exact results:

- separating probes: `vertical, diagonal, joint`;
- information-minimal separators: `vertical, diagonal`;
- cost-minimal separators: `diagonal`;
- only separating-probe Pareto dominance edge: `joint -> vertical`;
- Pareto separators: `diagonal, joint`.

Wolfram was attempted for independent context/verification but its connector returned an upstream 404, so no Wolfram-verification claim is made. Consensus search quota was exhausted, so no Consensus citation is claimed.

## HOLD

Do not promote `cost@1`, `pareto@1`, `probe_choice@1`, `utility@1`, `budget@1`, or `experiment@1` from this specimen.

## Next frontier

Add a third independently declared coordinate such as capability/availability, or move from one-shot probes to **sequential adaptive probes** where the cost of the second question depends on the first answer. The smallest useful hostile specimen would ask whether a globally cheaper adaptive policy can be incomparable with every fixed one-shot probe while preserving a complete branch-by-branch receipt.

Candidate next seal:

`EXPECTED COST REQUIRES A DECLARED DISTRIBUTION; WORST-CASE COST DOES NOT.`
