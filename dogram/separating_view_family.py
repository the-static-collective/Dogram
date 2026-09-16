"""Bounded research kernel for separating families of declared views.

Research-only: this module does not promote a public Dogram operator.
"""

from itertools import combinations


def signature(item, tests, selected=None):
    names = tuple(selected) if selected is not None else tuple(tests)
    return tuple(int(item in tests[name]) for name in names)


def collisions(items, tests, selected=None):
    names = tuple(selected) if selected is not None else tuple(tests)
    out = []
    for left, right in combinations(items, 2):
        if signature(left, tests, names) == signature(right, tests, names):
            out.append((left, right))
    return tuple(out)


def is_separating(items, tests, selected=None):
    return not collisions(items, tests, selected)


def minimum_separating_subfamilies(items, tests):
    names = tuple(tests)
    for size in range(len(names) + 1):
        winners = tuple(
            subset for subset in combinations(names, size)
            if is_separating(items, tests, subset)
        )
        if winners:
            return winners
    return tuple()


def frozen_specimen():
    items = ("x0", "x1", "x2", "x3")
    tests = {
        "t1": frozenset({"x1", "x2", "x3"}),
        "t2": frozenset({"x2", "x3"}),
        "t3": frozenset({"x3"}),
    }
    omissions = {
        name: collisions(items, tests, tuple(n for n in tests if n != name))
        for name in tests
    }
    return {
        "items": items,
        "tests": tests,
        "signatures": {item: signature(item, tests) for item in items},
        "full_collisions": collisions(items, tests),
        "minimum_subfamilies": minimum_separating_subfamilies(items, tests),
        "omission_collisions": omissions,
    }
