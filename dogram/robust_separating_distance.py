"""Bounded research kernel: separating signatures as a finite binary code."""
from itertools import combinations


def hamming(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError("signatures must have equal length")
    return sum(x != y for x, y in zip(a, b))


def pair_receipt(signatures: dict[str, str]) -> list[dict[str, object]]:
    rows = []
    for left, right in combinations(sorted(signatures), 2):
        rows.append({"pair": [left, right], "distance": hamming(signatures[left], signatures[right])})
    return rows


def minimum_distance(signatures: dict[str, str]) -> int:
    rows = pair_receipt(signatures)
    if not rows:
        raise ValueError("need at least two states")
    return min(int(row["distance"]) for row in rows)


def erase(signature: str, coordinates: tuple[int, ...]) -> str:
    removed = set(coordinates)
    return "".join(bit for i, bit in enumerate(signature) if i not in removed)


def all_erasures_separate(signatures: dict[str, str], erasures: int) -> bool:
    width = len(next(iter(signatures.values())))
    for coordinates in combinations(range(width), erasures):
        projected = [erase(signatures[state], coordinates) for state in sorted(signatures)]
        if len(set(projected)) != len(projected):
            return False
    return True


SPECIMEN = {"x0": "000", "x1": "011", "x2": "101", "x3": "110"}
