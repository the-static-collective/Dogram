from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass
class FieldReductionInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class PrimeFieldBasisComparison:
    rank: int
    prime_a: int
    prime_b: int
    prime_a_basis_count: int
    prime_b_basis_count: int
    only_a: tuple[tuple[str, ...], ...]
    only_b: tuple[tuple[str, ...], ...]
    changed_subsets: tuple[tuple[str, ...], ...]

    def to_data(self) -> dict[str, object]:
        return {
            "rank": self.rank,
            "prime_a": self.prime_a,
            "prime_b": self.prime_b,
            "prime_a_basis_count": self.prime_a_basis_count,
            "prime_b_basis_count": self.prime_b_basis_count,
            "only_a": self.only_a,
            "only_b": self.only_b,
            "changed_subsets": self.changed_subsets,
        }


def _is_prime(value: int) -> bool:
    if not isinstance(value, int) or isinstance(value, bool) or value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _validate_prime(value: int) -> None:
    if not _is_prime(value):
        raise FieldReductionInputError(
            "FIELD_NOT_PRIME",
            "prime-field reduction requires a prime characteristic",
        )


def _validate_matrix_and_labels(
    matrix: tuple[tuple[int, ...], ...], labels: tuple[str, ...], rank: int
) -> None:
    if not matrix or not matrix[0]:
        raise FieldReductionInputError("EMPTY_MATRIX", "matrix must be nonempty")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise FieldReductionInputError("RAGGED_MATRIX", "matrix rows must have equal width")
    if any(
        not isinstance(value, int) or isinstance(value, bool)
        for row in matrix
        for value in row
    ):
        raise FieldReductionInputError("NON_INTEGER_ENTRY", "matrix entries must be integers")
    if len(labels) != width or len(set(labels)) != len(labels):
        raise FieldReductionInputError(
            "INVALID_LABELS", "labels must be unique and match the column count"
        )
    if not isinstance(rank, int) or isinstance(rank, bool) or rank <= 0:
        raise FieldReductionInputError("INVALID_RANK", "rank must be a positive integer")
    if rank > len(matrix) or rank > width:
        raise FieldReductionInputError(
            "INVALID_RANK", "rank cannot exceed row or column count"
        )


def _rank_mod_prime(rows: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in rows]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0

    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column] % prime),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [(value * inverse) % prime for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column] % prime
            if factor:
                work[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def _basis_support_mod_prime(
    matrix: tuple[tuple[int, ...], ...],
    labels: tuple[str, ...],
    rank: int,
    prime: int,
) -> tuple[tuple[str, ...], ...]:
    support: list[tuple[str, ...]] = []
    for columns in combinations(range(len(labels)), rank):
        submatrix = [[row[column] for column in columns] for row in matrix]
        if _rank_mod_prime(submatrix, prime) == rank:
            support.append(tuple(labels[column] for column in columns))
    return tuple(support)


def compare_prime_field_basis_support(
    matrix: tuple[tuple[int, ...], ...],
    labels: tuple[str, ...],
    *,
    rank: int,
    prime_a: int,
    prime_b: int,
) -> PrimeFieldBasisComparison:
    """Compare rank-sized basis support after reducing one integer matrix mod p."""

    _validate_matrix_and_labels(matrix, labels, rank)
    _validate_prime(prime_a)
    _validate_prime(prime_b)

    support_a = _basis_support_mod_prime(matrix, labels, rank, prime_a)
    support_b = _basis_support_mod_prime(matrix, labels, rank, prime_b)
    set_a = set(support_a)
    set_b = set(support_b)
    only_a = tuple(sorted(set_a - set_b))
    only_b = tuple(sorted(set_b - set_a))
    changed = tuple(sorted(set_a ^ set_b))

    return PrimeFieldBasisComparison(
        rank=rank,
        prime_a=prime_a,
        prime_b=prime_b,
        prime_a_basis_count=len(support_a),
        prime_b_basis_count=len(support_b),
        only_a=only_a,
        only_b=only_b,
        changed_subsets=changed,
    )


__all__ = [
    "FieldReductionInputError",
    "PrimeFieldBasisComparison",
    "compare_prime_field_basis_support",
]
