"""PARALLEL-EQUIVALENCE-WITNESS-001: bounded witness-level rewrite receipt.

Research-only. Equal endpoints and equal quotient equality need not determine the
rewrite witness that licensed the identification.
"""

RULES = {
    "alpha": ("aa", "bb"),
    "rho": ("aa", "cc"),
    "sigma": ("cc", "bb"),
}


def apply(word, rule_name):
    lhs, rhs = RULES[rule_name]
    if word != lhs:
        raise ValueError(f"{rule_name} does not apply to {word}")
    return rhs


def replay(rule_names, start="aa"):
    states = [start]
    word = start
    for name in rule_names:
        word = apply(word, name)
        states.append(word)
    return {"rules": list(rule_names), "states": states, "target": word}


def receipt():
    direct = replay(["alpha"])
    composite = replay(["rho", "sigma"])
    return {
        "source": "aa",
        "target": "bb",
        "direct_witness": direct,
        "composite_witness": composite,
        "same_endpoints": direct["states"][0] == composite["states"][0]
        and direct["target"] == composite["target"],
        "same_induced_path_equivalence": True,
        "witnesses_distinct": direct["rules"] != composite["rules"],
        "non_claims": [
            "rewrite witness is not occurrence",
            "same quotient equality is not same derivation",
            "parallel 2-cells are not evidence of historical alternatives",
            "structural coherence is not semantic authority",
        ],
    }
