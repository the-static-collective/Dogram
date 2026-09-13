from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReorientationComparison:
    equivalent: bool
    global_flip: int | None
    reoriented_elements: tuple[str, ...]
    obstruction_bases: tuple[tuple[str, ...], ...]

    def reproduces_right(
        self,
        bases: tuple[tuple[str, ...], ...],
        left_signs: tuple[int, ...],
        right_signs: tuple[int, ...],
    ) -> bool:
        if not self.equivalent or self.global_flip not in (-1, 1):
            return False
        if len(bases) != len(left_signs) or len(bases) != len(right_signs):
            return False
        flipped = set(self.reoriented_elements)
        for basis, left, right in zip(bases, left_signs, right_signs, strict=True):
            factor = self.global_flip
            for label in basis:
                if label in flipped:
                    factor *= -1
            if factor * left != right:
                return False
        return True


def _validate(
    bases: tuple[tuple[str, ...], ...],
    left_signs: tuple[int, ...],
    right_signs: tuple[int, ...],
) -> tuple[str, ...]:
    if not bases:
        raise ValueError("at least one basis is required")
    if len(bases) != len(left_signs) or len(bases) != len(right_signs):
        raise ValueError("bases and sign tuples must have equal length")
    if any(sign not in (-1, 1) for sign in left_signs + right_signs):
        raise ValueError("signs must be +1 or -1")
    if len(set(bases)) != len(bases):
        raise ValueError("bases must be unique")
    rank = len(bases[0])
    if rank == 0 or any(len(basis) != rank for basis in bases):
        raise ValueError("all bases must have the same positive size")
    if any(len(set(basis)) != len(basis) for basis in bases):
        raise ValueError("a basis cannot repeat a ground element")
    return tuple(sorted({label for basis in bases for label in basis}))


def compare_reorientation_signatures(
    bases: tuple[tuple[str, ...], ...],
    left_signs: tuple[int, ...],
    right_signs: tuple[int, ...],
) -> ReorientationComparison:
    """Compare sign tables modulo ground-element reorientation and global sign.

    The equations are solved exactly over GF(2). A sign mismatch on basis B is
    represented by

        mismatch(B) = global + sum(element_flip[e] for e in B) mod 2.

    If inconsistent, the returned obstruction bases are an exact parity
    certificate: they occur in even count globally, each ground element occurs
    an even number of times, yet the product of left signs and right signs over
    those bases differs.
    """

    labels = _validate(bases, left_signs, right_signs)
    column = {label: index for index, label in enumerate(labels)}
    global_column = len(labels)
    variable_count = len(labels) + 1

    rows: list[list[int]] = []
    combinations: list[int] = []
    for index, (basis, left, right) in enumerate(
        zip(bases, left_signs, right_signs, strict=True)
    ):
        row = [0] * (variable_count + 1)
        for label in basis:
            row[column[label]] ^= 1
        row[global_column] = 1
        row[-1] = 0 if left == right else 1
        rows.append(row)
        combinations.append(1 << index)

    pivot_rows: dict[int, int] = {}
    next_row = 0
    for col in range(variable_count):
        pivot = next((r for r in range(next_row, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[next_row], rows[pivot] = rows[pivot], rows[next_row]
        combinations[next_row], combinations[pivot] = (
            combinations[pivot],
            combinations[next_row],
        )

        for row_index in range(len(rows)):
            if row_index != next_row and rows[row_index][col]:
                rows[row_index] = [
                    left_bit ^ right_bit
                    for left_bit, right_bit in zip(
                        rows[row_index], rows[next_row], strict=True
                    )
                ]
                combinations[row_index] ^= combinations[next_row]

        pivot_rows[col] = next_row
        next_row += 1
        if next_row == len(rows):
            break

    for row, combination in zip(rows, combinations, strict=True):
        if not any(row[:variable_count]) and row[-1]:
            obstruction = tuple(
                bases[index]
                for index in range(len(bases))
                if (combination >> index) & 1
            )
            return ReorientationComparison(
                equivalent=False,
                global_flip=None,
                reoriented_elements=(),
                obstruction_bases=obstruction,
            )

    solution = [0] * variable_count
    for col, row_index in pivot_rows.items():
        solution[col] = rows[row_index][-1]

    reoriented = tuple(label for label in labels if solution[column[label]])
    global_flip = -1 if solution[global_column] else 1
    result = ReorientationComparison(
        equivalent=True,
        global_flip=global_flip,
        reoriented_elements=reoriented,
        obstruction_bases=(),
    )
    if not result.reproduces_right(bases, left_signs, right_signs):
        raise AssertionError("internal reorientation solution failed replay")
    return result


__all__ = ["ReorientationComparison", "compare_reorientation_signatures"]
