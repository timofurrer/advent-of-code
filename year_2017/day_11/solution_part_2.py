"""
Solution for the first puzzle of Day 11
"""

import os
import math

import pytest

# My puzzle input
MY_PUZZLE_INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')


# Use of odd-q vertical layout
MOVEMENTS = {
    'n': lambda x, y: (x, y - 1),
    'ne': lambda x, y: (x + 1, y - 1 if x % 2 == 0 else y),
    'se': lambda x, y: (x + 1, y + 1 if x % 2 == 1 else y),
    's': lambda x, y: (x, y + 1),
    'sw': lambda x, y: (x - 1, y + 1 if x % 2 == 1 else y),
    'nw': lambda x, y: (x - 1, y - 1 if x % 2 == 0 else y)
}


def convert_oddq_to_cube_coords(col, row):
    """
    Convert the given odd-q vertical layout coordinates
    to cube coordinates
    """
    x = col
    z = row - (col - (col & 1)) / 2
    y = -x-z

    return (x, y, z)


def calc_distance(a, b):
    """
    Calculate the distance from two coordinates in the odd-q vertical layout
    """
    a_cube = convert_oddq_to_cube_coords(*a)
    b_cube = convert_oddq_to_cube_coords(*b)
    return (math.fabs(a_cube[0] - b_cube[0]) +
            math.fabs(a_cube[1] - b_cube[1]) +
            math.fabs(a_cube[2] - b_cube[2])) / 2


def max_distance(directions: list) -> int:
    """
    Count the steps it takes to move to
    the given directions.
    """
    current_coordinate = (0, 0)
    max_distance = 0
    # simulate moves
    for direction in directions:
        current_coordinate = MOVEMENTS[direction](*current_coordinate)
        distance = calc_distance((0, 0), current_coordinate)
        if distance > max_distance:
            max_distance = distance

    return max_distance


@pytest.mark.parametrize('raw_directions, expected_max_distance', [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 2),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
    # my puzzle input
    (open(MY_PUZZLE_INPUT).read(), 1567)
])
def test_max_distance(raw_directions, expected_max_distance):
    """Test the solution"""
    # given & when
    actual_max_distance = max_distance(
            [x for x in raw_directions.strip().split(',')])

    # then
    assert actual_max_distance == expected_max_distance
