# PETRI-INCIDENCE-CONCURRENCY-001

## Status

Research-only bounded specimen. No public Dogram operator is proposed.

## Question

Can two ordinary 1-safe place/transition nets have the same incidence matrix and the same complete labeled *sequential* reachability graph while disagreeing about which transitions can occur as one concurrent step?

Yes.

## Frozen carrier

Use places

`(guard, pa, qa, pb, qb)`

and transitions `(a,b)`, with initial marking

`(1,1,0,1,0)`.

Both nets move `a: pa -> qa` and `b: pb -> qb`.

### Parallel control

Neither transition touches `guard`.

### Shared-resource control

Both `a` and `b` additionally have a unit self-loop through `guard`:

`guard -> a -> guard`

`guard -> b -> guard`.

The self-loop consumes and reproduces the same token during an individual firing.

## Exact receipts

For both nets, `C = Post - Pre` is exactly

| place | a | b |
|---|---:|---:|
| guard | 0 | 0 |
| pa | -1 | 0 |
| qa | +1 | 0 |
| pb | 0 | -1 |
| qb | 0 | +1 |

The complete sequential labeled reachability graph is also identical:

- initial --`a`--> after-a --`b`--> final;
- initial --`b`--> after-b --`a`--> final.

Both legal words `ab` and `ba` reach the same final marking `(1,0,1,0,1)` in each net.

The step-enabling receipt differs. For the joint step `{a,b}`:

- parallel control requires `0` guard tokens, so the step is enabled;
- shared-resource control requires `2` guard tokens, but only `1` exists, so the step is not enabled.

Therefore:

**SAME INCIDENCE + SAME SEQUENTIAL REACHABILITY != SAME CONCURRENCY STRUCTURE.**

**A ZERO INCIDENCE DELTA CAN STILL HIDE AN ENABLING CONSTRAINT.**

**POST - PRE IS A QUOTIENT OF THE ARC CONTRACT, NOT A RECONSTRUCTION OF IT.**

## Why the collision exists

The incidence matrix records the *net token change* of a transition. A unit self-loop contributes `+1 - 1 = 0`, exactly the same incidence entry as absence of any arc. But transition enabling is checked against input demand before firing. Hence equal `Post - Pre` does not imply equal `Pre`, and equal sequential markings need not imply equal jointly enabled steps.

This is a deliberate hostile specimen for any decoder that treats a state equation or interleaving reachability graph as a complete occurrence/concurrency description.

## Documented mathematics

Standard P/T-net semantics define enabling from the input/preset weights and firing by subtracting input weights and adding output weights. The incidence matrix is their difference. See Kuo, Chao & Lee (2010), DOI `10.1002/asjc.186`, and Chen et al. (2015), DOI `10.1155/2015/636959`. The latter explicitly restricts straightforward incidence-matrix structural representation to self-loop-free/pure nets, which is exactly the pressure point used here.

Chen et al. (2015), DOI `10.1002/tee.22188`, additionally note that a reachability graph cannot in general distinguish independent concurrency from concurrency entangled with conflict. Song et al. (2013), DOI `10.1155/2013/962765`, describe occurrence-net unfoldings and their causal/conflict/concurrency relations as a way to preserve true-concurrency structure without enumerating all interleavings.

The specific five-place pair in this receipt is a bounded Dogram construction; no claim is made that it is a published or globally smallest example.

## Inference earned by the specimen

If a Dogram input surface retains only:

- `C = Post - Pre`, or
- reachable markings plus sequential labeled edges,

then it has already quotient-ed away enough input-arc information to make this concurrency distinction unrecoverable on the frozen pair.

That is an information-loss statement about the declared mathematical representation. It is not an occurrence claim.

## Speculative bridge — HOLD

There is a possible architectural analogy to receipts that preserve `consumed_inputs`: a resource may be returned unchanged in the output surface while still having been required/consumed during execution. This specimen is mathematically suggestive of why `net delta = 0` should not imply `not consumed`.

Do **not** promote that analogy from this research slice. Petri tokens are not evidence, historical resources, causal mechanisms, or LOADOUT authority.

## Refusals

- `REACHABLE MARKING != OCCURRENCE HISTORY`
- `SEQUENTIAL DIAMOND != CONCURRENT STEP`
- `INCIDENCE EQUALITY != NET IDENTITY`
- `ZERO NET CHANGE != ZERO INPUT DEMAND`
- `STEP CONCURRENCY != HISTORICAL SIMULTANEITY`
- `SHARED PLACE != REAL-WORLD RESOURCE`
- `PETRI CAUSALITY != EVIDENCE OR AUTHORITY`

## Verification contract

The stdlib-only kernel must exactly verify:

1. equal incidence matrices;
2. equal complete sequential labeled reachability edge sets;
3. `ab` and `ba` reach the same final marking in both nets;
4. joint step `{a,b}` is enabled only in the parallel control;
5. the sole hidden structural change is the pair of balanced `guard` self-loop demands.
