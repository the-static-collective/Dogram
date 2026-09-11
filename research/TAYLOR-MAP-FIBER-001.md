# TAYLOR-MAP-FIBER-001

## Question

Can complete formal Taylor data determine a unique smooth germ, and if not, what extra structure would a reconstruction require?

## Documented mathematics

For smooth germs at the origin, the classical Borel theorem says that every formal power series occurs as the Taylor series of some smooth function germ. Equivalently, the Taylor/Borel map from smooth germs to formal power series is surjective.

Barostichi, Cordaro & Petronilho (Mathematische Nachrichten 286, 2013, DOI 10.1002/mana.201200231) state the classical Borel theorem in precisely this realizability form: any formal power series is the formal Taylor series at the origin of a smooth function.

Surjectivity does not imply injectivity. A nonzero flat germ lies in the kernel of the Taylor map. The prior SMOOTH-FLAT-GERM-001 slice froze the standard specimen

```text
h(x)=exp(-1/x^2), x!=0; h(0)=0,
```

whose derivatives of every order vanish at zero while the germ is nonzero away from zero.

The contrast is category-sensitive. Bierstone & Milman (Journal of the London Mathematical Society 95, 2017, DOI 10.1112/jlms.12032) define quasianalyticity by the condition that vanishing Taylor expansion forces local vanishing. Rolin & Servi (Proceedings of the London Mathematical Society 110, 2015, DOI 10.1112/plms/pdv010) likewise formulate quasianalyticity as injectivity of a germ-to-expansion map.

Extension literature also treats right inverses as additional structure. Jimenez-Garrido, Sanz & Schindl (Mathematische Nachrichten 293, 2020, DOI 10.1002/mana.201800465) explicitly discuss surjectivity of Borel maps via existence of right inverses in ultraholomorphic classes. A right inverse is therefore a chosen reconstruction mechanism, not something logically supplied by surjectivity alone.

No cited source is claimed to contain this exact Dogram fixture or interpretation.

## Frozen specimen

Let

```text
p(x)=1-2x+3x^2
h(x)=exp(-1/x^2), x!=0; h(0)=0.
```

For distinct declared scales `c`, define

```text
f_c(x)=p(x)+c h(x).
```

Because every derivative of `h` at zero vanishes,

```text
T_0(f_c)=T_0(p)
```

for every `c`.

But at any fixed nonzero point, for example `x=1/2`, `h(1/2)>0`; therefore distinct scales give distinct function germs. The frozen family `c in {0,1,2}` supplies a finite executable lower bound of three distinct smooth germs in one complete Taylor fiber.

This is enough to establish a strict local nonuniqueness specimen without pretending the kernel enumerates an infinite fiber.

## Borel direction

The converse direction is theorem-level rather than computational:

```text
formal power series -> at least one smooth germ
```

is supplied by Borel's theorem.

The executable kernel deliberately refuses to infer this universal existence statement from a finite list of coefficients. It returns an existence receipt only when the Borel theorem is explicitly declared as the proof basis, and it marks that no realization was constructed by the kernel.

## Dogram delta

The Taylor map therefore separates cleanly into two properties:

```text
SURJECTIVE:
    every formal Taylor series has at least one smooth realization

NOT INJECTIVE:
    distinct smooth germs can have the same complete Taylor series
```

Hence a formal Taylor object determines a fiber of compatible smooth germs, not a unique germ.

A right inverse / section

```text
s : formal series -> smooth germs
```

with

```text
T o s = id
```

would select one representative from each fiber. Such a selection is additional structure. Surjectivity asserts existence of representatives; it does not make one representative canonical.

## Seals

```text
THE TAYLOR MAP CAN BE SURJECTIVE WITHOUT BEING INJECTIVE.
A TAYLOR FIBER CAN CONTAIN DISTINCT SMOOTH GERMS.
RECONSTRUCTION NEEDS A SECTION, AND A SECTION IS EXTRA STRUCTURE.
EXISTENCE OF A PREIMAGE != CANONICAL CHOICE OF A PREIMAGE.
KEEP THE KERNEL OF THE PROBE IN THE RECEIPT.
```

## Refusals

```text
SAME FORMAL SERIES != SAME SMOOTH GERM
SURJECTIVE != INVERTIBLE
RIGHT INVERSE != INVERSE
SECTION != CANONICAL SECTION
RECONSTRUCTION CHOICE != OCCURRENCE
FLAT DIFFERENCE != ABSENCE
FORMAL COMPATIBILITY != EVIDENCE
SMOOTH REALIZABILITY != HISTORICAL REALIZATION
QUOTIENT CLASS != AUTHORITY CLASS
```

## Executable boundary

The bounded stdlib kernel does only the following:

1. evaluates the explicit family `p+c h`;
2. witnesses distinct family members at a nonzero point;
3. receipts complete Taylor collision only when the flat-kernel theorem is declared;
4. receipts arbitrary formal smooth realizability only when Borel's theorem is declared;
5. never constructs or chooses a general Borel realization.

The fixture freezes three scales and one polynomial Taylor series. This is a specimen, not an implementation of the full infinite-dimensional theorem.

## HOLD

No `taylor_map@1`, `borel@1`, `section@1`, `reconstruct@1`, `fiber@1`, `quotient@1`, `canonical_representative@1`, evidence semantics, causal semantics, or authority semantics is promoted.

## Next frontier

The mathematically stronger continuation is to distinguish a quotient object from a chosen splitting. The flat germs form the kernel of the smooth Taylor map, so formally one may view Taylor data as collapsing smooth germs modulo flat differences. The next bounded pressure should ask when an exact sequence

```text
0 -> Flat -> SmoothGerms -> FormalSeries -> 0
```

admits a chosen linear/continuous splitting, and which properties of that splitting depend on topology or regularity class.

Candidate seal:

```text
A QUOTIENT FORGETS THE KERNEL; A SPLITTING CHOOSES HOW TO PUT IT BACK.
```
