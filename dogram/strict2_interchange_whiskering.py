from __future__ import annotations

from dataclasses import dataclass

Permutation = tuple[int, int, int]


class Strict2InterchangeInputError(ValueError):
    pass


def _validate_permutation(value: Permutation) -> Permutation:
    if tuple(sorted(value)) != (1, 2, 3):
        raise Strict2InterchangeInputError("expected a permutation of (1,2,3)")
    return value


def identity() -> Permutation:
    return (1, 2, 3)


def transposition_12() -> Permutation:
    return (2, 1, 3)


def transposition_23() -> Permutation:
    return (1, 3, 2)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left o right: apply right first, then left."""

    left = _validate_permutation(left)
    right = _validate_permutation(right)
    return tuple(left[right[index] - 1] for index in range(3))  # type: ignore[return-value]


def inverse(value: Permutation) -> Permutation:
    value = _validate_permutation(value)
    out = [0, 0, 0]
    for source, target in enumerate(value, start=1):
        out[target - 1] = source
    return tuple(out)  # type: ignore[return-value]


def conjugate(g: Permutation, h: Permutation) -> Permutation:
    """Conjugation action g.h = g h g^-1."""

    return compose(compose(g, h), inverse(g))


@dataclass(frozen=True)
class TwoCell:
    """A 2-cell (h,g): g => h g in the identity crossed module S3 -> S3."""

    h: Permutation
    g: Permutation

    @property
    def source(self) -> Permutation:
        return self.g

    @property
    def target(self) -> Permutation:
        return compose(self.h, self.g)



def vertical_compose(*, top: TwoCell, bottom: TwoCell) -> TwoCell:
    if top.source != bottom.target:
        raise Strict2InterchangeInputError("2-cells are not vertically composable")
    return TwoCell(h=compose(top.h, bottom.h), g=bottom.g)


def horizontal_compose(*, left: TwoCell, right: TwoCell) -> TwoCell:
    """Lawful strict-2-group horizontal composition.

    For a crossed module (H -> G), the semidirect law is
    (h,g) tensor (k,l) = (h * (g.k), g*l). Here H=G=S3,
    boundary is identity, and the G-action on H is conjugation.
    """

    acted_right = conjugate(left.g, right.h)
    return TwoCell(
        h=compose(left.h, acted_right),
        g=compose(left.g, right.g),
    )


def naive_horizontal_without_action(*, left: TwoCell, right: TwoCell) -> TwoCell:
    """Hostile control: illegally replace the semidirect law by a direct product."""

    return TwoCell(
        h=compose(left.h, right.h),
        g=compose(left.g, right.g),
    )


@dataclass(frozen=True)
class Strict2InterchangeReceipt:
    left_bottom_h: Permutation
    left_top_h: Permutation
    right_bottom_h: Permutation
    right_top_h: Permutation
    whiskered_right_top_h: Permutation
    lawful_vertical_then_horizontal: Permutation
    lawful_horizontal_then_vertical: Permutation
    naive_vertical_then_horizontal: Permutation
    naive_horizontal_then_vertical: Permutation

    @property
    def interchange_holds(self) -> bool:
        return self.lawful_vertical_then_horizontal == self.lawful_horizontal_then_vertical

    @property
    def naive_interchange_fails(self) -> bool:
        return self.naive_vertical_then_horizontal != self.naive_horizontal_then_vertical


def analyze_interchange_specimen() -> Strict2InterchangeReceipt:
    """Replay the frozen four-cell S3 interchange specimen exactly."""

    e = identity()
    a = transposition_12()
    b = transposition_23()

    left_bottom = TwoCell(h=a, g=e)  # e => a
    left_top = TwoCell(h=e, g=a)  # a => a
    right_bottom = TwoCell(h=e, g=e)  # e => e
    right_top = TwoCell(h=b, g=e)  # e => b

    left_vertical = vertical_compose(top=left_top, bottom=left_bottom)
    right_vertical = vertical_compose(top=right_top, bottom=right_bottom)
    lawful_vh = horizontal_compose(left=left_vertical, right=right_vertical)

    lawful_bottom_h = horizontal_compose(left=left_bottom, right=right_bottom)
    lawful_top_h = horizontal_compose(left=left_top, right=right_top)
    lawful_hv = vertical_compose(top=lawful_top_h, bottom=lawful_bottom_h)

    naive_vh = naive_horizontal_without_action(left=left_vertical, right=right_vertical)
    naive_bottom_h = naive_horizontal_without_action(left=left_bottom, right=right_bottom)
    naive_top_h = naive_horizontal_without_action(left=left_top, right=right_top)
    naive_hv = vertical_compose(top=naive_top_h, bottom=naive_bottom_h)

    return Strict2InterchangeReceipt(
        left_bottom_h=left_bottom.h,
        left_top_h=left_top.h,
        right_bottom_h=right_bottom.h,
        right_top_h=right_top.h,
        whiskered_right_top_h=conjugate(left_top.g, right_top.h),
        lawful_vertical_then_horizontal=lawful_vh.h,
        lawful_horizontal_then_vertical=lawful_hv.h,
        naive_vertical_then_horizontal=naive_vh.h,
        naive_horizontal_then_vertical=naive_hv.h,
    )
