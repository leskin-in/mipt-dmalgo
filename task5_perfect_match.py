#!/usr/bin/env python3

import math
import random
import copy


class Float1997:
    """
    A float over Z1997 (module 1997) field
    """
    PRECISION_ROUND = 16

    def __init__(self, n: float):
        self.n = math.fmod(n, 1997.)

    def __add__(self, other):
        return Float1997(math.fsum((self.n, other.n)))

    def __sub__(self, other):
        return Float1997(math.fsum((self.n, -other.n)))

    def __mul__(self, other):
        return Float1997(self.n * other.n)

    def __truediv__(self, other):
        return Float1997(self.n / other.n)

    def __float__(self):
        return self.n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'F1997({})'.format(self.n)

    def __gt__(self, other):
        return round(self.n, Float1997.PRECISION_ROUND) > round(other.n, Float1997.PRECISION_ROUND)

    def __lt__(self, other):
        return round(self.n, Float1997.PRECISION_ROUND) < round(other.n, Float1997.PRECISION_ROUND)

    def __eq__(self, other):
        return round(self.n, Float1997.PRECISION_ROUND) == round(other.n, Float1997.PRECISION_ROUND)

    def __abs__(self):
        if self < Float1997(0.0):
            return Float1997(-self.n)
        return self


def _input_graph():
    """
    Input a matrix from stdin
    :return: an empty matrix and a set of pairs (int, int) of coordinates of edges
    """
    n = int(input())

    edges = []
    max_vertices_indexes = [-1, -1]
    for _ in range(n):
        edge = list(map(int, input().split()))
        max_vertices_indexes[0] = edge[0] if max_vertices_indexes[0] < edge[0] else max_vertices_indexes[0]
        max_vertices_indexes[1] = edge[1] if max_vertices_indexes[1] < edge[1] else max_vertices_indexes[1]
        edges.append(edge)

    if max_vertices_indexes[0] != max_vertices_indexes[1]:
        raise Exception(
            "The left and right graph parts have different sizes {} and {}".format(
                max_vertices_indexes[0], max_vertices_indexes[1]
            )
        )

    graph_matrix_size = max_vertices_indexes[0] + 1

    graph = [[Float1997(0.0) for _ in range(graph_matrix_size)] for _ in range(graph_matrix_size)]

    return graph, edges


def _check_matrix_det_0(mat: list) -> bool:
    """
    Check the given matrix has a determinant equal to 0, using the Gauss elimination method
    """
    r = 0
    c = 0
    matrix_size = len(mat)

    zero_row_found = False

    while r < matrix_size and c < matrix_size:
        # Find the maximum row
        r_i_max = None
        r_i_max_value = Float1997(0.0)
        for r_i in range(r, matrix_size):
            r_i_abs = abs(mat[r_i][c])
            if r_i_abs > r_i_max_value:
                r_i_max = r_i
                r_i_max_value = r_i_abs
        # Check the maximum value is not zero
        if r_i_max_value == Float1997(0.0):
            column_zero_row_found = True
            for r_i in range(r):
                if not (mat[r_i][c] == Float1997(0.0)):
                    column_zero_row_found = False
                    break
            if column_zero_row_found:
                zero_row_found = True
                break
            c += 1
            continue
        # Swap the maximum and the current rows
        if r_i_max != r:
            r_tmp = mat[r_i_max]
            mat[r_i_max] = mat[r]
            mat[r] = r_tmp

        # Divide all rows below
        for r_i in range(r + 1, matrix_size):
            multiplier = mat[r_i][c] / mat[r][c]
            mat[r_i][c] = Float1997(0.0)
            for c_i in range(c + 1, matrix_size):
                mat[r_i][c_i] = mat[r_i][c_i] - (mat[r][c] * Float1997(multiplier))
            # Check the resulting row is not a zero-row. If it is, set the flag variable and break from the cycle
            row_zero_row_found = True
            for c_i in range(c + 1, matrix_size):
                if not (mat[r_i][c_i] == Float1997(0.0)):
                    row_zero_row_found = False
                    break
            if row_zero_row_found:
                zero_row_found = True
                break

        # Check if zero_row_found and increase iterator indexes
        if zero_row_found:
            break
        r += 1
        c += 1

    return zero_row_found


PRECISION = 8  # Do this number of repeated random iterator calculations before concluding the matrix' determinant is 0


def _is_perfect_match_exists(standard_graph, edges) -> bool:
    """
    Check if the given graph contains a perfect match
    """
    perfect_match_exists = False

    for _ in range(PRECISION):
        # Form a "randomized" graph according to Corollary and Schwartz-Zippel, as defined by Kozen
        graph = copy.deepcopy(standard_graph)
        for edge in edges:
            val = float(random.randint(-1997, 1997))
            graph[edge[0]][edge[1]] = Float1997(val)

        # Check if the randomized matrix determinant is zero
        if not _check_matrix_det_0(graph):
            perfect_match_exists = True
            break

    return perfect_match_exists


def main():
    standard_graph, edges = _input_graph()
    perfect_match_exists = _is_perfect_match_exists(standard_graph, edges)

    if perfect_match_exists:
        print('yes')
    else:
        print('no')


if __name__ == '__main__':
    main()
