"""PARALLEL-COHERENCE-WITNESS-001.

Finite globular/computadic specimen.  This records supplied generators only;
it does not interpret any cell as occurrence, evidence, causation, or truth.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cell2:
    name: str
    source: str
    target: str

@dataclass(frozen=True)
class Cell3:
    name: str
    source: Cell2
    target: Cell2


def specimen():
    alpha = Cell2("alpha", "aa", "bb")
    beta = Cell2("beta", "aa", "bb")
    gamma = Cell3("Gamma", alpha, beta)
    delta = Cell3("Delta", alpha, beta)
    return alpha, beta, gamma, delta


def receipt():
    alpha, beta, gamma, delta = specimen()
    return {
        "parallel_2_cells": alpha != beta and (alpha.source, alpha.target) == (beta.source, beta.target),
        "parallel_3_cells": gamma != delta and (gamma.source, gamma.target) == (delta.source, delta.target),
        "same_2_cell_equivalence": (gamma.source, gamma.target) == (delta.source, delta.target),
        "same_coherence_witness": gamma == delta,
        "seal": "SAME WITNESS EQUIVALENCE != SAME COHERENCE WITNESS",
    }

if __name__ == "__main__":
    import json
    print(json.dumps(receipt(), indent=2))
