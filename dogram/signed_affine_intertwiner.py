from fractions import Fraction


def adjacency_matrix(vertex_count, edges):
    matrix = [[Fraction(0) for _ in range(vertex_count)] for _ in range(vertex_count)]
    for left, right in edges:
        if left == right:
            raise ValueError("loops are outside this specimen")
        matrix[left][right] = Fraction(1)
        matrix[right][left] = Fraction(1)
    return matrix


def matmul(left, right):
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def degrees(matrix):
    return [sum(row) for row in matrix]


def row_sums(matrix):
    return [sum(row) for row in matrix]


def column_sums(matrix):
    return [sum(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]


def is_affine_intertwiner(left_adjacency, witness, right_adjacency):
    size = len(witness)
    ones = [Fraction(1)] * size
    return (
        row_sums(witness) == ones
        and column_sums(witness) == ones
        and matmul(left_adjacency, witness) == matmul(witness, right_adjacency)
    )


def has_negative_entry(matrix):
    return any(value < 0 for row in matrix for value in row)


def degree_transport(left_adjacency, witness, right_adjacency):
    left_degree = degrees(left_adjacency)
    right_degree = [[value] for value in degrees(right_adjacency)]
    transported = [row[0] for row in matmul(witness, right_degree)]
    return left_degree, transported


def isolate_nonnegative_obstruction(left_adjacency, right_adjacency):
    """Return the exact degree-convexity obstruction used by the frozen specimen.

    If the left graph has an isolated vertex and every right-graph vertex has
    positive degree, then no nonnegative row-stochastic X can satisfy
    d_left = X d_right at the isolated row. Any affine adjacency intertwiner
    must therefore use a negative coefficient somewhere in that row.
    """
    left_degree = degrees(left_adjacency)
    right_degree = degrees(right_adjacency)
    isolated = [index for index, degree in enumerate(left_degree) if degree == 0]
    return {
        "isolated_left_vertices": isolated,
        "right_min_degree": min(right_degree),
        "nonnegative_row_stochastic_impossible": bool(isolated) and min(right_degree) > 0,
    }


def total_walk_counts(adjacency, max_length):
    vector = [Fraction(1)] * len(adjacency)
    counts = []
    for _ in range(max_length + 1):
        counts.append(sum(vector))
        vector = [sum(adjacency[i][j] * vector[j] for j in range(len(adjacency))) for i in range(len(adjacency))]
    return counts
