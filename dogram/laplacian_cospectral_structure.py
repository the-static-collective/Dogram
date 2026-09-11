"""Bounded exact kernel for one finite Laplacian-cospectral structure specimen.

Research only. This module does not promote a public Dogram operator.
"""

from itertools import combinations


def _normalize_edges(vertex_count: int, edges):
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    normalized = set()
    for raw_u, raw_v in edges:
        u = int(raw_u)
        v = int(raw_v)
        if u == v:
            raise ValueError("self-loops are not supported")
        if not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise ValueError("edge endpoint outside declared vertex range")
        normalized.add((u, v) if u < v else (v, u))
    return tuple(sorted(normalized))


def _adjacency(vertex_count: int, edges):
    matrix = [[0 for _ in range(vertex_count)] for _ in range(vertex_count)]
    for u, v in edges:
        matrix[u][v] = 1
        matrix[v][u] = 1
    return matrix


def _laplacian(vertex_count: int, edges):
    adjacency = _adjacency(vertex_count, edges)
    degrees = [sum(row) for row in adjacency]
    return [
        [degrees[i] if i == j else -adjacency[i][j] for j in range(vertex_count)]
        for i in range(vertex_count)
    ]


def _matmul(a, b):
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def _trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def _characteristic_coefficients(matrix):
    """Return coefficients of det(lambda I - A) via Newton identities."""
    n = len(matrix)
    powers = []
    current = [row[:] for row in matrix]
    for _ in range(1, n + 1):
        powers.append(_trace(current))
        current = _matmul(current, matrix)

    coefficients = [1]
    for k in range(1, n + 1):
        numerator = sum(coefficients[k - i] * powers[i - 1] for i in range(1, k + 1))
        if numerator % k != 0:
            raise ArithmeticError("Newton-identity division was not exact")
        coefficients.append(-(numerator // k))
    return tuple(coefficients)


def _connected(adjacency):
    seen = {0}
    frontier = [0]
    while frontier:
        u = frontier.pop()
        for v, joined in enumerate(adjacency[u]):
            if joined and v not in seen:
                seen.add(v)
                frontier.append(v)
    return len(seen) == len(adjacency)


def _triangle_count(adjacency):
    count = 0
    for a, b, c in combinations(range(len(adjacency)), 3):
        if adjacency[a][b] and adjacency[b][c] and adjacency[a][c]:
            count += 1
    return count


def graph_receipt(vertex_count: int, edges):
    """Compute exact finite structural and Laplacian receipts for a simple graph."""
    normalized = _normalize_edges(vertex_count, edges)
    adjacency = _adjacency(vertex_count, normalized)
    degrees = tuple(sorted((sum(row) for row in adjacency), reverse=True))
    coefficients = _characteristic_coefficients(_laplacian(vertex_count, normalized))

    # Matrix-tree theorem: for a connected n-vertex graph, the product of
    # nonzero Laplacian eigenvalues divided by n equals the spanning-tree count.
    # For det(lambda I - L), c_{n-1} = (-1)^(n-1) * product(nonzero eigenvalues).
    connected = _connected(adjacency)
    spanning_tree_count = None
    if connected:
        product_nonzero = ((-1) ** (vertex_count - 1)) * coefficients[-2]
        if product_nonzero % vertex_count != 0:
            raise ArithmeticError("spectrum-derived spanning-tree count was not integral")
        spanning_tree_count = product_nonzero // vertex_count

    return {
        "vertex_count": vertex_count,
        "edge_count": len(normalized),
        "edges": normalized,
        "connected": connected,
        "degree_sequence": degrees,
        "triangle_count": _triangle_count(adjacency),
        "laplacian_characteristic_coefficients": coefficients,
        "spanning_tree_count_from_spectrum": spanning_tree_count,
    }
