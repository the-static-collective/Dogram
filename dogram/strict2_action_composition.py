from __future__ import annotations

from dataclasses import dataclass


class Strict2ActionInputError(ValueError):
    pass


@dataclass(frozen=True)
class HorizontalComposite:
    left_h: int
    left_g: int
    right_h: int
    right_g: int
    acted_right_h: int
    composite_h: int
    total_g: int
    naive_h_without_action: int

    def to_data(self) -> dict[str, int]:
        return {
            "left_h": self.left_h,
            "left_g": self.left_g,
            "right_h": self.right_h,
            "right_g": self.right_g,
            "acted_right_h": self.acted_right_h,
            "composite_h": self.composite_h,
            "total_g": self.total_g,
            "naive_h_without_action": self.naive_h_without_action,
        }


@dataclass(frozen=True)
class Strict2ActionCompositionReceipt:
    even_factorization: HorizontalComposite
    odd_factorization: HorizontalComposite
    higher_composite_delta: int

    @property
    def same_outer_g(self) -> bool:
        return self.even_factorization.total_g == self.odd_factorization.total_g

    @property
    def same_h_labels(self) -> bool:
        return (
            self.even_factorization.left_h,
            self.even_factorization.right_h,
        ) == (
            self.odd_factorization.left_h,
            self.odd_factorization.right_h,
        )

    @property
    def naive_composition_collapses_delta(self) -> bool:
        return (
            self.even_factorization.naive_h_without_action
            == self.odd_factorization.naive_h_without_action
            and self.even_factorization.composite_h
            != self.odd_factorization.composite_h
        )

    def to_data(self) -> dict[str, object]:
        return {
            "crossed_module": {
                "H": "Z/3Z",
                "G": "Z/2Z",
                "boundary": "trivial",
                "action": "0 acts identically; 1 acts by inversion on Z/3Z",
            },
            "even_factorization": self.even_factorization.to_data(),
            "odd_factorization": self.odd_factorization.to_data(),
            "same_outer_g": self.same_outer_g,
            "same_h_labels": self.same_h_labels,
            "higher_composite_delta_mod_3": self.higher_composite_delta,
            "naive_composition_collapses_delta": self.naive_composition_collapses_delta,
        }


def _canonical(name: str, value: int, modulus: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Strict2ActionInputError(f"{name} must be an integer")
    if not 0 <= value < modulus:
        raise Strict2ActionInputError(
            f"{name} must be a canonical representative modulo {modulus}"
        )
    return value


def inversion_action_z3_by_z2(g: int, h: int) -> int:
    """The nontrivial element of Z/2Z acts on Z/3Z by inversion."""

    g = _canonical("g", g, 2)
    h = _canonical("h", h, 3)
    return h if g == 0 else (-h) % 3


def horizontal_compose(
    *, left_h: int, left_g: int, right_h: int, right_g: int
) -> HorizontalComposite:
    """Exact tensor/horizontal product in the frozen strict 2-group specimen.

    For the crossed module with trivial boundary H=Z/3Z -> G=Z/2Z and
    inversion action, the strict-2-group semidirect product is

        (h,g) tensor (h',g') = (h + g.h' mod 3, g + g' mod 2).

    The naive H sum is receipted only as a hostile control; it is not the
    declared composition law.
    """

    left_h = _canonical("left_h", left_h, 3)
    right_h = _canonical("right_h", right_h, 3)
    left_g = _canonical("left_g", left_g, 2)
    right_g = _canonical("right_g", right_g, 2)

    acted_right_h = inversion_action_z3_by_z2(left_g, right_h)
    return HorizontalComposite(
        left_h=left_h,
        left_g=left_g,
        right_h=right_h,
        right_g=right_g,
        acted_right_h=acted_right_h,
        composite_h=(left_h + acted_right_h) % 3,
        total_g=(left_g + right_g) % 2,
        naive_h_without_action=(left_h + right_h) % 3,
    )


def analyze_strict2_action_composition() -> Strict2ActionCompositionReceipt:
    """Compare two fixed factorizations with the same outer G product.

    Both cases use higher labels (1,1) and total G product 0.  The only
    changed datum is the internal G factorization: (0,0) versus (1,1).
    """

    even = horizontal_compose(left_h=1, left_g=0, right_h=1, right_g=0)
    odd = horizontal_compose(left_h=1, left_g=1, right_h=1, right_g=1)
    return Strict2ActionCompositionReceipt(
        even_factorization=even,
        odd_factorization=odd,
        higher_composite_delta=(odd.composite_h - even.composite_h) % 3,
    )
