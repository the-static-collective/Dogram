"""PARALLEL-ARROW-FACTORIZATION-001.

Finite hostile specimen: the one-object groupoid BV4 for the Klein four group.
This is structural mathematics only. Arrows are not occurrences or evidence.
"""

from __future__ import annotations

from dataclasses import dataclass

Element = tuple[int, int]
E: Element = (0, 0)
A: Element = (1, 0)
B: Element = (0, 1)


def compose(left: Element, right: Element) -> Element:
    """Composition in V4 = componentwise addition mod 2."""
    return ((left[0] + right[0]) % 2, (left[1] + right[1]) % 2)


@dataclass(frozen=True)
class PathReceipt:
    objects: tuple[str, str, str]
    arrows: tuple[Element, Element]
    composite: Element


def receipt(first: Element, second: Element) -> PathReceipt:
    return PathReceipt(
        objects=("X", "X", "X"),
        arrows=(first, second),
        composite=compose(second, first),
    )


def hostile_pair() -> tuple[PathReceipt, PathReceipt]:
    """Same object sequence and composite; distinct nonidentity arrow paths."""
    return receipt(A, A), receipt(B, B)


def verify() -> dict[str, object]:
    left, right = hostile_pair()
    return {
        "same_objects": left.objects == right.objects,
        "same_composite": left.composite == right.composite == E,
        "different_arrows": left.arrows != right.arrows,
        "all_arrows_nonidentity": all(x != E for x in left.arrows + right.arrows),
        "left": left,
        "right": right,
    }


if __name__ == "__main__":
    print(verify())
