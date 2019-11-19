#!/usr/bin/env python3

import math


def main():
    e = int(input())

    edges = []
    max_vertex_index = -1
    for _ in range(e):
        edges.append(list(map(int, input().split())))
        if edges[-1][0] > max_vertex_index:
            max_vertex_index = edges[-1][0]
        if edges[-1][1] > max_vertex_index:
            max_vertex_index = edges[-1][1]

    graph = [[] for _ in range(max_vertex_index + 1)]
    for e in edges:
        graph[e[0]].append(e[1])
        graph[e[1]].append(e[0])

    cycle_finish = find_border_cycle(graph)
    graph = planarize_border_and_prepare_graph(graph, cycle_finish)
    graph = planarize_graph(graph, cycle_finish + 1)

    for i in range(len(graph)):
        print(i, graph[i][1][0], graph[i][1][1])


def find_border_cycle(graph: list) -> int:
    """
    Find a cycle which is a border of some edge
    :returns: the index of a vertex which is the last vertex in the cycle
    """
    cycle = set()
    cycle_finish_index = -1
    previous_v = -1

    i = 0
    while i < len(graph) and cycle_finish_index < 0:
        cycle.add(i)
        for v in cycle:
            if v != previous_v and v in graph[i]:
                cycle_finish_index = i
        previous_v = i
        i += 1

    return cycle_finish_index


CIRCLE_RADIUS = 1.0


def _put_points_on_circle(graph: list, border_cycle_finish: int) -> list:
    """
    Put points from the border cycle on a circle
    """
    angle_diff = (2.0 * math.pi) / float(border_cycle_finish + 1)
    angle = 0.0
    for i in range(border_cycle_finish + 1):
        graph[i][1] = [math.cos(angle) * CIRCLE_RADIUS, math.sin(angle) * CIRCLE_RADIUS]
        angle += angle_diff
    return graph


def planarize_border_and_prepare_graph(graph: list, border_cycle_finish: int) -> list:
    """
    Prepare the 'graph' for planarization and planarize its border cycle
    """
    for i in range(len(graph)):
        graph[i] = [graph[i], [0.0, 0.0]]

    graph = _put_points_on_circle(graph, border_cycle_finish)

    return graph


def _solve_leq(mat: list, b: list) -> list:
    """
    Solve the linear equation using Gaussian elimination method
    """
    r = 0
    c = 0
    matrix_size = len(mat)

    while r < matrix_size and c < matrix_size:
        # Find the maximum row
        r_i_max = None
        r_i_max_value = 0.0
        for r_i in range(r, matrix_size):
            r_i_abs = abs(mat[r_i][c])
            if r_i_abs > r_i_max_value:
                r_i_max = r_i
                r_i_max_value = r_i_abs

        # Swap the maximum and the current rows
        if r_i_max != r:
            r_tmp = mat[r_i_max]
            mat[r_i_max] = mat[r]
            mat[r] = r_tmp
            b_tmp = b[r_i_max]
            b[r_i_max] = b[r]
            b[r] = b_tmp

        # Divide all rows below
        for r_i in range(r + 1, matrix_size):
            multiplier = mat[r_i][c] / mat[r][c]
            mat[r_i][c] = 0.0
            for c_i in range(c + 1, matrix_size):
                mat[r_i][c_i] = mat[r_i][c_i] - (mat[r][c] * multiplier)
            b[r_i] = b[r_i] - (b[r] * multiplier)

        r += 1
        c += 1

    # Now we have a triangulated matrix. Reverse-solve the linear system
    solution = []
    for i in range(matrix_size - 1, -1, -1):
        solution_i = b[i] / mat[i][i]
        solution.append(solution_i)
        for j in range(i):
            b[j] -= mat[j][i] * solution_i

    return solution


def planarize_graph(graph: list, planarization_start_i: int) -> list:
    """
    Planarize the graph whose border is already planarized. The border consists of the first N vertices, where N is
    equal to 'planarization_start_i'
    """
    matrix_size = len(graph) - planarization_start_i

    # Calculate X coordinates for the points being examined
    matrix = [[0.0 for _ in range(matrix_size)] for _ in range(matrix_size)]
    b_vector = [0.0 for _ in range(matrix_size)]
    for i in range(planarization_start_i, len(graph)):
        adjacent = graph[i][0]
        for adj in adjacent:
            if adj >= planarization_start_i:
                matrix[i - planarization_start_i][adj - planarization_start_i] = 1.0
            else:
                b_vector[i - planarization_start_i] -= graph[adj][1][0]
        matrix[i - planarization_start_i][i - planarization_start_i] = -float(len(adjacent))

    # Now we must solve a system of linear equations: (matrix) * x = b
    solutions_x = _solve_leq(matrix, b_vector)

    # Calculate X coordinates for the points being examined
    matrix = [[0.0 for _ in range(matrix_size)] for _ in range(matrix_size)]
    b_vector = [0.0 for _ in range(matrix_size)]
    for i in range(planarization_start_i, len(graph)):
        adjacent = graph[i][0]
        for adj in adjacent:
            if adj >= planarization_start_i:
                matrix[i - planarization_start_i][adj - planarization_start_i] = 1.0
            else:
                b_vector[i - planarization_start_i] -= graph[adj][1][1]
        matrix[i - planarization_start_i][i - planarization_start_i] = -float(len(adjacent))

    # Now we must solve a system of linear equations: (matrix) * y = b
    solutions_y = _solve_leq(matrix, b_vector)

    # Now set the coordinates for each vertex
    for i in range(planarization_start_i, len(graph)):
        graph[i][1] = [solutions_x[i - planarization_start_i], solutions_y[i - planarization_start_i]]

    return graph


if __name__ == '__main__':
    main()
