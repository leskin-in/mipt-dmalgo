#!/usr/bin/env python3

import math


def main():
    p = float(input())
    e = int(input())

    edges = []
    for _ in range(e):
        edges.append(input().split(' '))

    a_matrix, mapping = _prepare_a_matrix(edges)
    pr_matrix = _convert_a_to_pr_matrix(a_matrix, p)

    result = calculate_pagerank(pr_matrix)

    for i in range(len(result)):
        print(mapping[i], result[i])


class Matrix:
    def __init__(self, values: list, mapping: list or None = None):
        """
        :param values: a two-dimensional list
        :param mapping: a list, where an element at the i-th position denotes i-th graph vertex
        """
        self.m = values
        self.L = len(values)
        self.mapping = mapping

    def __add__(self, other):
        if self.L != other.L:
            raise Exception(
                "__add__ is called on matrices of different size. Arguments: {}; {}".format(self.m, other.m)
            )

        return Matrix([[self.m[i1][i2] + other.m[i1][i2] for i2 in range(self.L)] for i1 in range(self.L)])

    def __sub__(self, other):
        if self.L != other.L:
            raise Exception(
                "__sub__ is called on matrices of different size. Arguments: {}; {}".format(self.m, other.m)
            )

        return Matrix([[self.m[i1][i2] - other.m[i1][i2] for i2 in range(self.L)] for i1 in range(self.L)])

    def multiply_by_vector(self, v: list) -> list:
        """
        Multiply this matrix by the given vector
        """
        result = []
        for i in range(self.L):
            result.append(0.0)
            for j in range(self.L):
                result[-1] += self.m[i][j] * v[j]
        return result

    def __str__(self):
        return '\n'.join([' '.join([str(self.m[i][j]) for j in range(self.L)]) for i in range(self.L)])


def _prepare_a_matrix(edges: list) -> tuple:
    """
    Prepare A - the matrix required for PageRank matrix calculation
    """
    graph_map = {}
    vertices = set()
    for e in edges:
        map_entry_0 = graph_map.get(e[0], [])
        map_entry_0.append(e[1])
        graph_map[e[0]] = map_entry_0
        vertices.add(e[0])
        vertices.add(e[1])

    values = [[0.0 for _ in range(len(vertices))] for _ in range(len(vertices))]
    vertices_mapping = []
    vertices_reverse_mapping = {}
    for v in vertices:
        vertices_reverse_mapping[v] = len(vertices_mapping)
        vertices_mapping.append(v)

    equal_importance = 1.0 / float(len(vertices))

    for i in range(len(vertices_mapping)):
        if vertices_mapping[i] not in graph_map:
            # This is a dangling vertex, add equal importance
            for j in range(len(vertices)):
                values[j][i] = equal_importance
            continue
        outgoing = graph_map[vertices_mapping[i]]
        outgoing_value = 1.0 / float(len(outgoing))
        for d_vertex in outgoing:
            values[vertices_reverse_mapping[d_vertex]][i] = outgoing_value

    return Matrix(values), vertices_mapping


def _convert_a_to_pr_matrix(a_matrix: Matrix, p: float) -> Matrix:
    """
    Convert the A matrix to a PageRank matrix using the given regularisation parameter 'p'
    """
    n = float(a_matrix.L)
    filler_value = p / n

    filler_matrix = Matrix([[filler_value for _ in range(a_matrix.L)] for _ in range(a_matrix.L)], None)

    a_multiplier = 1.0 - p
    for i in range(a_matrix.L):
        for j in range(a_matrix.L):
            a_matrix.m[i][j] *= a_multiplier

    result = a_matrix + filler_matrix
    return result


VECTOR_DIFFERENCE_TOLERANCE = 0.0


def _check_vector_difference(a: list, b: list) -> bool:
    """
    Check if the two given vectors are different enough
    """
    for i in range(len(a)):
        if math.fabs(a[i] - b[i]) > VECTOR_DIFFERENCE_TOLERANCE:
            return False
    return True


def calculate_pagerank(pr_matrix: Matrix) -> list:
    """
    Calculate the pagerank for all vertices in the given 'pr_matrix'
    :return: a list of PageRanks, where i-th value corresponds to the i-th vertex in 'pr_matrix.mapping'
    """
    result_initial_value = 1.0 / float(pr_matrix.L)
    result = [result_initial_value for _ in range(pr_matrix.L)]

    while True:
        result_current = pr_matrix.multiply_by_vector(result)
        if not _check_vector_difference(result, result_current):
            result = result_current
        else:
            break

    return result


if __name__ == '__main__':
    main()
