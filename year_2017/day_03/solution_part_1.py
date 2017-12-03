"""
Solution for the first puzzle of Day 3
"""

import math
from collections import namedtuple

import pytest

# My puzzle input
MY_PUZZLE_INPUT = 361527

Point = namedtuple('Point', ['x', 'y'])


def first(cycle):
    """
    Get the first number for the given cycle

    It's a quadratic sequence.
    """
    return math.pow(2 * cycle - 1, 2) + 1


def cycle_number(square):
    """
    Returns the cycle where the square is in
    """
    return math.floor((math.sqrt(square - 1) + 1) / 2)


def cycle_len(cycle):
    """
    Get the length of the cycle
    """
    return first(cycle + 1) - first(cycle)


def square_sector(square):
    """Get the sector where the square is in

    * 0 -> East
    * 1 -> North
    * 2 -> West
    * 3 -> South
    """
    cycle = cycle_number(square)
    offset = square - first(cycle)
    return math.floor(4 * offset / cycle_len(cycle))


def get_coordinate_in_spiral(square):
    """
    Get the 2D coordinate of the given square
    """
    cycle = cycle_number(square)
    sector = square_sector(square)
    offset_to_first = square - first(cycle)
    offset = offset_to_first - sector * cycle_len(cycle) // 4

    if sector == 0:
        x = cycle
        y = cycle - offset - 1
    elif sector == 1:
        x = cycle - offset - 1
        y = -cycle
    elif sector == 2:
        x = -cycle
        y = -cycle + offset + 1
    elif sector == 3:
        x = -cycle + offset + 1
        y = cycle
    else:
        raise ArithmeticError('Failed to calculate sector for square: {0}'.format(
            square))
    return Point(x=x, y=y)


def manhatten_distance_ulam_spiral(square: int) -> int:
    """
    Each square on the grid is allocated in a spiral pattern
    starting at a location marked 1 and then counting up while
    spiraling outward.
    For example, the first few squares are allocated like this:

    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...

    While this is very space-efficient (no squares are skipped),
    requested data must be carried back to square 1
    (the location of the only access port for this memory system) by programs
    that can only move up, down, left, or right.
    They always take the shortest path:
    the Manhattan Distance between the location of the data and square 1.

    For example:

    * Data from square 1 is carried 0 steps, since it's at the access port.
    * Data from square 12 is carried 3 steps, such as: down, left, left.
    * Data from square 23 is carried only 2 steps: up twice.
    * Data from square 1024 must be carried 31 steps.
    """
    origin = Point(0, 0)
    # Get coordinate for the given square (Ulam Spiral)
    square_coord = get_coordinate_in_spiral(square)
    # Manhatten distance
    return int(
            math.fabs(square_coord.y - origin.y) +
            math.fabs(square_coord.x - origin.x))


@pytest.mark.parametrize('square, expected_steps', [
    (12, 3),
    (23, 2),
    (1024, 31),
    # my puzzle input
    (MY_PUZZLE_INPUT, 326)
])
def test_manhatten_distance_ulam_spiral(square, expected_steps):
    """Test the solution"""
    # given & when
    actual_steps = manhatten_distance_ulam_spiral(square)

    # then
    assert actual_steps == expected_steps


@pytest.mark.parametrize('square, expected_coordinate', [
    (2, Point(1, 0)),
    (3, Point(1, -1)),
    (4, Point(0, -1)),
    (5, Point(-1, -1)),
    (6, Point(-1, 0)),
    (7, Point(-1, 1)),
    (8, Point(0, 1)),
    (9, Point(1, 1)),
    (10, Point(2, 1)),
    (11, Point(2, 0)),
    (12, Point(2, -1)),
    (13, Point(2, -2)),
    (14, Point(1, -2)),
    (15, Point(0, -2)),
    (16, Point(-1, -2)),
    (17, Point(-2, -2)),
    (18, Point(-2, -1)),
    (19, Point(-2, 0)),
    (20, Point(-2, 1)),
    (21, Point(-2, 2)),
    (22, Point(-1, 2)),
    (23, Point(0, 2)),
    (24, Point(1, 2)),
    (25, Point(2, 2)),
    (26, Point(3, 2))
])
def test_ulam_spiral_position(square, expected_coordinate):
    """Test the solution"""
    # given & when
    actual_coordinate = get_coordinate_in_spiral(square)

    # then
    assert actual_coordinate == expected_coordinate
