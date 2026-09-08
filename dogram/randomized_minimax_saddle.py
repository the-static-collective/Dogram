from fractions import Fraction


def _fractions(values):
    return tuple(value if isinstance(value, Fraction) else Fraction(value) for value in values)


def _validate_prior(prior, dimension):
    values = _fractions(prior)
    if len(values) != dimension:
        raise ValueError("prior dimension must match cost vector")
    if any(value < 0 for value in values):
        raise ValueError("prior weights must be nonnegative")
    if sum(values, Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("prior weights must sum to one")
    return values


def _validate_policies(policies):
    if not policies:
        raise ValueError("at least one policy is required")
    lengths = {len(costs) for costs in policies.values()}
    if len(lengths) != 1:
        raise ValueError("all policy cost vectors must have the same dimension")
    dimension = lengths.pop()
    if dimension == 0:
        raise ValueError("policy cost vectors must be nonempty")
    return dimension


def expected_cost(costs, prior):
    costs = _fractions(costs)
    prior = _validate_prior(prior, len(costs))
    return sum((cost * weight for cost, weight in zip(costs, prior)), Fraction(0, 1))


def pure_minimax(policies, priors):
    dimension = _validate_policies(policies)
    priors = tuple(_validate_prior(prior, dimension) for prior in priors)
    if not priors:
        raise ValueError("at least one ambiguity vertex is required")
    maxima = {
        name: max(expected_cost(costs, prior) for prior in priors)
        for name, costs in policies.items()
    }
    best_value = min(maxima.values())
    winners = sorted(name for name, value in maxima.items() if value == best_value)
    if len(winners) != 1:
        raise ValueError("pure minimax winner is not unique")
    return winners[0], best_value, maxima


def mixed_cost_vector(policies, mixture):
    dimension = _validate_policies(policies)
    if set(mixture) != set(policies):
        raise ValueError("mixture must declare one weight for every policy")
    weights = {
        name: weight if isinstance(weight, Fraction) else Fraction(weight)
        for name, weight in mixture.items()
    }
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("mixture weights must be nonnegative")
    if sum(weights.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("mixture weights must sum to one")
    return tuple(
        sum(
            (weights[name] * Fraction(policies[name][index]) for name in policies),
            Fraction(0, 1),
        )
        for index in range(dimension)
    )


def _solve_square(matrix, rhs):
    n = len(rhs)
    augmented = [
        [Fraction(value) for value in matrix[row]] + [Fraction(rhs[row])]
        for row in range(n)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n) if augmented[row][column]), None)
        if pivot is None:
            raise ValueError("ambiguity vertices are affinely dependent for this solve")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    current - factor * pivot_entry
                    for current, pivot_entry in zip(augmented[row], augmented[column])
                ]
    return tuple(augmented[row][-1] for row in range(n))


def ambiguity_barycentric_weights(prior, vertices):
    vertices = tuple(_fractions(vertex) for vertex in vertices)
    if not vertices:
        raise ValueError("at least one ambiguity vertex is required")
    dimension = len(vertices[0])
    if len(vertices) != dimension or any(len(vertex) != dimension for vertex in vertices):
        raise ValueError("this bounded kernel requires a square vertex system")
    prior = _validate_prior(prior, dimension)
    matrix = tuple(
        tuple(vertices[column][row] for column in range(dimension))
        for row in range(dimension)
    )
    return _solve_square(matrix, prior)


def verify_saddle(policies, ambiguity_vertices, mixture, least_favorable_prior):
    dimension = _validate_policies(policies)
    ambiguity_vertices = tuple(
        _validate_prior(prior, dimension) for prior in ambiguity_vertices
    )
    pure_winner, pure_value, maxima = pure_minimax(policies, ambiguity_vertices)
    mixed_vector = mixed_cost_vector(policies, mixture)
    mixed_value = max(expected_cost(mixed_vector, prior) for prior in ambiguity_vertices)

    least_favorable_prior = _validate_prior(least_favorable_prior, dimension)
    barycentric = ambiguity_barycentric_weights(least_favorable_prior, ambiguity_vertices)
    if any(weight < 0 for weight in barycentric) or sum(barycentric, Fraction(0, 1)) != 1:
        raise ValueError("least-favorable prior is outside the declared ambiguity hull")

    pure_risks_at_witness = {
        name: expected_cost(costs, least_favorable_prior)
        for name, costs in policies.items()
    }
    maximin_value = min(pure_risks_at_witness.values())

    return {
        "pure_minimax_winner": pure_winner,
        "pure_minimax_value": pure_value,
        "pure_policy_maxima": maxima,
        "mixed_state_cost_vector": mixed_vector,
        "mixed_minimax_value": mixed_value,
        "least_favorable_prior": least_favorable_prior,
        "least_favorable_barycentric_weights": barycentric,
        "pure_risks_at_least_favorable_prior": pure_risks_at_witness,
        "maximin_value": maximin_value,
        "strict_gap": pure_value > mixed_value,
        "saddle_closed": mixed_value == maximin_value,
    }
