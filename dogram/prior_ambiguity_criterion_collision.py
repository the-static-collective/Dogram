from fractions import Fraction


def _normalized_prior(prior, width):
    if prior is None or len(prior) != width:
        raise ValueError("prior must match the policy state width")
    values = tuple(Fraction(value) for value in prior)
    if any(value < 0 for value in values) or sum(values, Fraction(0, 1)) != 1:
        raise ValueError("prior must be nonnegative and normalized")
    return values


def expected_cost(policy_costs, prior):
    costs = tuple(Fraction(value) for value in policy_costs)
    weights = _normalized_prior(prior, len(costs))
    return sum((cost * weight for cost, weight in zip(costs, weights)), Fraction(0, 1))


def bayes_costs(policies, prior):
    return {name: expected_cost(costs, prior) for name, costs in policies.items()}


def _unique_minimum(values):
    minimum = min(values.values())
    winners = [name for name, value in values.items() if value == minimum]
    if len(winners) != 1:
        raise ValueError("criterion does not have a unique winner")
    return winners[0]


def unique_bayes_winner(policies, prior):
    return _unique_minimum(bayes_costs(policies, prior))


def max_expected_costs(policies, ambiguity_priors):
    priors = tuple(ambiguity_priors)
    if not priors:
        raise ValueError("ambiguity set must contain at least one declared prior")
    return {
        name: max(expected_cost(costs, prior) for prior in priors)
        for name, costs in policies.items()
    }


def robust_minimax_winner(policies, ambiguity_priors):
    return _unique_minimum(max_expected_costs(policies, ambiguity_priors))


def max_regrets(policies, ambiguity_priors):
    priors = tuple(ambiguity_priors)
    if not priors:
        raise ValueError("ambiguity set must contain at least one declared prior")

    maxima = {name: Fraction(0, 1) for name in policies}
    for prior in priors:
        costs = {name: expected_cost(policy, prior) for name, policy in policies.items()}
        oracle = min(costs.values())
        for name, value in costs.items():
            maxima[name] = max(maxima[name], value - oracle)
    return maxima


def minimax_regret_winner(policies, ambiguity_priors):
    return _unique_minimum(max_regrets(policies, ambiguity_priors))
