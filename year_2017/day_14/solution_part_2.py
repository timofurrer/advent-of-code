"""
Solution for the first puzzle of Day 14
"""

import pytest

from year_2017.day_10.solution_part_2 import knothash


# My puzzle input
MY_PUZZLE_INPUT = 'ugkiagan'


class Graph:
    NEIGHBORS = (
        (0, -1), (-1, 0), (1, 0), (0, 1)
    )

    def __init__(self, matrix):
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.matrix = matrix

    def in_graph(self, i, j):
        return i >= 0 and i < self.rows and j >= 0 and j < self.cols

    def dfs(self, i, j, value, visited):
        """
        Do a Depth-first search for all
        adjucent vertices for the given vertice (i, j).
        Neighbors are the ones marked with a one from the middle one.

        0 1 0
        1 1 1
        0 1 0

        Thus, no diagonals!

        the visited array must be an 2D matrix of bools marking visited
        vertices with True.
        """
        # mark this vertice as visited
        visited[i][j] = True

        # visit all neighbors
        for x, y in self.NEIGHBORS:
            neighbor_i = i + x
            neighbor_j = j + y
            # check if neighbor is valid:
            # in matrix, not visited and belongs to region
            if self.in_graph(neighbor_i, neighbor_j):
                if not visited[neighbor_i][neighbor_j]:
                    if self.matrix[neighbor_i][neighbor_j] == value:
                        self.dfs(neighbor_i, neighbor_j, value, visited)

    def count_regions(self, value):
        """
        Count regions of adjacent vertices with value 1.
        """
        # setup matrix of bools marking visited vertices
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        regions = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if not visited[i][j] and self.matrix[i][j] == value:
                    self.dfs(i, j, value, visited)
                    regions += 1
        return regions


def generate_graph(input_hash, hash_len=128):
    """
    Generate Graph based on the input hash
    """
    matrix = []
    for i in range(hash_len):
        knot_hash = knothash(input_hash + '-' + str(i))
        binhash = bin(int(knot_hash, 16))
        matrix.append(list(int(x) for x in binhash[2:].zfill(hash_len)))

    graph = Graph(matrix)
    return graph


def calc_used_regions(input_hash):
    """
    Calculate the used regions by the given hash
    """
    graph = generate_graph(input_hash)
    return graph.count_regions(value=1)


@pytest.mark.parametrize('input_hash, expected_used_regions', [
    ('flqrgnkx', 1242),
    # my puzzle input
    (MY_PUZZLE_INPUT, 1069)
])
def test_calc_used_regions(input_hash, expected_used_regions):
    """Test the solution"""
    # given & when
    actual_used_regions = calc_used_regions(input_hash)

    # then
    assert actual_used_regions == expected_used_regions
