from __future__ import annotations

from dataclasses import dataclass


class CyclicCrossedModuleInputError(ValueError):
    pass


@dataclass(frozen=True)
class CyclicFaceLiftReceipt:
    h_modulus: int
    g_modulus: int
    boundary_multiplier: int
    boundary_value: int
    kernel: tuple[int, ...]
    face_lifts: tuple[int, ...]
    boundary_images: tuple[int, ...]
    lift_deltas: tuple[int, ...]

    @property
    def boundary_forgets_higher_lift(self) -> bool:
        return len(self.face_lifts) > 1

    def to_data(self) -> dict[str, object]:
        return {
            "crossed_module": {
                "H": f"Z/{self.h_modulus}Z",
                "G": f"Z/{self.g_modulus}Z",
                "boundary": (
                    f"h -> {self.boundary_multiplier}*h mod {self.g_modulus}"
                ),
                "action": "trivial",
            },
            "boundary_value": self.boundary_value,
            "kernel": list(self.kernel),
            "face_lifts": list(self.face_lifts),
            "boundary_images": list(self.boundary_images),
            "lift_deltas": list(self.lift_deltas),
            "boundary_forgets_higher_lift": self.boundary_forgets_higher_lift,
        }


def _require_int(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CyclicCrossedModuleInputError(f"{name} must be an integer")
    return value


def analyze_cyclic_face_lifts(
    h_modulus: int,
    g_modulus: int,
    boundary_multiplier: int,
    boundary_value: int,
) -> CyclicFaceLiftReceipt:
    """Receipt fibers of a declared cyclic crossed-module boundary map.

    The crossed module is restricted to cyclic groups written additively with
    trivial G-action on H.  The boundary map is

        partial(h) = boundary_multiplier * h mod g_modulus.

    This is well-defined on Z/h_modulus exactly when g_modulus divides
    boundary_multiplier * h_modulus.  For cyclic (therefore abelian) H and G,
    the trivial action then satisfies both Peiffer identities.
    """

    h_modulus = _require_int("h_modulus", h_modulus)
    g_modulus = _require_int("g_modulus", g_modulus)
    boundary_multiplier = _require_int("boundary_multiplier", boundary_multiplier)
    boundary_value = _require_int("boundary_value", boundary_value)

    if h_modulus <= 0 or g_modulus <= 0:
        raise CyclicCrossedModuleInputError("group moduli must be positive")
    if not 0 <= boundary_value < g_modulus:
        raise CyclicCrossedModuleInputError(
            "boundary_value must be the canonical representative in G"
        )
    if (boundary_multiplier * h_modulus) % g_modulus != 0:
        raise CyclicCrossedModuleInputError(
            "boundary formula is not well-defined on the declared cyclic H"
        )

    def boundary(h: int) -> int:
        return (boundary_multiplier * h) % g_modulus

    kernel = tuple(h for h in range(h_modulus) if boundary(h) == 0)
    face_lifts = tuple(
        h for h in range(h_modulus) if boundary(h) == boundary_value
    )
    boundary_images = tuple(boundary(h) for h in face_lifts)

    deltas = {
        (right - left) % h_modulus
        for index, left in enumerate(face_lifts)
        for right in face_lifts[index + 1 :]
        if (right - left) % h_modulus != 0
    }

    return CyclicFaceLiftReceipt(
        h_modulus=h_modulus,
        g_modulus=g_modulus,
        boundary_multiplier=boundary_multiplier,
        boundary_value=boundary_value,
        kernel=kernel,
        face_lifts=face_lifts,
        boundary_images=boundary_images,
        lift_deltas=tuple(sorted(deltas)),
    )
